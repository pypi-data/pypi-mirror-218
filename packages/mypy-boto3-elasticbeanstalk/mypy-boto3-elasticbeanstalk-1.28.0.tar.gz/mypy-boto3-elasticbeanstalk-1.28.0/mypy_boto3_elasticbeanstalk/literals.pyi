"""
Type annotations for elasticbeanstalk service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/literals/)

Usage::

    ```python
    from mypy_boto3_elasticbeanstalk.literals import ActionHistoryStatusType

    data: ActionHistoryStatusType = "Completed"
    ```
"""
import sys

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ActionHistoryStatusType",
    "ActionStatusType",
    "ActionTypeType",
    "ApplicationVersionStatusType",
    "ComputeTypeType",
    "ConfigurationDeploymentStatusType",
    "ConfigurationOptionValueTypeType",
    "DescribeApplicationVersionsPaginatorName",
    "DescribeEnvironmentManagedActionHistoryPaginatorName",
    "DescribeEnvironmentsPaginatorName",
    "DescribeEventsPaginatorName",
    "EnvironmentExistsWaiterName",
    "EnvironmentHealthAttributeType",
    "EnvironmentHealthStatusType",
    "EnvironmentHealthType",
    "EnvironmentInfoTypeType",
    "EnvironmentStatusType",
    "EnvironmentTerminatedWaiterName",
    "EnvironmentUpdatedWaiterName",
    "EventSeverityType",
    "FailureTypeType",
    "InstancesHealthAttributeType",
    "ListPlatformVersionsPaginatorName",
    "PlatformStatusType",
    "SourceRepositoryType",
    "SourceTypeType",
    "ValidationSeverityType",
    "ElasticBeanstalkServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "WaiterName",
    "RegionName",
)

ActionHistoryStatusType = Literal["Completed", "Failed", "Unknown"]
ActionStatusType = Literal["Pending", "Running", "Scheduled", "Unknown"]
ActionTypeType = Literal["InstanceRefresh", "PlatformUpdate", "Unknown"]
ApplicationVersionStatusType = Literal[
    "Building", "Failed", "Processed", "Processing", "Unprocessed"
]
ComputeTypeType = Literal["BUILD_GENERAL1_LARGE", "BUILD_GENERAL1_MEDIUM", "BUILD_GENERAL1_SMALL"]
ConfigurationDeploymentStatusType = Literal["deployed", "failed", "pending"]
ConfigurationOptionValueTypeType = Literal["List", "Scalar"]
DescribeApplicationVersionsPaginatorName = Literal["describe_application_versions"]
DescribeEnvironmentManagedActionHistoryPaginatorName = Literal[
    "describe_environment_managed_action_history"
]
DescribeEnvironmentsPaginatorName = Literal["describe_environments"]
DescribeEventsPaginatorName = Literal["describe_events"]
EnvironmentExistsWaiterName = Literal["environment_exists"]
EnvironmentHealthAttributeType = Literal[
    "All",
    "ApplicationMetrics",
    "Causes",
    "Color",
    "HealthStatus",
    "InstancesHealth",
    "RefreshedAt",
    "Status",
]
EnvironmentHealthStatusType = Literal[
    "Degraded", "Info", "NoData", "Ok", "Pending", "Severe", "Suspended", "Unknown", "Warning"
]
EnvironmentHealthType = Literal["Green", "Grey", "Red", "Yellow"]
EnvironmentInfoTypeType = Literal["bundle", "tail"]
EnvironmentStatusType = Literal[
    "Aborting",
    "Launching",
    "LinkingFrom",
    "LinkingTo",
    "Ready",
    "Terminated",
    "Terminating",
    "Updating",
]
EnvironmentTerminatedWaiterName = Literal["environment_terminated"]
EnvironmentUpdatedWaiterName = Literal["environment_updated"]
EventSeverityType = Literal["DEBUG", "ERROR", "FATAL", "INFO", "TRACE", "WARN"]
FailureTypeType = Literal[
    "CancellationFailed",
    "InternalFailure",
    "InvalidEnvironmentState",
    "PermissionsError",
    "RollbackFailed",
    "RollbackSuccessful",
    "UpdateCancelled",
]
InstancesHealthAttributeType = Literal[
    "All",
    "ApplicationMetrics",
    "AvailabilityZone",
    "Causes",
    "Color",
    "Deployment",
    "HealthStatus",
    "InstanceType",
    "LaunchedAt",
    "RefreshedAt",
    "System",
]
ListPlatformVersionsPaginatorName = Literal["list_platform_versions"]
PlatformStatusType = Literal["Creating", "Deleted", "Deleting", "Failed", "Ready"]
SourceRepositoryType = Literal["CodeCommit", "S3"]
SourceTypeType = Literal["Git", "Zip"]
ValidationSeverityType = Literal["error", "warning"]
ElasticBeanstalkServiceName = Literal["elasticbeanstalk"]
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
    "describe_application_versions",
    "describe_environment_managed_action_history",
    "describe_environments",
    "describe_events",
    "list_platform_versions",
]
WaiterName = Literal["environment_exists", "environment_terminated", "environment_updated"]
RegionName = Literal[
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ca-central-1",
    "eu-central-1",
    "eu-north-1",
    "eu-south-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "me-south-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]
