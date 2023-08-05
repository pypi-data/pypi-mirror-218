"""
Type annotations for comprehend service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/type_defs/)

Usage::

    ```python
    from mypy_boto3_comprehend.type_defs import AugmentedManifestsListItemTypeDef

    data: AugmentedManifestsListItemTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AugmentedManifestsDocumentTypeFormatType,
    BlockTypeType,
    DatasetDataFormatType,
    DatasetStatusType,
    DatasetTypeType,
    DocumentClassifierDataFormatType,
    DocumentClassifierDocumentTypeFormatType,
    DocumentClassifierModeType,
    DocumentReadActionType,
    DocumentReadFeatureTypesType,
    DocumentReadModeType,
    DocumentTypeType,
    EndpointStatusType,
    EntityRecognizerDataFormatType,
    EntityTypeType,
    FlywheelIterationStatusType,
    FlywheelStatusType,
    InputFormatType,
    JobStatusType,
    LanguageCodeType,
    ModelStatusType,
    ModelTypeType,
    PageBasedErrorCodeType,
    PageBasedWarningCodeType,
    PartOfSpeechTagTypeType,
    PiiEntitiesDetectionMaskModeType,
    PiiEntitiesDetectionModeType,
    PiiEntityTypeType,
    SentimentTypeType,
    SplitType,
    SyntaxLanguageCodeType,
    TargetedSentimentEntityTypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AugmentedManifestsListItemTypeDef",
    "DominantLanguageTypeDef",
    "BatchDetectDominantLanguageRequestRequestTypeDef",
    "BatchItemErrorTypeDef",
    "BatchDetectEntitiesRequestRequestTypeDef",
    "KeyPhraseTypeDef",
    "BatchDetectKeyPhrasesRequestRequestTypeDef",
    "SentimentScoreTypeDef",
    "BatchDetectSentimentRequestRequestTypeDef",
    "BatchDetectSyntaxRequestRequestTypeDef",
    "BatchDetectTargetedSentimentRequestRequestTypeDef",
    "ChildBlockTypeDef",
    "RelationshipsListItemTypeDef",
    "BoundingBoxTypeDef",
    "ClassifierEvaluationMetricsTypeDef",
    "DocumentReaderConfigTypeDef",
    "DocumentClassTypeDef",
    "DocumentLabelTypeDef",
    "DocumentTypeListItemTypeDef",
    "ErrorsListItemTypeDef",
    "WarningsListItemTypeDef",
    "ContainsPiiEntitiesRequestRequestTypeDef",
    "EntityLabelTypeDef",
    "TagTypeDef",
    "CreateDatasetResponseTypeDef",
    "DocumentClassifierOutputDataConfigTypeDef",
    "VpcConfigTypeDef",
    "CreateDocumentClassifierResponseTypeDef",
    "CreateEndpointResponseTypeDef",
    "CreateEntityRecognizerResponseTypeDef",
    "CreateFlywheelResponseTypeDef",
    "DatasetAugmentedManifestsListItemTypeDef",
    "DatasetDocumentClassifierInputDataConfigTypeDef",
    "DatasetEntityRecognizerAnnotationsTypeDef",
    "DatasetEntityRecognizerDocumentsTypeDef",
    "DatasetEntityRecognizerEntityListTypeDef",
    "DatasetFilterTypeDef",
    "DatasetPropertiesTypeDef",
    "DeleteDocumentClassifierRequestRequestTypeDef",
    "DeleteEndpointRequestRequestTypeDef",
    "DeleteEntityRecognizerRequestRequestTypeDef",
    "DeleteFlywheelRequestRequestTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeDocumentClassificationJobRequestRequestTypeDef",
    "DescribeDocumentClassifierRequestRequestTypeDef",
    "DescribeDominantLanguageDetectionJobRequestRequestTypeDef",
    "DescribeEndpointRequestRequestTypeDef",
    "EndpointPropertiesTypeDef",
    "DescribeEntitiesDetectionJobRequestRequestTypeDef",
    "DescribeEntityRecognizerRequestRequestTypeDef",
    "DescribeEventsDetectionJobRequestRequestTypeDef",
    "DescribeFlywheelIterationRequestRequestTypeDef",
    "DescribeFlywheelRequestRequestTypeDef",
    "DescribeKeyPhrasesDetectionJobRequestRequestTypeDef",
    "DescribePiiEntitiesDetectionJobRequestRequestTypeDef",
    "DescribeResourcePolicyRequestRequestTypeDef",
    "DescribeResourcePolicyResponseTypeDef",
    "DescribeSentimentDetectionJobRequestRequestTypeDef",
    "DescribeTargetedSentimentDetectionJobRequestRequestTypeDef",
    "DescribeTopicsDetectionJobRequestRequestTypeDef",
    "DetectDominantLanguageRequestRequestTypeDef",
    "DetectKeyPhrasesRequestRequestTypeDef",
    "DetectPiiEntitiesRequestRequestTypeDef",
    "PiiEntityTypeDef",
    "DetectSentimentRequestRequestTypeDef",
    "DetectSyntaxRequestRequestTypeDef",
    "DetectTargetedSentimentRequestRequestTypeDef",
    "DocumentClassificationConfigTypeDef",
    "DocumentClassificationJobFilterTypeDef",
    "OutputDataConfigTypeDef",
    "DocumentClassifierDocumentsTypeDef",
    "DocumentClassifierFilterTypeDef",
    "DocumentClassifierSummaryTypeDef",
    "ExtractedCharactersListItemTypeDef",
    "DominantLanguageDetectionJobFilterTypeDef",
    "EndpointFilterTypeDef",
    "EntitiesDetectionJobFilterTypeDef",
    "EntityTypesListItemTypeDef",
    "EntityRecognizerAnnotationsTypeDef",
    "EntityRecognizerDocumentsTypeDef",
    "EntityRecognizerEntityListTypeDef",
    "EntityRecognizerEvaluationMetricsTypeDef",
    "EntityRecognizerFilterTypeDef",
    "EntityTypesEvaluationMetricsTypeDef",
    "EntityRecognizerOutputDataConfigTypeDef",
    "EntityRecognizerSummaryTypeDef",
    "EventsDetectionJobFilterTypeDef",
    "FlywheelFilterTypeDef",
    "FlywheelIterationFilterTypeDef",
    "FlywheelModelEvaluationMetricsTypeDef",
    "FlywheelSummaryTypeDef",
    "PointTypeDef",
    "ImportModelResponseTypeDef",
    "KeyPhrasesDetectionJobFilterTypeDef",
    "ListDocumentClassifierSummariesRequestRequestTypeDef",
    "ListEntityRecognizerSummariesRequestRequestTypeDef",
    "PiiEntitiesDetectionJobFilterTypeDef",
    "SentimentDetectionJobFilterTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TargetedSentimentDetectionJobFilterTypeDef",
    "TopicsDetectionJobFilterTypeDef",
    "PaginatorConfigTypeDef",
    "PartOfSpeechTagTypeDef",
    "PiiOutputDataConfigTypeDef",
    "RedactionConfigTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "ResponseMetadataTypeDef",
    "StartDocumentClassificationJobResponseTypeDef",
    "StartDominantLanguageDetectionJobResponseTypeDef",
    "StartEntitiesDetectionJobResponseTypeDef",
    "StartEventsDetectionJobResponseTypeDef",
    "StartFlywheelIterationRequestRequestTypeDef",
    "StartFlywheelIterationResponseTypeDef",
    "StartKeyPhrasesDetectionJobResponseTypeDef",
    "StartPiiEntitiesDetectionJobResponseTypeDef",
    "StartSentimentDetectionJobResponseTypeDef",
    "StartTargetedSentimentDetectionJobResponseTypeDef",
    "StartTopicsDetectionJobResponseTypeDef",
    "StopDominantLanguageDetectionJobRequestRequestTypeDef",
    "StopDominantLanguageDetectionJobResponseTypeDef",
    "StopEntitiesDetectionJobRequestRequestTypeDef",
    "StopEntitiesDetectionJobResponseTypeDef",
    "StopEventsDetectionJobRequestRequestTypeDef",
    "StopEventsDetectionJobResponseTypeDef",
    "StopKeyPhrasesDetectionJobRequestRequestTypeDef",
    "StopKeyPhrasesDetectionJobResponseTypeDef",
    "StopPiiEntitiesDetectionJobRequestRequestTypeDef",
    "StopPiiEntitiesDetectionJobResponseTypeDef",
    "StopSentimentDetectionJobRequestRequestTypeDef",
    "StopSentimentDetectionJobResponseTypeDef",
    "StopTargetedSentimentDetectionJobRequestRequestTypeDef",
    "StopTargetedSentimentDetectionJobResponseTypeDef",
    "StopTrainingDocumentClassifierRequestRequestTypeDef",
    "StopTrainingEntityRecognizerRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateEndpointRequestRequestTypeDef",
    "UpdateEndpointResponseTypeDef",
    "BatchDetectDominantLanguageItemResultTypeDef",
    "DetectDominantLanguageResponseTypeDef",
    "BatchDetectKeyPhrasesItemResultTypeDef",
    "DetectKeyPhrasesResponseTypeDef",
    "BatchDetectSentimentItemResultTypeDef",
    "DetectSentimentResponseTypeDef",
    "MentionSentimentTypeDef",
    "BlockReferenceTypeDef",
    "ClassifierMetadataTypeDef",
    "ClassifyDocumentRequestRequestTypeDef",
    "DetectEntitiesRequestRequestTypeDef",
    "InputDataConfigTypeDef",
    "ContainsPiiEntitiesResponseTypeDef",
    "CreateEndpointRequestRequestTypeDef",
    "ImportModelRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "DataSecurityConfigTypeDef",
    "UpdateDataSecurityConfigTypeDef",
    "DatasetEntityRecognizerInputDataConfigTypeDef",
    "ListDatasetsRequestRequestTypeDef",
    "DescribeDatasetResponseTypeDef",
    "ListDatasetsResponseTypeDef",
    "DescribeEndpointResponseTypeDef",
    "ListEndpointsResponseTypeDef",
    "DetectPiiEntitiesResponseTypeDef",
    "ListDocumentClassificationJobsRequestListDocumentClassificationJobsPaginateTypeDef",
    "ListDocumentClassificationJobsRequestRequestTypeDef",
    "DocumentClassifierInputDataConfigTypeDef",
    "ListDocumentClassifiersRequestListDocumentClassifiersPaginateTypeDef",
    "ListDocumentClassifiersRequestRequestTypeDef",
    "ListDocumentClassifierSummariesResponseTypeDef",
    "DocumentMetadataTypeDef",
    "ListDominantLanguageDetectionJobsRequestListDominantLanguageDetectionJobsPaginateTypeDef",
    "ListDominantLanguageDetectionJobsRequestRequestTypeDef",
    "ListEndpointsRequestListEndpointsPaginateTypeDef",
    "ListEndpointsRequestRequestTypeDef",
    "ListEntitiesDetectionJobsRequestListEntitiesDetectionJobsPaginateTypeDef",
    "ListEntitiesDetectionJobsRequestRequestTypeDef",
    "EntityRecognitionConfigTypeDef",
    "EntityRecognizerInputDataConfigTypeDef",
    "ListEntityRecognizersRequestListEntityRecognizersPaginateTypeDef",
    "ListEntityRecognizersRequestRequestTypeDef",
    "EntityRecognizerMetadataEntityTypesListItemTypeDef",
    "ListEntityRecognizerSummariesResponseTypeDef",
    "ListEventsDetectionJobsRequestRequestTypeDef",
    "ListFlywheelsRequestRequestTypeDef",
    "ListFlywheelIterationHistoryRequestRequestTypeDef",
    "FlywheelIterationPropertiesTypeDef",
    "ListFlywheelsResponseTypeDef",
    "GeometryTypeDef",
    "ListKeyPhrasesDetectionJobsRequestListKeyPhrasesDetectionJobsPaginateTypeDef",
    "ListKeyPhrasesDetectionJobsRequestRequestTypeDef",
    "ListPiiEntitiesDetectionJobsRequestListPiiEntitiesDetectionJobsPaginateTypeDef",
    "ListPiiEntitiesDetectionJobsRequestRequestTypeDef",
    "ListSentimentDetectionJobsRequestListSentimentDetectionJobsPaginateTypeDef",
    "ListSentimentDetectionJobsRequestRequestTypeDef",
    "ListTargetedSentimentDetectionJobsRequestRequestTypeDef",
    "ListTopicsDetectionJobsRequestListTopicsDetectionJobsPaginateTypeDef",
    "ListTopicsDetectionJobsRequestRequestTypeDef",
    "SyntaxTokenTypeDef",
    "BatchDetectDominantLanguageResponseTypeDef",
    "BatchDetectKeyPhrasesResponseTypeDef",
    "BatchDetectSentimentResponseTypeDef",
    "TargetedSentimentMentionTypeDef",
    "EntityTypeDef",
    "DocumentClassificationJobPropertiesTypeDef",
    "DominantLanguageDetectionJobPropertiesTypeDef",
    "EntitiesDetectionJobPropertiesTypeDef",
    "EventsDetectionJobPropertiesTypeDef",
    "KeyPhrasesDetectionJobPropertiesTypeDef",
    "PiiEntitiesDetectionJobPropertiesTypeDef",
    "SentimentDetectionJobPropertiesTypeDef",
    "StartDocumentClassificationJobRequestRequestTypeDef",
    "StartDominantLanguageDetectionJobRequestRequestTypeDef",
    "StartEntitiesDetectionJobRequestRequestTypeDef",
    "StartEventsDetectionJobRequestRequestTypeDef",
    "StartKeyPhrasesDetectionJobRequestRequestTypeDef",
    "StartPiiEntitiesDetectionJobRequestRequestTypeDef",
    "StartSentimentDetectionJobRequestRequestTypeDef",
    "StartTargetedSentimentDetectionJobRequestRequestTypeDef",
    "StartTopicsDetectionJobRequestRequestTypeDef",
    "TargetedSentimentDetectionJobPropertiesTypeDef",
    "TopicsDetectionJobPropertiesTypeDef",
    "UpdateFlywheelRequestRequestTypeDef",
    "DatasetInputDataConfigTypeDef",
    "CreateDocumentClassifierRequestRequestTypeDef",
    "DocumentClassifierPropertiesTypeDef",
    "ClassifyDocumentResponseTypeDef",
    "TaskConfigTypeDef",
    "CreateEntityRecognizerRequestRequestTypeDef",
    "EntityRecognizerMetadataTypeDef",
    "DescribeFlywheelIterationResponseTypeDef",
    "ListFlywheelIterationHistoryResponseTypeDef",
    "BlockTypeDef",
    "BatchDetectSyntaxItemResultTypeDef",
    "DetectSyntaxResponseTypeDef",
    "TargetedSentimentEntityTypeDef",
    "BatchDetectEntitiesItemResultTypeDef",
    "DescribeDocumentClassificationJobResponseTypeDef",
    "ListDocumentClassificationJobsResponseTypeDef",
    "DescribeDominantLanguageDetectionJobResponseTypeDef",
    "ListDominantLanguageDetectionJobsResponseTypeDef",
    "DescribeEntitiesDetectionJobResponseTypeDef",
    "ListEntitiesDetectionJobsResponseTypeDef",
    "DescribeEventsDetectionJobResponseTypeDef",
    "ListEventsDetectionJobsResponseTypeDef",
    "DescribeKeyPhrasesDetectionJobResponseTypeDef",
    "ListKeyPhrasesDetectionJobsResponseTypeDef",
    "DescribePiiEntitiesDetectionJobResponseTypeDef",
    "ListPiiEntitiesDetectionJobsResponseTypeDef",
    "DescribeSentimentDetectionJobResponseTypeDef",
    "ListSentimentDetectionJobsResponseTypeDef",
    "DescribeTargetedSentimentDetectionJobResponseTypeDef",
    "ListTargetedSentimentDetectionJobsResponseTypeDef",
    "DescribeTopicsDetectionJobResponseTypeDef",
    "ListTopicsDetectionJobsResponseTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "DescribeDocumentClassifierResponseTypeDef",
    "ListDocumentClassifiersResponseTypeDef",
    "CreateFlywheelRequestRequestTypeDef",
    "FlywheelPropertiesTypeDef",
    "EntityRecognizerPropertiesTypeDef",
    "DetectEntitiesResponseTypeDef",
    "BatchDetectSyntaxResponseTypeDef",
    "BatchDetectTargetedSentimentItemResultTypeDef",
    "DetectTargetedSentimentResponseTypeDef",
    "BatchDetectEntitiesResponseTypeDef",
    "DescribeFlywheelResponseTypeDef",
    "UpdateFlywheelResponseTypeDef",
    "DescribeEntityRecognizerResponseTypeDef",
    "ListEntityRecognizersResponseTypeDef",
    "BatchDetectTargetedSentimentResponseTypeDef",
)

_RequiredAugmentedManifestsListItemTypeDef = TypedDict(
    "_RequiredAugmentedManifestsListItemTypeDef",
    {
        "S3Uri": str,
        "AttributeNames": Sequence[str],
    },
)
_OptionalAugmentedManifestsListItemTypeDef = TypedDict(
    "_OptionalAugmentedManifestsListItemTypeDef",
    {
        "Split": SplitType,
        "AnnotationDataS3Uri": str,
        "SourceDocumentsS3Uri": str,
        "DocumentType": AugmentedManifestsDocumentTypeFormatType,
    },
    total=False,
)

class AugmentedManifestsListItemTypeDef(
    _RequiredAugmentedManifestsListItemTypeDef, _OptionalAugmentedManifestsListItemTypeDef
):
    pass

DominantLanguageTypeDef = TypedDict(
    "DominantLanguageTypeDef",
    {
        "LanguageCode": str,
        "Score": float,
    },
    total=False,
)

BatchDetectDominantLanguageRequestRequestTypeDef = TypedDict(
    "BatchDetectDominantLanguageRequestRequestTypeDef",
    {
        "TextList": Sequence[str],
    },
)

BatchItemErrorTypeDef = TypedDict(
    "BatchItemErrorTypeDef",
    {
        "Index": int,
        "ErrorCode": str,
        "ErrorMessage": str,
    },
    total=False,
)

BatchDetectEntitiesRequestRequestTypeDef = TypedDict(
    "BatchDetectEntitiesRequestRequestTypeDef",
    {
        "TextList": Sequence[str],
        "LanguageCode": LanguageCodeType,
    },
)

KeyPhraseTypeDef = TypedDict(
    "KeyPhraseTypeDef",
    {
        "Score": float,
        "Text": str,
        "BeginOffset": int,
        "EndOffset": int,
    },
    total=False,
)

BatchDetectKeyPhrasesRequestRequestTypeDef = TypedDict(
    "BatchDetectKeyPhrasesRequestRequestTypeDef",
    {
        "TextList": Sequence[str],
        "LanguageCode": LanguageCodeType,
    },
)

SentimentScoreTypeDef = TypedDict(
    "SentimentScoreTypeDef",
    {
        "Positive": float,
        "Negative": float,
        "Neutral": float,
        "Mixed": float,
    },
    total=False,
)

BatchDetectSentimentRequestRequestTypeDef = TypedDict(
    "BatchDetectSentimentRequestRequestTypeDef",
    {
        "TextList": Sequence[str],
        "LanguageCode": LanguageCodeType,
    },
)

BatchDetectSyntaxRequestRequestTypeDef = TypedDict(
    "BatchDetectSyntaxRequestRequestTypeDef",
    {
        "TextList": Sequence[str],
        "LanguageCode": SyntaxLanguageCodeType,
    },
)

BatchDetectTargetedSentimentRequestRequestTypeDef = TypedDict(
    "BatchDetectTargetedSentimentRequestRequestTypeDef",
    {
        "TextList": Sequence[str],
        "LanguageCode": LanguageCodeType,
    },
)

ChildBlockTypeDef = TypedDict(
    "ChildBlockTypeDef",
    {
        "ChildBlockId": str,
        "BeginOffset": int,
        "EndOffset": int,
    },
    total=False,
)

RelationshipsListItemTypeDef = TypedDict(
    "RelationshipsListItemTypeDef",
    {
        "Ids": List[str],
        "Type": Literal["CHILD"],
    },
    total=False,
)

BoundingBoxTypeDef = TypedDict(
    "BoundingBoxTypeDef",
    {
        "Height": float,
        "Left": float,
        "Top": float,
        "Width": float,
    },
    total=False,
)

ClassifierEvaluationMetricsTypeDef = TypedDict(
    "ClassifierEvaluationMetricsTypeDef",
    {
        "Accuracy": float,
        "Precision": float,
        "Recall": float,
        "F1Score": float,
        "MicroPrecision": float,
        "MicroRecall": float,
        "MicroF1Score": float,
        "HammingLoss": float,
    },
    total=False,
)

_RequiredDocumentReaderConfigTypeDef = TypedDict(
    "_RequiredDocumentReaderConfigTypeDef",
    {
        "DocumentReadAction": DocumentReadActionType,
    },
)
_OptionalDocumentReaderConfigTypeDef = TypedDict(
    "_OptionalDocumentReaderConfigTypeDef",
    {
        "DocumentReadMode": DocumentReadModeType,
        "FeatureTypes": Sequence[DocumentReadFeatureTypesType],
    },
    total=False,
)

class DocumentReaderConfigTypeDef(
    _RequiredDocumentReaderConfigTypeDef, _OptionalDocumentReaderConfigTypeDef
):
    pass

DocumentClassTypeDef = TypedDict(
    "DocumentClassTypeDef",
    {
        "Name": str,
        "Score": float,
        "Page": int,
    },
    total=False,
)

DocumentLabelTypeDef = TypedDict(
    "DocumentLabelTypeDef",
    {
        "Name": str,
        "Score": float,
        "Page": int,
    },
    total=False,
)

DocumentTypeListItemTypeDef = TypedDict(
    "DocumentTypeListItemTypeDef",
    {
        "Page": int,
        "Type": DocumentTypeType,
    },
    total=False,
)

ErrorsListItemTypeDef = TypedDict(
    "ErrorsListItemTypeDef",
    {
        "Page": int,
        "ErrorCode": PageBasedErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
)

WarningsListItemTypeDef = TypedDict(
    "WarningsListItemTypeDef",
    {
        "Page": int,
        "WarnCode": PageBasedWarningCodeType,
        "WarnMessage": str,
    },
    total=False,
)

ContainsPiiEntitiesRequestRequestTypeDef = TypedDict(
    "ContainsPiiEntitiesRequestRequestTypeDef",
    {
        "Text": str,
        "LanguageCode": LanguageCodeType,
    },
)

EntityLabelTypeDef = TypedDict(
    "EntityLabelTypeDef",
    {
        "Name": PiiEntityTypeType,
        "Score": float,
    },
    total=False,
)

_RequiredTagTypeDef = TypedDict(
    "_RequiredTagTypeDef",
    {
        "Key": str,
    },
)
_OptionalTagTypeDef = TypedDict(
    "_OptionalTagTypeDef",
    {
        "Value": str,
    },
    total=False,
)

class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass

CreateDatasetResponseTypeDef = TypedDict(
    "CreateDatasetResponseTypeDef",
    {
        "DatasetArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DocumentClassifierOutputDataConfigTypeDef = TypedDict(
    "DocumentClassifierOutputDataConfigTypeDef",
    {
        "S3Uri": str,
        "KmsKeyId": str,
        "FlywheelStatsS3Prefix": str,
    },
    total=False,
)

VpcConfigTypeDef = TypedDict(
    "VpcConfigTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "Subnets": Sequence[str],
    },
)

CreateDocumentClassifierResponseTypeDef = TypedDict(
    "CreateDocumentClassifierResponseTypeDef",
    {
        "DocumentClassifierArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateEndpointResponseTypeDef = TypedDict(
    "CreateEndpointResponseTypeDef",
    {
        "EndpointArn": str,
        "ModelArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateEntityRecognizerResponseTypeDef = TypedDict(
    "CreateEntityRecognizerResponseTypeDef",
    {
        "EntityRecognizerArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateFlywheelResponseTypeDef = TypedDict(
    "CreateFlywheelResponseTypeDef",
    {
        "FlywheelArn": str,
        "ActiveModelArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDatasetAugmentedManifestsListItemTypeDef = TypedDict(
    "_RequiredDatasetAugmentedManifestsListItemTypeDef",
    {
        "AttributeNames": Sequence[str],
        "S3Uri": str,
    },
)
_OptionalDatasetAugmentedManifestsListItemTypeDef = TypedDict(
    "_OptionalDatasetAugmentedManifestsListItemTypeDef",
    {
        "AnnotationDataS3Uri": str,
        "SourceDocumentsS3Uri": str,
        "DocumentType": AugmentedManifestsDocumentTypeFormatType,
    },
    total=False,
)

class DatasetAugmentedManifestsListItemTypeDef(
    _RequiredDatasetAugmentedManifestsListItemTypeDef,
    _OptionalDatasetAugmentedManifestsListItemTypeDef,
):
    pass

_RequiredDatasetDocumentClassifierInputDataConfigTypeDef = TypedDict(
    "_RequiredDatasetDocumentClassifierInputDataConfigTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalDatasetDocumentClassifierInputDataConfigTypeDef = TypedDict(
    "_OptionalDatasetDocumentClassifierInputDataConfigTypeDef",
    {
        "LabelDelimiter": str,
    },
    total=False,
)

class DatasetDocumentClassifierInputDataConfigTypeDef(
    _RequiredDatasetDocumentClassifierInputDataConfigTypeDef,
    _OptionalDatasetDocumentClassifierInputDataConfigTypeDef,
):
    pass

DatasetEntityRecognizerAnnotationsTypeDef = TypedDict(
    "DatasetEntityRecognizerAnnotationsTypeDef",
    {
        "S3Uri": str,
    },
)

_RequiredDatasetEntityRecognizerDocumentsTypeDef = TypedDict(
    "_RequiredDatasetEntityRecognizerDocumentsTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalDatasetEntityRecognizerDocumentsTypeDef = TypedDict(
    "_OptionalDatasetEntityRecognizerDocumentsTypeDef",
    {
        "InputFormat": InputFormatType,
    },
    total=False,
)

class DatasetEntityRecognizerDocumentsTypeDef(
    _RequiredDatasetEntityRecognizerDocumentsTypeDef,
    _OptionalDatasetEntityRecognizerDocumentsTypeDef,
):
    pass

DatasetEntityRecognizerEntityListTypeDef = TypedDict(
    "DatasetEntityRecognizerEntityListTypeDef",
    {
        "S3Uri": str,
    },
)

DatasetFilterTypeDef = TypedDict(
    "DatasetFilterTypeDef",
    {
        "Status": DatasetStatusType,
        "DatasetType": DatasetTypeType,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
    },
    total=False,
)

DatasetPropertiesTypeDef = TypedDict(
    "DatasetPropertiesTypeDef",
    {
        "DatasetArn": str,
        "DatasetName": str,
        "DatasetType": DatasetTypeType,
        "DatasetS3Uri": str,
        "Description": str,
        "Status": DatasetStatusType,
        "Message": str,
        "NumberOfDocuments": int,
        "CreationTime": datetime,
        "EndTime": datetime,
    },
    total=False,
)

DeleteDocumentClassifierRequestRequestTypeDef = TypedDict(
    "DeleteDocumentClassifierRequestRequestTypeDef",
    {
        "DocumentClassifierArn": str,
    },
)

DeleteEndpointRequestRequestTypeDef = TypedDict(
    "DeleteEndpointRequestRequestTypeDef",
    {
        "EndpointArn": str,
    },
)

DeleteEntityRecognizerRequestRequestTypeDef = TypedDict(
    "DeleteEntityRecognizerRequestRequestTypeDef",
    {
        "EntityRecognizerArn": str,
    },
)

DeleteFlywheelRequestRequestTypeDef = TypedDict(
    "DeleteFlywheelRequestRequestTypeDef",
    {
        "FlywheelArn": str,
    },
)

_RequiredDeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalDeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteResourcePolicyRequestRequestTypeDef",
    {
        "PolicyRevisionId": str,
    },
    total=False,
)

class DeleteResourcePolicyRequestRequestTypeDef(
    _RequiredDeleteResourcePolicyRequestRequestTypeDef,
    _OptionalDeleteResourcePolicyRequestRequestTypeDef,
):
    pass

DescribeDatasetRequestRequestTypeDef = TypedDict(
    "DescribeDatasetRequestRequestTypeDef",
    {
        "DatasetArn": str,
    },
)

DescribeDocumentClassificationJobRequestRequestTypeDef = TypedDict(
    "DescribeDocumentClassificationJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DescribeDocumentClassifierRequestRequestTypeDef = TypedDict(
    "DescribeDocumentClassifierRequestRequestTypeDef",
    {
        "DocumentClassifierArn": str,
    },
)

DescribeDominantLanguageDetectionJobRequestRequestTypeDef = TypedDict(
    "DescribeDominantLanguageDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DescribeEndpointRequestRequestTypeDef = TypedDict(
    "DescribeEndpointRequestRequestTypeDef",
    {
        "EndpointArn": str,
    },
)

EndpointPropertiesTypeDef = TypedDict(
    "EndpointPropertiesTypeDef",
    {
        "EndpointArn": str,
        "Status": EndpointStatusType,
        "Message": str,
        "ModelArn": str,
        "DesiredModelArn": str,
        "DesiredInferenceUnits": int,
        "CurrentInferenceUnits": int,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "DataAccessRoleArn": str,
        "DesiredDataAccessRoleArn": str,
        "FlywheelArn": str,
    },
    total=False,
)

DescribeEntitiesDetectionJobRequestRequestTypeDef = TypedDict(
    "DescribeEntitiesDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DescribeEntityRecognizerRequestRequestTypeDef = TypedDict(
    "DescribeEntityRecognizerRequestRequestTypeDef",
    {
        "EntityRecognizerArn": str,
    },
)

DescribeEventsDetectionJobRequestRequestTypeDef = TypedDict(
    "DescribeEventsDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DescribeFlywheelIterationRequestRequestTypeDef = TypedDict(
    "DescribeFlywheelIterationRequestRequestTypeDef",
    {
        "FlywheelArn": str,
        "FlywheelIterationId": str,
    },
)

DescribeFlywheelRequestRequestTypeDef = TypedDict(
    "DescribeFlywheelRequestRequestTypeDef",
    {
        "FlywheelArn": str,
    },
)

DescribeKeyPhrasesDetectionJobRequestRequestTypeDef = TypedDict(
    "DescribeKeyPhrasesDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DescribePiiEntitiesDetectionJobRequestRequestTypeDef = TypedDict(
    "DescribePiiEntitiesDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DescribeResourcePolicyRequestRequestTypeDef = TypedDict(
    "DescribeResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DescribeResourcePolicyResponseTypeDef = TypedDict(
    "DescribeResourcePolicyResponseTypeDef",
    {
        "ResourcePolicy": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "PolicyRevisionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSentimentDetectionJobRequestRequestTypeDef = TypedDict(
    "DescribeSentimentDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DescribeTargetedSentimentDetectionJobRequestRequestTypeDef = TypedDict(
    "DescribeTargetedSentimentDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DescribeTopicsDetectionJobRequestRequestTypeDef = TypedDict(
    "DescribeTopicsDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

DetectDominantLanguageRequestRequestTypeDef = TypedDict(
    "DetectDominantLanguageRequestRequestTypeDef",
    {
        "Text": str,
    },
)

DetectKeyPhrasesRequestRequestTypeDef = TypedDict(
    "DetectKeyPhrasesRequestRequestTypeDef",
    {
        "Text": str,
        "LanguageCode": LanguageCodeType,
    },
)

DetectPiiEntitiesRequestRequestTypeDef = TypedDict(
    "DetectPiiEntitiesRequestRequestTypeDef",
    {
        "Text": str,
        "LanguageCode": LanguageCodeType,
    },
)

PiiEntityTypeDef = TypedDict(
    "PiiEntityTypeDef",
    {
        "Score": float,
        "Type": PiiEntityTypeType,
        "BeginOffset": int,
        "EndOffset": int,
    },
    total=False,
)

DetectSentimentRequestRequestTypeDef = TypedDict(
    "DetectSentimentRequestRequestTypeDef",
    {
        "Text": str,
        "LanguageCode": LanguageCodeType,
    },
)

DetectSyntaxRequestRequestTypeDef = TypedDict(
    "DetectSyntaxRequestRequestTypeDef",
    {
        "Text": str,
        "LanguageCode": SyntaxLanguageCodeType,
    },
)

DetectTargetedSentimentRequestRequestTypeDef = TypedDict(
    "DetectTargetedSentimentRequestRequestTypeDef",
    {
        "Text": str,
        "LanguageCode": LanguageCodeType,
    },
)

_RequiredDocumentClassificationConfigTypeDef = TypedDict(
    "_RequiredDocumentClassificationConfigTypeDef",
    {
        "Mode": DocumentClassifierModeType,
    },
)
_OptionalDocumentClassificationConfigTypeDef = TypedDict(
    "_OptionalDocumentClassificationConfigTypeDef",
    {
        "Labels": Sequence[str],
    },
    total=False,
)

class DocumentClassificationConfigTypeDef(
    _RequiredDocumentClassificationConfigTypeDef, _OptionalDocumentClassificationConfigTypeDef
):
    pass

DocumentClassificationJobFilterTypeDef = TypedDict(
    "DocumentClassificationJobFilterTypeDef",
    {
        "JobName": str,
        "JobStatus": JobStatusType,
        "SubmitTimeBefore": Union[datetime, str],
        "SubmitTimeAfter": Union[datetime, str],
    },
    total=False,
)

_RequiredOutputDataConfigTypeDef = TypedDict(
    "_RequiredOutputDataConfigTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalOutputDataConfigTypeDef = TypedDict(
    "_OptionalOutputDataConfigTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)

class OutputDataConfigTypeDef(_RequiredOutputDataConfigTypeDef, _OptionalOutputDataConfigTypeDef):
    pass

_RequiredDocumentClassifierDocumentsTypeDef = TypedDict(
    "_RequiredDocumentClassifierDocumentsTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalDocumentClassifierDocumentsTypeDef = TypedDict(
    "_OptionalDocumentClassifierDocumentsTypeDef",
    {
        "TestS3Uri": str,
    },
    total=False,
)

class DocumentClassifierDocumentsTypeDef(
    _RequiredDocumentClassifierDocumentsTypeDef, _OptionalDocumentClassifierDocumentsTypeDef
):
    pass

DocumentClassifierFilterTypeDef = TypedDict(
    "DocumentClassifierFilterTypeDef",
    {
        "Status": ModelStatusType,
        "DocumentClassifierName": str,
        "SubmitTimeBefore": Union[datetime, str],
        "SubmitTimeAfter": Union[datetime, str],
    },
    total=False,
)

DocumentClassifierSummaryTypeDef = TypedDict(
    "DocumentClassifierSummaryTypeDef",
    {
        "DocumentClassifierName": str,
        "NumberOfVersions": int,
        "LatestVersionCreatedAt": datetime,
        "LatestVersionName": str,
        "LatestVersionStatus": ModelStatusType,
    },
    total=False,
)

ExtractedCharactersListItemTypeDef = TypedDict(
    "ExtractedCharactersListItemTypeDef",
    {
        "Page": int,
        "Count": int,
    },
    total=False,
)

DominantLanguageDetectionJobFilterTypeDef = TypedDict(
    "DominantLanguageDetectionJobFilterTypeDef",
    {
        "JobName": str,
        "JobStatus": JobStatusType,
        "SubmitTimeBefore": Union[datetime, str],
        "SubmitTimeAfter": Union[datetime, str],
    },
    total=False,
)

EndpointFilterTypeDef = TypedDict(
    "EndpointFilterTypeDef",
    {
        "ModelArn": str,
        "Status": EndpointStatusType,
        "CreationTimeBefore": Union[datetime, str],
        "CreationTimeAfter": Union[datetime, str],
    },
    total=False,
)

EntitiesDetectionJobFilterTypeDef = TypedDict(
    "EntitiesDetectionJobFilterTypeDef",
    {
        "JobName": str,
        "JobStatus": JobStatusType,
        "SubmitTimeBefore": Union[datetime, str],
        "SubmitTimeAfter": Union[datetime, str],
    },
    total=False,
)

EntityTypesListItemTypeDef = TypedDict(
    "EntityTypesListItemTypeDef",
    {
        "Type": str,
    },
)

_RequiredEntityRecognizerAnnotationsTypeDef = TypedDict(
    "_RequiredEntityRecognizerAnnotationsTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalEntityRecognizerAnnotationsTypeDef = TypedDict(
    "_OptionalEntityRecognizerAnnotationsTypeDef",
    {
        "TestS3Uri": str,
    },
    total=False,
)

class EntityRecognizerAnnotationsTypeDef(
    _RequiredEntityRecognizerAnnotationsTypeDef, _OptionalEntityRecognizerAnnotationsTypeDef
):
    pass

_RequiredEntityRecognizerDocumentsTypeDef = TypedDict(
    "_RequiredEntityRecognizerDocumentsTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalEntityRecognizerDocumentsTypeDef = TypedDict(
    "_OptionalEntityRecognizerDocumentsTypeDef",
    {
        "TestS3Uri": str,
        "InputFormat": InputFormatType,
    },
    total=False,
)

class EntityRecognizerDocumentsTypeDef(
    _RequiredEntityRecognizerDocumentsTypeDef, _OptionalEntityRecognizerDocumentsTypeDef
):
    pass

EntityRecognizerEntityListTypeDef = TypedDict(
    "EntityRecognizerEntityListTypeDef",
    {
        "S3Uri": str,
    },
)

EntityRecognizerEvaluationMetricsTypeDef = TypedDict(
    "EntityRecognizerEvaluationMetricsTypeDef",
    {
        "Precision": float,
        "Recall": float,
        "F1Score": float,
    },
    total=False,
)

EntityRecognizerFilterTypeDef = TypedDict(
    "EntityRecognizerFilterTypeDef",
    {
        "Status": ModelStatusType,
        "RecognizerName": str,
        "SubmitTimeBefore": Union[datetime, str],
        "SubmitTimeAfter": Union[datetime, str],
    },
    total=False,
)

EntityTypesEvaluationMetricsTypeDef = TypedDict(
    "EntityTypesEvaluationMetricsTypeDef",
    {
        "Precision": float,
        "Recall": float,
        "F1Score": float,
    },
    total=False,
)

EntityRecognizerOutputDataConfigTypeDef = TypedDict(
    "EntityRecognizerOutputDataConfigTypeDef",
    {
        "FlywheelStatsS3Prefix": str,
    },
    total=False,
)

EntityRecognizerSummaryTypeDef = TypedDict(
    "EntityRecognizerSummaryTypeDef",
    {
        "RecognizerName": str,
        "NumberOfVersions": int,
        "LatestVersionCreatedAt": datetime,
        "LatestVersionName": str,
        "LatestVersionStatus": ModelStatusType,
    },
    total=False,
)

EventsDetectionJobFilterTypeDef = TypedDict(
    "EventsDetectionJobFilterTypeDef",
    {
        "JobName": str,
        "JobStatus": JobStatusType,
        "SubmitTimeBefore": Union[datetime, str],
        "SubmitTimeAfter": Union[datetime, str],
    },
    total=False,
)

FlywheelFilterTypeDef = TypedDict(
    "FlywheelFilterTypeDef",
    {
        "Status": FlywheelStatusType,
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
    },
    total=False,
)

FlywheelIterationFilterTypeDef = TypedDict(
    "FlywheelIterationFilterTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
    },
    total=False,
)

FlywheelModelEvaluationMetricsTypeDef = TypedDict(
    "FlywheelModelEvaluationMetricsTypeDef",
    {
        "AverageF1Score": float,
        "AveragePrecision": float,
        "AverageRecall": float,
        "AverageAccuracy": float,
    },
    total=False,
)

FlywheelSummaryTypeDef = TypedDict(
    "FlywheelSummaryTypeDef",
    {
        "FlywheelArn": str,
        "ActiveModelArn": str,
        "DataLakeS3Uri": str,
        "Status": FlywheelStatusType,
        "ModelType": ModelTypeType,
        "Message": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LatestFlywheelIteration": str,
    },
    total=False,
)

PointTypeDef = TypedDict(
    "PointTypeDef",
    {
        "X": float,
        "Y": float,
    },
    total=False,
)

ImportModelResponseTypeDef = TypedDict(
    "ImportModelResponseTypeDef",
    {
        "ModelArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

KeyPhrasesDetectionJobFilterTypeDef = TypedDict(
    "KeyPhrasesDetectionJobFilterTypeDef",
    {
        "JobName": str,
        "JobStatus": JobStatusType,
        "SubmitTimeBefore": Union[datetime, str],
        "SubmitTimeAfter": Union[datetime, str],
    },
    total=False,
)

ListDocumentClassifierSummariesRequestRequestTypeDef = TypedDict(
    "ListDocumentClassifierSummariesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListEntityRecognizerSummariesRequestRequestTypeDef = TypedDict(
    "ListEntityRecognizerSummariesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

PiiEntitiesDetectionJobFilterTypeDef = TypedDict(
    "PiiEntitiesDetectionJobFilterTypeDef",
    {
        "JobName": str,
        "JobStatus": JobStatusType,
        "SubmitTimeBefore": Union[datetime, str],
        "SubmitTimeAfter": Union[datetime, str],
    },
    total=False,
)

SentimentDetectionJobFilterTypeDef = TypedDict(
    "SentimentDetectionJobFilterTypeDef",
    {
        "JobName": str,
        "JobStatus": JobStatusType,
        "SubmitTimeBefore": Union[datetime, str],
        "SubmitTimeAfter": Union[datetime, str],
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

TargetedSentimentDetectionJobFilterTypeDef = TypedDict(
    "TargetedSentimentDetectionJobFilterTypeDef",
    {
        "JobName": str,
        "JobStatus": JobStatusType,
        "SubmitTimeBefore": Union[datetime, str],
        "SubmitTimeAfter": Union[datetime, str],
    },
    total=False,
)

TopicsDetectionJobFilterTypeDef = TypedDict(
    "TopicsDetectionJobFilterTypeDef",
    {
        "JobName": str,
        "JobStatus": JobStatusType,
        "SubmitTimeBefore": Union[datetime, str],
        "SubmitTimeAfter": Union[datetime, str],
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

PartOfSpeechTagTypeDef = TypedDict(
    "PartOfSpeechTagTypeDef",
    {
        "Tag": PartOfSpeechTagTypeType,
        "Score": float,
    },
    total=False,
)

_RequiredPiiOutputDataConfigTypeDef = TypedDict(
    "_RequiredPiiOutputDataConfigTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalPiiOutputDataConfigTypeDef = TypedDict(
    "_OptionalPiiOutputDataConfigTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)

class PiiOutputDataConfigTypeDef(
    _RequiredPiiOutputDataConfigTypeDef, _OptionalPiiOutputDataConfigTypeDef
):
    pass

RedactionConfigTypeDef = TypedDict(
    "RedactionConfigTypeDef",
    {
        "PiiEntityTypes": List[PiiEntityTypeType],
        "MaskMode": PiiEntitiesDetectionMaskModeType,
        "MaskCharacter": str,
    },
    total=False,
)

_RequiredPutResourcePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredPutResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "ResourcePolicy": str,
    },
)
_OptionalPutResourcePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalPutResourcePolicyRequestRequestTypeDef",
    {
        "PolicyRevisionId": str,
    },
    total=False,
)

class PutResourcePolicyRequestRequestTypeDef(
    _RequiredPutResourcePolicyRequestRequestTypeDef, _OptionalPutResourcePolicyRequestRequestTypeDef
):
    pass

PutResourcePolicyResponseTypeDef = TypedDict(
    "PutResourcePolicyResponseTypeDef",
    {
        "PolicyRevisionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

StartDocumentClassificationJobResponseTypeDef = TypedDict(
    "StartDocumentClassificationJobResponseTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobStatus": JobStatusType,
        "DocumentClassifierArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartDominantLanguageDetectionJobResponseTypeDef = TypedDict(
    "StartDominantLanguageDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartEntitiesDetectionJobResponseTypeDef = TypedDict(
    "StartEntitiesDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobStatus": JobStatusType,
        "EntityRecognizerArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartEventsDetectionJobResponseTypeDef = TypedDict(
    "StartEventsDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredStartFlywheelIterationRequestRequestTypeDef = TypedDict(
    "_RequiredStartFlywheelIterationRequestRequestTypeDef",
    {
        "FlywheelArn": str,
    },
)
_OptionalStartFlywheelIterationRequestRequestTypeDef = TypedDict(
    "_OptionalStartFlywheelIterationRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
    },
    total=False,
)

class StartFlywheelIterationRequestRequestTypeDef(
    _RequiredStartFlywheelIterationRequestRequestTypeDef,
    _OptionalStartFlywheelIterationRequestRequestTypeDef,
):
    pass

StartFlywheelIterationResponseTypeDef = TypedDict(
    "StartFlywheelIterationResponseTypeDef",
    {
        "FlywheelArn": str,
        "FlywheelIterationId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartKeyPhrasesDetectionJobResponseTypeDef = TypedDict(
    "StartKeyPhrasesDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartPiiEntitiesDetectionJobResponseTypeDef = TypedDict(
    "StartPiiEntitiesDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartSentimentDetectionJobResponseTypeDef = TypedDict(
    "StartSentimentDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartTargetedSentimentDetectionJobResponseTypeDef = TypedDict(
    "StartTargetedSentimentDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartTopicsDetectionJobResponseTypeDef = TypedDict(
    "StartTopicsDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopDominantLanguageDetectionJobRequestRequestTypeDef = TypedDict(
    "StopDominantLanguageDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

StopDominantLanguageDetectionJobResponseTypeDef = TypedDict(
    "StopDominantLanguageDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopEntitiesDetectionJobRequestRequestTypeDef = TypedDict(
    "StopEntitiesDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

StopEntitiesDetectionJobResponseTypeDef = TypedDict(
    "StopEntitiesDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopEventsDetectionJobRequestRequestTypeDef = TypedDict(
    "StopEventsDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

StopEventsDetectionJobResponseTypeDef = TypedDict(
    "StopEventsDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopKeyPhrasesDetectionJobRequestRequestTypeDef = TypedDict(
    "StopKeyPhrasesDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

StopKeyPhrasesDetectionJobResponseTypeDef = TypedDict(
    "StopKeyPhrasesDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopPiiEntitiesDetectionJobRequestRequestTypeDef = TypedDict(
    "StopPiiEntitiesDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

StopPiiEntitiesDetectionJobResponseTypeDef = TypedDict(
    "StopPiiEntitiesDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopSentimentDetectionJobRequestRequestTypeDef = TypedDict(
    "StopSentimentDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

StopSentimentDetectionJobResponseTypeDef = TypedDict(
    "StopSentimentDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopTargetedSentimentDetectionJobRequestRequestTypeDef = TypedDict(
    "StopTargetedSentimentDetectionJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

StopTargetedSentimentDetectionJobResponseTypeDef = TypedDict(
    "StopTargetedSentimentDetectionJobResponseTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopTrainingDocumentClassifierRequestRequestTypeDef = TypedDict(
    "StopTrainingDocumentClassifierRequestRequestTypeDef",
    {
        "DocumentClassifierArn": str,
    },
)

StopTrainingEntityRecognizerRequestRequestTypeDef = TypedDict(
    "StopTrainingEntityRecognizerRequestRequestTypeDef",
    {
        "EntityRecognizerArn": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEndpointRequestRequestTypeDef",
    {
        "EndpointArn": str,
    },
)
_OptionalUpdateEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEndpointRequestRequestTypeDef",
    {
        "DesiredModelArn": str,
        "DesiredInferenceUnits": int,
        "DesiredDataAccessRoleArn": str,
        "FlywheelArn": str,
    },
    total=False,
)

class UpdateEndpointRequestRequestTypeDef(
    _RequiredUpdateEndpointRequestRequestTypeDef, _OptionalUpdateEndpointRequestRequestTypeDef
):
    pass

UpdateEndpointResponseTypeDef = TypedDict(
    "UpdateEndpointResponseTypeDef",
    {
        "DesiredModelArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchDetectDominantLanguageItemResultTypeDef = TypedDict(
    "BatchDetectDominantLanguageItemResultTypeDef",
    {
        "Index": int,
        "Languages": List[DominantLanguageTypeDef],
    },
    total=False,
)

DetectDominantLanguageResponseTypeDef = TypedDict(
    "DetectDominantLanguageResponseTypeDef",
    {
        "Languages": List[DominantLanguageTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchDetectKeyPhrasesItemResultTypeDef = TypedDict(
    "BatchDetectKeyPhrasesItemResultTypeDef",
    {
        "Index": int,
        "KeyPhrases": List[KeyPhraseTypeDef],
    },
    total=False,
)

DetectKeyPhrasesResponseTypeDef = TypedDict(
    "DetectKeyPhrasesResponseTypeDef",
    {
        "KeyPhrases": List[KeyPhraseTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchDetectSentimentItemResultTypeDef = TypedDict(
    "BatchDetectSentimentItemResultTypeDef",
    {
        "Index": int,
        "Sentiment": SentimentTypeType,
        "SentimentScore": SentimentScoreTypeDef,
    },
    total=False,
)

DetectSentimentResponseTypeDef = TypedDict(
    "DetectSentimentResponseTypeDef",
    {
        "Sentiment": SentimentTypeType,
        "SentimentScore": SentimentScoreTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MentionSentimentTypeDef = TypedDict(
    "MentionSentimentTypeDef",
    {
        "Sentiment": SentimentTypeType,
        "SentimentScore": SentimentScoreTypeDef,
    },
    total=False,
)

BlockReferenceTypeDef = TypedDict(
    "BlockReferenceTypeDef",
    {
        "BlockId": str,
        "BeginOffset": int,
        "EndOffset": int,
        "ChildBlocks": List[ChildBlockTypeDef],
    },
    total=False,
)

ClassifierMetadataTypeDef = TypedDict(
    "ClassifierMetadataTypeDef",
    {
        "NumberOfLabels": int,
        "NumberOfTrainedDocuments": int,
        "NumberOfTestDocuments": int,
        "EvaluationMetrics": ClassifierEvaluationMetricsTypeDef,
    },
    total=False,
)

_RequiredClassifyDocumentRequestRequestTypeDef = TypedDict(
    "_RequiredClassifyDocumentRequestRequestTypeDef",
    {
        "EndpointArn": str,
    },
)
_OptionalClassifyDocumentRequestRequestTypeDef = TypedDict(
    "_OptionalClassifyDocumentRequestRequestTypeDef",
    {
        "Text": str,
        "Bytes": Union[str, bytes, IO[Any], StreamingBody],
        "DocumentReaderConfig": DocumentReaderConfigTypeDef,
    },
    total=False,
)

class ClassifyDocumentRequestRequestTypeDef(
    _RequiredClassifyDocumentRequestRequestTypeDef, _OptionalClassifyDocumentRequestRequestTypeDef
):
    pass

DetectEntitiesRequestRequestTypeDef = TypedDict(
    "DetectEntitiesRequestRequestTypeDef",
    {
        "Text": str,
        "LanguageCode": LanguageCodeType,
        "EndpointArn": str,
        "Bytes": Union[str, bytes, IO[Any], StreamingBody],
        "DocumentReaderConfig": DocumentReaderConfigTypeDef,
    },
    total=False,
)

_RequiredInputDataConfigTypeDef = TypedDict(
    "_RequiredInputDataConfigTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalInputDataConfigTypeDef = TypedDict(
    "_OptionalInputDataConfigTypeDef",
    {
        "InputFormat": InputFormatType,
        "DocumentReaderConfig": DocumentReaderConfigTypeDef,
    },
    total=False,
)

class InputDataConfigTypeDef(_RequiredInputDataConfigTypeDef, _OptionalInputDataConfigTypeDef):
    pass

ContainsPiiEntitiesResponseTypeDef = TypedDict(
    "ContainsPiiEntitiesResponseTypeDef",
    {
        "Labels": List[EntityLabelTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEndpointRequestRequestTypeDef",
    {
        "EndpointName": str,
        "DesiredInferenceUnits": int,
    },
)
_OptionalCreateEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEndpointRequestRequestTypeDef",
    {
        "ModelArn": str,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
        "DataAccessRoleArn": str,
        "FlywheelArn": str,
    },
    total=False,
)

class CreateEndpointRequestRequestTypeDef(
    _RequiredCreateEndpointRequestRequestTypeDef, _OptionalCreateEndpointRequestRequestTypeDef
):
    pass

_RequiredImportModelRequestRequestTypeDef = TypedDict(
    "_RequiredImportModelRequestRequestTypeDef",
    {
        "SourceModelArn": str,
    },
)
_OptionalImportModelRequestRequestTypeDef = TypedDict(
    "_OptionalImportModelRequestRequestTypeDef",
    {
        "ModelName": str,
        "VersionName": str,
        "ModelKmsKeyId": str,
        "DataAccessRoleArn": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class ImportModelRequestRequestTypeDef(
    _RequiredImportModelRequestRequestTypeDef, _OptionalImportModelRequestRequestTypeDef
):
    pass

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "ResourceArn": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

DataSecurityConfigTypeDef = TypedDict(
    "DataSecurityConfigTypeDef",
    {
        "ModelKmsKeyId": str,
        "VolumeKmsKeyId": str,
        "DataLakeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
    },
    total=False,
)

UpdateDataSecurityConfigTypeDef = TypedDict(
    "UpdateDataSecurityConfigTypeDef",
    {
        "ModelKmsKeyId": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
    },
    total=False,
)

_RequiredDatasetEntityRecognizerInputDataConfigTypeDef = TypedDict(
    "_RequiredDatasetEntityRecognizerInputDataConfigTypeDef",
    {
        "Documents": DatasetEntityRecognizerDocumentsTypeDef,
    },
)
_OptionalDatasetEntityRecognizerInputDataConfigTypeDef = TypedDict(
    "_OptionalDatasetEntityRecognizerInputDataConfigTypeDef",
    {
        "Annotations": DatasetEntityRecognizerAnnotationsTypeDef,
        "EntityList": DatasetEntityRecognizerEntityListTypeDef,
    },
    total=False,
)

class DatasetEntityRecognizerInputDataConfigTypeDef(
    _RequiredDatasetEntityRecognizerInputDataConfigTypeDef,
    _OptionalDatasetEntityRecognizerInputDataConfigTypeDef,
):
    pass

ListDatasetsRequestRequestTypeDef = TypedDict(
    "ListDatasetsRequestRequestTypeDef",
    {
        "FlywheelArn": str,
        "Filter": DatasetFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribeDatasetResponseTypeDef = TypedDict(
    "DescribeDatasetResponseTypeDef",
    {
        "DatasetProperties": DatasetPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDatasetsResponseTypeDef = TypedDict(
    "ListDatasetsResponseTypeDef",
    {
        "DatasetPropertiesList": List[DatasetPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEndpointResponseTypeDef = TypedDict(
    "DescribeEndpointResponseTypeDef",
    {
        "EndpointProperties": EndpointPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEndpointsResponseTypeDef = TypedDict(
    "ListEndpointsResponseTypeDef",
    {
        "EndpointPropertiesList": List[EndpointPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DetectPiiEntitiesResponseTypeDef = TypedDict(
    "DetectPiiEntitiesResponseTypeDef",
    {
        "Entities": List[PiiEntityTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDocumentClassificationJobsRequestListDocumentClassificationJobsPaginateTypeDef = TypedDict(
    "ListDocumentClassificationJobsRequestListDocumentClassificationJobsPaginateTypeDef",
    {
        "Filter": DocumentClassificationJobFilterTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDocumentClassificationJobsRequestRequestTypeDef = TypedDict(
    "ListDocumentClassificationJobsRequestRequestTypeDef",
    {
        "Filter": DocumentClassificationJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DocumentClassifierInputDataConfigTypeDef = TypedDict(
    "DocumentClassifierInputDataConfigTypeDef",
    {
        "DataFormat": DocumentClassifierDataFormatType,
        "S3Uri": str,
        "TestS3Uri": str,
        "LabelDelimiter": str,
        "AugmentedManifests": Sequence[AugmentedManifestsListItemTypeDef],
        "DocumentType": DocumentClassifierDocumentTypeFormatType,
        "Documents": DocumentClassifierDocumentsTypeDef,
        "DocumentReaderConfig": DocumentReaderConfigTypeDef,
    },
    total=False,
)

ListDocumentClassifiersRequestListDocumentClassifiersPaginateTypeDef = TypedDict(
    "ListDocumentClassifiersRequestListDocumentClassifiersPaginateTypeDef",
    {
        "Filter": DocumentClassifierFilterTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDocumentClassifiersRequestRequestTypeDef = TypedDict(
    "ListDocumentClassifiersRequestRequestTypeDef",
    {
        "Filter": DocumentClassifierFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListDocumentClassifierSummariesResponseTypeDef = TypedDict(
    "ListDocumentClassifierSummariesResponseTypeDef",
    {
        "DocumentClassifierSummariesList": List[DocumentClassifierSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DocumentMetadataTypeDef = TypedDict(
    "DocumentMetadataTypeDef",
    {
        "Pages": int,
        "ExtractedCharacters": List[ExtractedCharactersListItemTypeDef],
    },
    total=False,
)

ListDominantLanguageDetectionJobsRequestListDominantLanguageDetectionJobsPaginateTypeDef = (
    TypedDict(
        "ListDominantLanguageDetectionJobsRequestListDominantLanguageDetectionJobsPaginateTypeDef",
        {
            "Filter": DominantLanguageDetectionJobFilterTypeDef,
            "PaginationConfig": "PaginatorConfigTypeDef",
        },
        total=False,
    )
)

ListDominantLanguageDetectionJobsRequestRequestTypeDef = TypedDict(
    "ListDominantLanguageDetectionJobsRequestRequestTypeDef",
    {
        "Filter": DominantLanguageDetectionJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListEndpointsRequestListEndpointsPaginateTypeDef = TypedDict(
    "ListEndpointsRequestListEndpointsPaginateTypeDef",
    {
        "Filter": EndpointFilterTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEndpointsRequestRequestTypeDef = TypedDict(
    "ListEndpointsRequestRequestTypeDef",
    {
        "Filter": EndpointFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListEntitiesDetectionJobsRequestListEntitiesDetectionJobsPaginateTypeDef = TypedDict(
    "ListEntitiesDetectionJobsRequestListEntitiesDetectionJobsPaginateTypeDef",
    {
        "Filter": EntitiesDetectionJobFilterTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEntitiesDetectionJobsRequestRequestTypeDef = TypedDict(
    "ListEntitiesDetectionJobsRequestRequestTypeDef",
    {
        "Filter": EntitiesDetectionJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

EntityRecognitionConfigTypeDef = TypedDict(
    "EntityRecognitionConfigTypeDef",
    {
        "EntityTypes": Sequence[EntityTypesListItemTypeDef],
    },
)

_RequiredEntityRecognizerInputDataConfigTypeDef = TypedDict(
    "_RequiredEntityRecognizerInputDataConfigTypeDef",
    {
        "EntityTypes": Sequence[EntityTypesListItemTypeDef],
    },
)
_OptionalEntityRecognizerInputDataConfigTypeDef = TypedDict(
    "_OptionalEntityRecognizerInputDataConfigTypeDef",
    {
        "DataFormat": EntityRecognizerDataFormatType,
        "Documents": EntityRecognizerDocumentsTypeDef,
        "Annotations": EntityRecognizerAnnotationsTypeDef,
        "EntityList": EntityRecognizerEntityListTypeDef,
        "AugmentedManifests": Sequence[AugmentedManifestsListItemTypeDef],
    },
    total=False,
)

class EntityRecognizerInputDataConfigTypeDef(
    _RequiredEntityRecognizerInputDataConfigTypeDef, _OptionalEntityRecognizerInputDataConfigTypeDef
):
    pass

ListEntityRecognizersRequestListEntityRecognizersPaginateTypeDef = TypedDict(
    "ListEntityRecognizersRequestListEntityRecognizersPaginateTypeDef",
    {
        "Filter": EntityRecognizerFilterTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEntityRecognizersRequestRequestTypeDef = TypedDict(
    "ListEntityRecognizersRequestRequestTypeDef",
    {
        "Filter": EntityRecognizerFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

EntityRecognizerMetadataEntityTypesListItemTypeDef = TypedDict(
    "EntityRecognizerMetadataEntityTypesListItemTypeDef",
    {
        "Type": str,
        "EvaluationMetrics": EntityTypesEvaluationMetricsTypeDef,
        "NumberOfTrainMentions": int,
    },
    total=False,
)

ListEntityRecognizerSummariesResponseTypeDef = TypedDict(
    "ListEntityRecognizerSummariesResponseTypeDef",
    {
        "EntityRecognizerSummariesList": List[EntityRecognizerSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEventsDetectionJobsRequestRequestTypeDef = TypedDict(
    "ListEventsDetectionJobsRequestRequestTypeDef",
    {
        "Filter": EventsDetectionJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListFlywheelsRequestRequestTypeDef = TypedDict(
    "ListFlywheelsRequestRequestTypeDef",
    {
        "Filter": FlywheelFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListFlywheelIterationHistoryRequestRequestTypeDef = TypedDict(
    "_RequiredListFlywheelIterationHistoryRequestRequestTypeDef",
    {
        "FlywheelArn": str,
    },
)
_OptionalListFlywheelIterationHistoryRequestRequestTypeDef = TypedDict(
    "_OptionalListFlywheelIterationHistoryRequestRequestTypeDef",
    {
        "Filter": FlywheelIterationFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListFlywheelIterationHistoryRequestRequestTypeDef(
    _RequiredListFlywheelIterationHistoryRequestRequestTypeDef,
    _OptionalListFlywheelIterationHistoryRequestRequestTypeDef,
):
    pass

FlywheelIterationPropertiesTypeDef = TypedDict(
    "FlywheelIterationPropertiesTypeDef",
    {
        "FlywheelArn": str,
        "FlywheelIterationId": str,
        "CreationTime": datetime,
        "EndTime": datetime,
        "Status": FlywheelIterationStatusType,
        "Message": str,
        "EvaluatedModelArn": str,
        "EvaluatedModelMetrics": FlywheelModelEvaluationMetricsTypeDef,
        "TrainedModelArn": str,
        "TrainedModelMetrics": FlywheelModelEvaluationMetricsTypeDef,
        "EvaluationManifestS3Prefix": str,
    },
    total=False,
)

ListFlywheelsResponseTypeDef = TypedDict(
    "ListFlywheelsResponseTypeDef",
    {
        "FlywheelSummaryList": List[FlywheelSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GeometryTypeDef = TypedDict(
    "GeometryTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Polygon": List[PointTypeDef],
    },
    total=False,
)

ListKeyPhrasesDetectionJobsRequestListKeyPhrasesDetectionJobsPaginateTypeDef = TypedDict(
    "ListKeyPhrasesDetectionJobsRequestListKeyPhrasesDetectionJobsPaginateTypeDef",
    {
        "Filter": KeyPhrasesDetectionJobFilterTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListKeyPhrasesDetectionJobsRequestRequestTypeDef = TypedDict(
    "ListKeyPhrasesDetectionJobsRequestRequestTypeDef",
    {
        "Filter": KeyPhrasesDetectionJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListPiiEntitiesDetectionJobsRequestListPiiEntitiesDetectionJobsPaginateTypeDef = TypedDict(
    "ListPiiEntitiesDetectionJobsRequestListPiiEntitiesDetectionJobsPaginateTypeDef",
    {
        "Filter": PiiEntitiesDetectionJobFilterTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListPiiEntitiesDetectionJobsRequestRequestTypeDef = TypedDict(
    "ListPiiEntitiesDetectionJobsRequestRequestTypeDef",
    {
        "Filter": PiiEntitiesDetectionJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListSentimentDetectionJobsRequestListSentimentDetectionJobsPaginateTypeDef = TypedDict(
    "ListSentimentDetectionJobsRequestListSentimentDetectionJobsPaginateTypeDef",
    {
        "Filter": SentimentDetectionJobFilterTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListSentimentDetectionJobsRequestRequestTypeDef = TypedDict(
    "ListSentimentDetectionJobsRequestRequestTypeDef",
    {
        "Filter": SentimentDetectionJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTargetedSentimentDetectionJobsRequestRequestTypeDef = TypedDict(
    "ListTargetedSentimentDetectionJobsRequestRequestTypeDef",
    {
        "Filter": TargetedSentimentDetectionJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTopicsDetectionJobsRequestListTopicsDetectionJobsPaginateTypeDef = TypedDict(
    "ListTopicsDetectionJobsRequestListTopicsDetectionJobsPaginateTypeDef",
    {
        "Filter": TopicsDetectionJobFilterTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListTopicsDetectionJobsRequestRequestTypeDef = TypedDict(
    "ListTopicsDetectionJobsRequestRequestTypeDef",
    {
        "Filter": TopicsDetectionJobFilterTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

SyntaxTokenTypeDef = TypedDict(
    "SyntaxTokenTypeDef",
    {
        "TokenId": int,
        "Text": str,
        "BeginOffset": int,
        "EndOffset": int,
        "PartOfSpeech": PartOfSpeechTagTypeDef,
    },
    total=False,
)

BatchDetectDominantLanguageResponseTypeDef = TypedDict(
    "BatchDetectDominantLanguageResponseTypeDef",
    {
        "ResultList": List[BatchDetectDominantLanguageItemResultTypeDef],
        "ErrorList": List[BatchItemErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchDetectKeyPhrasesResponseTypeDef = TypedDict(
    "BatchDetectKeyPhrasesResponseTypeDef",
    {
        "ResultList": List[BatchDetectKeyPhrasesItemResultTypeDef],
        "ErrorList": List[BatchItemErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchDetectSentimentResponseTypeDef = TypedDict(
    "BatchDetectSentimentResponseTypeDef",
    {
        "ResultList": List[BatchDetectSentimentItemResultTypeDef],
        "ErrorList": List[BatchItemErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TargetedSentimentMentionTypeDef = TypedDict(
    "TargetedSentimentMentionTypeDef",
    {
        "Score": float,
        "GroupScore": float,
        "Text": str,
        "Type": TargetedSentimentEntityTypeType,
        "MentionSentiment": MentionSentimentTypeDef,
        "BeginOffset": int,
        "EndOffset": int,
    },
    total=False,
)

EntityTypeDef = TypedDict(
    "EntityTypeDef",
    {
        "Score": float,
        "Type": EntityTypeType,
        "Text": str,
        "BeginOffset": int,
        "EndOffset": int,
        "BlockReferences": List[BlockReferenceTypeDef],
    },
    total=False,
)

DocumentClassificationJobPropertiesTypeDef = TypedDict(
    "DocumentClassificationJobPropertiesTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobName": str,
        "JobStatus": JobStatusType,
        "Message": str,
        "SubmitTime": datetime,
        "EndTime": datetime,
        "DocumentClassifierArn": str,
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
        "FlywheelArn": str,
    },
    total=False,
)

DominantLanguageDetectionJobPropertiesTypeDef = TypedDict(
    "DominantLanguageDetectionJobPropertiesTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobName": str,
        "JobStatus": JobStatusType,
        "Message": str,
        "SubmitTime": datetime,
        "EndTime": datetime,
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
    },
    total=False,
)

EntitiesDetectionJobPropertiesTypeDef = TypedDict(
    "EntitiesDetectionJobPropertiesTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobName": str,
        "JobStatus": JobStatusType,
        "Message": str,
        "SubmitTime": datetime,
        "EndTime": datetime,
        "EntityRecognizerArn": str,
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "LanguageCode": LanguageCodeType,
        "DataAccessRoleArn": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
        "FlywheelArn": str,
    },
    total=False,
)

EventsDetectionJobPropertiesTypeDef = TypedDict(
    "EventsDetectionJobPropertiesTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobName": str,
        "JobStatus": JobStatusType,
        "Message": str,
        "SubmitTime": datetime,
        "EndTime": datetime,
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "LanguageCode": LanguageCodeType,
        "DataAccessRoleArn": str,
        "TargetEventTypes": List[str],
    },
    total=False,
)

KeyPhrasesDetectionJobPropertiesTypeDef = TypedDict(
    "KeyPhrasesDetectionJobPropertiesTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobName": str,
        "JobStatus": JobStatusType,
        "Message": str,
        "SubmitTime": datetime,
        "EndTime": datetime,
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "LanguageCode": LanguageCodeType,
        "DataAccessRoleArn": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
    },
    total=False,
)

PiiEntitiesDetectionJobPropertiesTypeDef = TypedDict(
    "PiiEntitiesDetectionJobPropertiesTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobName": str,
        "JobStatus": JobStatusType,
        "Message": str,
        "SubmitTime": datetime,
        "EndTime": datetime,
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": PiiOutputDataConfigTypeDef,
        "RedactionConfig": RedactionConfigTypeDef,
        "LanguageCode": LanguageCodeType,
        "DataAccessRoleArn": str,
        "Mode": PiiEntitiesDetectionModeType,
    },
    total=False,
)

SentimentDetectionJobPropertiesTypeDef = TypedDict(
    "SentimentDetectionJobPropertiesTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobName": str,
        "JobStatus": JobStatusType,
        "Message": str,
        "SubmitTime": datetime,
        "EndTime": datetime,
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "LanguageCode": LanguageCodeType,
        "DataAccessRoleArn": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
    },
    total=False,
)

_RequiredStartDocumentClassificationJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartDocumentClassificationJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
    },
)
_OptionalStartDocumentClassificationJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartDocumentClassificationJobRequestRequestTypeDef",
    {
        "JobName": str,
        "DocumentClassifierArn": str,
        "ClientRequestToken": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
        "FlywheelArn": str,
    },
    total=False,
)

class StartDocumentClassificationJobRequestRequestTypeDef(
    _RequiredStartDocumentClassificationJobRequestRequestTypeDef,
    _OptionalStartDocumentClassificationJobRequestRequestTypeDef,
):
    pass

_RequiredStartDominantLanguageDetectionJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartDominantLanguageDetectionJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
    },
)
_OptionalStartDominantLanguageDetectionJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartDominantLanguageDetectionJobRequestRequestTypeDef",
    {
        "JobName": str,
        "ClientRequestToken": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class StartDominantLanguageDetectionJobRequestRequestTypeDef(
    _RequiredStartDominantLanguageDetectionJobRequestRequestTypeDef,
    _OptionalStartDominantLanguageDetectionJobRequestRequestTypeDef,
):
    pass

_RequiredStartEntitiesDetectionJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartEntitiesDetectionJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "LanguageCode": LanguageCodeType,
    },
)
_OptionalStartEntitiesDetectionJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartEntitiesDetectionJobRequestRequestTypeDef",
    {
        "JobName": str,
        "EntityRecognizerArn": str,
        "ClientRequestToken": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
        "FlywheelArn": str,
    },
    total=False,
)

class StartEntitiesDetectionJobRequestRequestTypeDef(
    _RequiredStartEntitiesDetectionJobRequestRequestTypeDef,
    _OptionalStartEntitiesDetectionJobRequestRequestTypeDef,
):
    pass

_RequiredStartEventsDetectionJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartEventsDetectionJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "LanguageCode": LanguageCodeType,
        "TargetEventTypes": Sequence[str],
    },
)
_OptionalStartEventsDetectionJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartEventsDetectionJobRequestRequestTypeDef",
    {
        "JobName": str,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class StartEventsDetectionJobRequestRequestTypeDef(
    _RequiredStartEventsDetectionJobRequestRequestTypeDef,
    _OptionalStartEventsDetectionJobRequestRequestTypeDef,
):
    pass

_RequiredStartKeyPhrasesDetectionJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartKeyPhrasesDetectionJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "LanguageCode": LanguageCodeType,
    },
)
_OptionalStartKeyPhrasesDetectionJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartKeyPhrasesDetectionJobRequestRequestTypeDef",
    {
        "JobName": str,
        "ClientRequestToken": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class StartKeyPhrasesDetectionJobRequestRequestTypeDef(
    _RequiredStartKeyPhrasesDetectionJobRequestRequestTypeDef,
    _OptionalStartKeyPhrasesDetectionJobRequestRequestTypeDef,
):
    pass

_RequiredStartPiiEntitiesDetectionJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartPiiEntitiesDetectionJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "Mode": PiiEntitiesDetectionModeType,
        "DataAccessRoleArn": str,
        "LanguageCode": LanguageCodeType,
    },
)
_OptionalStartPiiEntitiesDetectionJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartPiiEntitiesDetectionJobRequestRequestTypeDef",
    {
        "RedactionConfig": RedactionConfigTypeDef,
        "JobName": str,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class StartPiiEntitiesDetectionJobRequestRequestTypeDef(
    _RequiredStartPiiEntitiesDetectionJobRequestRequestTypeDef,
    _OptionalStartPiiEntitiesDetectionJobRequestRequestTypeDef,
):
    pass

_RequiredStartSentimentDetectionJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartSentimentDetectionJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "LanguageCode": LanguageCodeType,
    },
)
_OptionalStartSentimentDetectionJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartSentimentDetectionJobRequestRequestTypeDef",
    {
        "JobName": str,
        "ClientRequestToken": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class StartSentimentDetectionJobRequestRequestTypeDef(
    _RequiredStartSentimentDetectionJobRequestRequestTypeDef,
    _OptionalStartSentimentDetectionJobRequestRequestTypeDef,
):
    pass

_RequiredStartTargetedSentimentDetectionJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartTargetedSentimentDetectionJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "LanguageCode": LanguageCodeType,
    },
)
_OptionalStartTargetedSentimentDetectionJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartTargetedSentimentDetectionJobRequestRequestTypeDef",
    {
        "JobName": str,
        "ClientRequestToken": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class StartTargetedSentimentDetectionJobRequestRequestTypeDef(
    _RequiredStartTargetedSentimentDetectionJobRequestRequestTypeDef,
    _OptionalStartTargetedSentimentDetectionJobRequestRequestTypeDef,
):
    pass

_RequiredStartTopicsDetectionJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartTopicsDetectionJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
    },
)
_OptionalStartTopicsDetectionJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartTopicsDetectionJobRequestRequestTypeDef",
    {
        "JobName": str,
        "NumberOfTopics": int,
        "ClientRequestToken": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class StartTopicsDetectionJobRequestRequestTypeDef(
    _RequiredStartTopicsDetectionJobRequestRequestTypeDef,
    _OptionalStartTopicsDetectionJobRequestRequestTypeDef,
):
    pass

TargetedSentimentDetectionJobPropertiesTypeDef = TypedDict(
    "TargetedSentimentDetectionJobPropertiesTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobName": str,
        "JobStatus": JobStatusType,
        "Message": str,
        "SubmitTime": datetime,
        "EndTime": datetime,
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "LanguageCode": LanguageCodeType,
        "DataAccessRoleArn": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
    },
    total=False,
)

TopicsDetectionJobPropertiesTypeDef = TypedDict(
    "TopicsDetectionJobPropertiesTypeDef",
    {
        "JobId": str,
        "JobArn": str,
        "JobName": str,
        "JobStatus": JobStatusType,
        "Message": str,
        "SubmitTime": datetime,
        "EndTime": datetime,
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "NumberOfTopics": int,
        "DataAccessRoleArn": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
    },
    total=False,
)

_RequiredUpdateFlywheelRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFlywheelRequestRequestTypeDef",
    {
        "FlywheelArn": str,
    },
)
_OptionalUpdateFlywheelRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFlywheelRequestRequestTypeDef",
    {
        "ActiveModelArn": str,
        "DataAccessRoleArn": str,
        "DataSecurityConfig": UpdateDataSecurityConfigTypeDef,
    },
    total=False,
)

class UpdateFlywheelRequestRequestTypeDef(
    _RequiredUpdateFlywheelRequestRequestTypeDef, _OptionalUpdateFlywheelRequestRequestTypeDef
):
    pass

DatasetInputDataConfigTypeDef = TypedDict(
    "DatasetInputDataConfigTypeDef",
    {
        "AugmentedManifests": Sequence[DatasetAugmentedManifestsListItemTypeDef],
        "DataFormat": DatasetDataFormatType,
        "DocumentClassifierInputDataConfig": DatasetDocumentClassifierInputDataConfigTypeDef,
        "EntityRecognizerInputDataConfig": DatasetEntityRecognizerInputDataConfigTypeDef,
    },
    total=False,
)

_RequiredCreateDocumentClassifierRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDocumentClassifierRequestRequestTypeDef",
    {
        "DocumentClassifierName": str,
        "DataAccessRoleArn": str,
        "InputDataConfig": DocumentClassifierInputDataConfigTypeDef,
        "LanguageCode": LanguageCodeType,
    },
)
_OptionalCreateDocumentClassifierRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDocumentClassifierRequestRequestTypeDef",
    {
        "VersionName": str,
        "Tags": Sequence[TagTypeDef],
        "OutputDataConfig": DocumentClassifierOutputDataConfigTypeDef,
        "ClientRequestToken": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
        "Mode": DocumentClassifierModeType,
        "ModelKmsKeyId": str,
        "ModelPolicy": str,
    },
    total=False,
)

class CreateDocumentClassifierRequestRequestTypeDef(
    _RequiredCreateDocumentClassifierRequestRequestTypeDef,
    _OptionalCreateDocumentClassifierRequestRequestTypeDef,
):
    pass

DocumentClassifierPropertiesTypeDef = TypedDict(
    "DocumentClassifierPropertiesTypeDef",
    {
        "DocumentClassifierArn": str,
        "LanguageCode": LanguageCodeType,
        "Status": ModelStatusType,
        "Message": str,
        "SubmitTime": datetime,
        "EndTime": datetime,
        "TrainingStartTime": datetime,
        "TrainingEndTime": datetime,
        "InputDataConfig": DocumentClassifierInputDataConfigTypeDef,
        "OutputDataConfig": DocumentClassifierOutputDataConfigTypeDef,
        "ClassifierMetadata": ClassifierMetadataTypeDef,
        "DataAccessRoleArn": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
        "Mode": DocumentClassifierModeType,
        "ModelKmsKeyId": str,
        "VersionName": str,
        "SourceModelArn": str,
        "FlywheelArn": str,
    },
    total=False,
)

ClassifyDocumentResponseTypeDef = TypedDict(
    "ClassifyDocumentResponseTypeDef",
    {
        "Classes": List[DocumentClassTypeDef],
        "Labels": List[DocumentLabelTypeDef],
        "DocumentMetadata": DocumentMetadataTypeDef,
        "DocumentType": List[DocumentTypeListItemTypeDef],
        "Errors": List[ErrorsListItemTypeDef],
        "Warnings": List[WarningsListItemTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredTaskConfigTypeDef = TypedDict(
    "_RequiredTaskConfigTypeDef",
    {
        "LanguageCode": LanguageCodeType,
    },
)
_OptionalTaskConfigTypeDef = TypedDict(
    "_OptionalTaskConfigTypeDef",
    {
        "DocumentClassificationConfig": DocumentClassificationConfigTypeDef,
        "EntityRecognitionConfig": EntityRecognitionConfigTypeDef,
    },
    total=False,
)

class TaskConfigTypeDef(_RequiredTaskConfigTypeDef, _OptionalTaskConfigTypeDef):
    pass

_RequiredCreateEntityRecognizerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEntityRecognizerRequestRequestTypeDef",
    {
        "RecognizerName": str,
        "DataAccessRoleArn": str,
        "InputDataConfig": EntityRecognizerInputDataConfigTypeDef,
        "LanguageCode": LanguageCodeType,
    },
)
_OptionalCreateEntityRecognizerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEntityRecognizerRequestRequestTypeDef",
    {
        "VersionName": str,
        "Tags": Sequence[TagTypeDef],
        "ClientRequestToken": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
        "ModelKmsKeyId": str,
        "ModelPolicy": str,
    },
    total=False,
)

class CreateEntityRecognizerRequestRequestTypeDef(
    _RequiredCreateEntityRecognizerRequestRequestTypeDef,
    _OptionalCreateEntityRecognizerRequestRequestTypeDef,
):
    pass

EntityRecognizerMetadataTypeDef = TypedDict(
    "EntityRecognizerMetadataTypeDef",
    {
        "NumberOfTrainedDocuments": int,
        "NumberOfTestDocuments": int,
        "EvaluationMetrics": EntityRecognizerEvaluationMetricsTypeDef,
        "EntityTypes": List[EntityRecognizerMetadataEntityTypesListItemTypeDef],
    },
    total=False,
)

DescribeFlywheelIterationResponseTypeDef = TypedDict(
    "DescribeFlywheelIterationResponseTypeDef",
    {
        "FlywheelIterationProperties": FlywheelIterationPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFlywheelIterationHistoryResponseTypeDef = TypedDict(
    "ListFlywheelIterationHistoryResponseTypeDef",
    {
        "FlywheelIterationPropertiesList": List[FlywheelIterationPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BlockTypeDef = TypedDict(
    "BlockTypeDef",
    {
        "Id": str,
        "BlockType": BlockTypeType,
        "Text": str,
        "Page": int,
        "Geometry": GeometryTypeDef,
        "Relationships": List[RelationshipsListItemTypeDef],
    },
    total=False,
)

BatchDetectSyntaxItemResultTypeDef = TypedDict(
    "BatchDetectSyntaxItemResultTypeDef",
    {
        "Index": int,
        "SyntaxTokens": List[SyntaxTokenTypeDef],
    },
    total=False,
)

DetectSyntaxResponseTypeDef = TypedDict(
    "DetectSyntaxResponseTypeDef",
    {
        "SyntaxTokens": List[SyntaxTokenTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TargetedSentimentEntityTypeDef = TypedDict(
    "TargetedSentimentEntityTypeDef",
    {
        "DescriptiveMentionIndex": List[int],
        "Mentions": List[TargetedSentimentMentionTypeDef],
    },
    total=False,
)

BatchDetectEntitiesItemResultTypeDef = TypedDict(
    "BatchDetectEntitiesItemResultTypeDef",
    {
        "Index": int,
        "Entities": List[EntityTypeDef],
    },
    total=False,
)

DescribeDocumentClassificationJobResponseTypeDef = TypedDict(
    "DescribeDocumentClassificationJobResponseTypeDef",
    {
        "DocumentClassificationJobProperties": DocumentClassificationJobPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDocumentClassificationJobsResponseTypeDef = TypedDict(
    "ListDocumentClassificationJobsResponseTypeDef",
    {
        "DocumentClassificationJobPropertiesList": List[DocumentClassificationJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDominantLanguageDetectionJobResponseTypeDef = TypedDict(
    "DescribeDominantLanguageDetectionJobResponseTypeDef",
    {
        "DominantLanguageDetectionJobProperties": DominantLanguageDetectionJobPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDominantLanguageDetectionJobsResponseTypeDef = TypedDict(
    "ListDominantLanguageDetectionJobsResponseTypeDef",
    {
        "DominantLanguageDetectionJobPropertiesList": List[
            DominantLanguageDetectionJobPropertiesTypeDef
        ],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEntitiesDetectionJobResponseTypeDef = TypedDict(
    "DescribeEntitiesDetectionJobResponseTypeDef",
    {
        "EntitiesDetectionJobProperties": EntitiesDetectionJobPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEntitiesDetectionJobsResponseTypeDef = TypedDict(
    "ListEntitiesDetectionJobsResponseTypeDef",
    {
        "EntitiesDetectionJobPropertiesList": List[EntitiesDetectionJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEventsDetectionJobResponseTypeDef = TypedDict(
    "DescribeEventsDetectionJobResponseTypeDef",
    {
        "EventsDetectionJobProperties": EventsDetectionJobPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEventsDetectionJobsResponseTypeDef = TypedDict(
    "ListEventsDetectionJobsResponseTypeDef",
    {
        "EventsDetectionJobPropertiesList": List[EventsDetectionJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeKeyPhrasesDetectionJobResponseTypeDef = TypedDict(
    "DescribeKeyPhrasesDetectionJobResponseTypeDef",
    {
        "KeyPhrasesDetectionJobProperties": KeyPhrasesDetectionJobPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListKeyPhrasesDetectionJobsResponseTypeDef = TypedDict(
    "ListKeyPhrasesDetectionJobsResponseTypeDef",
    {
        "KeyPhrasesDetectionJobPropertiesList": List[KeyPhrasesDetectionJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribePiiEntitiesDetectionJobResponseTypeDef = TypedDict(
    "DescribePiiEntitiesDetectionJobResponseTypeDef",
    {
        "PiiEntitiesDetectionJobProperties": PiiEntitiesDetectionJobPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPiiEntitiesDetectionJobsResponseTypeDef = TypedDict(
    "ListPiiEntitiesDetectionJobsResponseTypeDef",
    {
        "PiiEntitiesDetectionJobPropertiesList": List[PiiEntitiesDetectionJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSentimentDetectionJobResponseTypeDef = TypedDict(
    "DescribeSentimentDetectionJobResponseTypeDef",
    {
        "SentimentDetectionJobProperties": SentimentDetectionJobPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSentimentDetectionJobsResponseTypeDef = TypedDict(
    "ListSentimentDetectionJobsResponseTypeDef",
    {
        "SentimentDetectionJobPropertiesList": List[SentimentDetectionJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeTargetedSentimentDetectionJobResponseTypeDef = TypedDict(
    "DescribeTargetedSentimentDetectionJobResponseTypeDef",
    {
        "TargetedSentimentDetectionJobProperties": TargetedSentimentDetectionJobPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTargetedSentimentDetectionJobsResponseTypeDef = TypedDict(
    "ListTargetedSentimentDetectionJobsResponseTypeDef",
    {
        "TargetedSentimentDetectionJobPropertiesList": List[
            TargetedSentimentDetectionJobPropertiesTypeDef
        ],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeTopicsDetectionJobResponseTypeDef = TypedDict(
    "DescribeTopicsDetectionJobResponseTypeDef",
    {
        "TopicsDetectionJobProperties": TopicsDetectionJobPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTopicsDetectionJobsResponseTypeDef = TypedDict(
    "ListTopicsDetectionJobsResponseTypeDef",
    {
        "TopicsDetectionJobPropertiesList": List[TopicsDetectionJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateDatasetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetRequestRequestTypeDef",
    {
        "FlywheelArn": str,
        "DatasetName": str,
        "InputDataConfig": DatasetInputDataConfigTypeDef,
    },
)
_OptionalCreateDatasetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetRequestRequestTypeDef",
    {
        "DatasetType": DatasetTypeType,
        "Description": str,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateDatasetRequestRequestTypeDef(
    _RequiredCreateDatasetRequestRequestTypeDef, _OptionalCreateDatasetRequestRequestTypeDef
):
    pass

DescribeDocumentClassifierResponseTypeDef = TypedDict(
    "DescribeDocumentClassifierResponseTypeDef",
    {
        "DocumentClassifierProperties": DocumentClassifierPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDocumentClassifiersResponseTypeDef = TypedDict(
    "ListDocumentClassifiersResponseTypeDef",
    {
        "DocumentClassifierPropertiesList": List[DocumentClassifierPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateFlywheelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFlywheelRequestRequestTypeDef",
    {
        "FlywheelName": str,
        "DataAccessRoleArn": str,
        "DataLakeS3Uri": str,
    },
)
_OptionalCreateFlywheelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFlywheelRequestRequestTypeDef",
    {
        "ActiveModelArn": str,
        "TaskConfig": TaskConfigTypeDef,
        "ModelType": ModelTypeType,
        "DataSecurityConfig": DataSecurityConfigTypeDef,
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateFlywheelRequestRequestTypeDef(
    _RequiredCreateFlywheelRequestRequestTypeDef, _OptionalCreateFlywheelRequestRequestTypeDef
):
    pass

FlywheelPropertiesTypeDef = TypedDict(
    "FlywheelPropertiesTypeDef",
    {
        "FlywheelArn": str,
        "ActiveModelArn": str,
        "DataAccessRoleArn": str,
        "TaskConfig": TaskConfigTypeDef,
        "DataLakeS3Uri": str,
        "DataSecurityConfig": DataSecurityConfigTypeDef,
        "Status": FlywheelStatusType,
        "ModelType": ModelTypeType,
        "Message": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LatestFlywheelIteration": str,
    },
    total=False,
)

EntityRecognizerPropertiesTypeDef = TypedDict(
    "EntityRecognizerPropertiesTypeDef",
    {
        "EntityRecognizerArn": str,
        "LanguageCode": LanguageCodeType,
        "Status": ModelStatusType,
        "Message": str,
        "SubmitTime": datetime,
        "EndTime": datetime,
        "TrainingStartTime": datetime,
        "TrainingEndTime": datetime,
        "InputDataConfig": EntityRecognizerInputDataConfigTypeDef,
        "RecognizerMetadata": EntityRecognizerMetadataTypeDef,
        "DataAccessRoleArn": str,
        "VolumeKmsKeyId": str,
        "VpcConfig": VpcConfigTypeDef,
        "ModelKmsKeyId": str,
        "VersionName": str,
        "SourceModelArn": str,
        "FlywheelArn": str,
        "OutputDataConfig": EntityRecognizerOutputDataConfigTypeDef,
    },
    total=False,
)

DetectEntitiesResponseTypeDef = TypedDict(
    "DetectEntitiesResponseTypeDef",
    {
        "Entities": List[EntityTypeDef],
        "DocumentMetadata": DocumentMetadataTypeDef,
        "DocumentType": List[DocumentTypeListItemTypeDef],
        "Blocks": List[BlockTypeDef],
        "Errors": List[ErrorsListItemTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchDetectSyntaxResponseTypeDef = TypedDict(
    "BatchDetectSyntaxResponseTypeDef",
    {
        "ResultList": List[BatchDetectSyntaxItemResultTypeDef],
        "ErrorList": List[BatchItemErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchDetectTargetedSentimentItemResultTypeDef = TypedDict(
    "BatchDetectTargetedSentimentItemResultTypeDef",
    {
        "Index": int,
        "Entities": List[TargetedSentimentEntityTypeDef],
    },
    total=False,
)

DetectTargetedSentimentResponseTypeDef = TypedDict(
    "DetectTargetedSentimentResponseTypeDef",
    {
        "Entities": List[TargetedSentimentEntityTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchDetectEntitiesResponseTypeDef = TypedDict(
    "BatchDetectEntitiesResponseTypeDef",
    {
        "ResultList": List[BatchDetectEntitiesItemResultTypeDef],
        "ErrorList": List[BatchItemErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFlywheelResponseTypeDef = TypedDict(
    "DescribeFlywheelResponseTypeDef",
    {
        "FlywheelProperties": FlywheelPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateFlywheelResponseTypeDef = TypedDict(
    "UpdateFlywheelResponseTypeDef",
    {
        "FlywheelProperties": FlywheelPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEntityRecognizerResponseTypeDef = TypedDict(
    "DescribeEntityRecognizerResponseTypeDef",
    {
        "EntityRecognizerProperties": EntityRecognizerPropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEntityRecognizersResponseTypeDef = TypedDict(
    "ListEntityRecognizersResponseTypeDef",
    {
        "EntityRecognizerPropertiesList": List[EntityRecognizerPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchDetectTargetedSentimentResponseTypeDef = TypedDict(
    "BatchDetectTargetedSentimentResponseTypeDef",
    {
        "ResultList": List[BatchDetectTargetedSentimentItemResultTypeDef],
        "ErrorList": List[BatchItemErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
