"""
Type annotations for codedeploy service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/literals/)

Usage::

    ```python
    from mypy_boto3_codedeploy.literals import ApplicationRevisionSortByType

    data: ApplicationRevisionSortByType = "firstUsedTime"
    ```
"""
import sys

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ApplicationRevisionSortByType",
    "AutoRollbackEventType",
    "BundleTypeType",
    "ComputePlatformType",
    "DeploymentCreatorType",
    "DeploymentOptionType",
    "DeploymentReadyActionType",
    "DeploymentStatusType",
    "DeploymentSuccessfulWaiterName",
    "DeploymentTargetTypeType",
    "DeploymentTypeType",
    "DeploymentWaitTypeType",
    "EC2TagFilterTypeType",
    "ErrorCodeType",
    "FileExistsBehaviorType",
    "GreenFleetProvisioningActionType",
    "InstanceActionType",
    "InstanceStatusType",
    "InstanceTypeType",
    "LifecycleErrorCodeType",
    "LifecycleEventStatusType",
    "ListApplicationRevisionsPaginatorName",
    "ListApplicationsPaginatorName",
    "ListDeploymentConfigsPaginatorName",
    "ListDeploymentGroupsPaginatorName",
    "ListDeploymentInstancesPaginatorName",
    "ListDeploymentTargetsPaginatorName",
    "ListDeploymentsPaginatorName",
    "ListGitHubAccountTokenNamesPaginatorName",
    "ListOnPremisesInstancesPaginatorName",
    "ListStateFilterActionType",
    "MinimumHealthyHostsTypeType",
    "OutdatedInstancesStrategyType",
    "RegistrationStatusType",
    "RevisionLocationTypeType",
    "SortOrderType",
    "StopStatusType",
    "TagFilterTypeType",
    "TargetFilterNameType",
    "TargetLabelType",
    "TargetStatusType",
    "TrafficRoutingTypeType",
    "TriggerEventTypeType",
    "CodeDeployServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "WaiterName",
    "RegionName",
)


