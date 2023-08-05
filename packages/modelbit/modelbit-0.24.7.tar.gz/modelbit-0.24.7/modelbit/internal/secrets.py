import base64
import json
import os
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from modelbit.api import MbApi, SecretApi, SecretDesc
from modelbit.error import UserFacingError
from modelbit.helpers import getCurrentBranch, getDeploymentName
from modelbit.utils import boto3Client, inDeployment


def s3KeyForSecrets(workspaceId: str) -> str:
  return f"{workspaceId}/secrets.json.enc"


def get_secret(
    name: str,
    deployment: Optional[str] = None,
    branch: Optional[str] = None,
    encoding: str = "utf8",
    mbApi: Optional[MbApi] = None,
) -> str:
  "Defaults to current deployment/branch"
  if mbApi is None:
    mbApi = MbApi()
  branch = branch or getCurrentBranch()
  secretBytes = getSecretFromS3(branch, name, deployment or
                                getDeploymentName() or "") if inDeployment() else getSecretFromWeb(
                                    branch, name, deployment or "", mbApi)
  if secretBytes is None:
    raise UserFacingError(f"Secret not found: {name}")
  return secretBytes.decode(encoding)


def getSecretFromWeb(branch: str, secretName: str, runtimeName: str, mbApi: MbApi) -> Optional[bytes]:
  secretInfo = SecretApi(mbApi).getSecret(branch, secretName, runtimeName)
  return secretInfo.secretValue if secretInfo is not None else None


def getSecretFromS3(branch: str, name: str, runtimeName: str) -> Optional[bytes]:
  if _secretsFetchedAt is None or datetime.now() - _secretsFetchedAt > timedelta(seconds=300):
    _updateSecretsFromS3()
  _updateSecretsFromS3()

  secrets = _secrets.get(name, [])
  if (len(secrets)) == 0:
    return None

  # Filter to match current runtime
  for secret in secrets:
    if secret.matches(runtimeName=runtimeName, branch=branch):
      return secret.decryptedValue()

  return None


### Private S3 Stuff


class DecryptableSecretDesc(SecretDesc):
  name: str
  runtimeNameFilter: str
  runtimeBranchFilter: str
  valueEnc64: str
  keyEnc64: str
  iv64: str
  ownerId: str
  createdAtMs: int

  def __init__(self, data: Dict[str, Any]):
    super().__init__(data)
    self.name = data['name']
    self.runtimeNameFilter = data['runtimeNameFilter']
    self.runtimeBranchFilter = data['runtimeBranchFilter']
    self.valueEnc64 = data['valueEnc64']
    self.keyEnc64 = data['keyEnc64']
    self.iv64 = data['iv64']
    self.ownerId = data['ownerId']
    self.createdAtMs = data['createdAtMs']

  def decryptedValue(self):
    if self.secretValue is not None:
      return self.secretValue
    _pystateKeys = os.getenv('PYSTATE_KEYS')
    for key64 in str(_pystateKeys).split(","):
      cipher = AES.new(base64.b64decode(key64), AES.MODE_ECB)  # type: ignore
      fileKey = unpad(cipher.decrypt(base64.b64decode(self.keyEnc64)), AES.block_size)
      cipher = AES.new(fileKey, AES.MODE_CBC, base64.b64decode(self.iv64))  # type: ignore
      decState = unpad(cipher.decrypt(base64.b64decode(self.valueEnc64)), AES.block_size)
      self.secretValue = decState
      return decState

  def __lt__(self, other: "DecryptableSecretDesc"):
    return len(other.runtimeNameFilter) + len(other.runtimeBranchFilter) < len(self.runtimeNameFilter) + len(
        self.runtimeBranchFilter)

  def matches(self, runtimeName: str, branch: str) -> bool:
    if not len(self.runtimeNameFilter) + len(self.runtimeBranchFilter):
      return True
    return (matchesFilter(self.runtimeBranchFilter, branch) and
            matchesFilter(self.runtimeNameFilter, runtimeName))


def matchesFilter(filterPattern: str, target: str) -> bool:
  return bool(re.match('^' + filterPattern.replace("*", ".*?") + '$', target))


# TODO: Save to disk now that we are reloading?
_secrets: Dict[str, List[DecryptableSecretDesc]] = {}
_secretsFetchedAt: Optional[datetime] = None


def _updateSecretsFromS3() -> None:
  secrets = _downloadS3Secrets()
  if secrets is None:
    return
  global _secrets, _secretsFetchedAt
  secretDict: Dict[str, List[DecryptableSecretDesc]] = {}

  for s in (DecryptableSecretDesc(s) for s in json.loads(secrets)):
    if s.name not in secretDict:
      secretDict[s.name] = []
    secretDict[s.name].append(s)

  for name in secretDict.keys():
    secretDict[name].sort()

  _secrets = secretDict
  _secretsFetchedAt = datetime.now()


def _downloadS3Secrets() -> Optional[str]:
  _workspaceId = os.getenv('WORKSPACE_ID')
  _pystateBucket = os.getenv('PYSTATE_BUCKET')

  if _workspaceId is None or _pystateBucket is None:
    raise Exception(f"EnvVar Missing: WORKSPACE_ID, PYSTATE_BUCKET")
  try:
    s3Key = s3KeyForSecrets(_workspaceId)
    s3Obj = boto3Client('s3').get_object(Bucket=_pystateBucket, Key=s3Key)  # type: ignore
    return s3Obj['Body'].read()  # type: ignore
  except Exception as err:
    strErr = str(err)
    if 'AccessDenied' not in strErr and 'NoSuchKey' not in strErr:
      raise err
  return None
