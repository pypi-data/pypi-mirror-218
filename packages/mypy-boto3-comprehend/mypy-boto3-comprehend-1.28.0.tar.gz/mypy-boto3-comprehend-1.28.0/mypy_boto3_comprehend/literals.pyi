"""
Type annotations for comprehend service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/literals/)

Usage::

    ```python
    from mypy_boto3_comprehend.literals import AugmentedManifestsDocumentTypeFormatType

    data: AugmentedManifestsDocumentTypeFormatType = "PLAIN_TEXT_DOCUMENT"
    ```
"""
import sys

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "AugmentedManifestsDocumentTypeFormatType",
    "BlockTypeType",
    "DatasetDataFormatType",
    "DatasetStatusType",
    "DatasetTypeType",
    "DocumentClassifierDataFormatType",
    "DocumentClassifierDocumentTypeFormatType",
    "DocumentClassifierModeType",
    "DocumentReadActionType",
    "DocumentReadFeatureTypesType",
    "DocumentReadModeType",
    "DocumentTypeType",
    "EndpointStatusType",
    "EntityRecognizerDataFormatType",
    "EntityTypeType",
    "FlywheelIterationStatusType",
    "FlywheelStatusType",
    "InputFormatType",
    "JobStatusType",
    "LanguageCodeType",
    "ListDocumentClassificationJobsPaginatorName",
    "ListDocumentClassifiersPaginatorName",
    "ListDominantLanguageDetectionJobsPaginatorName",
    "ListEndpointsPaginatorName",
    "ListEntitiesDetectionJobsPaginatorName",
    "ListEntityRecognizersPaginatorName",
    "ListKeyPhrasesDetectionJobsPaginatorName",
    "ListPiiEntitiesDetectionJobsPaginatorName",
    "ListSentimentDetectionJobsPaginatorName",
    "ListTopicsDetectionJobsPaginatorName",
    "ModelStatusType",
    "ModelTypeType",
    "PageBasedErrorCodeType",
    "PageBasedWarningCodeType",
    "PartOfSpeechTagTypeType",
    "PiiEntitiesDetectionMaskModeType",
    "PiiEntitiesDetectionModeType",
    "PiiEntityTypeType",
    "RelationshipTypeType",
    "SentimentTypeType",
    "SplitType",
    "SyntaxLanguageCodeType",
    "TargetedSentimentEntityTypeType",
    "ComprehendServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "RegionName",
)