ApplicationRevisionSortByType = Literal["firstUsedTime", "lastUsedTime", "registerTime"]
AutoRollbackEventType = Literal[
    "DEPLOYMENT_FAILURE", "DEPLOYMENT_STOP_ON_ALARM", "DEPLOYMENT_STOP_ON_REQUEST"
]
BundleTypeType = Literal["JSON", "YAML", "tar", "tgz", "zip"]
ComputePlatformType = Literal["ECS", "Lambda", "Server"]
DeploymentCreatorType = Literal[
    "CloudFormation",
    "CloudFormationRollback",
    "CodeDeploy",
    "CodeDeployAutoUpdate",
    "autoscaling",
    "codeDeployRollback",
    "user",
]
DeploymentOptionType = Literal["WITHOUT_TRAFFIC_CONTROL", "WITH_TRAFFIC_CONTROL"]
DeploymentReadyActionType = Literal["CONTINUE_DEPLOYMENT", "STOP_DEPLOYMENT"]
DeploymentStatusType = Literal[
    "Baking", "Created", "Failed", "InProgress", "Queued", "Ready", "Stopped", "Succeeded"
]
DeploymentSuccessfulWaiterName = Literal["deployment_successful"]
DeploymentTargetTypeType = Literal[
    "CloudFormationTarget", "ECSTarget", "InstanceTarget", "LambdaTarget"
]
DeploymentTypeType = Literal["BLUE_GREEN", "IN_PLACE"]
DeploymentWaitTypeType = Literal["READY_WAIT", "TERMINATION_WAIT"]
EC2TagFilterTypeType = Literal["KEY_AND_VALUE", "KEY_ONLY", "VALUE_ONLY"]
ErrorCodeType = Literal[
    "AGENT_ISSUE",
    "ALARM_ACTIVE",
    "APPLICATION_MISSING",
    "AUTOSCALING_VALIDATION_ERROR",
    "AUTO_SCALING_CONFIGURATION",
    "AUTO_SCALING_IAM_ROLE_PERMISSIONS",
    "CLOUDFORMATION_STACK_FAILURE",
    "CODEDEPLOY_RESOURCE_CANNOT_BE_FOUND",
    "CUSTOMER_APPLICATION_UNHEALTHY",
    "DEPLOYMENT_GROUP_MISSING",
    "ECS_UPDATE_ERROR",
    "ELASTIC_LOAD_BALANCING_INVALID",
    "ELB_INVALID_INSTANCE",
    "HEALTH_CONSTRAINTS",
    "HEALTH_CONSTRAINTS_INVALID",
    "HOOK_EXECUTION_FAILURE",
    "IAM_ROLE_MISSING",
    "IAM_ROLE_PERMISSIONS",
    "INTERNAL_ERROR",
    "INVALID_ECS_SERVICE",
    "INVALID_LAMBDA_CONFIGURATION",
    "INVALID_LAMBDA_FUNCTION",
    "INVALID_REVISION",
    "MANUAL_STOP",
    "MISSING_BLUE_GREEN_DEPLOYMENT_CONFIGURATION",
    "MISSING_ELB_INFORMATION",
    "MISSING_GITHUB_TOKEN",
    "NO_EC2_SUBSCRIPTION",
    "NO_INSTANCES",
    "OVER_MAX_INSTANCES",
    "RESOURCE_LIMIT_EXCEEDED",
    "REVISION_MISSING",
    "THROTTLED",
    "TIMEOUT",
]
FileExistsBehaviorType = Literal["DISALLOW", "OVERWRITE", "RETAIN"]
GreenFleetProvisioningActionType = Literal["COPY_AUTO_SCALING_GROUP", "DISCOVER_EXISTING"]
InstanceActionType = Literal["KEEP_ALIVE", "TERMINATE"]
InstanceStatusType = Literal[
    "Failed", "InProgress", "Pending", "Ready", "Skipped", "Succeeded", "Unknown"
]
InstanceTypeType = Literal["Blue", "Green"]
LifecycleErrorCodeType = Literal[
    "ScriptFailed",
    "ScriptMissing",
    "ScriptNotExecutable",
    "ScriptTimedOut",
    "Success",
    "UnknownError",
]
LifecycleEventStatusType = Literal[
    "Failed", "InProgress", "Pending", "Skipped", "Succeeded", "Unknown"
]
ListApplicationRevisionsPaginatorName = Literal["list_application_revisions"]
ListApplicationsPaginatorName = Literal["list_applications"]
ListDeploymentConfigsPaginatorName = Literal["list_deployment_configs"]
ListDeploymentGroupsPaginatorName = Literal["list_deployment_groups"]
ListDeploymentInstancesPaginatorName = Literal["list_deployment_instances"]
ListDeploymentTargetsPaginatorName = Literal["list_deployment_targets"]
ListDeploymentsPaginatorName = Literal["list_deployments"]
ListGitHubAccountTokenNamesPaginatorName = Literal["list_git_hub_account_token_names"]
ListOnPremisesInstancesPaginatorName = Literal["list_on_premises_instances"]
ListStateFilterActionType = Literal["exclude", "ignore", "include"]
MinimumHealthyHostsTypeType = Literal["FLEET_PERCENT", "HOST_COUNT"]
OutdatedInstancesStrategyType = Literal["IGNORE", "UPDATE"]
RegistrationStatusType = Literal["Deregistered", "Registered"]
RevisionLocationTypeType = Literal["AppSpecContent", "GitHub", "S3", "String"]
SortOrderType = Literal["ascending", "descending"]
StopStatusType = Literal["Pending", "Succeeded"]
TagFilterTypeType = Literal["KEY_AND_VALUE", "KEY_ONLY", "VALUE_ONLY"]
TargetFilterNameType = Literal["ServerInstanceLabel", "TargetStatus"]
TargetLabelType = Literal["Blue", "Green"]
TargetStatusType = Literal[
    "Failed", "InProgress", "Pending", "Ready", "Skipped", "Succeeded", "Unknown"
]
TrafficRoutingTypeType = Literal["AllAtOnce", "TimeBasedCanary", "TimeBasedLinear"]
TriggerEventTypeType = Literal[
    "DeploymentFailure",
    "DeploymentReady",
    "DeploymentRollback",
    "DeploymentStart",
    "DeploymentStop",
    "DeploymentSuccess",
    "InstanceFailure",
    "InstanceReady",
    "InstanceStart",
    "InstanceSuccess",
]
CodeDeployServiceName = Literal["codedeploy"]
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
    "list_application_revisions",
    "list_applications",
    "list_deployment_configs",
    "list_deployment_groups",
    "list_deployment_instances",
    "list_deployment_targets",
    "list_deployments",
    "list_git_hub_account_token_names",
    "list_on_premises_instances",
]
WaiterName = Literal["deployment_successful"]
RegionName = Literal[
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-south-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ap-southeast-4",
    "ca-central-1",
    "eu-central-1",
    "eu-central-2",
    "eu-north-1",
    "eu-south-1",
    "eu-south-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "me-central-1",
    "me-south-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]
