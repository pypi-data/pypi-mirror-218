# flake8: noqa

"""
    NCBI Datasets API

    ### NCBI Datasets is a resource that lets you easily gather data from NCBI. The Datasets version 1 API is considred stable and will not be subject to breaking changes.  However, certain endpoints will be [deprecated](https://www.ncbi.nlm.nih.gov/datasets/docs/v1/reference-docs/rest-api/deprecated_apis/), and then sunset as newer versions are published. For some larger downloads, you may want to download a [dehydrated zip archive](https://www.ncbi.nlm.nih.gov/datasets/docs/v1/how-tos/genomes/large-download/), and retrieve the individual data files at a later time.   # noqa: E501

    The version of the OpenAPI document: v1
    Generated by: https://openapi-generator.tech
"""


__version__ = "15.8.0"

# import ApiClient
from ncbi.datasets.openapi.api_client import ApiClient

# import Configuration
from ncbi.datasets.openapi.configuration import Configuration

# import exceptions
from ncbi.datasets.openapi.exceptions import OpenApiException
from ncbi.datasets.openapi.exceptions import ApiAttributeError
from ncbi.datasets.openapi.exceptions import ApiTypeError
from ncbi.datasets.openapi.exceptions import ApiValueError
from ncbi.datasets.openapi.exceptions import ApiKeyError
from ncbi.datasets.openapi.exceptions import ApiException
