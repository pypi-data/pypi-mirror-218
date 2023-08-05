from typing import Optional, Dict, List, Any
import json, pandas, numpy, tempfile, sqlite3, logging, time
from modelbit.api import MbApi, DatasetApi
from modelbit.error import UserFacingError
from modelbit.utils import inDeployment
from modelbit.internal.secure_storage import getSecureData
from modelbit.internal.s3 import getS3FileBytes

logger = logging.getLogger(__name__)

FilterType = Optional[Dict[str, List[Any]]]


def downloadDecryptData(mbApi: MbApi, path: str, desc: str) -> Optional[bytes]:
  if inDeployment():
    return getS3FileBytes(path)
  else:
    return _downloadFromWeb(mbApi, path=path, desc=desc)


def _downloadFromWeb(mbApi: MbApi, path: str, desc: str) -> Optional[bytes]:
  dri = DatasetApi(mbApi).getDatasetPartDownloadInfo(path)
  if dri is None:
    raise UserFacingError(f"Failed finding download info for dataset part: {path}")
  return getSecureData(dri, desc)


class Shard:

  def __init__(self, mbApi: MbApi, params: Dict[str, Any], dsName: str, numShards: int):
    self.mbApi = mbApi
    self.dsName = dsName
    self.numShards = numShards
    self.shardId = params["shardId"]
    self.shardPath = params["shardPath"]
    self.shardColumn = params["shardColumn"]
    self.minValue = params["minValue"]
    self.maxValue = params["maxValue"]
    self.numBytes = params["numBytes"]
    self.numRows = params["numRows"]
    self.featureDbFile = tempfile.NamedTemporaryFile()
    self.completeDf: Optional[pandas.DataFrame] = None
    self.dbConn: Optional[sqlite3.Connection] = None

  def __del__(self):
    if self.dbConn is not None:
      self.dbConn.close()
    self.featureDbFile.close()

  def getDbConn(self) -> sqlite3.Connection:
    if self.dbConn is None:
      shardData = downloadDecryptData(self.mbApi, self.shardPath,
                                      f"{self.dsName} (part {self.shardId} of {self.numShards})")
      if shardData is None:
        raise Exception(f"FailedGettingShard path={self.shardPath}")
      self.featureDbFile.write(shardData)
      self.dbConn = sqlite3.connect(self.featureDbFile.name)
    return self.dbConn

  def filterToDf(self, filters: FilterType) -> Optional[pandas.DataFrame]:
    if filters is None:
      return self.getCompleteDf()

    if self.canSkip(filters):
      return None

    filterGroups: List[str] = []
    filterParams: List[Any] = []
    for filterCol, filterValues in filters.items():
      filterGroup: List[str] = []
      for val in filterValues:
        filterGroup.append(f"`{filterCol}` = ?")
        filterParams.append(val)
      filterGroups.append(f'({" or ".join(filterGroup)})')
    sql = f"select * from df where {' and '.join(filterGroups)}"
    df = pandas.read_sql_query(sql=sql, params=filterParams, con=self.getDbConn())
    self.convertDbNulls(df)
    return df

  def getCompleteDf(self) -> pandas.DataFrame:
    if self.completeDf is None:
      df = pandas.read_sql_query(sql="select * from df", con=self.getDbConn())
      self.convertDbNulls(df)
      self.completeDf = df
    return self.completeDf

  def canSkip(self, filters: FilterType) -> bool:
    if filters is None:
      return False

    colNameCaseMap: Dict[str, str] = {}
    for fName in filters.keys():
      colNameCaseMap[fName.lower()] = fName
    if self.shardColumn.lower() not in colNameCaseMap:
      return False

    filterShardColCasedToFilters = colNameCaseMap[self.shardColumn.lower()]
    lastFilterVal: Any = None
    try:
      canSkip = True
      for filterVal in filters[filterShardColCasedToFilters]:
        lastFilterVal = filterVal
        if filterVal is None or self.minValue is None or self.maxValue is None:
          canSkip = False
        elif self.minValue <= filterVal <= self.maxValue:
          canSkip = False
      return canSkip
    except TypeError as err:
      if "<=" in str(err):
        comparison = " <= ".join([
            f"{type(self.minValue).__name__}({self.minValue})",
            f"{type(lastFilterVal).__name__}({lastFilterVal})",
            f"{type(self.maxValue).__name__}({self.maxValue})",
        ])
        raise UserFacingError(f"Invalid comparison when searching for feature, {comparison}. Error: {err}")
      raise err

  def convertDbNulls(self, df: pandas.DataFrame):
    df.replace(["\\N", "\\\\N"], numpy.nan, inplace=True)  # type: ignore