AugmentedManifestsDocumentTypeFormatType = Literal[
    "PLAIN_TEXT_DOCUMENT", "SEMI_STRUCTURED_DOCUMENT"
]
BlockTypeType = Literal["LINE", "WORD"]
DatasetDataFormatType = Literal["AUGMENTED_MANIFEST", "COMPREHEND_CSV"]
DatasetStatusType = Literal["COMPLETED", "CREATING", "FAILED"]
DatasetTypeType = Literal["TEST", "TRAIN"]
DocumentClassifierDataFormatType = Literal["AUGMENTED_MANIFEST", "COMPREHEND_CSV"]
DocumentClassifierDocumentTypeFormatType = Literal[
    "PLAIN_TEXT_DOCUMENT", "SEMI_STRUCTURED_DOCUMENT"
]
DocumentClassifierModeType = Literal["MULTI_CLASS", "MULTI_LABEL"]
DocumentReadActionType = Literal["TEXTRACT_ANALYZE_DOCUMENT", "TEXTRACT_DETECT_DOCUMENT_TEXT"]
DocumentReadFeatureTypesType = Literal["FORMS", "TABLES"]
DocumentReadModeType = Literal["FORCE_DOCUMENT_READ_ACTION", "SERVICE_DEFAULT"]
DocumentTypeType = Literal[
    "IMAGE",
    "MS_WORD",
    "NATIVE_PDF",
    "PLAIN_TEXT",
    "SCANNED_PDF",
    "TEXTRACT_ANALYZE_DOCUMENT_JSON",
    "TEXTRACT_DETECT_DOCUMENT_TEXT_JSON",
]
EndpointStatusType = Literal["CREATING", "DELETING", "FAILED", "IN_SERVICE", "UPDATING"]
EntityRecognizerDataFormatType = Literal["AUGMENTED_MANIFEST", "COMPREHEND_CSV"]
EntityTypeType = Literal[
    "COMMERCIAL_ITEM",
    "DATE",
    "EVENT",
    "LOCATION",
    "ORGANIZATION",
    "OTHER",
    "PERSON",
    "QUANTITY",
    "TITLE",
]
FlywheelIterationStatusType = Literal[
    "COMPLETED", "EVALUATING", "FAILED", "STOPPED", "STOP_REQUESTED", "TRAINING"
]
FlywheelStatusType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED", "UPDATING"]
InputFormatType = Literal["ONE_DOC_PER_FILE", "ONE_DOC_PER_LINE"]
JobStatusType = Literal[
    "COMPLETED", "FAILED", "IN_PROGRESS", "STOPPED", "STOP_REQUESTED", "SUBMITTED"
]
LanguageCodeType = Literal[
    "ar", "de", "en", "es", "fr", "hi", "it", "ja", "ko", "pt", "zh", "zh-TW"
]
ListDocumentClassificationJobsPaginatorName = Literal["list_document_classification_jobs"]
ListDocumentClassifiersPaginatorName = Literal["list_document_classifiers"]
ListDominantLanguageDetectionJobsPaginatorName = Literal["list_dominant_language_detection_jobs"]
ListEndpointsPaginatorName = Literal["list_endpoints"]
ListEntitiesDetectionJobsPaginatorName = Literal["list_entities_detection_jobs"]
ListEntityRecognizersPaginatorName = Literal["list_entity_recognizers"]
ListKeyPhrasesDetectionJobsPaginatorName = Literal["list_key_phrases_detection_jobs"]
ListPiiEntitiesDetectionJobsPaginatorName = Literal["list_pii_entities_detection_jobs"]
ListSentimentDetectionJobsPaginatorName = Literal["list_sentiment_detection_jobs"]
ListTopicsDetectionJobsPaginatorName = Literal["list_topics_detection_jobs"]
ModelStatusType = Literal[
    "DELETING",
    "IN_ERROR",
    "STOPPED",
    "STOP_REQUESTED",
    "SUBMITTED",
    "TRAINED",
    "TRAINED_WITH_WARNING",
    "TRAINING",
]
ModelTypeType = Literal["DOCUMENT_CLASSIFIER", "ENTITY_RECOGNIZER"]
PageBasedErrorCodeType = Literal[
    "INTERNAL_SERVER_ERROR",
    "PAGE_CHARACTERS_EXCEEDED",
    "PAGE_SIZE_EXCEEDED",
    "TEXTRACT_BAD_PAGE",
    "TEXTRACT_PROVISIONED_THROUGHPUT_EXCEEDED",
]
PageBasedWarningCodeType = Literal[
    "INFERENCING_NATIVE_DOCUMENT_WITH_PLAINTEXT_TRAINED_MODEL",
    "INFERENCING_PLAINTEXT_WITH_NATIVE_TRAINED_MODEL",
]
PartOfSpeechTagTypeType = Literal[
    "ADJ",
    "ADP",
    "ADV",
    "AUX",
    "CCONJ",
    "CONJ",
    "DET",
    "INTJ",
    "NOUN",
    "NUM",
    "O",
    "PART",
    "PRON",
    "PROPN",
    "PUNCT",
    "SCONJ",
    "SYM",
    "VERB",
]
PiiEntitiesDetectionMaskModeType = Literal["MASK", "REPLACE_WITH_PII_ENTITY_TYPE"]
PiiEntitiesDetectionModeType = Literal["ONLY_OFFSETS", "ONLY_REDACTION"]
PiiEntityTypeType = Literal[
    "ADDRESS",
    "AGE",
    "ALL",
    "AWS_ACCESS_KEY",
    "AWS_SECRET_KEY",
    "BANK_ACCOUNT_NUMBER",
    "BANK_ROUTING",
    "CA_HEALTH_NUMBER",
    "CA_SOCIAL_INSURANCE_NUMBER",
    "CREDIT_DEBIT_CVV",
    "CREDIT_DEBIT_EXPIRY",
    "CREDIT_DEBIT_NUMBER",
    "DATE_TIME",
    "DRIVER_ID",
    "EMAIL",
    "INTERNATIONAL_BANK_ACCOUNT_NUMBER",
    "IN_AADHAAR",
    "IN_NREGA",
    "IN_PERMANENT_ACCOUNT_NUMBER",
    "IN_VOTER_NUMBER",
    "IP_ADDRESS",
    "LICENSE_PLATE",
    "MAC_ADDRESS",
    "NAME",
    "PASSPORT_NUMBER",
    "PASSWORD",
    "PHONE",
    "PIN",
    "SSN",
    "SWIFT_CODE",
    "UK_NATIONAL_HEALTH_SERVICE_NUMBER",
    "UK_NATIONAL_INSURANCE_NUMBER",
    "UK_UNIQUE_TAXPAYER_REFERENCE_NUMBER",
    "URL",
    "USERNAME",
    "US_INDIVIDUAL_TAX_IDENTIFICATION_NUMBER",
    "VEHICLE_IDENTIFICATION_NUMBER",
]
RelationshipTypeType = Literal["CHILD"]
SentimentTypeType = Literal["MIXED", "NEGATIVE", "NEUTRAL", "POSITIVE"]
SplitType = Literal["TEST", "TRAIN"]
SyntaxLanguageCodeType = Literal["de", "en", "es", "fr", "it", "pt"]
TargetedSentimentEntityTypeType = Literal[
    "ATTRIBUTE",
    "BOOK",
    "BRAND",
    "COMMERCIAL_ITEM",
    "DATE",
    "EVENT",
    "FACILITY",
    "GAME",
    "LOCATION",
    "MOVIE",
    "MUSIC",
    "ORGANIZATION",
    "OTHER",
    "PERSON",
    "PERSONAL_TITLE",
    "QUANTITY",
    "SOFTWARE",
]
ComprehendServiceName = Literal["comprehend"]
ServiceName = Literal[
    "accessanalyzer",
    "account",
    "acm",
    "acm-pca",
    "alexaforbusiness",
    "amp",
    "amplify",
    "amplifybackend",
    "amplifyuibuilder",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appconfigdata",
    "appfabric",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "arc-zonal-shift",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "backup",
    "backup-gateway",
    "backupstorage",
    "batch",
    "billingconductor",
    "braket",
    "budgets",
    "ce",
    "chime",
    "chime-sdk-identity",
    "chime-sdk-media-pipelines",
    "chime-sdk-meetings",
    "chime-sdk-messaging",
    "chime-sdk-voice",
    "cleanrooms",
    "cloud9",
    "cloudcontrol",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudtrail-data",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecatalyst",
    "codecommit",
    "codedeploy",
    "codeguru-reviewer",
    "codeguru-security",
    "codeguruprofiler",
    "codepipeline",
    "codestar",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "config",
    "connect",
    "connect-contact-lens",
    "connectcampaigns",
    "connectcases",
    "connectparticipant",
    "controltower",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "dax",
    "detective",
    "devicefarm",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "docdb-elastic",
    "drs",
    "ds",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elastictranscoder",
    "elb",
    "elbv2",
    "emr",
    "emr-containers",
    "emr-serverless",
    "es",
    "events",
    "evidently",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "fsx",
    "gamelift",
    "gamesparks",
    "glacier",
    "globalaccelerator",
    "glue",
    "grafana",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "honeycode",
    "iam",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "inspector2",
    "internetmonitor",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot-roborunner",
    "iot1click-devices",
    "iot1click-projects",
    "iotanalytics",
    "iotdeviceadvisor",
    "iotevents",
    "iotevents-data",
    "iotfleethub",
    "iotfleetwise",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iottwinmaker",
    "iotwireless",
    "ivs",
    "ivs-realtime",
    "ivschat",
    "kafka",
    "kafkaconnect",
    "kendra",
    "kendra-ranking",
    "keyspaces",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesis-video-webrtc-storage",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "license-manager-linux-subscriptions",
    "license-manager-user-subscriptions",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "lookoutmetrics",
    "lookoutvision",
    "m2",
    "machinelearning",
    "macie",
    "macie2",
    "managedblockchain",
    "marketplace-catalog",
    "marketplace-entitlement",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediapackagev2",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "memorydb",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migration-hub-refactor-spaces",
    "migrationhub-config",
    "migrationhuborchestrator",
    "migrationhubstrategy",
    "mobile",
    "mq",
    "mturk",
    "mwaa",
    "neptune",
    "network-firewall",
    "networkmanager",
    "nimble",
    "oam",
    "omics",
    "opensearch",
    "opensearchserverless",
    "opsworks",
    "opsworkscm",
    "organizations",
    "osis",
    "outposts",
    "panorama",
    "payment-cryptography",
    "payment-cryptography-data",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "pinpoint-sms-voice-v2",
    "pipes",
    "polly",
    "pricing",
    "privatenetworks",
    "proton",
    "qldb",
    "qldb-session",
    "quicksight",
    "ram",
    "rbin",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "redshift-serverless",
    "rekognition",
    "resiliencehub",
    "resource-explorer-2",
    "resource-groups",
    "resourcegroupstaggingapi",
    "robomaker",
    "rolesanywhere",
    "route53",
    "route53-recovery-cluster",
    "route53-recovery-control-config",
    "route53-recovery-readiness",
    "route53domains",
    "route53resolver",
    "rum",
    "s3",
    "s3control",
    "s3outposts",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-geospatial",
    "sagemaker-metrics",
    "sagemaker-runtime",
    "savingsplans",
    "scheduler",
    "schemas",
    "sdb",
    "secretsmanager",
    "securityhub",
    "securitylake",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "simspaceweaver",
    "sms",
    "sms-voice",
    "snow-device-management",
    "snowball",
    "sns",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-incidents",
    "ssm-sap",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "support",
    "support-app",
    "swf",
    "synthetics",
    "textract",
    "timestream-query",
    "timestream-write",
    "tnb",
    "transcribe",
    "transfer",
    "translate",
    "verifiedpermissions",
    "voice-id",
    "vpc-lattice",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "wisdom",
    "workdocs",
    "worklink",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "workspaces-web",
    "xray",
]
ResourceServiceName = Literal[
    "cloudformation",
    "cloudwatch",
    "dynamodb",
    "ec2",
    "glacier",
    "iam",
    "opsworks",
    "s3",
    "sns",
    "sqs",
]
PaginatorName = Literal[
    "list_document_classification_jobs",
    "list_document_classifiers",
    "list_dominant_language_detection_jobs",
    "list_endpoints",
    "list_entities_detection_jobs",
    "list_entity_recognizers",
    "list_key_phrases_detection_jobs",
    "list_pii_entities_detection_jobs",
    "list_sentiment_detection_jobs",
    "list_topics_detection_jobs",
]
RegionName = Literal[
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-south-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ca-central-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "us-east-1",
    "us-east-2",
    "us-west-2",
]
