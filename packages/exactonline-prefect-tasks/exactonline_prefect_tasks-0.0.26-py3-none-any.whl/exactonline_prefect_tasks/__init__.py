"""
Tasks for interacting with Exact Online.
"""
try:
    from exactonline.http import *
    from exactonline.api import *
    from .exactonline_api import ExactOnlineApi
    from .exceptions import ApiException, AuthException, MissingParametersException, NoRecordFoundException
    from .aws import S3Storage, S3Client, SecretsManagerClient, SecretsManagerStorage
    from .tasks import Create, Read, GetById, GetAll, Search, Delete, Update
except ImportError:
    raise ImportError(
        'Using `prefect.tasks.exactonline` requires Prefect to be installed with the "exactonline" extra.'
    )
