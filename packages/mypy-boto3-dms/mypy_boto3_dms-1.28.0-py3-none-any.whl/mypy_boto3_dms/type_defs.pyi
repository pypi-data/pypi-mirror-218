"""
Type annotations for dms service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/type_defs/)

Usage::

    ```python
    from mypy_boto3_dms.type_defs import AccountQuotaTypeDef

    data: AccountQuotaTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AuthMechanismValueType,
    AuthTypeValueType,
    CannedAclForObjectsValueType,
    CharLengthSemanticsType,
    CollectorStatusType,
    CompressionTypeValueType,
    DataFormatValueType,
    DatePartitionDelimiterValueType,
    DatePartitionSequenceValueType,
    DmsSslModeValueType,
    EncodingTypeValueType,
    EncryptionModeValueType,
    EndpointSettingTypeValueType,
    KafkaSaslMechanismType,
    KafkaSecurityProtocolType,
    MessageFormatValueType,
    MigrationTypeValueType,
    NestingLevelValueType,
    ParquetVersionValueType,
    PluginNameValueType,
    RedisAuthTypeValueType,
    RefreshSchemasStatusTypeValueType,
    ReleaseStatusValuesType,
    ReloadOptionValueType,
    ReplicationEndpointTypeValueType,
    SafeguardPolicyType,
    SslSecurityProtocolValueType,
    StartReplicationTaskTypeValueType,
    TargetDbTypeType,
    TlogAccessModeType,
    VersionStatusType,
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
    "AccountQuotaTypeDef",
    "TagTypeDef",
    "ApplyPendingMaintenanceActionMessageRequestTypeDef",
    "AvailabilityZoneTypeDef",
    "BatchStartRecommendationsErrorEntryTypeDef",
    "CancelReplicationTaskAssessmentRunMessageRequestTypeDef",
    "CertificateTypeDef",
    "CollectorHealthCheckTypeDef",
    "InventoryDataTypeDef",
    "CollectorShortInfoResponseTypeDef",
    "ConnectionTypeDef",
    "DmsTransferSettingsTypeDef",
    "DocDbSettingsTypeDef",
    "DynamoDbSettingsTypeDef",
    "ElasticsearchSettingsTypeDef",
    "GcpMySQLSettingsTypeDef",
    "IBMDb2SettingsTypeDef",
    "KafkaSettingsTypeDef",
    "KinesisSettingsTypeDef",
    "MicrosoftSQLServerSettingsTypeDef",
    "MongoDbSettingsTypeDef",
    "MySQLSettingsTypeDef",
    "NeptuneSettingsTypeDef",
    "OracleSettingsTypeDef",
    "PostgreSQLSettingsTypeDef",
    "RedisSettingsTypeDef",
    "RedshiftSettingsTypeDef",
    "S3SettingsTypeDef",
    "SybaseSettingsTypeDef",
    "EventSubscriptionTypeDef",
    "CreateFleetAdvisorCollectorRequestRequestTypeDef",
    "CreateFleetAdvisorCollectorResponseTypeDef",
    "DatabaseInstanceSoftwareDetailsResponseTypeDef",
    "ServerShortInfoResponseTypeDef",
    "DatabaseShortInfoResponseTypeDef",
    "DeleteCertificateMessageRequestTypeDef",
    "DeleteCollectorRequestRequestTypeDef",
    "DeleteConnectionMessageRequestTypeDef",
    "DeleteEndpointMessageRequestTypeDef",
    "DeleteEventSubscriptionMessageRequestTypeDef",
    "DeleteFleetAdvisorDatabasesRequestRequestTypeDef",
    "DeleteFleetAdvisorDatabasesResponseTypeDef",
    "DeleteReplicationInstanceMessageRequestTypeDef",
    "DeleteReplicationSubnetGroupMessageRequestTypeDef",
    "DeleteReplicationTaskAssessmentRunMessageRequestTypeDef",
    "DeleteReplicationTaskMessageRequestTypeDef",
    "DescribeApplicableIndividualAssessmentsMessageRequestTypeDef",
    "DescribeApplicableIndividualAssessmentsResponseTypeDef",
    "FilterTypeDef",
    "WaiterConfigTypeDef",
    "DescribeEndpointSettingsMessageRequestTypeDef",
    "EndpointSettingTypeDef",
    "SupportedEndpointTypeTypeDef",
    "EventCategoryGroupTypeDef",
    "EventTypeDef",
    "DescribeFleetAdvisorLsaAnalysisRequestRequestTypeDef",
    "FleetAdvisorLsaAnalysisResponseTypeDef",
    "FleetAdvisorSchemaObjectResponseTypeDef",
    "DescribeOrderableReplicationInstancesMessageDescribeOrderableReplicationInstancesPaginateTypeDef",
    "DescribeOrderableReplicationInstancesMessageRequestTypeDef",
    "OrderableReplicationInstanceTypeDef",
    "LimitationTypeDef",
    "DescribeRefreshSchemasStatusMessageRequestTypeDef",
    "RefreshSchemasStatusTypeDef",
    "DescribeReplicationInstanceTaskLogsMessageRequestTypeDef",
    "ReplicationInstanceTaskLogTypeDef",
    "DescribeReplicationTaskAssessmentResultsMessageDescribeReplicationTaskAssessmentResultsPaginateTypeDef",
    "DescribeReplicationTaskAssessmentResultsMessageRequestTypeDef",
    "ReplicationTaskAssessmentResultTypeDef",
    "ReplicationTaskIndividualAssessmentTypeDef",
    "DescribeSchemasMessageDescribeSchemasPaginateTypeDef",
    "DescribeSchemasMessageRequestTypeDef",
    "DescribeSchemasResponseTypeDef",
    "TableStatisticsTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListTagsForResourceMessageRequestTypeDef",
    "ModifyEventSubscriptionMessageRequestTypeDef",
    "ModifyReplicationInstanceMessageRequestTypeDef",
    "ModifyReplicationSubnetGroupMessageRequestTypeDef",
    "ModifyReplicationTaskMessageRequestTypeDef",
    "MoveReplicationTaskMessageRequestTypeDef",
    "PaginatorConfigTypeDef",
    "PendingMaintenanceActionTypeDef",
    "RdsConfigurationTypeDef",
    "RdsRequirementsTypeDef",
    "RebootReplicationInstanceMessageRequestTypeDef",
    "RecommendationSettingsTypeDef",
    "RefreshSchemasMessageRequestTypeDef",
    "TableToReloadTypeDef",
    "ReloadTablesResponseTypeDef",
    "RemoveTagsFromResourceMessageRequestTypeDef",
    "ReplicationPendingModifiedValuesTypeDef",
    "VpcSecurityGroupMembershipTypeDef",
    "ReplicationTaskAssessmentRunProgressTypeDef",
    "ReplicationTaskStatsTypeDef",
    "ResponseMetadataTypeDef",
    "RunFleetAdvisorLsaAnalysisResponseTypeDef",
    "SchemaShortInfoResponseTypeDef",
    "StartReplicationTaskAssessmentMessageRequestTypeDef",
    "StartReplicationTaskAssessmentRunMessageRequestTypeDef",
    "StartReplicationTaskMessageRequestTypeDef",
    "StopReplicationTaskMessageRequestTypeDef",
    "TestConnectionMessageRequestTypeDef",
    "UpdateSubscriptionsToEventBridgeMessageRequestTypeDef",
    "UpdateSubscriptionsToEventBridgeResponseTypeDef",
    "DescribeAccountAttributesResponseTypeDef",
    "AddTagsToResourceMessageRequestTypeDef",
    "CreateEventSubscriptionMessageRequestTypeDef",
    "CreateReplicationInstanceMessageRequestTypeDef",
    "CreateReplicationSubnetGroupMessageRequestTypeDef",
    "CreateReplicationTaskMessageRequestTypeDef",
    "ImportCertificateMessageRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "SubnetTypeDef",
    "BatchStartRecommendationsResponseTypeDef",
    "DeleteCertificateResponseTypeDef",
    "DescribeCertificatesResponseTypeDef",
    "ImportCertificateResponseTypeDef",
    "CollectorResponseTypeDef",
    "DeleteConnectionResponseTypeDef",
    "DescribeConnectionsResponseTypeDef",
    "TestConnectionResponseTypeDef",
    "CreateEndpointMessageRequestTypeDef",
    "EndpointTypeDef",
    "ModifyEndpointMessageRequestTypeDef",
    "CreateEventSubscriptionResponseTypeDef",
    "DeleteEventSubscriptionResponseTypeDef",
    "DescribeEventSubscriptionsResponseTypeDef",
    "ModifyEventSubscriptionResponseTypeDef",
    "DatabaseResponseTypeDef",
    "DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef",
    "DescribeCertificatesMessageRequestTypeDef",
    "DescribeConnectionsMessageDescribeConnectionsPaginateTypeDef",
    "DescribeConnectionsMessageRequestTypeDef",
    "DescribeEndpointTypesMessageDescribeEndpointTypesPaginateTypeDef",
    "DescribeEndpointTypesMessageRequestTypeDef",
    "DescribeEndpointsMessageDescribeEndpointsPaginateTypeDef",
    "DescribeEndpointsMessageRequestTypeDef",
    "DescribeEventCategoriesMessageRequestTypeDef",
    "DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef",
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    "DescribeEventsMessageDescribeEventsPaginateTypeDef",
    "DescribeEventsMessageRequestTypeDef",
    "DescribeFleetAdvisorCollectorsRequestRequestTypeDef",
    "DescribeFleetAdvisorDatabasesRequestRequestTypeDef",
    "DescribeFleetAdvisorSchemaObjectSummaryRequestRequestTypeDef",
    "DescribeFleetAdvisorSchemasRequestRequestTypeDef",
    "DescribePendingMaintenanceActionsMessageRequestTypeDef",
    "DescribeRecommendationLimitationsRequestRequestTypeDef",
    "DescribeRecommendationsRequestRequestTypeDef",
    "DescribeReplicationInstancesMessageDescribeReplicationInstancesPaginateTypeDef",
    "DescribeReplicationInstancesMessageRequestTypeDef",
    "DescribeReplicationSubnetGroupsMessageDescribeReplicationSubnetGroupsPaginateTypeDef",
    "DescribeReplicationSubnetGroupsMessageRequestTypeDef",
    "DescribeReplicationTaskAssessmentRunsMessageRequestTypeDef",
    "DescribeReplicationTaskIndividualAssessmentsMessageRequestTypeDef",
    "DescribeReplicationTasksMessageDescribeReplicationTasksPaginateTypeDef",
    "DescribeReplicationTasksMessageRequestTypeDef",
    "DescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef",
    "DescribeTableStatisticsMessageRequestTypeDef",
    "DescribeConnectionsMessageTestConnectionSucceedsWaitTypeDef",
    "DescribeEndpointsMessageEndpointDeletedWaitTypeDef",
    "DescribeReplicationInstancesMessageReplicationInstanceAvailableWaitTypeDef",
    "DescribeReplicationInstancesMessageReplicationInstanceDeletedWaitTypeDef",
    "DescribeReplicationTasksMessageReplicationTaskDeletedWaitTypeDef",
    "DescribeReplicationTasksMessageReplicationTaskReadyWaitTypeDef",
    "DescribeReplicationTasksMessageReplicationTaskRunningWaitTypeDef",
    "DescribeReplicationTasksMessageReplicationTaskStoppedWaitTypeDef",
    "DescribeEndpointSettingsResponseTypeDef",
    "DescribeEndpointTypesResponseTypeDef",
    "DescribeEventCategoriesResponseTypeDef",
    "DescribeEventsResponseTypeDef",
    "DescribeFleetAdvisorLsaAnalysisResponseTypeDef",
    "DescribeFleetAdvisorSchemaObjectSummaryResponseTypeDef",
    "DescribeOrderableReplicationInstancesResponseTypeDef",
    "DescribeRecommendationLimitationsResponseTypeDef",
    "DescribeRefreshSchemasStatusResponseTypeDef",
    "RefreshSchemasResponseTypeDef",
    "DescribeReplicationInstanceTaskLogsResponseTypeDef",
    "DescribeReplicationTaskAssessmentResultsResponseTypeDef",
    "DescribeReplicationTaskIndividualAssessmentsResponseTypeDef",
    "DescribeTableStatisticsResponseTypeDef",
    "ResourcePendingMaintenanceActionsTypeDef",
    "RdsRecommendationTypeDef",
    "StartRecommendationsRequestEntryTypeDef",
    "StartRecommendationsRequestRequestTypeDef",
    "ReloadTablesMessageRequestTypeDef",
    "ReplicationTaskAssessmentRunTypeDef",
    "ReplicationTaskTypeDef",
    "SchemaResponseTypeDef",
    "ReplicationSubnetGroupTypeDef",
    "DescribeFleetAdvisorCollectorsResponseTypeDef",
    "CreateEndpointResponseTypeDef",
    "DeleteEndpointResponseTypeDef",
    "DescribeEndpointsResponseTypeDef",
    "ModifyEndpointResponseTypeDef",
    "DescribeFleetAdvisorDatabasesResponseTypeDef",
    "ApplyPendingMaintenanceActionResponseTypeDef",
    "DescribePendingMaintenanceActionsResponseTypeDef",
    "RecommendationDataTypeDef",
    "BatchStartRecommendationsRequestRequestTypeDef",
    "CancelReplicationTaskAssessmentRunResponseTypeDef",
    "DeleteReplicationTaskAssessmentRunResponseTypeDef",
    "DescribeReplicationTaskAssessmentRunsResponseTypeDef",
    "StartReplicationTaskAssessmentRunResponseTypeDef",
    "CreateReplicationTaskResponseTypeDef",
    "DeleteReplicationTaskResponseTypeDef",
    "DescribeReplicationTasksResponseTypeDef",
    "ModifyReplicationTaskResponseTypeDef",
    "MoveReplicationTaskResponseTypeDef",
    "StartReplicationTaskAssessmentResponseTypeDef",
    "StartReplicationTaskResponseTypeDef",
    "StopReplicationTaskResponseTypeDef",
    "DescribeFleetAdvisorSchemasResponseTypeDef",
    "CreateReplicationSubnetGroupResponseTypeDef",
    "DescribeReplicationSubnetGroupsResponseTypeDef",
    "ModifyReplicationSubnetGroupResponseTypeDef",
    "ReplicationInstanceTypeDef",
    "RecommendationTypeDef",
    "CreateReplicationInstanceResponseTypeDef",
    "DeleteReplicationInstanceResponseTypeDef",
    "DescribeReplicationInstancesResponseTypeDef",
    "ModifyReplicationInstanceResponseTypeDef",
    "RebootReplicationInstanceResponseTypeDef",
    "DescribeRecommendationsResponseTypeDef",
)

AccountQuotaTypeDef = TypedDict(
    "AccountQuotaTypeDef",
    {
        "AccountQuotaName": str,
        "Used": int,
        "Max": int,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
        "ResourceArn": str,
    },
    total=False,
)

ApplyPendingMaintenanceActionMessageRequestTypeDef = TypedDict(
    "ApplyPendingMaintenanceActionMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
        "ApplyAction": str,
        "OptInType": str,
    },
)

AvailabilityZoneTypeDef = TypedDict(
    "AvailabilityZoneTypeDef",
    {
        "Name": str,
    },
    total=False,
)

BatchStartRecommendationsErrorEntryTypeDef = TypedDict(
    "BatchStartRecommendationsErrorEntryTypeDef",
    {
        "DatabaseId": str,
        "Message": str,
        "Code": str,
    },
    total=False,
)

CancelReplicationTaskAssessmentRunMessageRequestTypeDef = TypedDict(
    "CancelReplicationTaskAssessmentRunMessageRequestTypeDef",
    {
        "ReplicationTaskAssessmentRunArn": str,
    },
)

CertificateTypeDef = TypedDict(
    "CertificateTypeDef",
    {
        "CertificateIdentifier": str,
        "CertificateCreationDate": datetime,
        "CertificatePem": str,
        "CertificateWallet": bytes,
        "CertificateArn": str,
        "CertificateOwner": str,
        "ValidFromDate": datetime,
        "ValidToDate": datetime,
        "SigningAlgorithm": str,
        "KeyLength": int,
    },
    total=False,
)

CollectorHealthCheckTypeDef = TypedDict(
    "CollectorHealthCheckTypeDef",
    {
        "CollectorStatus": CollectorStatusType,
        "LocalCollectorS3Access": bool,
        "WebCollectorS3Access": bool,
        "WebCollectorGrantedRoleBasedAccess": bool,
    },
    total=False,
)

InventoryDataTypeDef = TypedDict(
    "InventoryDataTypeDef",
    {
        "NumberOfDatabases": int,
        "NumberOfSchemas": int,
    },
    total=False,
)

CollectorShortInfoResponseTypeDef = TypedDict(
    "CollectorShortInfoResponseTypeDef",
    {
        "CollectorReferencedId": str,
        "CollectorName": str,
    },
    total=False,
)

ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "ReplicationInstanceArn": str,
        "EndpointArn": str,
        "Status": str,
        "LastFailureMessage": str,
        "EndpointIdentifier": str,
        "ReplicationInstanceIdentifier": str,
    },
    total=False,
)

DmsTransferSettingsTypeDef = TypedDict(
    "DmsTransferSettingsTypeDef",
    {
        "ServiceAccessRoleArn": str,
        "BucketName": str,
    },
    total=False,
)

DocDbSettingsTypeDef = TypedDict(
    "DocDbSettingsTypeDef",
    {
        "Username": str,
        "Password": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "NestingLevel": NestingLevelValueType,
        "ExtractDocId": bool,
        "DocsToInvestigate": int,
        "KmsKeyId": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
    total=False,
)

DynamoDbSettingsTypeDef = TypedDict(
    "DynamoDbSettingsTypeDef",
    {
        "ServiceAccessRoleArn": str,
    },
)

_RequiredElasticsearchSettingsTypeDef = TypedDict(
    "_RequiredElasticsearchSettingsTypeDef",
    {
        "ServiceAccessRoleArn": str,
        "EndpointUri": str,
    },
)
_OptionalElasticsearchSettingsTypeDef = TypedDict(
    "_OptionalElasticsearchSettingsTypeDef",
    {
        "FullLoadErrorPercentage": int,
        "ErrorRetryDuration": int,
        "UseNewMappingType": bool,
    },
    total=False,
)

class ElasticsearchSettingsTypeDef(
    _RequiredElasticsearchSettingsTypeDef, _OptionalElasticsearchSettingsTypeDef
):
    pass

GcpMySQLSettingsTypeDef = TypedDict(
    "GcpMySQLSettingsTypeDef",
    {
        "AfterConnectScript": str,
        "CleanSourceMetadataOnMismatch": bool,
        "DatabaseName": str,
        "EventsPollInterval": int,
        "TargetDbType": TargetDbTypeType,
        "MaxFileSize": int,
        "ParallelLoadThreads": int,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "ServerTimezone": str,
        "Username": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
    total=False,
)

IBMDb2SettingsTypeDef = TypedDict(
    "IBMDb2SettingsTypeDef",
    {
        "DatabaseName": str,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "SetDataCaptureChanges": bool,
        "CurrentLsn": str,
        "MaxKBytesPerRead": int,
        "Username": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
    total=False,
)

KafkaSettingsTypeDef = TypedDict(
    "KafkaSettingsTypeDef",
    {
        "Broker": str,
        "Topic": str,
        "MessageFormat": MessageFormatValueType,
        "IncludeTransactionDetails": bool,
        "IncludePartitionValue": bool,
        "PartitionIncludeSchemaTable": bool,
        "IncludeTableAlterOperations": bool,
        "IncludeControlDetails": bool,
        "MessageMaxBytes": int,
        "IncludeNullAndEmpty": bool,
        "SecurityProtocol": KafkaSecurityProtocolType,
        "SslClientCertificateArn": str,
        "SslClientKeyArn": str,
        "SslClientKeyPassword": str,
        "SslCaCertificateArn": str,
        "SaslUsername": str,
        "SaslPassword": str,
        "NoHexPrefix": bool,
        "SaslMechanism": KafkaSaslMechanismType,
    },
    total=False,
)

KinesisSettingsTypeDef = TypedDict(
    "KinesisSettingsTypeDef",
    {
        "StreamArn": str,
        "MessageFormat": MessageFormatValueType,
        "ServiceAccessRoleArn": str,
        "IncludeTransactionDetails": bool,
        "IncludePartitionValue": bool,
        "PartitionIncludeSchemaTable": bool,
        "IncludeTableAlterOperations": bool,
        "IncludeControlDetails": bool,
        "IncludeNullAndEmpty": bool,
        "NoHexPrefix": bool,
    },
    total=False,
)

MicrosoftSQLServerSettingsTypeDef = TypedDict(
    "MicrosoftSQLServerSettingsTypeDef",
    {
        "Port": int,
        "BcpPacketSize": int,
        "DatabaseName": str,
        "ControlTablesFileGroup": str,
        "Password": str,
        "QuerySingleAlwaysOnNode": bool,
        "ReadBackupOnly": bool,
        "SafeguardPolicy": SafeguardPolicyType,
        "ServerName": str,
        "Username": str,
        "UseBcpFullLoad": bool,
        "UseThirdPartyBackupDevice": bool,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "TrimSpaceInChar": bool,
        "TlogAccessMode": TlogAccessModeType,
        "ForceLobLookup": bool,
    },
    total=False,
)

MongoDbSettingsTypeDef = TypedDict(
    "MongoDbSettingsTypeDef",
    {
        "Username": str,
        "Password": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "AuthType": AuthTypeValueType,
        "AuthMechanism": AuthMechanismValueType,
        "NestingLevel": NestingLevelValueType,
        "ExtractDocId": str,
        "DocsToInvestigate": str,
        "AuthSource": str,
        "KmsKeyId": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
    total=False,
)

MySQLSettingsTypeDef = TypedDict(
    "MySQLSettingsTypeDef",
    {
        "AfterConnectScript": str,
        "CleanSourceMetadataOnMismatch": bool,
        "DatabaseName": str,
        "EventsPollInterval": int,
        "TargetDbType": TargetDbTypeType,
        "MaxFileSize": int,
        "ParallelLoadThreads": int,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "ServerTimezone": str,
        "Username": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
    total=False,
)

_RequiredNeptuneSettingsTypeDef = TypedDict(
    "_RequiredNeptuneSettingsTypeDef",
    {
        "S3BucketName": str,
        "S3BucketFolder": str,
    },
)
_OptionalNeptuneSettingsTypeDef = TypedDict(
    "_OptionalNeptuneSettingsTypeDef",
    {
        "ServiceAccessRoleArn": str,
        "ErrorRetryDuration": int,
        "MaxFileSize": int,
        "MaxRetryCount": int,
        "IamAuthEnabled": bool,
    },
    total=False,
)

class NeptuneSettingsTypeDef(_RequiredNeptuneSettingsTypeDef, _OptionalNeptuneSettingsTypeDef):
    pass

OracleSettingsTypeDef = TypedDict(
    "OracleSettingsTypeDef",
    {
        "AddSupplementalLogging": bool,
        "ArchivedLogDestId": int,
        "AdditionalArchivedLogDestId": int,
        "ExtraArchivedLogDestIds": Sequence[int],
        "AllowSelectNestedTables": bool,
        "ParallelAsmReadThreads": int,
        "ReadAheadBlocks": int,
        "AccessAlternateDirectly": bool,
        "UseAlternateFolderForOnline": bool,
        "OraclePathPrefix": str,
        "UsePathPrefix": str,
        "ReplacePathPrefix": bool,
        "EnableHomogenousTablespace": bool,
        "DirectPathNoLog": bool,
        "ArchivedLogsOnly": bool,
        "AsmPassword": str,
        "AsmServer": str,
        "AsmUser": str,
        "CharLengthSemantics": CharLengthSemanticsType,
        "DatabaseName": str,
        "DirectPathParallelLoad": bool,
        "FailTasksOnLobTruncation": bool,
        "NumberDatatypeScale": int,
        "Password": str,
        "Port": int,
        "ReadTableSpaceName": bool,
        "RetryInterval": int,
        "SecurityDbEncryption": str,
        "SecurityDbEncryptionName": str,
        "ServerName": str,
        "SpatialDataOptionToGeoJsonFunctionName": str,
        "StandbyDelayTime": int,
        "Username": str,
        "UseBFile": bool,
        "UseDirectPathFullLoad": bool,
        "UseLogminerReader": bool,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "SecretsManagerOracleAsmAccessRoleArn": str,
        "SecretsManagerOracleAsmSecretId": str,
        "TrimSpaceInChar": bool,
        "ConvertTimestampWithZoneToUTC": bool,
    },
    total=False,
)

PostgreSQLSettingsTypeDef = TypedDict(
    "PostgreSQLSettingsTypeDef",
    {
        "AfterConnectScript": str,
        "CaptureDdls": bool,
        "MaxFileSize": int,
        "DatabaseName": str,
        "DdlArtifactsSchema": str,
        "ExecuteTimeout": int,
        "FailTasksOnLobTruncation": bool,
        "HeartbeatEnable": bool,
        "HeartbeatSchema": str,
        "HeartbeatFrequency": int,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "Username": str,
        "SlotName": str,
        "PluginName": PluginNameValueType,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "TrimSpaceInChar": bool,
        "MapBooleanAsBoolean": bool,
    },
    total=False,
)

_RequiredRedisSettingsTypeDef = TypedDict(
    "_RequiredRedisSettingsTypeDef",
    {
        "ServerName": str,
        "Port": int,
    },
)
_OptionalRedisSettingsTypeDef = TypedDict(
    "_OptionalRedisSettingsTypeDef",
    {
        "SslSecurityProtocol": SslSecurityProtocolValueType,
        "AuthType": RedisAuthTypeValueType,
        "AuthUserName": str,
        "AuthPassword": str,
        "SslCaCertificateArn": str,
    },
    total=False,
)

class RedisSettingsTypeDef(_RequiredRedisSettingsTypeDef, _OptionalRedisSettingsTypeDef):
    pass

RedshiftSettingsTypeDef = TypedDict(
    "RedshiftSettingsTypeDef",
    {
        "AcceptAnyDate": bool,
        "AfterConnectScript": str,
        "BucketFolder": str,
        "BucketName": str,
        "CaseSensitiveNames": bool,
        "CompUpdate": bool,
        "ConnectionTimeout": int,
        "DatabaseName": str,
        "DateFormat": str,
        "EmptyAsNull": bool,
        "EncryptionMode": EncryptionModeValueType,
        "ExplicitIds": bool,
        "FileTransferUploadStreams": int,
        "LoadTimeout": int,
        "MaxFileSize": int,
        "Password": str,
        "Port": int,
        "RemoveQuotes": bool,
        "ReplaceInvalidChars": str,
        "ReplaceChars": str,
        "ServerName": str,
        "ServiceAccessRoleArn": str,
        "ServerSideEncryptionKmsKeyId": str,
        "TimeFormat": str,
        "TrimBlanks": bool,
        "TruncateColumns": bool,
        "Username": str,
        "WriteBufferSize": int,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
        "MapBooleanAsBoolean": bool,
    },
    total=False,
)

S3SettingsTypeDef = TypedDict(
    "S3SettingsTypeDef",
    {
        "ServiceAccessRoleArn": str,
        "ExternalTableDefinition": str,
        "CsvRowDelimiter": str,
        "CsvDelimiter": str,
        "BucketFolder": str,
        "BucketName": str,
        "CompressionType": CompressionTypeValueType,
        "EncryptionMode": EncryptionModeValueType,
        "ServerSideEncryptionKmsKeyId": str,
        "DataFormat": DataFormatValueType,
        "EncodingType": EncodingTypeValueType,
        "DictPageSizeLimit": int,
        "RowGroupLength": int,
        "DataPageSize": int,
        "ParquetVersion": ParquetVersionValueType,
        "EnableStatistics": bool,
        "IncludeOpForFullLoad": bool,
        "CdcInsertsOnly": bool,
        "TimestampColumnName": str,
        "ParquetTimestampInMillisecond": bool,
        "CdcInsertsAndUpdates": bool,
        "DatePartitionEnabled": bool,
        "DatePartitionSequence": DatePartitionSequenceValueType,
        "DatePartitionDelimiter": DatePartitionDelimiterValueType,
        "UseCsvNoSupValue": bool,
        "CsvNoSupValue": str,
        "PreserveTransactions": bool,
        "CdcPath": str,
        "UseTaskStartTimeForFullLoadTimestamp": bool,
        "CannedAclForObjects": CannedAclForObjectsValueType,
        "AddColumnName": bool,
        "CdcMaxBatchInterval": int,
        "CdcMinFileSize": int,
        "CsvNullValue": str,
        "IgnoreHeaderRows": int,
        "MaxFileSize": int,
        "Rfc4180": bool,
        "DatePartitionTimezone": str,
        "AddTrailingPaddingCharacter": bool,
        "ExpectedBucketOwner": str,
        "GlueCatalogGeneration": bool,
    },
    total=False,
)

SybaseSettingsTypeDef = TypedDict(
    "SybaseSettingsTypeDef",
    {
        "DatabaseName": str,
        "Password": str,
        "Port": int,
        "ServerName": str,
        "Username": str,
        "SecretsManagerAccessRoleArn": str,
        "SecretsManagerSecretId": str,
    },
    total=False,
)

EventSubscriptionTypeDef = TypedDict(
    "EventSubscriptionTypeDef",
    {
        "CustomerAwsId": str,
        "CustSubscriptionId": str,
        "SnsTopicArn": str,
        "Status": str,
        "SubscriptionCreationTime": str,
        "SourceType": str,
        "SourceIdsList": List[str],
        "EventCategoriesList": List[str],
        "Enabled": bool,
    },
    total=False,
)

_RequiredCreateFleetAdvisorCollectorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFleetAdvisorCollectorRequestRequestTypeDef",
    {
        "CollectorName": str,
        "ServiceAccessRoleArn": str,
        "S3BucketName": str,
    },
)
_OptionalCreateFleetAdvisorCollectorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFleetAdvisorCollectorRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)

class CreateFleetAdvisorCollectorRequestRequestTypeDef(
    _RequiredCreateFleetAdvisorCollectorRequestRequestTypeDef,
    _OptionalCreateFleetAdvisorCollectorRequestRequestTypeDef,
):
    pass

CreateFleetAdvisorCollectorResponseTypeDef = TypedDict(
    "CreateFleetAdvisorCollectorResponseTypeDef",
    {
        "CollectorReferencedId": str,
        "CollectorName": str,
        "Description": str,
        "ServiceAccessRoleArn": str,
        "S3BucketName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DatabaseInstanceSoftwareDetailsResponseTypeDef = TypedDict(
    "DatabaseInstanceSoftwareDetailsResponseTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "EngineEdition": str,
        "ServicePack": str,
        "SupportLevel": str,
        "OsArchitecture": int,
        "Tooltip": str,
    },
    total=False,
)

ServerShortInfoResponseTypeDef = TypedDict(
    "ServerShortInfoResponseTypeDef",
    {
        "ServerId": str,
        "IpAddress": str,
        "ServerName": str,
    },
    total=False,
)

DatabaseShortInfoResponseTypeDef = TypedDict(
    "DatabaseShortInfoResponseTypeDef",
    {
        "DatabaseId": str,
        "DatabaseName": str,
        "DatabaseIpAddress": str,
        "DatabaseEngine": str,
    },
    total=False,
)

DeleteCertificateMessageRequestTypeDef = TypedDict(
    "DeleteCertificateMessageRequestTypeDef",
    {
        "CertificateArn": str,
    },
)

DeleteCollectorRequestRequestTypeDef = TypedDict(
    "DeleteCollectorRequestRequestTypeDef",
    {
        "CollectorReferencedId": str,
    },
)

DeleteConnectionMessageRequestTypeDef = TypedDict(
    "DeleteConnectionMessageRequestTypeDef",
    {
        "EndpointArn": str,
        "ReplicationInstanceArn": str,
    },
)

DeleteEndpointMessageRequestTypeDef = TypedDict(
    "DeleteEndpointMessageRequestTypeDef",
    {
        "EndpointArn": str,
    },
)

DeleteEventSubscriptionMessageRequestTypeDef = TypedDict(
    "DeleteEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
    },
)

DeleteFleetAdvisorDatabasesRequestRequestTypeDef = TypedDict(
    "DeleteFleetAdvisorDatabasesRequestRequestTypeDef",
    {
        "DatabaseIds": Sequence[str],
    },
)

DeleteFleetAdvisorDatabasesResponseTypeDef = TypedDict(
    "DeleteFleetAdvisorDatabasesResponseTypeDef",
    {
        "DatabaseIds": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteReplicationInstanceMessageRequestTypeDef = TypedDict(
    "DeleteReplicationInstanceMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
    },
)

DeleteReplicationSubnetGroupMessageRequestTypeDef = TypedDict(
    "DeleteReplicationSubnetGroupMessageRequestTypeDef",
    {
        "ReplicationSubnetGroupIdentifier": str,
    },
)

DeleteReplicationTaskAssessmentRunMessageRequestTypeDef = TypedDict(
    "DeleteReplicationTaskAssessmentRunMessageRequestTypeDef",
    {
        "ReplicationTaskAssessmentRunArn": str,
    },
)

DeleteReplicationTaskMessageRequestTypeDef = TypedDict(
    "DeleteReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
    },
)

DescribeApplicableIndividualAssessmentsMessageRequestTypeDef = TypedDict(
    "DescribeApplicableIndividualAssessmentsMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
        "ReplicationInstanceArn": str,
        "SourceEngineName": str,
        "TargetEngineName": str,
        "MigrationType": MigrationTypeValueType,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeApplicableIndividualAssessmentsResponseTypeDef = TypedDict(
    "DescribeApplicableIndividualAssessmentsResponseTypeDef",
    {
        "IndividualAssessmentNames": List[str],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

_RequiredDescribeEndpointSettingsMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeEndpointSettingsMessageRequestTypeDef",
    {
        "EngineName": str,
    },
)
_OptionalDescribeEndpointSettingsMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeEndpointSettingsMessageRequestTypeDef",
    {
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

class DescribeEndpointSettingsMessageRequestTypeDef(
    _RequiredDescribeEndpointSettingsMessageRequestTypeDef,
    _OptionalDescribeEndpointSettingsMessageRequestTypeDef,
):
    pass

EndpointSettingTypeDef = TypedDict(
    "EndpointSettingTypeDef",
    {
        "Name": str,
        "Type": EndpointSettingTypeValueType,
        "EnumValues": List[str],
        "Sensitive": bool,
        "Units": str,
        "Applicability": str,
        "IntValueMin": int,
        "IntValueMax": int,
        "DefaultValue": str,
    },
    total=False,
)

SupportedEndpointTypeTypeDef = TypedDict(
    "SupportedEndpointTypeTypeDef",
    {
        "EngineName": str,
        "SupportsCDC": bool,
        "EndpointType": ReplicationEndpointTypeValueType,
        "ReplicationInstanceEngineMinimumVersion": str,
        "EngineDisplayName": str,
    },
    total=False,
)

EventCategoryGroupTypeDef = TypedDict(
    "EventCategoryGroupTypeDef",
    {
        "SourceType": str,
        "EventCategories": List[str],
    },
    total=False,
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": Literal["replication-instance"],
        "Message": str,
        "EventCategories": List[str],
        "Date": datetime,
    },
    total=False,
)

DescribeFleetAdvisorLsaAnalysisRequestRequestTypeDef = TypedDict(
    "DescribeFleetAdvisorLsaAnalysisRequestRequestTypeDef",
    {
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

FleetAdvisorLsaAnalysisResponseTypeDef = TypedDict(
    "FleetAdvisorLsaAnalysisResponseTypeDef",
    {
        "LsaAnalysisId": str,
        "Status": str,
    },
    total=False,
)

FleetAdvisorSchemaObjectResponseTypeDef = TypedDict(
    "FleetAdvisorSchemaObjectResponseTypeDef",
    {
        "SchemaId": str,
        "ObjectType": str,
        "NumberOfObjects": int,
        "CodeLineCount": int,
        "CodeSize": int,
    },
    total=False,
)

DescribeOrderableReplicationInstancesMessageDescribeOrderableReplicationInstancesPaginateTypeDef = TypedDict(
    "DescribeOrderableReplicationInstancesMessageDescribeOrderableReplicationInstancesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeOrderableReplicationInstancesMessageRequestTypeDef = TypedDict(
    "DescribeOrderableReplicationInstancesMessageRequestTypeDef",
    {
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

OrderableReplicationInstanceTypeDef = TypedDict(
    "OrderableReplicationInstanceTypeDef",
    {
        "EngineVersion": str,
        "ReplicationInstanceClass": str,
        "StorageType": str,
        "MinAllocatedStorage": int,
        "MaxAllocatedStorage": int,
        "DefaultAllocatedStorage": int,
        "IncludedAllocatedStorage": int,
        "AvailabilityZones": List[str],
        "ReleaseStatus": ReleaseStatusValuesType,
    },
    total=False,
)

LimitationTypeDef = TypedDict(
    "LimitationTypeDef",
    {
        "DatabaseId": str,
        "EngineName": str,
        "Name": str,
        "Description": str,
        "Impact": str,
        "Type": str,
    },
    total=False,
)

DescribeRefreshSchemasStatusMessageRequestTypeDef = TypedDict(
    "DescribeRefreshSchemasStatusMessageRequestTypeDef",
    {
        "EndpointArn": str,
    },
)

RefreshSchemasStatusTypeDef = TypedDict(
    "RefreshSchemasStatusTypeDef",
    {
        "EndpointArn": str,
        "ReplicationInstanceArn": str,
        "Status": RefreshSchemasStatusTypeValueType,
        "LastRefreshDate": datetime,
        "LastFailureMessage": str,
    },
    total=False,
)

_RequiredDescribeReplicationInstanceTaskLogsMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeReplicationInstanceTaskLogsMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
    },
)
_OptionalDescribeReplicationInstanceTaskLogsMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeReplicationInstanceTaskLogsMessageRequestTypeDef",
    {
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

class DescribeReplicationInstanceTaskLogsMessageRequestTypeDef(
    _RequiredDescribeReplicationInstanceTaskLogsMessageRequestTypeDef,
    _OptionalDescribeReplicationInstanceTaskLogsMessageRequestTypeDef,
):
    pass

ReplicationInstanceTaskLogTypeDef = TypedDict(
    "ReplicationInstanceTaskLogTypeDef",
    {
        "ReplicationTaskName": str,
        "ReplicationTaskArn": str,
        "ReplicationInstanceTaskLogSize": int,
    },
    total=False,
)

DescribeReplicationTaskAssessmentResultsMessageDescribeReplicationTaskAssessmentResultsPaginateTypeDef = TypedDict(
    "DescribeReplicationTaskAssessmentResultsMessageDescribeReplicationTaskAssessmentResultsPaginateTypeDef",
    {
        "ReplicationTaskArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeReplicationTaskAssessmentResultsMessageRequestTypeDef = TypedDict(
    "DescribeReplicationTaskAssessmentResultsMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

ReplicationTaskAssessmentResultTypeDef = TypedDict(
    "ReplicationTaskAssessmentResultTypeDef",
    {
        "ReplicationTaskIdentifier": str,
        "ReplicationTaskArn": str,
        "ReplicationTaskLastAssessmentDate": datetime,
        "AssessmentStatus": str,
        "AssessmentResultsFile": str,
        "AssessmentResults": str,
        "S3ObjectUrl": str,
    },
    total=False,
)

ReplicationTaskIndividualAssessmentTypeDef = TypedDict(
    "ReplicationTaskIndividualAssessmentTypeDef",
    {
        "ReplicationTaskIndividualAssessmentArn": str,
        "ReplicationTaskAssessmentRunArn": str,
        "IndividualAssessmentName": str,
        "Status": str,
        "ReplicationTaskIndividualAssessmentStartDate": datetime,
    },
    total=False,
)

_RequiredDescribeSchemasMessageDescribeSchemasPaginateTypeDef = TypedDict(
    "_RequiredDescribeSchemasMessageDescribeSchemasPaginateTypeDef",
    {
        "EndpointArn": str,
    },
)
_OptionalDescribeSchemasMessageDescribeSchemasPaginateTypeDef = TypedDict(
    "_OptionalDescribeSchemasMessageDescribeSchemasPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class DescribeSchemasMessageDescribeSchemasPaginateTypeDef(
    _RequiredDescribeSchemasMessageDescribeSchemasPaginateTypeDef,
    _OptionalDescribeSchemasMessageDescribeSchemasPaginateTypeDef,
):
    pass

_RequiredDescribeSchemasMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeSchemasMessageRequestTypeDef",
    {
        "EndpointArn": str,
    },
)
_OptionalDescribeSchemasMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeSchemasMessageRequestTypeDef",
    {
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

class DescribeSchemasMessageRequestTypeDef(
    _RequiredDescribeSchemasMessageRequestTypeDef, _OptionalDescribeSchemasMessageRequestTypeDef
):
    pass

DescribeSchemasResponseTypeDef = TypedDict(
    "DescribeSchemasResponseTypeDef",
    {
        "Marker": str,
        "Schemas": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TableStatisticsTypeDef = TypedDict(
    "TableStatisticsTypeDef",
    {
        "SchemaName": str,
        "TableName": str,
        "Inserts": int,
        "Deletes": int,
        "Updates": int,
        "Ddls": int,
        "AppliedInserts": int,
        "AppliedDeletes": int,
        "AppliedUpdates": int,
        "AppliedDdls": int,
        "FullLoadRows": int,
        "FullLoadCondtnlChkFailedRows": int,
        "FullLoadErrorRows": int,
        "FullLoadStartTime": datetime,
        "FullLoadEndTime": datetime,
        "FullLoadReloaded": bool,
        "LastUpdateTime": datetime,
        "TableState": str,
        "ValidationPendingRecords": int,
        "ValidationFailedRecords": int,
        "ValidationSuspendedRecords": int,
        "ValidationState": str,
        "ValidationStateDetails": str,
    },
    total=False,
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTagsForResourceMessageRequestTypeDef = TypedDict(
    "ListTagsForResourceMessageRequestTypeDef",
    {
        "ResourceArn": str,
        "ResourceArnList": Sequence[str],
    },
    total=False,
)

_RequiredModifyEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_RequiredModifyEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
    },
)
_OptionalModifyEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_OptionalModifyEventSubscriptionMessageRequestTypeDef",
    {
        "SnsTopicArn": str,
        "SourceType": str,
        "EventCategories": Sequence[str],
        "Enabled": bool,
    },
    total=False,
)

class ModifyEventSubscriptionMessageRequestTypeDef(
    _RequiredModifyEventSubscriptionMessageRequestTypeDef,
    _OptionalModifyEventSubscriptionMessageRequestTypeDef,
):
    pass

_RequiredModifyReplicationInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredModifyReplicationInstanceMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
    },
)
_OptionalModifyReplicationInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalModifyReplicationInstanceMessageRequestTypeDef",
    {
        "AllocatedStorage": int,
        "ApplyImmediately": bool,
        "ReplicationInstanceClass": str,
        "VpcSecurityGroupIds": Sequence[str],
        "PreferredMaintenanceWindow": str,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AllowMajorVersionUpgrade": bool,
        "AutoMinorVersionUpgrade": bool,
        "ReplicationInstanceIdentifier": str,
        "NetworkType": str,
    },
    total=False,
)

class ModifyReplicationInstanceMessageRequestTypeDef(
    _RequiredModifyReplicationInstanceMessageRequestTypeDef,
    _OptionalModifyReplicationInstanceMessageRequestTypeDef,
):
    pass

_RequiredModifyReplicationSubnetGroupMessageRequestTypeDef = TypedDict(
    "_RequiredModifyReplicationSubnetGroupMessageRequestTypeDef",
    {
        "ReplicationSubnetGroupIdentifier": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalModifyReplicationSubnetGroupMessageRequestTypeDef = TypedDict(
    "_OptionalModifyReplicationSubnetGroupMessageRequestTypeDef",
    {
        "ReplicationSubnetGroupDescription": str,
    },
    total=False,
)

class ModifyReplicationSubnetGroupMessageRequestTypeDef(
    _RequiredModifyReplicationSubnetGroupMessageRequestTypeDef,
    _OptionalModifyReplicationSubnetGroupMessageRequestTypeDef,
):
    pass

_RequiredModifyReplicationTaskMessageRequestTypeDef = TypedDict(
    "_RequiredModifyReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
    },
)
_OptionalModifyReplicationTaskMessageRequestTypeDef = TypedDict(
    "_OptionalModifyReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskIdentifier": str,
        "MigrationType": MigrationTypeValueType,
        "TableMappings": str,
        "ReplicationTaskSettings": str,
        "CdcStartTime": Union[datetime, str],
        "CdcStartPosition": str,
        "CdcStopPosition": str,
        "TaskData": str,
    },
    total=False,
)

class ModifyReplicationTaskMessageRequestTypeDef(
    _RequiredModifyReplicationTaskMessageRequestTypeDef,
    _OptionalModifyReplicationTaskMessageRequestTypeDef,
):
    pass

MoveReplicationTaskMessageRequestTypeDef = TypedDict(
    "MoveReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
        "TargetReplicationInstanceArn": str,
    },
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

PendingMaintenanceActionTypeDef = TypedDict(
    "PendingMaintenanceActionTypeDef",
    {
        "Action": str,
        "AutoAppliedAfterDate": datetime,
        "ForcedApplyDate": datetime,
        "OptInStatus": str,
        "CurrentApplyDate": datetime,
        "Description": str,
    },
    total=False,
)

RdsConfigurationTypeDef = TypedDict(
    "RdsConfigurationTypeDef",
    {
        "EngineEdition": str,
        "InstanceType": str,
        "InstanceVcpu": float,
        "InstanceMemory": float,
        "StorageType": str,
        "StorageSize": int,
        "StorageIops": int,
        "DeploymentOption": str,
    },
    total=False,
)

RdsRequirementsTypeDef = TypedDict(
    "RdsRequirementsTypeDef",
    {
        "EngineEdition": str,
        "InstanceVcpu": float,
        "InstanceMemory": float,
        "StorageSize": int,
        "StorageIops": int,
        "DeploymentOption": str,
    },
    total=False,
)

_RequiredRebootReplicationInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredRebootReplicationInstanceMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
    },
)
_OptionalRebootReplicationInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalRebootReplicationInstanceMessageRequestTypeDef",
    {
        "ForceFailover": bool,
        "ForcePlannedFailover": bool,
    },
    total=False,
)

class RebootReplicationInstanceMessageRequestTypeDef(
    _RequiredRebootReplicationInstanceMessageRequestTypeDef,
    _OptionalRebootReplicationInstanceMessageRequestTypeDef,
):
    pass

RecommendationSettingsTypeDef = TypedDict(
    "RecommendationSettingsTypeDef",
    {
        "InstanceSizingType": str,
        "WorkloadType": str,
    },
)

RefreshSchemasMessageRequestTypeDef = TypedDict(
    "RefreshSchemasMessageRequestTypeDef",
    {
        "EndpointArn": str,
        "ReplicationInstanceArn": str,
    },
)

TableToReloadTypeDef = TypedDict(
    "TableToReloadTypeDef",
    {
        "SchemaName": str,
        "TableName": str,
    },
)

ReloadTablesResponseTypeDef = TypedDict(
    "ReloadTablesResponseTypeDef",
    {
        "ReplicationTaskArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RemoveTagsFromResourceMessageRequestTypeDef = TypedDict(
    "RemoveTagsFromResourceMessageRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

ReplicationPendingModifiedValuesTypeDef = TypedDict(
    "ReplicationPendingModifiedValuesTypeDef",
    {
        "ReplicationInstanceClass": str,
        "AllocatedStorage": int,
        "MultiAZ": bool,
        "EngineVersion": str,
        "NetworkType": str,
    },
    total=False,
)

VpcSecurityGroupMembershipTypeDef = TypedDict(
    "VpcSecurityGroupMembershipTypeDef",
    {
        "VpcSecurityGroupId": str,
        "Status": str,
    },
    total=False,
)

ReplicationTaskAssessmentRunProgressTypeDef = TypedDict(
    "ReplicationTaskAssessmentRunProgressTypeDef",
    {
        "IndividualAssessmentCount": int,
        "IndividualAssessmentCompletedCount": int,
    },
    total=False,
)

ReplicationTaskStatsTypeDef = TypedDict(
    "ReplicationTaskStatsTypeDef",
    {
        "FullLoadProgressPercent": int,
        "ElapsedTimeMillis": int,
        "TablesLoaded": int,
        "TablesLoading": int,
        "TablesQueued": int,
        "TablesErrored": int,
        "FreshStartDate": datetime,
        "StartDate": datetime,
        "StopDate": datetime,
        "FullLoadStartDate": datetime,
        "FullLoadFinishDate": datetime,
    },
    total=False,
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

RunFleetAdvisorLsaAnalysisResponseTypeDef = TypedDict(
    "RunFleetAdvisorLsaAnalysisResponseTypeDef",
    {
        "LsaAnalysisId": str,
        "Status": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SchemaShortInfoResponseTypeDef = TypedDict(
    "SchemaShortInfoResponseTypeDef",
    {
        "SchemaId": str,
        "SchemaName": str,
        "DatabaseId": str,
        "DatabaseName": str,
        "DatabaseIpAddress": str,
    },
    total=False,
)

StartReplicationTaskAssessmentMessageRequestTypeDef = TypedDict(
    "StartReplicationTaskAssessmentMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
    },
)

_RequiredStartReplicationTaskAssessmentRunMessageRequestTypeDef = TypedDict(
    "_RequiredStartReplicationTaskAssessmentRunMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
        "ServiceAccessRoleArn": str,
        "ResultLocationBucket": str,
        "AssessmentRunName": str,
    },
)
_OptionalStartReplicationTaskAssessmentRunMessageRequestTypeDef = TypedDict(
    "_OptionalStartReplicationTaskAssessmentRunMessageRequestTypeDef",
    {
        "ResultLocationFolder": str,
        "ResultEncryptionMode": str,
        "ResultKmsKeyArn": str,
        "IncludeOnly": Sequence[str],
        "Exclude": Sequence[str],
    },
    total=False,
)

class StartReplicationTaskAssessmentRunMessageRequestTypeDef(
    _RequiredStartReplicationTaskAssessmentRunMessageRequestTypeDef,
    _OptionalStartReplicationTaskAssessmentRunMessageRequestTypeDef,
):
    pass

_RequiredStartReplicationTaskMessageRequestTypeDef = TypedDict(
    "_RequiredStartReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
        "StartReplicationTaskType": StartReplicationTaskTypeValueType,
    },
)
_OptionalStartReplicationTaskMessageRequestTypeDef = TypedDict(
    "_OptionalStartReplicationTaskMessageRequestTypeDef",
    {
        "CdcStartTime": Union[datetime, str],
        "CdcStartPosition": str,
        "CdcStopPosition": str,
    },
    total=False,
)

class StartReplicationTaskMessageRequestTypeDef(
    _RequiredStartReplicationTaskMessageRequestTypeDef,
    _OptionalStartReplicationTaskMessageRequestTypeDef,
):
    pass

StopReplicationTaskMessageRequestTypeDef = TypedDict(
    "StopReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
    },
)

TestConnectionMessageRequestTypeDef = TypedDict(
    "TestConnectionMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
        "EndpointArn": str,
    },
)

UpdateSubscriptionsToEventBridgeMessageRequestTypeDef = TypedDict(
    "UpdateSubscriptionsToEventBridgeMessageRequestTypeDef",
    {
        "ForceMove": bool,
    },
    total=False,
)

UpdateSubscriptionsToEventBridgeResponseTypeDef = TypedDict(
    "UpdateSubscriptionsToEventBridgeResponseTypeDef",
    {
        "Result": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeAccountAttributesResponseTypeDef = TypedDict(
    "DescribeAccountAttributesResponseTypeDef",
    {
        "AccountQuotas": List[AccountQuotaTypeDef],
        "UniqueAccountIdentifier": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AddTagsToResourceMessageRequestTypeDef = TypedDict(
    "AddTagsToResourceMessageRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_RequiredCreateEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "SnsTopicArn": str,
    },
)
_OptionalCreateEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_OptionalCreateEventSubscriptionMessageRequestTypeDef",
    {
        "SourceType": str,
        "EventCategories": Sequence[str],
        "SourceIds": Sequence[str],
        "Enabled": bool,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateEventSubscriptionMessageRequestTypeDef(
    _RequiredCreateEventSubscriptionMessageRequestTypeDef,
    _OptionalCreateEventSubscriptionMessageRequestTypeDef,
):
    pass

_RequiredCreateReplicationInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredCreateReplicationInstanceMessageRequestTypeDef",
    {
        "ReplicationInstanceIdentifier": str,
        "ReplicationInstanceClass": str,
    },
)
_OptionalCreateReplicationInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalCreateReplicationInstanceMessageRequestTypeDef",
    {
        "AllocatedStorage": int,
        "VpcSecurityGroupIds": Sequence[str],
        "AvailabilityZone": str,
        "ReplicationSubnetGroupIdentifier": str,
        "PreferredMaintenanceWindow": str,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AutoMinorVersionUpgrade": bool,
        "Tags": Sequence[TagTypeDef],
        "KmsKeyId": str,
        "PubliclyAccessible": bool,
        "DnsNameServers": str,
        "ResourceIdentifier": str,
        "NetworkType": str,
    },
    total=False,
)

class CreateReplicationInstanceMessageRequestTypeDef(
    _RequiredCreateReplicationInstanceMessageRequestTypeDef,
    _OptionalCreateReplicationInstanceMessageRequestTypeDef,
):
    pass

_RequiredCreateReplicationSubnetGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateReplicationSubnetGroupMessageRequestTypeDef",
    {
        "ReplicationSubnetGroupIdentifier": str,
        "ReplicationSubnetGroupDescription": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalCreateReplicationSubnetGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateReplicationSubnetGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateReplicationSubnetGroupMessageRequestTypeDef(
    _RequiredCreateReplicationSubnetGroupMessageRequestTypeDef,
    _OptionalCreateReplicationSubnetGroupMessageRequestTypeDef,
):
    pass

_RequiredCreateReplicationTaskMessageRequestTypeDef = TypedDict(
    "_RequiredCreateReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskIdentifier": str,
        "SourceEndpointArn": str,
        "TargetEndpointArn": str,
        "ReplicationInstanceArn": str,
        "MigrationType": MigrationTypeValueType,
        "TableMappings": str,
    },
)
_OptionalCreateReplicationTaskMessageRequestTypeDef = TypedDict(
    "_OptionalCreateReplicationTaskMessageRequestTypeDef",
    {
        "ReplicationTaskSettings": str,
        "CdcStartTime": Union[datetime, str],
        "CdcStartPosition": str,
        "CdcStopPosition": str,
        "Tags": Sequence[TagTypeDef],
        "TaskData": str,
        "ResourceIdentifier": str,
    },
    total=False,
)

class CreateReplicationTaskMessageRequestTypeDef(
    _RequiredCreateReplicationTaskMessageRequestTypeDef,
    _OptionalCreateReplicationTaskMessageRequestTypeDef,
):
    pass

_RequiredImportCertificateMessageRequestTypeDef = TypedDict(
    "_RequiredImportCertificateMessageRequestTypeDef",
    {
        "CertificateIdentifier": str,
    },
)
_OptionalImportCertificateMessageRequestTypeDef = TypedDict(
    "_OptionalImportCertificateMessageRequestTypeDef",
    {
        "CertificatePem": str,
        "CertificateWallet": Union[str, bytes, IO[Any], StreamingBody],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class ImportCertificateMessageRequestTypeDef(
    _RequiredImportCertificateMessageRequestTypeDef, _OptionalImportCertificateMessageRequestTypeDef
):
    pass

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "TagList": List[TagTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SubnetTypeDef = TypedDict(
    "SubnetTypeDef",
    {
        "SubnetIdentifier": str,
        "SubnetAvailabilityZone": AvailabilityZoneTypeDef,
        "SubnetStatus": str,
    },
    total=False,
)

BatchStartRecommendationsResponseTypeDef = TypedDict(
    "BatchStartRecommendationsResponseTypeDef",
    {
        "ErrorEntries": List[BatchStartRecommendationsErrorEntryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteCertificateResponseTypeDef = TypedDict(
    "DeleteCertificateResponseTypeDef",
    {
        "Certificate": CertificateTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeCertificatesResponseTypeDef = TypedDict(
    "DescribeCertificatesResponseTypeDef",
    {
        "Marker": str,
        "Certificates": List[CertificateTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ImportCertificateResponseTypeDef = TypedDict(
    "ImportCertificateResponseTypeDef",
    {
        "Certificate": CertificateTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CollectorResponseTypeDef = TypedDict(
    "CollectorResponseTypeDef",
    {
        "CollectorReferencedId": str,
        "CollectorName": str,
        "CollectorVersion": str,
        "VersionStatus": VersionStatusType,
        "Description": str,
        "S3BucketName": str,
        "ServiceAccessRoleArn": str,
        "CollectorHealthCheck": CollectorHealthCheckTypeDef,
        "LastDataReceived": str,
        "RegisteredDate": str,
        "CreatedDate": str,
        "ModifiedDate": str,
        "InventoryData": InventoryDataTypeDef,
    },
    total=False,
)

DeleteConnectionResponseTypeDef = TypedDict(
    "DeleteConnectionResponseTypeDef",
    {
        "Connection": ConnectionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeConnectionsResponseTypeDef = TypedDict(
    "DescribeConnectionsResponseTypeDef",
    {
        "Marker": str,
        "Connections": List[ConnectionTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TestConnectionResponseTypeDef = TypedDict(
    "TestConnectionResponseTypeDef",
    {
        "Connection": ConnectionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateEndpointMessageRequestTypeDef = TypedDict(
    "_RequiredCreateEndpointMessageRequestTypeDef",
    {
        "EndpointIdentifier": str,
        "EndpointType": ReplicationEndpointTypeValueType,
        "EngineName": str,
    },
)
_OptionalCreateEndpointMessageRequestTypeDef = TypedDict(
    "_OptionalCreateEndpointMessageRequestTypeDef",
    {
        "Username": str,
        "Password": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "ExtraConnectionAttributes": str,
        "KmsKeyId": str,
        "Tags": Sequence[TagTypeDef],
        "CertificateArn": str,
        "SslMode": DmsSslModeValueType,
        "ServiceAccessRoleArn": str,
        "ExternalTableDefinition": str,
        "DynamoDbSettings": DynamoDbSettingsTypeDef,
        "S3Settings": S3SettingsTypeDef,
        "DmsTransferSettings": DmsTransferSettingsTypeDef,
        "MongoDbSettings": MongoDbSettingsTypeDef,
        "KinesisSettings": KinesisSettingsTypeDef,
        "KafkaSettings": KafkaSettingsTypeDef,
        "ElasticsearchSettings": ElasticsearchSettingsTypeDef,
        "NeptuneSettings": NeptuneSettingsTypeDef,
        "RedshiftSettings": RedshiftSettingsTypeDef,
        "PostgreSQLSettings": PostgreSQLSettingsTypeDef,
        "MySQLSettings": MySQLSettingsTypeDef,
        "OracleSettings": OracleSettingsTypeDef,
        "SybaseSettings": SybaseSettingsTypeDef,
        "MicrosoftSQLServerSettings": MicrosoftSQLServerSettingsTypeDef,
        "IBMDb2Settings": IBMDb2SettingsTypeDef,
        "ResourceIdentifier": str,
        "DocDbSettings": DocDbSettingsTypeDef,
        "RedisSettings": RedisSettingsTypeDef,
        "GcpMySQLSettings": GcpMySQLSettingsTypeDef,
    },
    total=False,
)

class CreateEndpointMessageRequestTypeDef(
    _RequiredCreateEndpointMessageRequestTypeDef, _OptionalCreateEndpointMessageRequestTypeDef
):
    pass

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "EndpointIdentifier": str,
        "EndpointType": ReplicationEndpointTypeValueType,
        "EngineName": str,
        "EngineDisplayName": str,
        "Username": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "ExtraConnectionAttributes": str,
        "Status": str,
        "KmsKeyId": str,
        "EndpointArn": str,
        "CertificateArn": str,
        "SslMode": DmsSslModeValueType,
        "ServiceAccessRoleArn": str,
        "ExternalTableDefinition": str,
        "ExternalId": str,
        "DynamoDbSettings": DynamoDbSettingsTypeDef,
        "S3Settings": S3SettingsTypeDef,
        "DmsTransferSettings": DmsTransferSettingsTypeDef,
        "MongoDbSettings": MongoDbSettingsTypeDef,
        "KinesisSettings": KinesisSettingsTypeDef,
        "KafkaSettings": KafkaSettingsTypeDef,
        "ElasticsearchSettings": ElasticsearchSettingsTypeDef,
        "NeptuneSettings": NeptuneSettingsTypeDef,
        "RedshiftSettings": RedshiftSettingsTypeDef,
        "PostgreSQLSettings": PostgreSQLSettingsTypeDef,
        "MySQLSettings": MySQLSettingsTypeDef,
        "OracleSettings": OracleSettingsTypeDef,
        "SybaseSettings": SybaseSettingsTypeDef,
        "MicrosoftSQLServerSettings": MicrosoftSQLServerSettingsTypeDef,
        "IBMDb2Settings": IBMDb2SettingsTypeDef,
        "DocDbSettings": DocDbSettingsTypeDef,
        "RedisSettings": RedisSettingsTypeDef,
        "GcpMySQLSettings": GcpMySQLSettingsTypeDef,
    },
    total=False,
)

_RequiredModifyEndpointMessageRequestTypeDef = TypedDict(
    "_RequiredModifyEndpointMessageRequestTypeDef",
    {
        "EndpointArn": str,
    },
)
_OptionalModifyEndpointMessageRequestTypeDef = TypedDict(
    "_OptionalModifyEndpointMessageRequestTypeDef",
    {
        "EndpointIdentifier": str,
        "EndpointType": ReplicationEndpointTypeValueType,
        "EngineName": str,
        "Username": str,
        "Password": str,
        "ServerName": str,
        "Port": int,
        "DatabaseName": str,
        "ExtraConnectionAttributes": str,
        "CertificateArn": str,
        "SslMode": DmsSslModeValueType,
        "ServiceAccessRoleArn": str,
        "ExternalTableDefinition": str,
        "DynamoDbSettings": DynamoDbSettingsTypeDef,
        "S3Settings": S3SettingsTypeDef,
        "DmsTransferSettings": DmsTransferSettingsTypeDef,
        "MongoDbSettings": MongoDbSettingsTypeDef,
        "KinesisSettings": KinesisSettingsTypeDef,
        "KafkaSettings": KafkaSettingsTypeDef,
        "ElasticsearchSettings": ElasticsearchSettingsTypeDef,
        "NeptuneSettings": NeptuneSettingsTypeDef,
        "RedshiftSettings": RedshiftSettingsTypeDef,
        "PostgreSQLSettings": PostgreSQLSettingsTypeDef,
        "MySQLSettings": MySQLSettingsTypeDef,
        "OracleSettings": OracleSettingsTypeDef,
        "SybaseSettings": SybaseSettingsTypeDef,
        "MicrosoftSQLServerSettings": MicrosoftSQLServerSettingsTypeDef,
        "IBMDb2Settings": IBMDb2SettingsTypeDef,
        "DocDbSettings": DocDbSettingsTypeDef,
        "RedisSettings": RedisSettingsTypeDef,
        "ExactSettings": bool,
        "GcpMySQLSettings": GcpMySQLSettingsTypeDef,
    },
    total=False,
)

class ModifyEndpointMessageRequestTypeDef(
    _RequiredModifyEndpointMessageRequestTypeDef, _OptionalModifyEndpointMessageRequestTypeDef
):
    pass

CreateEventSubscriptionResponseTypeDef = TypedDict(
    "CreateEventSubscriptionResponseTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteEventSubscriptionResponseTypeDef = TypedDict(
    "DeleteEventSubscriptionResponseTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEventSubscriptionsResponseTypeDef = TypedDict(
    "DescribeEventSubscriptionsResponseTypeDef",
    {
        "Marker": str,
        "EventSubscriptionsList": List[EventSubscriptionTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModifyEventSubscriptionResponseTypeDef = TypedDict(
    "ModifyEventSubscriptionResponseTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DatabaseResponseTypeDef = TypedDict(
    "DatabaseResponseTypeDef",
    {
        "DatabaseId": str,
        "DatabaseName": str,
        "IpAddress": str,
        "NumberOfSchemas": int,
        "Server": ServerShortInfoResponseTypeDef,
        "SoftwareDetails": DatabaseInstanceSoftwareDetailsResponseTypeDef,
        "Collectors": List[CollectorShortInfoResponseTypeDef],
    },
    total=False,
)

DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef = TypedDict(
    "DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeCertificatesMessageRequestTypeDef = TypedDict(
    "DescribeCertificatesMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeConnectionsMessageDescribeConnectionsPaginateTypeDef = TypedDict(
    "DescribeConnectionsMessageDescribeConnectionsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeConnectionsMessageRequestTypeDef = TypedDict(
    "DescribeConnectionsMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeEndpointTypesMessageDescribeEndpointTypesPaginateTypeDef = TypedDict(
    "DescribeEndpointTypesMessageDescribeEndpointTypesPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeEndpointTypesMessageRequestTypeDef = TypedDict(
    "DescribeEndpointTypesMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeEndpointsMessageDescribeEndpointsPaginateTypeDef = TypedDict(
    "DescribeEndpointsMessageDescribeEndpointsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeEndpointsMessageRequestTypeDef = TypedDict(
    "DescribeEndpointsMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeEventCategoriesMessageRequestTypeDef = TypedDict(
    "DescribeEventCategoriesMessageRequestTypeDef",
    {
        "SourceType": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef = TypedDict(
    "DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef",
    {
        "SubscriptionName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeEventSubscriptionsMessageRequestTypeDef = TypedDict(
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeEventsMessageDescribeEventsPaginateTypeDef = TypedDict(
    "DescribeEventsMessageDescribeEventsPaginateTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": Literal["replication-instance"],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Duration": int,
        "EventCategories": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeEventsMessageRequestTypeDef = TypedDict(
    "DescribeEventsMessageRequestTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": Literal["replication-instance"],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Duration": int,
        "EventCategories": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeFleetAdvisorCollectorsRequestRequestTypeDef = TypedDict(
    "DescribeFleetAdvisorCollectorsRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribeFleetAdvisorDatabasesRequestRequestTypeDef = TypedDict(
    "DescribeFleetAdvisorDatabasesRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribeFleetAdvisorSchemaObjectSummaryRequestRequestTypeDef = TypedDict(
    "DescribeFleetAdvisorSchemaObjectSummaryRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribeFleetAdvisorSchemasRequestRequestTypeDef = TypedDict(
    "DescribeFleetAdvisorSchemasRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribePendingMaintenanceActionsMessageRequestTypeDef = TypedDict(
    "DescribePendingMaintenanceActionsMessageRequestTypeDef",
    {
        "ReplicationInstanceArn": str,
        "Filters": Sequence[FilterTypeDef],
        "Marker": str,
        "MaxRecords": int,
    },
    total=False,
)

DescribeRecommendationLimitationsRequestRequestTypeDef = TypedDict(
    "DescribeRecommendationLimitationsRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribeRecommendationsRequestRequestTypeDef = TypedDict(
    "DescribeRecommendationsRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "NextToken": str,
    },
    total=False,
)

DescribeReplicationInstancesMessageDescribeReplicationInstancesPaginateTypeDef = TypedDict(
    "DescribeReplicationInstancesMessageDescribeReplicationInstancesPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeReplicationInstancesMessageRequestTypeDef = TypedDict(
    "DescribeReplicationInstancesMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeReplicationSubnetGroupsMessageDescribeReplicationSubnetGroupsPaginateTypeDef = TypedDict(
    "DescribeReplicationSubnetGroupsMessageDescribeReplicationSubnetGroupsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeReplicationSubnetGroupsMessageRequestTypeDef = TypedDict(
    "DescribeReplicationSubnetGroupsMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeReplicationTaskAssessmentRunsMessageRequestTypeDef = TypedDict(
    "DescribeReplicationTaskAssessmentRunsMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeReplicationTaskIndividualAssessmentsMessageRequestTypeDef = TypedDict(
    "DescribeReplicationTaskIndividualAssessmentsMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeReplicationTasksMessageDescribeReplicationTasksPaginateTypeDef = TypedDict(
    "DescribeReplicationTasksMessageDescribeReplicationTasksPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "WithoutSettings": bool,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeReplicationTasksMessageRequestTypeDef = TypedDict(
    "DescribeReplicationTasksMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WithoutSettings": bool,
    },
    total=False,
)

_RequiredDescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef = TypedDict(
    "_RequiredDescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef",
    {
        "ReplicationTaskArn": str,
    },
)
_OptionalDescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef = TypedDict(
    "_OptionalDescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class DescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef(
    _RequiredDescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef,
    _OptionalDescribeTableStatisticsMessageDescribeTableStatisticsPaginateTypeDef,
):
    pass

_RequiredDescribeTableStatisticsMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeTableStatisticsMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
    },
)
_OptionalDescribeTableStatisticsMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeTableStatisticsMessageRequestTypeDef",
    {
        "MaxRecords": int,
        "Marker": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

class DescribeTableStatisticsMessageRequestTypeDef(
    _RequiredDescribeTableStatisticsMessageRequestTypeDef,
    _OptionalDescribeTableStatisticsMessageRequestTypeDef,
):
    pass

DescribeConnectionsMessageTestConnectionSucceedsWaitTypeDef = TypedDict(
    "DescribeConnectionsMessageTestConnectionSucceedsWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeEndpointsMessageEndpointDeletedWaitTypeDef = TypedDict(
    "DescribeEndpointsMessageEndpointDeletedWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeReplicationInstancesMessageReplicationInstanceAvailableWaitTypeDef = TypedDict(
    "DescribeReplicationInstancesMessageReplicationInstanceAvailableWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeReplicationInstancesMessageReplicationInstanceDeletedWaitTypeDef = TypedDict(
    "DescribeReplicationInstancesMessageReplicationInstanceDeletedWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeReplicationTasksMessageReplicationTaskDeletedWaitTypeDef = TypedDict(
    "DescribeReplicationTasksMessageReplicationTaskDeletedWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WithoutSettings": bool,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeReplicationTasksMessageReplicationTaskReadyWaitTypeDef = TypedDict(
    "DescribeReplicationTasksMessageReplicationTaskReadyWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WithoutSettings": bool,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeReplicationTasksMessageReplicationTaskRunningWaitTypeDef = TypedDict(
    "DescribeReplicationTasksMessageReplicationTaskRunningWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WithoutSettings": bool,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeReplicationTasksMessageReplicationTaskStoppedWaitTypeDef = TypedDict(
    "DescribeReplicationTasksMessageReplicationTaskStoppedWaitTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WithoutSettings": bool,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeEndpointSettingsResponseTypeDef = TypedDict(
    "DescribeEndpointSettingsResponseTypeDef",
    {
        "Marker": str,
        "EndpointSettings": List[EndpointSettingTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEndpointTypesResponseTypeDef = TypedDict(
    "DescribeEndpointTypesResponseTypeDef",
    {
        "Marker": str,
        "SupportedEndpointTypes": List[SupportedEndpointTypeTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEventCategoriesResponseTypeDef = TypedDict(
    "DescribeEventCategoriesResponseTypeDef",
    {
        "EventCategoryGroupList": List[EventCategoryGroupTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEventsResponseTypeDef = TypedDict(
    "DescribeEventsResponseTypeDef",
    {
        "Marker": str,
        "Events": List[EventTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFleetAdvisorLsaAnalysisResponseTypeDef = TypedDict(
    "DescribeFleetAdvisorLsaAnalysisResponseTypeDef",
    {
        "Analysis": List[FleetAdvisorLsaAnalysisResponseTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFleetAdvisorSchemaObjectSummaryResponseTypeDef = TypedDict(
    "DescribeFleetAdvisorSchemaObjectSummaryResponseTypeDef",
    {
        "FleetAdvisorSchemaObjects": List[FleetAdvisorSchemaObjectResponseTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeOrderableReplicationInstancesResponseTypeDef = TypedDict(
    "DescribeOrderableReplicationInstancesResponseTypeDef",
    {
        "OrderableReplicationInstances": List[OrderableReplicationInstanceTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeRecommendationLimitationsResponseTypeDef = TypedDict(
    "DescribeRecommendationLimitationsResponseTypeDef",
    {
        "NextToken": str,
        "Limitations": List[LimitationTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeRefreshSchemasStatusResponseTypeDef = TypedDict(
    "DescribeRefreshSchemasStatusResponseTypeDef",
    {
        "RefreshSchemasStatus": RefreshSchemasStatusTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RefreshSchemasResponseTypeDef = TypedDict(
    "RefreshSchemasResponseTypeDef",
    {
        "RefreshSchemasStatus": RefreshSchemasStatusTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationInstanceTaskLogsResponseTypeDef = TypedDict(
    "DescribeReplicationInstanceTaskLogsResponseTypeDef",
    {
        "ReplicationInstanceArn": str,
        "ReplicationInstanceTaskLogs": List[ReplicationInstanceTaskLogTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationTaskAssessmentResultsResponseTypeDef = TypedDict(
    "DescribeReplicationTaskAssessmentResultsResponseTypeDef",
    {
        "Marker": str,
        "BucketName": str,
        "ReplicationTaskAssessmentResults": List[ReplicationTaskAssessmentResultTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationTaskIndividualAssessmentsResponseTypeDef = TypedDict(
    "DescribeReplicationTaskIndividualAssessmentsResponseTypeDef",
    {
        "Marker": str,
        "ReplicationTaskIndividualAssessments": List[ReplicationTaskIndividualAssessmentTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeTableStatisticsResponseTypeDef = TypedDict(
    "DescribeTableStatisticsResponseTypeDef",
    {
        "ReplicationTaskArn": str,
        "TableStatistics": List[TableStatisticsTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResourcePendingMaintenanceActionsTypeDef = TypedDict(
    "ResourcePendingMaintenanceActionsTypeDef",
    {
        "ResourceIdentifier": str,
        "PendingMaintenanceActionDetails": List[PendingMaintenanceActionTypeDef],
    },
    total=False,
)

RdsRecommendationTypeDef = TypedDict(
    "RdsRecommendationTypeDef",
    {
        "RequirementsToTarget": RdsRequirementsTypeDef,
        "TargetConfiguration": RdsConfigurationTypeDef,
    },
    total=False,
)

StartRecommendationsRequestEntryTypeDef = TypedDict(
    "StartRecommendationsRequestEntryTypeDef",
    {
        "DatabaseId": str,
        "Settings": RecommendationSettingsTypeDef,
    },
)

StartRecommendationsRequestRequestTypeDef = TypedDict(
    "StartRecommendationsRequestRequestTypeDef",
    {
        "DatabaseId": str,
        "Settings": RecommendationSettingsTypeDef,
    },
)

_RequiredReloadTablesMessageRequestTypeDef = TypedDict(
    "_RequiredReloadTablesMessageRequestTypeDef",
    {
        "ReplicationTaskArn": str,
        "TablesToReload": Sequence[TableToReloadTypeDef],
    },
)
_OptionalReloadTablesMessageRequestTypeDef = TypedDict(
    "_OptionalReloadTablesMessageRequestTypeDef",
    {
        "ReloadOption": ReloadOptionValueType,
    },
    total=False,
)

class ReloadTablesMessageRequestTypeDef(
    _RequiredReloadTablesMessageRequestTypeDef, _OptionalReloadTablesMessageRequestTypeDef
):
    pass

ReplicationTaskAssessmentRunTypeDef = TypedDict(
    "ReplicationTaskAssessmentRunTypeDef",
    {
        "ReplicationTaskAssessmentRunArn": str,
        "ReplicationTaskArn": str,
        "Status": str,
        "ReplicationTaskAssessmentRunCreationDate": datetime,
        "AssessmentProgress": ReplicationTaskAssessmentRunProgressTypeDef,
        "LastFailureMessage": str,
        "ServiceAccessRoleArn": str,
        "ResultLocationBucket": str,
        "ResultLocationFolder": str,
        "ResultEncryptionMode": str,
        "ResultKmsKeyArn": str,
        "AssessmentRunName": str,
    },
    total=False,
)

ReplicationTaskTypeDef = TypedDict(
    "ReplicationTaskTypeDef",
    {
        "ReplicationTaskIdentifier": str,
        "SourceEndpointArn": str,
        "TargetEndpointArn": str,
        "ReplicationInstanceArn": str,
        "MigrationType": MigrationTypeValueType,
        "TableMappings": str,
        "ReplicationTaskSettings": str,
        "Status": str,
        "LastFailureMessage": str,
        "StopReason": str,
        "ReplicationTaskCreationDate": datetime,
        "ReplicationTaskStartDate": datetime,
        "CdcStartPosition": str,
        "CdcStopPosition": str,
        "RecoveryCheckpoint": str,
        "ReplicationTaskArn": str,
        "ReplicationTaskStats": ReplicationTaskStatsTypeDef,
        "TaskData": str,
        "TargetReplicationInstanceArn": str,
    },
    total=False,
)

SchemaResponseTypeDef = TypedDict(
    "SchemaResponseTypeDef",
    {
        "CodeLineCount": int,
        "CodeSize": int,
        "Complexity": str,
        "Server": ServerShortInfoResponseTypeDef,
        "DatabaseInstance": DatabaseShortInfoResponseTypeDef,
        "SchemaId": str,
        "SchemaName": str,
        "OriginalSchema": SchemaShortInfoResponseTypeDef,
        "Similarity": float,
    },
    total=False,
)

ReplicationSubnetGroupTypeDef = TypedDict(
    "ReplicationSubnetGroupTypeDef",
    {
        "ReplicationSubnetGroupIdentifier": str,
        "ReplicationSubnetGroupDescription": str,
        "VpcId": str,
        "SubnetGroupStatus": str,
        "Subnets": List[SubnetTypeDef],
        "SupportedNetworkTypes": List[str],
    },
    total=False,
)

DescribeFleetAdvisorCollectorsResponseTypeDef = TypedDict(
    "DescribeFleetAdvisorCollectorsResponseTypeDef",
    {
        "Collectors": List[CollectorResponseTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateEndpointResponseTypeDef = TypedDict(
    "CreateEndpointResponseTypeDef",
    {
        "Endpoint": EndpointTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteEndpointResponseTypeDef = TypedDict(
    "DeleteEndpointResponseTypeDef",
    {
        "Endpoint": EndpointTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEndpointsResponseTypeDef = TypedDict(
    "DescribeEndpointsResponseTypeDef",
    {
        "Marker": str,
        "Endpoints": List[EndpointTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModifyEndpointResponseTypeDef = TypedDict(
    "ModifyEndpointResponseTypeDef",
    {
        "Endpoint": EndpointTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFleetAdvisorDatabasesResponseTypeDef = TypedDict(
    "DescribeFleetAdvisorDatabasesResponseTypeDef",
    {
        "Databases": List[DatabaseResponseTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ApplyPendingMaintenanceActionResponseTypeDef = TypedDict(
    "ApplyPendingMaintenanceActionResponseTypeDef",
    {
        "ResourcePendingMaintenanceActions": ResourcePendingMaintenanceActionsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribePendingMaintenanceActionsResponseTypeDef = TypedDict(
    "DescribePendingMaintenanceActionsResponseTypeDef",
    {
        "PendingMaintenanceActions": List[ResourcePendingMaintenanceActionsTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RecommendationDataTypeDef = TypedDict(
    "RecommendationDataTypeDef",
    {
        "RdsEngine": RdsRecommendationTypeDef,
    },
    total=False,
)

BatchStartRecommendationsRequestRequestTypeDef = TypedDict(
    "BatchStartRecommendationsRequestRequestTypeDef",
    {
        "Data": Sequence[StartRecommendationsRequestEntryTypeDef],
    },
    total=False,
)

CancelReplicationTaskAssessmentRunResponseTypeDef = TypedDict(
    "CancelReplicationTaskAssessmentRunResponseTypeDef",
    {
        "ReplicationTaskAssessmentRun": ReplicationTaskAssessmentRunTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteReplicationTaskAssessmentRunResponseTypeDef = TypedDict(
    "DeleteReplicationTaskAssessmentRunResponseTypeDef",
    {
        "ReplicationTaskAssessmentRun": ReplicationTaskAssessmentRunTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationTaskAssessmentRunsResponseTypeDef = TypedDict(
    "DescribeReplicationTaskAssessmentRunsResponseTypeDef",
    {
        "Marker": str,
        "ReplicationTaskAssessmentRuns": List[ReplicationTaskAssessmentRunTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartReplicationTaskAssessmentRunResponseTypeDef = TypedDict(
    "StartReplicationTaskAssessmentRunResponseTypeDef",
    {
        "ReplicationTaskAssessmentRun": ReplicationTaskAssessmentRunTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateReplicationTaskResponseTypeDef = TypedDict(
    "CreateReplicationTaskResponseTypeDef",
    {
        "ReplicationTask": ReplicationTaskTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteReplicationTaskResponseTypeDef = TypedDict(
    "DeleteReplicationTaskResponseTypeDef",
    {
        "ReplicationTask": ReplicationTaskTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationTasksResponseTypeDef = TypedDict(
    "DescribeReplicationTasksResponseTypeDef",
    {
        "Marker": str,
        "ReplicationTasks": List[ReplicationTaskTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModifyReplicationTaskResponseTypeDef = TypedDict(
    "ModifyReplicationTaskResponseTypeDef",
    {
        "ReplicationTask": ReplicationTaskTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MoveReplicationTaskResponseTypeDef = TypedDict(
    "MoveReplicationTaskResponseTypeDef",
    {
        "ReplicationTask": ReplicationTaskTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartReplicationTaskAssessmentResponseTypeDef = TypedDict(
    "StartReplicationTaskAssessmentResponseTypeDef",
    {
        "ReplicationTask": ReplicationTaskTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartReplicationTaskResponseTypeDef = TypedDict(
    "StartReplicationTaskResponseTypeDef",
    {
        "ReplicationTask": ReplicationTaskTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopReplicationTaskResponseTypeDef = TypedDict(
    "StopReplicationTaskResponseTypeDef",
    {
        "ReplicationTask": ReplicationTaskTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFleetAdvisorSchemasResponseTypeDef = TypedDict(
    "DescribeFleetAdvisorSchemasResponseTypeDef",
    {
        "FleetAdvisorSchemas": List[SchemaResponseTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateReplicationSubnetGroupResponseTypeDef = TypedDict(
    "CreateReplicationSubnetGroupResponseTypeDef",
    {
        "ReplicationSubnetGroup": ReplicationSubnetGroupTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationSubnetGroupsResponseTypeDef = TypedDict(
    "DescribeReplicationSubnetGroupsResponseTypeDef",
    {
        "Marker": str,
        "ReplicationSubnetGroups": List[ReplicationSubnetGroupTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModifyReplicationSubnetGroupResponseTypeDef = TypedDict(
    "ModifyReplicationSubnetGroupResponseTypeDef",
    {
        "ReplicationSubnetGroup": ReplicationSubnetGroupTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ReplicationInstanceTypeDef = TypedDict(
    "ReplicationInstanceTypeDef",
    {
        "ReplicationInstanceIdentifier": str,
        "ReplicationInstanceClass": str,
        "ReplicationInstanceStatus": str,
        "AllocatedStorage": int,
        "InstanceCreateTime": datetime,
        "VpcSecurityGroups": List[VpcSecurityGroupMembershipTypeDef],
        "AvailabilityZone": str,
        "ReplicationSubnetGroup": ReplicationSubnetGroupTypeDef,
        "PreferredMaintenanceWindow": str,
        "PendingModifiedValues": ReplicationPendingModifiedValuesTypeDef,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AutoMinorVersionUpgrade": bool,
        "KmsKeyId": str,
        "ReplicationInstanceArn": str,
        "ReplicationInstancePublicIpAddress": str,
        "ReplicationInstancePrivateIpAddress": str,
        "ReplicationInstancePublicIpAddresses": List[str],
        "ReplicationInstancePrivateIpAddresses": List[str],
        "ReplicationInstanceIpv6Addresses": List[str],
        "PubliclyAccessible": bool,
        "SecondaryAvailabilityZone": str,
        "FreeUntil": datetime,
        "DnsNameServers": str,
        "NetworkType": str,
    },
    total=False,
)

RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "DatabaseId": str,
        "EngineName": str,
        "CreatedDate": str,
        "Status": str,
        "Preferred": bool,
        "Settings": RecommendationSettingsTypeDef,
        "Data": RecommendationDataTypeDef,
    },
    total=False,
)

CreateReplicationInstanceResponseTypeDef = TypedDict(
    "CreateReplicationInstanceResponseTypeDef",
    {
        "ReplicationInstance": ReplicationInstanceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteReplicationInstanceResponseTypeDef = TypedDict(
    "DeleteReplicationInstanceResponseTypeDef",
    {
        "ReplicationInstance": ReplicationInstanceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReplicationInstancesResponseTypeDef = TypedDict(
    "DescribeReplicationInstancesResponseTypeDef",
    {
        "Marker": str,
        "ReplicationInstances": List[ReplicationInstanceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModifyReplicationInstanceResponseTypeDef = TypedDict(
    "ModifyReplicationInstanceResponseTypeDef",
    {
        "ReplicationInstance": ReplicationInstanceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RebootReplicationInstanceResponseTypeDef = TypedDict(
    "RebootReplicationInstanceResponseTypeDef",
    {
        "ReplicationInstance": ReplicationInstanceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeRecommendationsResponseTypeDef = TypedDict(
    "DescribeRecommendationsResponseTypeDef",
    {
        "NextToken": str,
        "Recommendations": List[RecommendationTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
