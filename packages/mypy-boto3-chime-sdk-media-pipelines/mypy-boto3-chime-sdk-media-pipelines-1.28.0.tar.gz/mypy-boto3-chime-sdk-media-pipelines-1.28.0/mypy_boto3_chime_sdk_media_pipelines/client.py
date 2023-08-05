"""
Type annotations for chime-sdk-media-pipelines service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_chime_sdk_media_pipelines.client import ChimeSDKMediaPipelinesClient

    session = Session()
    client: ChimeSDKMediaPipelinesClient = session.client("chime-sdk-media-pipelines")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import MediaPipelineStatusUpdateType
from .type_defs import (
    ChimeSdkMeetingConfigurationTypeDef,
    ConcatenationSinkTypeDef,
    ConcatenationSourceTypeDef,
    CreateMediaCapturePipelineResponseTypeDef,
    CreateMediaConcatenationPipelineResponseTypeDef,
    CreateMediaInsightsPipelineConfigurationResponseTypeDef,
    CreateMediaInsightsPipelineResponseTypeDef,
    CreateMediaLiveConnectorPipelineResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetMediaCapturePipelineResponseTypeDef,
    GetMediaInsightsPipelineConfigurationResponseTypeDef,
    GetMediaPipelineResponseTypeDef,
    KinesisVideoStreamRecordingSourceRuntimeConfigurationTypeDef,
    KinesisVideoStreamSourceRuntimeConfigurationTypeDef,
    ListMediaCapturePipelinesResponseTypeDef,
    ListMediaInsightsPipelineConfigurationsResponseTypeDef,
    ListMediaPipelinesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    LiveConnectorSinkConfigurationTypeDef,
    LiveConnectorSourceConfigurationTypeDef,
    MediaInsightsPipelineConfigurationElementTypeDef,
    RealTimeAlertConfigurationTypeDef,
    S3RecordingSinkRuntimeConfigurationTypeDef,
    TagTypeDef,
    UpdateMediaInsightsPipelineConfigurationResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ChimeSDKMediaPipelinesClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottledClientException: Type[BotocoreClientError]
    UnauthorizedClientException: Type[BotocoreClientError]


class ChimeSDKMediaPipelinesClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeSDKMediaPipelinesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#close)
        """

    def create_media_capture_pipeline(
        self,
        *,
        SourceType: Literal["ChimeSdkMeeting"],
        SourceArn: str,
        SinkType: Literal["S3Bucket"],
        SinkArn: str,
        ClientRequestToken: str = ...,
        ChimeSdkMeetingConfiguration: ChimeSdkMeetingConfigurationTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateMediaCapturePipelineResponseTypeDef:
        """
        Creates a media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.create_media_capture_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#create_media_capture_pipeline)
        """

    def create_media_concatenation_pipeline(
        self,
        *,
        Sources: Sequence[ConcatenationSourceTypeDef],
        Sinks: Sequence[ConcatenationSinkTypeDef],
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateMediaConcatenationPipelineResponseTypeDef:
        """
        Creates a media concatenation pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.create_media_concatenation_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#create_media_concatenation_pipeline)
        """

    def create_media_insights_pipeline(
        self,
        *,
        MediaInsightsPipelineConfigurationArn: str,
        KinesisVideoStreamSourceRuntimeConfiguration: KinesisVideoStreamSourceRuntimeConfigurationTypeDef = ...,
        MediaInsightsRuntimeMetadata: Mapping[str, str] = ...,
        KinesisVideoStreamRecordingSourceRuntimeConfiguration: KinesisVideoStreamRecordingSourceRuntimeConfigurationTypeDef = ...,
        S3RecordingSinkRuntimeConfiguration: S3RecordingSinkRuntimeConfigurationTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ClientRequestToken: str = ...
    ) -> CreateMediaInsightsPipelineResponseTypeDef:
        """
        Creates a media insights pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.create_media_insights_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#create_media_insights_pipeline)
        """

    def create_media_insights_pipeline_configuration(
        self,
        *,
        MediaInsightsPipelineConfigurationName: str,
        ResourceAccessRoleArn: str,
        Elements: Sequence[MediaInsightsPipelineConfigurationElementTypeDef],
        RealTimeAlertConfiguration: RealTimeAlertConfigurationTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ClientRequestToken: str = ...
    ) -> CreateMediaInsightsPipelineConfigurationResponseTypeDef:
        """
        A structure that contains the static configurations for a media insights
        pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.create_media_insights_pipeline_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#create_media_insights_pipeline_configuration)
        """

    def create_media_live_connector_pipeline(
        self,
        *,
        Sources: Sequence[LiveConnectorSourceConfigurationTypeDef],
        Sinks: Sequence[LiveConnectorSinkConfigurationTypeDef],
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateMediaLiveConnectorPipelineResponseTypeDef:
        """
        Creates a media live connector pipeline in an Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.create_media_live_connector_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#create_media_live_connector_pipeline)
        """

    def delete_media_capture_pipeline(
        self, *, MediaPipelineId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.delete_media_capture_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#delete_media_capture_pipeline)
        """

    def delete_media_insights_pipeline_configuration(
        self, *, Identifier: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified configuration settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.delete_media_insights_pipeline_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#delete_media_insights_pipeline_configuration)
        """

    def delete_media_pipeline(self, *, MediaPipelineId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.delete_media_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#delete_media_pipeline)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#generate_presigned_url)
        """

    def get_media_capture_pipeline(
        self, *, MediaPipelineId: str
    ) -> GetMediaCapturePipelineResponseTypeDef:
        """
        Gets an existing media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.get_media_capture_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#get_media_capture_pipeline)
        """

    def get_media_insights_pipeline_configuration(
        self, *, Identifier: str
    ) -> GetMediaInsightsPipelineConfigurationResponseTypeDef:
        """
        Gets the configuration settings for a media insights pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.get_media_insights_pipeline_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#get_media_insights_pipeline_configuration)
        """

    def get_media_pipeline(self, *, MediaPipelineId: str) -> GetMediaPipelineResponseTypeDef:
        """
        Gets an existing media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.get_media_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#get_media_pipeline)
        """

    def list_media_capture_pipelines(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMediaCapturePipelinesResponseTypeDef:
        """
        Returns a list of media pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.list_media_capture_pipelines)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#list_media_capture_pipelines)
        """

    def list_media_insights_pipeline_configurations(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMediaInsightsPipelineConfigurationsResponseTypeDef:
        """
        Lists the available media insights pipeline configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.list_media_insights_pipeline_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#list_media_insights_pipeline_configurations)
        """

    def list_media_pipelines(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMediaPipelinesResponseTypeDef:
        """
        Returns a list of media pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.list_media_pipelines)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#list_media_pipelines)
        """

    def list_tags_for_resource(self, *, ResourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags available for a media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#list_tags_for_resource)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        The ARN of the media pipeline that you want to tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes any tags from a media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#untag_resource)
        """

    def update_media_insights_pipeline_configuration(
        self,
        *,
        Identifier: str,
        ResourceAccessRoleArn: str,
        Elements: Sequence[MediaInsightsPipelineConfigurationElementTypeDef],
        RealTimeAlertConfiguration: RealTimeAlertConfigurationTypeDef = ...
    ) -> UpdateMediaInsightsPipelineConfigurationResponseTypeDef:
        """
        Updates the media insights pipeline's configuration settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.update_media_insights_pipeline_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#update_media_insights_pipeline_configuration)
        """

    def update_media_insights_pipeline_status(
        self, *, Identifier: str, UpdateStatus: MediaPipelineStatusUpdateType
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the status of a media insights pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client.update_media_insights_pipeline_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_media_pipelines/client/#update_media_insights_pipeline_status)
        """
