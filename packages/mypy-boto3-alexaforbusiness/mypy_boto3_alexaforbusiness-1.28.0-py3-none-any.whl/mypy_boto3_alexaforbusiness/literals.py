"""
Type annotations for alexaforbusiness service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/literals/)

Usage::

    ```python
    from mypy_boto3_alexaforbusiness.literals import BusinessReportFailureCodeType

    data: BusinessReportFailureCodeType = "ACCESS_DENIED"
    ```
"""
import sys

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "BusinessReportFailureCodeType",
    "BusinessReportFormatType",
    "BusinessReportIntervalType",
    "BusinessReportStatusType",
    "CommsProtocolType",
    "ConferenceProviderTypeType",
    "ConnectionStatusType",
    "DeviceEventTypeType",
    "DeviceStatusDetailCodeType",
    "DeviceStatusType",
    "DeviceUsageTypeType",
    "DistanceUnitType",
    "EnablementTypeFilterType",
    "EnablementTypeType",
    "EndOfMeetingReminderTypeType",
    "EnrollmentStatusType",
    "FeatureType",
    "ListBusinessReportSchedulesPaginatorName",
    "ListConferenceProvidersPaginatorName",
    "ListDeviceEventsPaginatorName",
    "ListSkillsPaginatorName",
    "ListSkillsStoreCategoriesPaginatorName",
    "ListSkillsStoreSkillsByCategoryPaginatorName",
    "ListSmartHomeAppliancesPaginatorName",
    "ListTagsPaginatorName",
    "LocaleType",
    "NetworkEapMethodType",
    "NetworkSecurityTypeType",
    "PhoneNumberTypeType",
    "RequirePinType",
    "SearchDevicesPaginatorName",
    "SearchProfilesPaginatorName",
    "SearchRoomsPaginatorName",
    "SearchSkillGroupsPaginatorName",
    "SearchUsersPaginatorName",
    "SipTypeType",
    "SkillTypeFilterType",
    "SkillTypeType",
    "SortValueType",
    "TemperatureUnitType",
    "WakeWordType",
    "AlexaForBusinessServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "RegionName",
)


BusinessReportFailureCodeType = Literal["ACCESS_DENIED", "INTERNAL_FAILURE", "NO_SUCH_BUCKET"]
BusinessReportFormatType = Literal["CSV", "CSV_ZIP"]
BusinessReportIntervalType = Literal["ONE_DAY", "ONE_WEEK", "THIRTY_DAYS"]
BusinessReportStatusType = Literal["FAILED", "RUNNING", "SUCCEEDED"]
CommsProtocolType = Literal["H323", "SIP", "SIPS"]
ConferenceProviderTypeType = Literal[
    "BLUEJEANS",
    "CHIME",
    "CUSTOM",
    "FUZE",
    "GOOGLE_HANGOUTS",
    "POLYCOM",
    "RINGCENTRAL",
    "SKYPE_FOR_BUSINESS",
    "WEBEX",
    "ZOOM",
]
ConnectionStatusType = Literal["OFFLINE", "ONLINE"]
DeviceEventTypeType = Literal["CONNECTION_STATUS", "DEVICE_STATUS"]
DeviceStatusDetailCodeType = Literal[
    "ASSOCIATION_REJECTION",
    "AUTHENTICATION_FAILURE",
    "CERTIFICATE_AUTHORITY_ACCESS_DENIED",
    "CERTIFICATE_ISSUING_LIMIT_EXCEEDED",
    "CREDENTIALS_ACCESS_FAILURE",
    "DEVICE_SOFTWARE_UPDATE_NEEDED",
    "DEVICE_WAS_OFFLINE",
    "DHCP_FAILURE",
    "DNS_FAILURE",
    "INTERNET_UNAVAILABLE",
    "INVALID_CERTIFICATE_AUTHORITY",
    "INVALID_PASSWORD_STATE",
    "NETWORK_PROFILE_NOT_FOUND",
    "PASSWORD_MANAGER_ACCESS_DENIED",
    "PASSWORD_NOT_FOUND",
    "TLS_VERSION_MISMATCH",
    "UNKNOWN_FAILURE",
]
DeviceStatusType = Literal["DEREGISTERED", "FAILED", "PENDING", "READY", "WAS_OFFLINE"]
DeviceUsageTypeType = Literal["VOICE"]
DistanceUnitType = Literal["IMPERIAL", "METRIC"]
EnablementTypeFilterType = Literal["ENABLED", "PENDING"]
EnablementTypeType = Literal["ENABLED", "PENDING"]
EndOfMeetingReminderTypeType = Literal[
    "ANNOUNCEMENT_TIME_CHECK", "ANNOUNCEMENT_VARIABLE_TIME_LEFT", "CHIME", "KNOCK"
]
EnrollmentStatusType = Literal[
    "DEREGISTERING", "DISASSOCIATING", "INITIALIZED", "PENDING", "REGISTERED"
]
FeatureType = Literal[
    "ALL", "BLUETOOTH", "LISTS", "NETWORK_PROFILE", "NOTIFICATIONS", "SETTINGS", "SKILLS", "VOLUME"
]
ListBusinessReportSchedulesPaginatorName = Literal["list_business_report_schedules"]
ListConferenceProvidersPaginatorName = Literal["list_conference_providers"]
ListDeviceEventsPaginatorName = Literal["list_device_events"]
ListSkillsPaginatorName = Literal["list_skills"]
ListSkillsStoreCategoriesPaginatorName = Literal["list_skills_store_categories"]
ListSkillsStoreSkillsByCategoryPaginatorName = Literal["list_skills_store_skills_by_category"]
ListSmartHomeAppliancesPaginatorName = Literal["list_smart_home_appliances"]
ListTagsPaginatorName = Literal["list_tags"]
LocaleType = Literal["en-US"]
NetworkEapMethodType = Literal["EAP_TLS"]
NetworkSecurityTypeType = Literal["OPEN", "WEP", "WPA2_ENTERPRISE", "WPA2_PSK", "WPA_PSK"]
PhoneNumberTypeType = Literal["HOME", "MOBILE", "WORK"]
RequirePinType = Literal["NO", "OPTIONAL", "YES"]
SearchDevicesPaginatorName = Literal["search_devices"]
SearchProfilesPaginatorName = Literal["search_profiles"]
SearchRoomsPaginatorName = Literal["search_rooms"]
SearchSkillGroupsPaginatorName = Literal["search_skill_groups"]
SearchUsersPaginatorName = Literal["search_users"]
SipTypeType = Literal["WORK"]
SkillTypeFilterType = Literal["ALL", "PRIVATE", "PUBLIC"]
SkillTypeType = Literal["PRIVATE", "PUBLIC"]
SortValueType = Literal["ASC", "DESC"]
TemperatureUnitType = Literal["CELSIUS", "FAHRENHEIT"]
WakeWordType = Literal["ALEXA", "AMAZON", "COMPUTER", "ECHO"]
AlexaForBusinessServiceName = Literal["alexaforbusiness"]
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
    "list_business_report_schedules",
    "list_conference_providers",
    "list_device_events",
    "list_skills",
    "list_skills_store_categories",
    "list_skills_store_skills_by_category",
    "list_smart_home_appliances",
    "list_tags",
    "search_devices",
    "search_profiles",
    "search_rooms",
    "search_skill_groups",
    "search_users",
]
RegionName = Literal["us-east-1"]
