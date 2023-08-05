"""
Type annotations for kinesis-video-webrtc-storage service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_webrtc_storage/type_defs/)

Usage::

    ```python
    from mypy_boto3_kinesis_video_webrtc_storage.type_defs import EmptyResponseMetadataTypeDef

    data: EmptyResponseMetadataTypeDef = {...}
    ```
"""
import sys
from typing import Dict

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "EmptyResponseMetadataTypeDef",
    "JoinStorageSessionInputRequestTypeDef",
    "ResponseMetadataTypeDef",
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

JoinStorageSessionInputRequestTypeDef = TypedDict(
    "JoinStorageSessionInputRequestTypeDef",
    {
        "channelArn": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)