class FeatureStore:

  ManifestTimeoutSeconds = 5 * 60 if inDeployment() else 10

  def __init__(self, mbApi: MbApi, branch: str, dsName: str):
    self.mbApi = mbApi
    self.branch = branch
    self.dsName = dsName
    self.manifestPath: str = self.getManifestPath()
    self.manifestBytes: bytes = b""
    self.shards: List[Shard] = []

  def getManifestPath(self) -> str:
    return f'datasets/{self.dsName}/{self.branch}.manifest'

  def maybeRefreshManifest(self):
    if len(self.manifestBytes) > 0 and time.time() < self.manifestExpiresAt:
      return
    newManifestBytes: Optional[bytes] = None
    try:
      newManifestBytes = downloadDecryptData(self.mbApi, self.manifestPath, f"{self.dsName} (index)")
    except:
      pass  # exceptions for not found, etc. we check for None after for a nicer error message
    if newManifestBytes is None:
      raise UserFacingError(f"Dataset not found: {self.branch}/{self.dsName}")
    if newManifestBytes != self.manifestBytes:
      self.manifestBytes = newManifestBytes
      newManifestData: Dict[str, Any] = json.loads(self.manifestBytes.decode())
      shardInfo: List[Dict[str, Any]] = newManifestData["shards"]
      self.shards = [
          Shard(self.mbApi, params=d, dsName=self.dsName, numShards=len(shardInfo)) for d in shardInfo
      ]
    self.manifestExpiresAt = time.time() + self.ManifestTimeoutSeconds

  def getDataFrame(self, filters: FilterType) -> pandas.DataFrame:
    if filters is not None and type(filters) is not dict:
      raise UserFacingError(f"filters= must be None or a dictionary. It's currently a {type(filters)}")
    self.maybeRefreshManifest()
    shardResults = [s.filterToDf(filters) for s in self.shards]
    shardResults = [s for s in shardResults if s is not None]
    if len(shardResults) == 0:
      firstDf = self.shards[0].getCompleteDf()
      assert firstDf is not None
      return firstDf.head(0)  # return empty df, not None, when filters match nothing
    return pandas.concat(shardResults)  #type: ignore


class FeatureStoreManager:

  def __init__(self, mbApi: MbApi):
    self.mbApi = mbApi
    self.featureStores: Dict[str, FeatureStore] = {}

  def getFeatureStore(self, branch: str, dsName: str) -> FeatureStore:
    lookupKey = f"{branch}/${dsName}"
    if lookupKey not in self.featureStores:
      self.featureStores[lookupKey] = FeatureStore(mbApi=self.mbApi, branch=branch, dsName=dsName)
    return self.featureStores[lookupKey]


_featureStoreManager: Optional[FeatureStoreManager] = None
_s3Client: Optional[Any] = None


def _getFeatureStoreManager(mbApi: MbApi) -> FeatureStoreManager:
  global _featureStoreManager
  if _featureStoreManager is None:
    _featureStoreManager = FeatureStoreManager(mbApi)
  return _featureStoreManager


def getDataFrame(mbApi: MbApi, branch: str, dsName: str, filters: FilterType = None) -> pandas.DataFrame:
  featureStore = _getFeatureStoreManager(mbApi).getFeatureStore(branch=branch, dsName=dsName)
  return featureStore.getDataFrame(filters)
