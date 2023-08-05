"""
Type annotations for glue service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_glue.client import GlueClient

    session = Session()
    client: GlueClient = session.client("glue")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    CompatibilityType,
    DataFormatType,
    EnableHybridValuesType,
    ExecutionClassType,
    ExistConditionType,
    LanguageType,
    PermissionTypeType,
    ResourceShareTypeType,
    SourceControlAuthStrategyType,
    SourceControlProviderType,
    TriggerTypeType,
    WorkerTypeType,
)
from .paginator import (
    GetClassifiersPaginator,
    GetConnectionsPaginator,
    GetCrawlerMetricsPaginator,
    GetCrawlersPaginator,
    GetDatabasesPaginator,
    GetDevEndpointsPaginator,
    GetJobRunsPaginator,
    GetJobsPaginator,
    GetPartitionIndexesPaginator,
    GetPartitionsPaginator,
    GetResourcePoliciesPaginator,
    GetSecurityConfigurationsPaginator,
    GetTablesPaginator,
    GetTableVersionsPaginator,
    GetTriggersPaginator,
    GetUserDefinedFunctionsPaginator,
    ListRegistriesPaginator,
    ListSchemasPaginator,
    ListSchemaVersionsPaginator,
)
from .type_defs import (
    ActionTypeDef,
    AuditContextTypeDef,
    BatchCreatePartitionResponseTypeDef,
    BatchDeleteConnectionResponseTypeDef,
    BatchDeletePartitionResponseTypeDef,
    BatchDeleteTableResponseTypeDef,
    BatchDeleteTableVersionResponseTypeDef,
    BatchGetBlueprintsResponseTypeDef,
    BatchGetCrawlersResponseTypeDef,
    BatchGetCustomEntityTypesResponseTypeDef,
    BatchGetDataQualityResultResponseTypeDef,
    BatchGetDevEndpointsResponseTypeDef,
    BatchGetJobsResponseTypeDef,
    BatchGetPartitionResponseTypeDef,
    BatchGetTriggersResponseTypeDef,
    BatchGetWorkflowsResponseTypeDef,
    BatchStopJobRunResponseTypeDef,
    BatchUpdatePartitionRequestEntryTypeDef,
    BatchUpdatePartitionResponseTypeDef,
    CancelMLTaskRunResponseTypeDef,
    CatalogEntryTypeDef,
    CheckSchemaVersionValidityResponseTypeDef,
    CodeGenConfigurationNodeTypeDef,
    CodeGenEdgeTypeDef,
    CodeGenNodeTypeDef,
    ColumnStatisticsTypeDef,
    ConnectionInputTypeDef,
    ConnectionsListTypeDef,
    CrawlerTargetsTypeDef,
    CrawlsFilterTypeDef,
    CreateBlueprintResponseTypeDef,
    CreateCsvClassifierRequestTypeDef,
    CreateCustomEntityTypeResponseTypeDef,
    CreateDataQualityRulesetResponseTypeDef,
    CreateDevEndpointResponseTypeDef,
    CreateGrokClassifierRequestTypeDef,
    CreateJobResponseTypeDef,
    CreateJsonClassifierRequestTypeDef,
    CreateMLTransformResponseTypeDef,
    CreateRegistryResponseTypeDef,
    CreateSchemaResponseTypeDef,
    CreateScriptResponseTypeDef,
    CreateSecurityConfigurationResponseTypeDef,
    CreateSessionResponseTypeDef,
    CreateTriggerResponseTypeDef,
    CreateWorkflowResponseTypeDef,
    CreateXMLClassifierRequestTypeDef,
    DatabaseInputTypeDef,
    DataCatalogEncryptionSettingsTypeDef,
    DataQualityEvaluationRunAdditionalRunOptionsTypeDef,
    DataQualityResultFilterCriteriaTypeDef,
    DataQualityRuleRecommendationRunFilterTypeDef,
    DataQualityRulesetEvaluationRunFilterTypeDef,
    DataQualityRulesetFilterCriteriaTypeDef,
    DataQualityTargetTableTypeDef,
    DataSourceTypeDef,
    DeleteBlueprintResponseTypeDef,
    DeleteCustomEntityTypeResponseTypeDef,
    DeleteJobResponseTypeDef,
    DeleteMLTransformResponseTypeDef,
    DeleteRegistryResponseTypeDef,
    DeleteSchemaResponseTypeDef,
    DeleteSchemaVersionsResponseTypeDef,
    DeleteSessionResponseTypeDef,
    DeleteTriggerResponseTypeDef,
    DeleteWorkflowResponseTypeDef,
    DevEndpointCustomLibrariesTypeDef,
    EncryptionConfigurationTypeDef,
    EventBatchingConditionTypeDef,
    ExecutionPropertyTypeDef,
    GetBlueprintResponseTypeDef,
    GetBlueprintRunResponseTypeDef,
    GetBlueprintRunsResponseTypeDef,
    GetCatalogImportStatusResponseTypeDef,
    GetClassifierResponseTypeDef,
    GetClassifiersResponseTypeDef,
    GetColumnStatisticsForPartitionResponseTypeDef,
    GetColumnStatisticsForTableResponseTypeDef,
    GetConnectionResponseTypeDef,
    GetConnectionsFilterTypeDef,
    GetConnectionsResponseTypeDef,
    GetCrawlerMetricsResponseTypeDef,
    GetCrawlerResponseTypeDef,
    GetCrawlersResponseTypeDef,
    GetCustomEntityTypeResponseTypeDef,
    GetDatabaseResponseTypeDef,
    GetDatabasesResponseTypeDef,
    GetDataCatalogEncryptionSettingsResponseTypeDef,
    GetDataflowGraphResponseTypeDef,
    GetDataQualityResultResponseTypeDef,
    GetDataQualityRuleRecommendationRunResponseTypeDef,
    GetDataQualityRulesetEvaluationRunResponseTypeDef,
    GetDataQualityRulesetResponseTypeDef,
    GetDevEndpointResponseTypeDef,
    GetDevEndpointsResponseTypeDef,
    GetJobBookmarkResponseTypeDef,
    GetJobResponseTypeDef,
    GetJobRunResponseTypeDef,
    GetJobRunsResponseTypeDef,
    GetJobsResponseTypeDef,
    GetMappingResponseTypeDef,
    GetMLTaskRunResponseTypeDef,
    GetMLTaskRunsResponseTypeDef,
    GetMLTransformResponseTypeDef,
    GetMLTransformsResponseTypeDef,
    GetPartitionIndexesResponseTypeDef,
    GetPartitionResponseTypeDef,
    GetPartitionsResponseTypeDef,
    GetPlanResponseTypeDef,
    GetRegistryResponseTypeDef,
    GetResourcePoliciesResponseTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetSchemaByDefinitionResponseTypeDef,
    GetSchemaResponseTypeDef,
    GetSchemaVersionResponseTypeDef,
    GetSchemaVersionsDiffResponseTypeDef,
    GetSecurityConfigurationResponseTypeDef,
    GetSecurityConfigurationsResponseTypeDef,
    GetSessionResponseTypeDef,
    GetStatementResponseTypeDef,
    GetTableResponseTypeDef,
    GetTablesResponseTypeDef,
    GetTableVersionResponseTypeDef,
    GetTableVersionsResponseTypeDef,
    GetTagsResponseTypeDef,
    GetTriggerResponseTypeDef,
    GetTriggersResponseTypeDef,
    GetUnfilteredPartitionMetadataResponseTypeDef,
    GetUnfilteredPartitionsMetadataResponseTypeDef,
    GetUnfilteredTableMetadataResponseTypeDef,
    GetUserDefinedFunctionResponseTypeDef,
    GetUserDefinedFunctionsResponseTypeDef,
    GetWorkflowResponseTypeDef,
    GetWorkflowRunPropertiesResponseTypeDef,
    GetWorkflowRunResponseTypeDef,
    GetWorkflowRunsResponseTypeDef,
    GlueTableTypeDef,
    JobCommandTypeDef,
    JobUpdateTypeDef,
    LakeFormationConfigurationTypeDef,
    LineageConfigurationTypeDef,
    ListBlueprintsResponseTypeDef,
    ListCrawlersResponseTypeDef,
    ListCrawlsResponseTypeDef,
    ListCustomEntityTypesResponseTypeDef,
    ListDataQualityResultsResponseTypeDef,
    ListDataQualityRuleRecommendationRunsResponseTypeDef,
    ListDataQualityRulesetEvaluationRunsResponseTypeDef,
    ListDataQualityRulesetsResponseTypeDef,
    ListDevEndpointsResponseTypeDef,
    ListJobsResponseTypeDef,
    ListMLTransformsResponseTypeDef,
    ListRegistriesResponseTypeDef,
    ListSchemasResponseTypeDef,
    ListSchemaVersionsResponseTypeDef,
    ListSessionsResponseTypeDef,
    ListStatementsResponseTypeDef,
    ListTriggersResponseTypeDef,
    ListWorkflowsResponseTypeDef,
    LocationTypeDef,
    MappingEntryTypeDef,
    MetadataKeyValuePairTypeDef,
    NotificationPropertyTypeDef,
    PartitionIndexTypeDef,
    PartitionInputTypeDef,
    PartitionValueListTypeDef,
    PredicateTypeDef,
    PropertyPredicateTypeDef,
    PutResourcePolicyResponseTypeDef,
    PutSchemaVersionMetadataResponseTypeDef,
    QuerySchemaVersionMetadataResponseTypeDef,
    RecrawlPolicyTypeDef,
    RegisterSchemaVersionResponseTypeDef,
    RegistryIdTypeDef,
    RemoveSchemaVersionMetadataResponseTypeDef,
    ResetJobBookmarkResponseTypeDef,
    ResumeWorkflowRunResponseTypeDef,
    RunStatementResponseTypeDef,
    SchemaChangePolicyTypeDef,
    SchemaIdTypeDef,
    SchemaVersionNumberTypeDef,
    SearchTablesResponseTypeDef,
    SegmentTypeDef,
    SessionCommandTypeDef,
    SortCriterionTypeDef,
    SourceControlDetailsTypeDef,
    StartBlueprintRunResponseTypeDef,
    StartDataQualityRuleRecommendationRunResponseTypeDef,
    StartDataQualityRulesetEvaluationRunResponseTypeDef,
    StartExportLabelsTaskRunResponseTypeDef,
    StartImportLabelsTaskRunResponseTypeDef,
    StartJobRunResponseTypeDef,
    StartMLEvaluationTaskRunResponseTypeDef,
    StartMLLabelingSetGenerationTaskRunResponseTypeDef,
    StartTriggerResponseTypeDef,
    StartWorkflowRunResponseTypeDef,
    StopSessionResponseTypeDef,
    StopTriggerResponseTypeDef,
    TableInputTypeDef,
    TaskRunFilterCriteriaTypeDef,
    TaskRunSortCriteriaTypeDef,
    TransformEncryptionTypeDef,
    TransformFilterCriteriaTypeDef,
    TransformParametersTypeDef,
    TransformSortCriteriaTypeDef,
    TriggerUpdateTypeDef,
    UpdateBlueprintResponseTypeDef,
    UpdateColumnStatisticsForPartitionResponseTypeDef,
    UpdateColumnStatisticsForTableResponseTypeDef,
    UpdateCsvClassifierRequestTypeDef,
    UpdateDataQualityRulesetResponseTypeDef,
    UpdateGrokClassifierRequestTypeDef,
    UpdateJobFromSourceControlResponseTypeDef,
    UpdateJobResponseTypeDef,
    UpdateJsonClassifierRequestTypeDef,
    UpdateMLTransformResponseTypeDef,
    UpdateRegistryResponseTypeDef,
    UpdateSchemaResponseTypeDef,
    UpdateSourceControlFromJobResponseTypeDef,
    UpdateTriggerResponseTypeDef,
    UpdateWorkflowResponseTypeDef,
    UpdateXMLClassifierRequestTypeDef,
    UserDefinedFunctionInputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("GlueClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConcurrentRunsExceededException: Type[BotocoreClientError]
    ConditionCheckFailureException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    CrawlerNotRunningException: Type[BotocoreClientError]
    CrawlerRunningException: Type[BotocoreClientError]
    CrawlerStoppingException: Type[BotocoreClientError]
    EntityNotFoundException: Type[BotocoreClientError]
    FederatedResourceAlreadyExistsException: Type[BotocoreClientError]
    FederationSourceException: Type[BotocoreClientError]
    FederationSourceRetryableException: Type[BotocoreClientError]
    GlueEncryptionException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    IllegalBlueprintStateException: Type[BotocoreClientError]
    IllegalSessionStateException: Type[BotocoreClientError]
    IllegalWorkflowStateException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    MLTransformNotReadyException: Type[BotocoreClientError]
    NoScheduleException: Type[BotocoreClientError]
    OperationTimeoutException: Type[BotocoreClientError]
    PermissionTypeMismatchException: Type[BotocoreClientError]
    ResourceNotReadyException: Type[BotocoreClientError]
    ResourceNumberLimitExceededException: Type[BotocoreClientError]
    SchedulerNotRunningException: Type[BotocoreClientError]
    SchedulerRunningException: Type[BotocoreClientError]
    SchedulerTransitioningException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]
    VersionMismatchException: Type[BotocoreClientError]


class GlueClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GlueClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#exceptions)
        """

    def batch_create_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionInputList: Sequence[PartitionInputTypeDef],
        CatalogId: str = ...
    ) -> BatchCreatePartitionResponseTypeDef:
        """
        Creates one or more partitions in a batch operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_create_partition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_create_partition)
        """

    def batch_delete_connection(
        self, *, ConnectionNameList: Sequence[str], CatalogId: str = ...
    ) -> BatchDeleteConnectionResponseTypeDef:
        """
        Deletes a list of connection definitions from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_delete_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_delete_connection)
        """

    def batch_delete_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionsToDelete: Sequence[PartitionValueListTypeDef],
        CatalogId: str = ...
    ) -> BatchDeletePartitionResponseTypeDef:
        """
        Deletes one or more partitions in a batch operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_delete_partition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_delete_partition)
        """

    def batch_delete_table(
        self,
        *,
        DatabaseName: str,
        TablesToDelete: Sequence[str],
        CatalogId: str = ...,
        TransactionId: str = ...
    ) -> BatchDeleteTableResponseTypeDef:
        """
        Deletes multiple tables at once.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_delete_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_delete_table)
        """

    def batch_delete_table_version(
        self, *, DatabaseName: str, TableName: str, VersionIds: Sequence[str], CatalogId: str = ...
    ) -> BatchDeleteTableVersionResponseTypeDef:
        """
        Deletes a specified batch of versions of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_delete_table_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_delete_table_version)
        """

    def batch_get_blueprints(
        self,
        *,
        Names: Sequence[str],
        IncludeBlueprint: bool = ...,
        IncludeParameterSpec: bool = ...
    ) -> BatchGetBlueprintsResponseTypeDef:
        """
        Retrieves information about a list of blueprints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_blueprints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_get_blueprints)
        """

    def batch_get_crawlers(self, *, CrawlerNames: Sequence[str]) -> BatchGetCrawlersResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of crawler names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_crawlers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_get_crawlers)
        """

    def batch_get_custom_entity_types(
        self, *, Names: Sequence[str]
    ) -> BatchGetCustomEntityTypesResponseTypeDef:
        """
        Retrieves the details for the custom patterns specified by a list of names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_custom_entity_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_get_custom_entity_types)
        """

    def batch_get_data_quality_result(
        self, *, ResultIds: Sequence[str]
    ) -> BatchGetDataQualityResultResponseTypeDef:
        """
        Retrieves a list of data quality results for the specified result IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_data_quality_result)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_get_data_quality_result)
        """

    def batch_get_dev_endpoints(
        self, *, DevEndpointNames: Sequence[str]
    ) -> BatchGetDevEndpointsResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of development endpoint
        names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_dev_endpoints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_get_dev_endpoints)
        """

    def batch_get_jobs(self, *, JobNames: Sequence[str]) -> BatchGetJobsResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of job names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_get_jobs)
        """

    def batch_get_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionsToGet: Sequence[PartitionValueListTypeDef],
        CatalogId: str = ...
    ) -> BatchGetPartitionResponseTypeDef:
        """
        Retrieves partitions in a batch request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_partition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_get_partition)
        """

    def batch_get_triggers(self, *, TriggerNames: Sequence[str]) -> BatchGetTriggersResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of trigger names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_triggers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_get_triggers)
        """

    def batch_get_workflows(
        self, *, Names: Sequence[str], IncludeGraph: bool = ...
    ) -> BatchGetWorkflowsResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of workflow names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_workflows)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_get_workflows)
        """

    def batch_stop_job_run(
        self, *, JobName: str, JobRunIds: Sequence[str]
    ) -> BatchStopJobRunResponseTypeDef:
        """
        Stops one or more job runs for a specified job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_stop_job_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_stop_job_run)
        """

    def batch_update_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        Entries: Sequence[BatchUpdatePartitionRequestEntryTypeDef],
        CatalogId: str = ...
    ) -> BatchUpdatePartitionResponseTypeDef:
        """
        Updates one or more partitions in a batch operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_update_partition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#batch_update_partition)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#can_paginate)
        """

    def cancel_data_quality_rule_recommendation_run(self, *, RunId: str) -> Dict[str, Any]:
        """
        Cancels the specified recommendation run that was being used to generate rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.cancel_data_quality_rule_recommendation_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#cancel_data_quality_rule_recommendation_run)
        """

    def cancel_data_quality_ruleset_evaluation_run(self, *, RunId: str) -> Dict[str, Any]:
        """
        Cancels a run where a ruleset is being evaluated against a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.cancel_data_quality_ruleset_evaluation_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#cancel_data_quality_ruleset_evaluation_run)
        """

    def cancel_ml_task_run(
        self, *, TransformId: str, TaskRunId: str
    ) -> CancelMLTaskRunResponseTypeDef:
        """
        Cancels (stops) a task run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.cancel_ml_task_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#cancel_ml_task_run)
        """

    def cancel_statement(
        self, *, SessionId: str, Id: int, RequestOrigin: str = ...
    ) -> Dict[str, Any]:
        """
        Cancels the statement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.cancel_statement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#cancel_statement)
        """

    def check_schema_version_validity(
        self, *, DataFormat: DataFormatType, SchemaDefinition: str
    ) -> CheckSchemaVersionValidityResponseTypeDef:
        """
        Validates the supplied schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.check_schema_version_validity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#check_schema_version_validity)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#close)
        """

    def create_blueprint(
        self,
        *,
        Name: str,
        BlueprintLocation: str,
        Description: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateBlueprintResponseTypeDef:
        """
        Registers a blueprint with Glue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_blueprint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_blueprint)
        """

    def create_classifier(
        self,
        *,
        GrokClassifier: CreateGrokClassifierRequestTypeDef = ...,
        XMLClassifier: CreateXMLClassifierRequestTypeDef = ...,
        JsonClassifier: CreateJsonClassifierRequestTypeDef = ...,
        CsvClassifier: CreateCsvClassifierRequestTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Creates a classifier in the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_classifier)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_classifier)
        """

    def create_connection(
        self,
        *,
        ConnectionInput: ConnectionInputTypeDef,
        CatalogId: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Creates a connection definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_connection)
        """

    def create_crawler(
        self,
        *,
        Name: str,
        Role: str,
        Targets: CrawlerTargetsTypeDef,
        DatabaseName: str = ...,
        Description: str = ...,
        Schedule: str = ...,
        Classifiers: Sequence[str] = ...,
        TablePrefix: str = ...,
        SchemaChangePolicy: SchemaChangePolicyTypeDef = ...,
        RecrawlPolicy: RecrawlPolicyTypeDef = ...,
        LineageConfiguration: LineageConfigurationTypeDef = ...,
        LakeFormationConfiguration: LakeFormationConfigurationTypeDef = ...,
        Configuration: str = ...,
        CrawlerSecurityConfiguration: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Creates a new crawler with specified targets, role, configuration, and optional
        schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_crawler)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_crawler)
        """

    def create_custom_entity_type(
        self,
        *,
        Name: str,
        RegexString: str,
        ContextWords: Sequence[str] = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateCustomEntityTypeResponseTypeDef:
        """
        Creates a custom pattern that is used to detect sensitive data across the
        columns and rows of your structured data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_custom_entity_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_custom_entity_type)
        """

    def create_data_quality_ruleset(
        self,
        *,
        Name: str,
        Ruleset: str,
        Description: str = ...,
        Tags: Mapping[str, str] = ...,
        TargetTable: DataQualityTargetTableTypeDef = ...,
        ClientToken: str = ...
    ) -> CreateDataQualityRulesetResponseTypeDef:
        """
        Creates a data quality ruleset with DQDL rules applied to a specified Glue
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_data_quality_ruleset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_data_quality_ruleset)
        """

    def create_database(
        self,
        *,
        DatabaseInput: DatabaseInputTypeDef,
        CatalogId: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Creates a new database in a Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_database)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_database)
        """

    def create_dev_endpoint(
        self,
        *,
        EndpointName: str,
        RoleArn: str,
        SecurityGroupIds: Sequence[str] = ...,
        SubnetId: str = ...,
        PublicKey: str = ...,
        PublicKeys: Sequence[str] = ...,
        NumberOfNodes: int = ...,
        WorkerType: WorkerTypeType = ...,
        GlueVersion: str = ...,
        NumberOfWorkers: int = ...,
        ExtraPythonLibsS3Path: str = ...,
        ExtraJarsS3Path: str = ...,
        SecurityConfiguration: str = ...,
        Tags: Mapping[str, str] = ...,
        Arguments: Mapping[str, str] = ...
    ) -> CreateDevEndpointResponseTypeDef:
        """
        Creates a new development endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_dev_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_dev_endpoint)
        """

    def create_job(
        self,
        *,
        Name: str,
        Role: str,
        Command: JobCommandTypeDef,
        Description: str = ...,
        LogUri: str = ...,
        ExecutionProperty: ExecutionPropertyTypeDef = ...,
        DefaultArguments: Mapping[str, str] = ...,
        NonOverridableArguments: Mapping[str, str] = ...,
        Connections: ConnectionsListTypeDef = ...,
        MaxRetries: int = ...,
        AllocatedCapacity: int = ...,
        Timeout: int = ...,
        MaxCapacity: float = ...,
        SecurityConfiguration: str = ...,
        Tags: Mapping[str, str] = ...,
        NotificationProperty: NotificationPropertyTypeDef = ...,
        GlueVersion: str = ...,
        NumberOfWorkers: int = ...,
        WorkerType: WorkerTypeType = ...,
        CodeGenConfigurationNodes: Mapping[str, CodeGenConfigurationNodeTypeDef] = ...,
        ExecutionClass: ExecutionClassType = ...,
        SourceControlDetails: SourceControlDetailsTypeDef = ...
    ) -> CreateJobResponseTypeDef:
        """
        Creates a new job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_job)
        """

    def create_ml_transform(
        self,
        *,
        Name: str,
        InputRecordTables: Sequence[GlueTableTypeDef],
        Parameters: TransformParametersTypeDef,
        Role: str,
        Description: str = ...,
        GlueVersion: str = ...,
        MaxCapacity: float = ...,
        WorkerType: WorkerTypeType = ...,
        NumberOfWorkers: int = ...,
        Timeout: int = ...,
        MaxRetries: int = ...,
        Tags: Mapping[str, str] = ...,
        TransformEncryption: TransformEncryptionTypeDef = ...
    ) -> CreateMLTransformResponseTypeDef:
        """
        Creates an Glue machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_ml_transform)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_ml_transform)
        """

    def create_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionInput: PartitionInputTypeDef,
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Creates a new partition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_partition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_partition)
        """

    def create_partition_index(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionIndex: PartitionIndexTypeDef,
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Creates a specified partition index in an existing table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_partition_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_partition_index)
        """

    def create_registry(
        self, *, RegistryName: str, Description: str = ..., Tags: Mapping[str, str] = ...
    ) -> CreateRegistryResponseTypeDef:
        """
        Creates a new registry which may be used to hold a collection of schemas.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_registry)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_registry)
        """

    def create_schema(
        self,
        *,
        SchemaName: str,
        DataFormat: DataFormatType,
        RegistryId: RegistryIdTypeDef = ...,
        Compatibility: CompatibilityType = ...,
        Description: str = ...,
        Tags: Mapping[str, str] = ...,
        SchemaDefinition: str = ...
    ) -> CreateSchemaResponseTypeDef:
        """
        Creates a new schema set and registers the schema definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_schema)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_schema)
        """

    def create_script(
        self,
        *,
        DagNodes: Sequence[CodeGenNodeTypeDef] = ...,
        DagEdges: Sequence[CodeGenEdgeTypeDef] = ...,
        Language: LanguageType = ...
    ) -> CreateScriptResponseTypeDef:
        """
        Transforms a directed acyclic graph (DAG) into code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_script)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_script)
        """

    def create_security_configuration(
        self, *, Name: str, EncryptionConfiguration: EncryptionConfigurationTypeDef
    ) -> CreateSecurityConfigurationResponseTypeDef:
        """
        Creates a new security configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_security_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_security_configuration)
        """

    def create_session(
        self,
        *,
        Id: str,
        Role: str,
        Command: SessionCommandTypeDef,
        Description: str = ...,
        Timeout: int = ...,
        IdleTimeout: int = ...,
        DefaultArguments: Mapping[str, str] = ...,
        Connections: ConnectionsListTypeDef = ...,
        MaxCapacity: float = ...,
        NumberOfWorkers: int = ...,
        WorkerType: WorkerTypeType = ...,
        SecurityConfiguration: str = ...,
        GlueVersion: str = ...,
        Tags: Mapping[str, str] = ...,
        RequestOrigin: str = ...
    ) -> CreateSessionResponseTypeDef:
        """
        Creates a new session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_session)
        """

    def create_table(
        self,
        *,
        DatabaseName: str,
        TableInput: TableInputTypeDef,
        CatalogId: str = ...,
        PartitionIndexes: Sequence[PartitionIndexTypeDef] = ...,
        TransactionId: str = ...
    ) -> Dict[str, Any]:
        """
        Creates a new table definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_table)
        """

    def create_trigger(
        self,
        *,
        Name: str,
        Type: TriggerTypeType,
        Actions: Sequence[ActionTypeDef],
        WorkflowName: str = ...,
        Schedule: str = ...,
        Predicate: PredicateTypeDef = ...,
        Description: str = ...,
        StartOnCreation: bool = ...,
        Tags: Mapping[str, str] = ...,
        EventBatchingCondition: EventBatchingConditionTypeDef = ...
    ) -> CreateTriggerResponseTypeDef:
        """
        Creates a new trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_trigger)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_trigger)
        """

    def create_user_defined_function(
        self,
        *,
        DatabaseName: str,
        FunctionInput: UserDefinedFunctionInputTypeDef,
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Creates a new function definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_user_defined_function)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_user_defined_function)
        """

    def create_workflow(
        self,
        *,
        Name: str,
        Description: str = ...,
        DefaultRunProperties: Mapping[str, str] = ...,
        Tags: Mapping[str, str] = ...,
        MaxConcurrentRuns: int = ...
    ) -> CreateWorkflowResponseTypeDef:
        """
        Creates a new workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_workflow)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#create_workflow)
        """

    def delete_blueprint(self, *, Name: str) -> DeleteBlueprintResponseTypeDef:
        """
        Deletes an existing blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_blueprint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_blueprint)
        """

    def delete_classifier(self, *, Name: str) -> Dict[str, Any]:
        """
        Removes a classifier from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_classifier)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_classifier)
        """

    def delete_column_statistics_for_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionValues: Sequence[str],
        ColumnName: str,
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Delete the partition column statistics of a column.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_column_statistics_for_partition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_column_statistics_for_partition)
        """

    def delete_column_statistics_for_table(
        self, *, DatabaseName: str, TableName: str, ColumnName: str, CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Retrieves table statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_column_statistics_for_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_column_statistics_for_table)
        """

    def delete_connection(self, *, ConnectionName: str, CatalogId: str = ...) -> Dict[str, Any]:
        """
        Deletes a connection from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_connection)
        """

    def delete_crawler(self, *, Name: str) -> Dict[str, Any]:
        """
        Removes a specified crawler from the Glue Data Catalog, unless the crawler state
        is `RUNNING`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_crawler)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_crawler)
        """

    def delete_custom_entity_type(self, *, Name: str) -> DeleteCustomEntityTypeResponseTypeDef:
        """
        Deletes a custom pattern by specifying its name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_custom_entity_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_custom_entity_type)
        """

    def delete_data_quality_ruleset(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes a data quality ruleset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_data_quality_ruleset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_data_quality_ruleset)
        """

    def delete_database(self, *, Name: str, CatalogId: str = ...) -> Dict[str, Any]:
        """
        Removes a specified database from a Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_database)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_database)
        """

    def delete_dev_endpoint(self, *, EndpointName: str) -> Dict[str, Any]:
        """
        Deletes a specified development endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_dev_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_dev_endpoint)
        """

    def delete_job(self, *, JobName: str) -> DeleteJobResponseTypeDef:
        """
        Deletes a specified job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_job)
        """

    def delete_ml_transform(self, *, TransformId: str) -> DeleteMLTransformResponseTypeDef:
        """
        Deletes an Glue machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_ml_transform)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_ml_transform)
        """

    def delete_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionValues: Sequence[str],
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a specified partition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_partition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_partition)
        """

    def delete_partition_index(
        self, *, DatabaseName: str, TableName: str, IndexName: str, CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a specified partition index from an existing table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_partition_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_partition_index)
        """

    def delete_registry(self, *, RegistryId: RegistryIdTypeDef) -> DeleteRegistryResponseTypeDef:
        """
        Delete the entire registry including schema and all of its versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_registry)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_registry)
        """

    def delete_resource_policy(
        self, *, PolicyHashCondition: str = ..., ResourceArn: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_resource_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_resource_policy)
        """

    def delete_schema(self, *, SchemaId: SchemaIdTypeDef) -> DeleteSchemaResponseTypeDef:
        """
        Deletes the entire schema set, including the schema set and all of its versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_schema)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_schema)
        """

    def delete_schema_versions(
        self, *, SchemaId: SchemaIdTypeDef, Versions: str
    ) -> DeleteSchemaVersionsResponseTypeDef:
        """
        Remove versions from the specified schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_schema_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_schema_versions)
        """

    def delete_security_configuration(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes a specified security configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_security_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_security_configuration)
        """

    def delete_session(self, *, Id: str, RequestOrigin: str = ...) -> DeleteSessionResponseTypeDef:
        """
        Deletes the session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_session)
        """

    def delete_table(
        self, *, DatabaseName: str, Name: str, CatalogId: str = ..., TransactionId: str = ...
    ) -> Dict[str, Any]:
        """
        Removes a table definition from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_table)
        """

    def delete_table_version(
        self, *, DatabaseName: str, TableName: str, VersionId: str, CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a specified version of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_table_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_table_version)
        """

    def delete_trigger(self, *, Name: str) -> DeleteTriggerResponseTypeDef:
        """
        Deletes a specified trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_trigger)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_trigger)
        """

    def delete_user_defined_function(
        self, *, DatabaseName: str, FunctionName: str, CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes an existing function definition from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_user_defined_function)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_user_defined_function)
        """

    def delete_workflow(self, *, Name: str) -> DeleteWorkflowResponseTypeDef:
        """
        Deletes a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_workflow)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#delete_workflow)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#generate_presigned_url)
        """

    def get_blueprint(
        self, *, Name: str, IncludeBlueprint: bool = ..., IncludeParameterSpec: bool = ...
    ) -> GetBlueprintResponseTypeDef:
        """
        Retrieves the details of a blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_blueprint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_blueprint)
        """

    def get_blueprint_run(
        self, *, BlueprintName: str, RunId: str
    ) -> GetBlueprintRunResponseTypeDef:
        """
        Retrieves the details of a blueprint run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_blueprint_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_blueprint_run)
        """

    def get_blueprint_runs(
        self, *, BlueprintName: str, NextToken: str = ..., MaxResults: int = ...
    ) -> GetBlueprintRunsResponseTypeDef:
        """
        Retrieves the details of blueprint runs for a specified blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_blueprint_runs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_blueprint_runs)
        """

    def get_catalog_import_status(
        self, *, CatalogId: str = ...
    ) -> GetCatalogImportStatusResponseTypeDef:
        """
        Retrieves the status of a migration operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_catalog_import_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_catalog_import_status)
        """

    def get_classifier(self, *, Name: str) -> GetClassifierResponseTypeDef:
        """
        Retrieve a classifier by name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_classifier)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_classifier)
        """

    def get_classifiers(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> GetClassifiersResponseTypeDef:
        """
        Lists all classifier objects in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_classifiers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_classifiers)
        """

    def get_column_statistics_for_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionValues: Sequence[str],
        ColumnNames: Sequence[str],
        CatalogId: str = ...
    ) -> GetColumnStatisticsForPartitionResponseTypeDef:
        """
        Retrieves partition statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_column_statistics_for_partition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_column_statistics_for_partition)
        """

    def get_column_statistics_for_table(
        self, *, DatabaseName: str, TableName: str, ColumnNames: Sequence[str], CatalogId: str = ...
    ) -> GetColumnStatisticsForTableResponseTypeDef:
        """
        Retrieves table statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_column_statistics_for_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_column_statistics_for_table)
        """

    def get_connection(
        self, *, Name: str, CatalogId: str = ..., HidePassword: bool = ...
    ) -> GetConnectionResponseTypeDef:
        """
        Retrieves a connection definition from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_connection)
        """

    def get_connections(
        self,
        *,
        CatalogId: str = ...,
        Filter: GetConnectionsFilterTypeDef = ...,
        HidePassword: bool = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> GetConnectionsResponseTypeDef:
        """
        Retrieves a list of connection definitions from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_connections)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_connections)
        """

    def get_crawler(self, *, Name: str) -> GetCrawlerResponseTypeDef:
        """
        Retrieves metadata for a specified crawler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_crawler)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_crawler)
        """

    def get_crawler_metrics(
        self, *, CrawlerNameList: Sequence[str] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> GetCrawlerMetricsResponseTypeDef:
        """
        Retrieves metrics about specified crawlers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_crawler_metrics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_crawler_metrics)
        """

    def get_crawlers(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> GetCrawlersResponseTypeDef:
        """
        Retrieves metadata for all crawlers defined in the customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_crawlers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_crawlers)
        """

    def get_custom_entity_type(self, *, Name: str) -> GetCustomEntityTypeResponseTypeDef:
        """
        Retrieves the details of a custom pattern by specifying its name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_custom_entity_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_custom_entity_type)
        """

    def get_data_catalog_encryption_settings(
        self, *, CatalogId: str = ...
    ) -> GetDataCatalogEncryptionSettingsResponseTypeDef:
        """
        Retrieves the security configuration for a specified catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_data_catalog_encryption_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_data_catalog_encryption_settings)
        """

    def get_data_quality_result(self, *, ResultId: str) -> GetDataQualityResultResponseTypeDef:
        """
        Retrieves the result of a data quality rule evaluation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_data_quality_result)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_data_quality_result)
        """

    def get_data_quality_rule_recommendation_run(
        self, *, RunId: str
    ) -> GetDataQualityRuleRecommendationRunResponseTypeDef:
        """
        Gets the specified recommendation run that was used to generate rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_data_quality_rule_recommendation_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_data_quality_rule_recommendation_run)
        """

    def get_data_quality_ruleset(self, *, Name: str) -> GetDataQualityRulesetResponseTypeDef:
        """
        Returns an existing ruleset by identifier or name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_data_quality_ruleset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_data_quality_ruleset)
        """

    def get_data_quality_ruleset_evaluation_run(
        self, *, RunId: str
    ) -> GetDataQualityRulesetEvaluationRunResponseTypeDef:
        """
        Retrieves a specific run where a ruleset is evaluated against a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_data_quality_ruleset_evaluation_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_data_quality_ruleset_evaluation_run)
        """

    def get_database(self, *, Name: str, CatalogId: str = ...) -> GetDatabaseResponseTypeDef:
        """
        Retrieves the definition of a specified database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_database)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_database)
        """

    def get_databases(
        self,
        *,
        CatalogId: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        ResourceShareType: ResourceShareTypeType = ...
    ) -> GetDatabasesResponseTypeDef:
        """
        Retrieves all databases defined in a given Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_databases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_databases)
        """

    def get_dataflow_graph(self, *, PythonScript: str = ...) -> GetDataflowGraphResponseTypeDef:
        """
        Transforms a Python script into a directed acyclic graph (DAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_dataflow_graph)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_dataflow_graph)
        """

    def get_dev_endpoint(self, *, EndpointName: str) -> GetDevEndpointResponseTypeDef:
        """
        Retrieves information about a specified development endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_dev_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_dev_endpoint)
        """

    def get_dev_endpoints(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> GetDevEndpointsResponseTypeDef:
        """
        Retrieves all the development endpoints in this Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_dev_endpoints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_dev_endpoints)
        """

    def get_job(self, *, JobName: str) -> GetJobResponseTypeDef:
        """
        Retrieves an existing job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_job)
        """

    def get_job_bookmark(self, *, JobName: str, RunId: str = ...) -> GetJobBookmarkResponseTypeDef:
        """
        Returns information on a job bookmark entry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_job_bookmark)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_job_bookmark)
        """

    def get_job_run(
        self, *, JobName: str, RunId: str, PredecessorsIncluded: bool = ...
    ) -> GetJobRunResponseTypeDef:
        """
        Retrieves the metadata for a given job run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_job_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_job_run)
        """

    def get_job_runs(
        self, *, JobName: str, NextToken: str = ..., MaxResults: int = ...
    ) -> GetJobRunsResponseTypeDef:
        """
        Retrieves metadata for all runs of a given job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_job_runs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_job_runs)
        """

    def get_jobs(self, *, NextToken: str = ..., MaxResults: int = ...) -> GetJobsResponseTypeDef:
        """
        Retrieves all current job definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_jobs)
        """

    def get_mapping(
        self,
        *,
        Source: CatalogEntryTypeDef,
        Sinks: Sequence[CatalogEntryTypeDef] = ...,
        Location: LocationTypeDef = ...
    ) -> GetMappingResponseTypeDef:
        """
        Creates mappings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_mapping)
        """

    def get_ml_task_run(self, *, TransformId: str, TaskRunId: str) -> GetMLTaskRunResponseTypeDef:
        """
        Gets details for a specific task run on a machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_ml_task_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_ml_task_run)
        """

    def get_ml_task_runs(
        self,
        *,
        TransformId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filter: TaskRunFilterCriteriaTypeDef = ...,
        Sort: TaskRunSortCriteriaTypeDef = ...
    ) -> GetMLTaskRunsResponseTypeDef:
        """
        Gets a list of runs for a machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_ml_task_runs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_ml_task_runs)
        """

    def get_ml_transform(self, *, TransformId: str) -> GetMLTransformResponseTypeDef:
        """
        Gets an Glue machine learning transform artifact and all its corresponding
        metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_ml_transform)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_ml_transform)
        """

    def get_ml_transforms(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filter: TransformFilterCriteriaTypeDef = ...,
        Sort: TransformSortCriteriaTypeDef = ...
    ) -> GetMLTransformsResponseTypeDef:
        """
        Gets a sortable, filterable list of existing Glue machine learning transforms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_ml_transforms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_ml_transforms)
        """

    def get_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionValues: Sequence[str],
        CatalogId: str = ...
    ) -> GetPartitionResponseTypeDef:
        """
        Retrieves information about a specified partition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_partition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_partition)
        """

    def get_partition_indexes(
        self, *, DatabaseName: str, TableName: str, CatalogId: str = ..., NextToken: str = ...
    ) -> GetPartitionIndexesResponseTypeDef:
        """
        Retrieves the partition indexes associated with a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_partition_indexes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_partition_indexes)
        """

    def get_partitions(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        CatalogId: str = ...,
        Expression: str = ...,
        NextToken: str = ...,
        Segment: SegmentTypeDef = ...,
        MaxResults: int = ...,
        ExcludeColumnSchema: bool = ...,
        TransactionId: str = ...,
        QueryAsOfTime: Union[datetime, str] = ...
    ) -> GetPartitionsResponseTypeDef:
        """
        Retrieves information about the partitions in a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_partitions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_partitions)
        """

    def get_plan(
        self,
        *,
        Mapping: Sequence[MappingEntryTypeDef],
        Source: CatalogEntryTypeDef,
        Sinks: Sequence[CatalogEntryTypeDef] = ...,
        Location: LocationTypeDef = ...,
        Language: LanguageType = ...,
        AdditionalPlanOptionsMap: Mapping[str, str] = ...
    ) -> GetPlanResponseTypeDef:
        """
        Gets code to perform a specified mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_plan)
        """

    def get_registry(self, *, RegistryId: RegistryIdTypeDef) -> GetRegistryResponseTypeDef:
        """
        Describes the specified registry in detail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_registry)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_registry)
        """

    def get_resource_policies(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> GetResourcePoliciesResponseTypeDef:
        """
        Retrieves the resource policies set on individual resources by Resource Access
        Manager during cross-account permission grants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_resource_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_resource_policies)
        """

    def get_resource_policy(self, *, ResourceArn: str = ...) -> GetResourcePolicyResponseTypeDef:
        """
        Retrieves a specified resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_resource_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_resource_policy)
        """

    def get_schema(self, *, SchemaId: SchemaIdTypeDef) -> GetSchemaResponseTypeDef:
        """
        Describes the specified schema in detail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_schema)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_schema)
        """

    def get_schema_by_definition(
        self, *, SchemaId: SchemaIdTypeDef, SchemaDefinition: str
    ) -> GetSchemaByDefinitionResponseTypeDef:
        """
        Retrieves a schema by the `SchemaDefinition`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_schema_by_definition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_schema_by_definition)
        """

    def get_schema_version(
        self,
        *,
        SchemaId: SchemaIdTypeDef = ...,
        SchemaVersionId: str = ...,
        SchemaVersionNumber: SchemaVersionNumberTypeDef = ...
    ) -> GetSchemaVersionResponseTypeDef:
        """
        Get the specified schema by its unique ID assigned when a version of the schema
        is created or registered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_schema_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_schema_version)
        """

    def get_schema_versions_diff(
        self,
        *,
        SchemaId: SchemaIdTypeDef,
        FirstSchemaVersionNumber: SchemaVersionNumberTypeDef,
        SecondSchemaVersionNumber: SchemaVersionNumberTypeDef,
        SchemaDiffType: Literal["SYNTAX_DIFF"]
    ) -> GetSchemaVersionsDiffResponseTypeDef:
        """
        Fetches the schema version difference in the specified difference type between
        two stored schema versions in the Schema Registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_schema_versions_diff)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_schema_versions_diff)
        """

    def get_security_configuration(self, *, Name: str) -> GetSecurityConfigurationResponseTypeDef:
        """
        Retrieves a specified security configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_security_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_security_configuration)
        """

    def get_security_configurations(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> GetSecurityConfigurationsResponseTypeDef:
        """
        Retrieves a list of all security configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_security_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_security_configurations)
        """

    def get_session(self, *, Id: str, RequestOrigin: str = ...) -> GetSessionResponseTypeDef:
        """
        Retrieves the session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_session)
        """

    def get_statement(
        self, *, SessionId: str, Id: int, RequestOrigin: str = ...
    ) -> GetStatementResponseTypeDef:
        """
        Retrieves the statement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_statement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_statement)
        """

    def get_table(
        self,
        *,
        DatabaseName: str,
        Name: str,
        CatalogId: str = ...,
        TransactionId: str = ...,
        QueryAsOfTime: Union[datetime, str] = ...
    ) -> GetTableResponseTypeDef:
        """
        Retrieves the `Table` definition in a Data Catalog for a specified table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_table)
        """

    def get_table_version(
        self, *, DatabaseName: str, TableName: str, CatalogId: str = ..., VersionId: str = ...
    ) -> GetTableVersionResponseTypeDef:
        """
        Retrieves a specified version of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_table_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_table_version)
        """

    def get_table_versions(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        CatalogId: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> GetTableVersionsResponseTypeDef:
        """
        Retrieves a list of strings that identify available versions of a specified
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_table_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_table_versions)
        """

    def get_tables(
        self,
        *,
        DatabaseName: str,
        CatalogId: str = ...,
        Expression: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        TransactionId: str = ...,
        QueryAsOfTime: Union[datetime, str] = ...
    ) -> GetTablesResponseTypeDef:
        """
        Retrieves the definitions of some or all of the tables in a given `Database`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_tables)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_tables)
        """

    def get_tags(self, *, ResourceArn: str) -> GetTagsResponseTypeDef:
        """
        Retrieves a list of tags associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_tags)
        """

    def get_trigger(self, *, Name: str) -> GetTriggerResponseTypeDef:
        """
        Retrieves the definition of a trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_trigger)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_trigger)
        """

    def get_triggers(
        self, *, NextToken: str = ..., DependentJobName: str = ..., MaxResults: int = ...
    ) -> GetTriggersResponseTypeDef:
        """
        Gets all the triggers associated with a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_triggers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_triggers)
        """

    def get_unfiltered_partition_metadata(
        self,
        *,
        CatalogId: str,
        DatabaseName: str,
        TableName: str,
        PartitionValues: Sequence[str],
        SupportedPermissionTypes: Sequence[PermissionTypeType],
        AuditContext: AuditContextTypeDef = ...
    ) -> GetUnfilteredPartitionMetadataResponseTypeDef:
        """
        Retrieves partition metadata from the Data Catalog that contains unfiltered
        metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_unfiltered_partition_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_unfiltered_partition_metadata)
        """

    def get_unfiltered_partitions_metadata(
        self,
        *,
        CatalogId: str,
        DatabaseName: str,
        TableName: str,
        SupportedPermissionTypes: Sequence[PermissionTypeType],
        Expression: str = ...,
        AuditContext: AuditContextTypeDef = ...,
        NextToken: str = ...,
        Segment: SegmentTypeDef = ...,
        MaxResults: int = ...
    ) -> GetUnfilteredPartitionsMetadataResponseTypeDef:
        """
        Retrieves partition metadata from the Data Catalog that contains unfiltered
        metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_unfiltered_partitions_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_unfiltered_partitions_metadata)
        """

    def get_unfiltered_table_metadata(
        self,
        *,
        CatalogId: str,
        DatabaseName: str,
        Name: str,
        SupportedPermissionTypes: Sequence[PermissionTypeType],
        AuditContext: AuditContextTypeDef = ...
    ) -> GetUnfilteredTableMetadataResponseTypeDef:
        """
        Retrieves table metadata from the Data Catalog that contains unfiltered
        metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_unfiltered_table_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_unfiltered_table_metadata)
        """

    def get_user_defined_function(
        self, *, DatabaseName: str, FunctionName: str, CatalogId: str = ...
    ) -> GetUserDefinedFunctionResponseTypeDef:
        """
        Retrieves a specified function definition from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_user_defined_function)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_user_defined_function)
        """

    def get_user_defined_functions(
        self,
        *,
        Pattern: str,
        CatalogId: str = ...,
        DatabaseName: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> GetUserDefinedFunctionsResponseTypeDef:
        """
        Retrieves multiple function definitions from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_user_defined_functions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_user_defined_functions)
        """

    def get_workflow(self, *, Name: str, IncludeGraph: bool = ...) -> GetWorkflowResponseTypeDef:
        """
        Retrieves resource metadata for a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_workflow)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_workflow)
        """

    def get_workflow_run(
        self, *, Name: str, RunId: str, IncludeGraph: bool = ...
    ) -> GetWorkflowRunResponseTypeDef:
        """
        Retrieves the metadata for a given workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_workflow_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_workflow_run)
        """

    def get_workflow_run_properties(
        self, *, Name: str, RunId: str
    ) -> GetWorkflowRunPropertiesResponseTypeDef:
        """
        Retrieves the workflow run properties which were set during the run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_workflow_run_properties)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_workflow_run_properties)
        """

    def get_workflow_runs(
        self, *, Name: str, IncludeGraph: bool = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> GetWorkflowRunsResponseTypeDef:
        """
        Retrieves metadata for all runs of a given workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_workflow_runs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_workflow_runs)
        """

    def import_catalog_to_glue(self, *, CatalogId: str = ...) -> Dict[str, Any]:
        """
        Imports an existing Amazon Athena Data Catalog to Glue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.import_catalog_to_glue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#import_catalog_to_glue)
        """

    def list_blueprints(
        self, *, NextToken: str = ..., MaxResults: int = ..., Tags: Mapping[str, str] = ...
    ) -> ListBlueprintsResponseTypeDef:
        """
        Lists all the blueprint names in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_blueprints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_blueprints)
        """

    def list_crawlers(
        self, *, MaxResults: int = ..., NextToken: str = ..., Tags: Mapping[str, str] = ...
    ) -> ListCrawlersResponseTypeDef:
        """
        Retrieves the names of all crawler resources in this Amazon Web Services
        account, or the resources with the specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_crawlers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_crawlers)
        """

    def list_crawls(
        self,
        *,
        CrawlerName: str,
        MaxResults: int = ...,
        Filters: Sequence[CrawlsFilterTypeDef] = ...,
        NextToken: str = ...
    ) -> ListCrawlsResponseTypeDef:
        """
        Returns all the crawls of a specified crawler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_crawls)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_crawls)
        """

    def list_custom_entity_types(
        self, *, NextToken: str = ..., MaxResults: int = ..., Tags: Mapping[str, str] = ...
    ) -> ListCustomEntityTypesResponseTypeDef:
        """
        Lists all the custom patterns that have been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_custom_entity_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_custom_entity_types)
        """

    def list_data_quality_results(
        self,
        *,
        Filter: DataQualityResultFilterCriteriaTypeDef = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListDataQualityResultsResponseTypeDef:
        """
        Returns all data quality execution results for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_data_quality_results)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_data_quality_results)
        """

    def list_data_quality_rule_recommendation_runs(
        self,
        *,
        Filter: DataQualityRuleRecommendationRunFilterTypeDef = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListDataQualityRuleRecommendationRunsResponseTypeDef:
        """
        Lists the recommendation runs meeting the filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_data_quality_rule_recommendation_runs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_data_quality_rule_recommendation_runs)
        """

    def list_data_quality_ruleset_evaluation_runs(
        self,
        *,
        Filter: DataQualityRulesetEvaluationRunFilterTypeDef = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListDataQualityRulesetEvaluationRunsResponseTypeDef:
        """
        Lists all the runs meeting the filter criteria, where a ruleset is evaluated
        against a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_data_quality_ruleset_evaluation_runs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_data_quality_ruleset_evaluation_runs)
        """

    def list_data_quality_rulesets(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filter: DataQualityRulesetFilterCriteriaTypeDef = ...,
        Tags: Mapping[str, str] = ...
    ) -> ListDataQualityRulesetsResponseTypeDef:
        """
        Returns a paginated list of rulesets for the specified list of Glue tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_data_quality_rulesets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_data_quality_rulesets)
        """

    def list_dev_endpoints(
        self, *, NextToken: str = ..., MaxResults: int = ..., Tags: Mapping[str, str] = ...
    ) -> ListDevEndpointsResponseTypeDef:
        """
        Retrieves the names of all `DevEndpoint` resources in this Amazon Web Services
        account, or the resources with the specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_dev_endpoints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_dev_endpoints)
        """

    def list_jobs(
        self, *, NextToken: str = ..., MaxResults: int = ..., Tags: Mapping[str, str] = ...
    ) -> ListJobsResponseTypeDef:
        """
        Retrieves the names of all job resources in this Amazon Web Services account, or
        the resources with the specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_jobs)
        """

    def list_ml_transforms(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filter: TransformFilterCriteriaTypeDef = ...,
        Sort: TransformSortCriteriaTypeDef = ...,
        Tags: Mapping[str, str] = ...
    ) -> ListMLTransformsResponseTypeDef:
        """
        Retrieves a sortable, filterable list of existing Glue machine learning
        transforms in this Amazon Web Services account, or the resources with the
        specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_ml_transforms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_ml_transforms)
        """

    def list_registries(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListRegistriesResponseTypeDef:
        """
        Returns a list of registries that you have created, with minimal registry
        information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_registries)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_registries)
        """

    def list_schema_versions(
        self, *, SchemaId: SchemaIdTypeDef, MaxResults: int = ..., NextToken: str = ...
    ) -> ListSchemaVersionsResponseTypeDef:
        """
        Returns a list of schema versions that you have created, with minimal
        information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_schema_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_schema_versions)
        """

    def list_schemas(
        self, *, RegistryId: RegistryIdTypeDef = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListSchemasResponseTypeDef:
        """
        Returns a list of schemas with minimal details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_schemas)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_schemas)
        """

    def list_sessions(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Tags: Mapping[str, str] = ...,
        RequestOrigin: str = ...
    ) -> ListSessionsResponseTypeDef:
        """
        Retrieve a list of sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_sessions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_sessions)
        """

    def list_statements(
        self, *, SessionId: str, RequestOrigin: str = ..., NextToken: str = ...
    ) -> ListStatementsResponseTypeDef:
        """
        Lists statements for the session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_statements)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_statements)
        """

    def list_triggers(
        self,
        *,
        NextToken: str = ...,
        DependentJobName: str = ...,
        MaxResults: int = ...,
        Tags: Mapping[str, str] = ...
    ) -> ListTriggersResponseTypeDef:
        """
        Retrieves the names of all trigger resources in this Amazon Web Services
        account, or the resources with the specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_triggers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_triggers)
        """

    def list_workflows(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListWorkflowsResponseTypeDef:
        """
        Lists names of workflows created in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_workflows)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#list_workflows)
        """

    def put_data_catalog_encryption_settings(
        self,
        *,
        DataCatalogEncryptionSettings: DataCatalogEncryptionSettingsTypeDef,
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Sets the security configuration for a specified catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.put_data_catalog_encryption_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#put_data_catalog_encryption_settings)
        """

    def put_resource_policy(
        self,
        *,
        PolicyInJson: str,
        ResourceArn: str = ...,
        PolicyHashCondition: str = ...,
        PolicyExistsCondition: ExistConditionType = ...,
        EnableHybrid: EnableHybridValuesType = ...
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Sets the Data Catalog resource policy for access control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.put_resource_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#put_resource_policy)
        """

    def put_schema_version_metadata(
        self,
        *,
        MetadataKeyValue: MetadataKeyValuePairTypeDef,
        SchemaId: SchemaIdTypeDef = ...,
        SchemaVersionNumber: SchemaVersionNumberTypeDef = ...,
        SchemaVersionId: str = ...
    ) -> PutSchemaVersionMetadataResponseTypeDef:
        """
        Puts the metadata key value pair for a specified schema version ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.put_schema_version_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#put_schema_version_metadata)
        """

    def put_workflow_run_properties(
        self, *, Name: str, RunId: str, RunProperties: Mapping[str, str]
    ) -> Dict[str, Any]:
        """
        Puts the specified workflow run properties for the given workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.put_workflow_run_properties)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#put_workflow_run_properties)
        """

    def query_schema_version_metadata(
        self,
        *,
        SchemaId: SchemaIdTypeDef = ...,
        SchemaVersionNumber: SchemaVersionNumberTypeDef = ...,
        SchemaVersionId: str = ...,
        MetadataList: Sequence[MetadataKeyValuePairTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> QuerySchemaVersionMetadataResponseTypeDef:
        """
        Queries for the schema version metadata information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.query_schema_version_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#query_schema_version_metadata)
        """

    def register_schema_version(
        self, *, SchemaId: SchemaIdTypeDef, SchemaDefinition: str
    ) -> RegisterSchemaVersionResponseTypeDef:
        """
        Adds a new version to the existing schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.register_schema_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#register_schema_version)
        """

    def remove_schema_version_metadata(
        self,
        *,
        MetadataKeyValue: MetadataKeyValuePairTypeDef,
        SchemaId: SchemaIdTypeDef = ...,
        SchemaVersionNumber: SchemaVersionNumberTypeDef = ...,
        SchemaVersionId: str = ...
    ) -> RemoveSchemaVersionMetadataResponseTypeDef:
        """
        Removes a key value pair from the schema version metadata for the specified
        schema version ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.remove_schema_version_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#remove_schema_version_metadata)
        """

    def reset_job_bookmark(
        self, *, JobName: str, RunId: str = ...
    ) -> ResetJobBookmarkResponseTypeDef:
        """
        Resets a bookmark entry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.reset_job_bookmark)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#reset_job_bookmark)
        """

    def resume_workflow_run(
        self, *, Name: str, RunId: str, NodeIds: Sequence[str]
    ) -> ResumeWorkflowRunResponseTypeDef:
        """
        Restarts selected nodes of a previous partially completed workflow run and
        resumes the workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.resume_workflow_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#resume_workflow_run)
        """

    def run_statement(
        self, *, SessionId: str, Code: str, RequestOrigin: str = ...
    ) -> RunStatementResponseTypeDef:
        """
        Executes the statement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.run_statement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#run_statement)
        """

    def search_tables(
        self,
        *,
        CatalogId: str = ...,
        NextToken: str = ...,
        Filters: Sequence[PropertyPredicateTypeDef] = ...,
        SearchText: str = ...,
        SortCriteria: Sequence[SortCriterionTypeDef] = ...,
        MaxResults: int = ...,
        ResourceShareType: ResourceShareTypeType = ...
    ) -> SearchTablesResponseTypeDef:
        """
        Searches a set of tables based on properties in the table metadata as well as on
        the parent database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.search_tables)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#search_tables)
        """

    def start_blueprint_run(
        self, *, BlueprintName: str, RoleArn: str, Parameters: str = ...
    ) -> StartBlueprintRunResponseTypeDef:
        """
        Starts a new run of the specified blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_blueprint_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#start_blueprint_run)
        """

    def start_crawler(self, *, Name: str) -> Dict[str, Any]:
        """
        Starts a crawl using the specified crawler, regardless of what is scheduled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_crawler)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#start_crawler)
        """

    def start_crawler_schedule(self, *, CrawlerName: str) -> Dict[str, Any]:
        """
        Changes the schedule state of the specified crawler to `SCHEDULED`, unless the
        crawler is already running or the schedule state is already `SCHEDULED`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_crawler_schedule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#start_crawler_schedule)
        """

    def start_data_quality_rule_recommendation_run(
        self,
        *,
        DataSource: DataSourceTypeDef,
        Role: str,
        NumberOfWorkers: int = ...,
        Timeout: int = ...,
        CreatedRulesetName: str = ...,
        ClientToken: str = ...
    ) -> StartDataQualityRuleRecommendationRunResponseTypeDef:
        """
        Starts a recommendation run that is used to generate rules when you don't know
        what rules to write.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_data_quality_rule_recommendation_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#start_data_quality_rule_recommendation_run)
        """

    def start_data_quality_ruleset_evaluation_run(
        self,
        *,
        DataSource: DataSourceTypeDef,
        Role: str,
        RulesetNames: Sequence[str],
        NumberOfWorkers: int = ...,
        Timeout: int = ...,
        ClientToken: str = ...,
        AdditionalRunOptions: DataQualityEvaluationRunAdditionalRunOptionsTypeDef = ...,
        AdditionalDataSources: Mapping[str, DataSourceTypeDef] = ...
    ) -> StartDataQualityRulesetEvaluationRunResponseTypeDef:
        """
        Once you have a ruleset definition (either recommended or your own), you call
        this operation to evaluate the ruleset against a data source (Glue table).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_data_quality_ruleset_evaluation_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#start_data_quality_ruleset_evaluation_run)
        """

    def start_export_labels_task_run(
        self, *, TransformId: str, OutputS3Path: str
    ) -> StartExportLabelsTaskRunResponseTypeDef:
        """
        Begins an asynchronous task to export all labeled data for a particular
        transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_export_labels_task_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#start_export_labels_task_run)
        """

    def start_import_labels_task_run(
        self, *, TransformId: str, InputS3Path: str, ReplaceAllLabels: bool = ...
    ) -> StartImportLabelsTaskRunResponseTypeDef:
        """
        Enables you to provide additional labels (examples of truth) to be used to teach
        the machine learning transform and improve its quality.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_import_labels_task_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#start_import_labels_task_run)
        """

    def start_job_run(
        self,
        *,
        JobName: str,
        JobRunId: str = ...,
        Arguments: Mapping[str, str] = ...,
        AllocatedCapacity: int = ...,
        Timeout: int = ...,
        MaxCapacity: float = ...,
        SecurityConfiguration: str = ...,
        NotificationProperty: NotificationPropertyTypeDef = ...,
        WorkerType: WorkerTypeType = ...,
        NumberOfWorkers: int = ...,
        ExecutionClass: ExecutionClassType = ...
    ) -> StartJobRunResponseTypeDef:
        """
        Starts a job run using a job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_job_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#start_job_run)
        """

    def start_ml_evaluation_task_run(
        self, *, TransformId: str
    ) -> StartMLEvaluationTaskRunResponseTypeDef:
        """
        Starts a task to estimate the quality of the transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_ml_evaluation_task_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#start_ml_evaluation_task_run)
        """

    def start_ml_labeling_set_generation_task_run(
        self, *, TransformId: str, OutputS3Path: str
    ) -> StartMLLabelingSetGenerationTaskRunResponseTypeDef:
        """
        Starts the active learning workflow for your machine learning transform to
        improve the transform's quality by generating label sets and adding labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_ml_labeling_set_generation_task_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#start_ml_labeling_set_generation_task_run)
        """

    def start_trigger(self, *, Name: str) -> StartTriggerResponseTypeDef:
        """
        Starts an existing trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_trigger)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#start_trigger)
        """

    def start_workflow_run(
        self, *, Name: str, RunProperties: Mapping[str, str] = ...
    ) -> StartWorkflowRunResponseTypeDef:
        """
        Starts a new run of the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_workflow_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#start_workflow_run)
        """

    def stop_crawler(self, *, Name: str) -> Dict[str, Any]:
        """
        If the specified crawler is running, stops the crawl.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.stop_crawler)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#stop_crawler)
        """

    def stop_crawler_schedule(self, *, CrawlerName: str) -> Dict[str, Any]:
        """
        Sets the schedule state of the specified crawler to `NOT_SCHEDULED`, but does
        not stop the crawler if it is already running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.stop_crawler_schedule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#stop_crawler_schedule)
        """

    def stop_session(self, *, Id: str, RequestOrigin: str = ...) -> StopSessionResponseTypeDef:
        """
        Stops the session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.stop_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#stop_session)
        """

    def stop_trigger(self, *, Name: str) -> StopTriggerResponseTypeDef:
        """
        Stops a specified trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.stop_trigger)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#stop_trigger)
        """

    def stop_workflow_run(self, *, Name: str, RunId: str) -> Dict[str, Any]:
        """
        Stops the execution of the specified workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.stop_workflow_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#stop_workflow_run)
        """

    def tag_resource(self, *, ResourceArn: str, TagsToAdd: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, TagsToRemove: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#untag_resource)
        """

    def update_blueprint(
        self, *, Name: str, BlueprintLocation: str, Description: str = ...
    ) -> UpdateBlueprintResponseTypeDef:
        """
        Updates a registered blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_blueprint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_blueprint)
        """

    def update_classifier(
        self,
        *,
        GrokClassifier: UpdateGrokClassifierRequestTypeDef = ...,
        XMLClassifier: UpdateXMLClassifierRequestTypeDef = ...,
        JsonClassifier: UpdateJsonClassifierRequestTypeDef = ...,
        CsvClassifier: UpdateCsvClassifierRequestTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Modifies an existing classifier (a `GrokClassifier`, an `XMLClassifier`, a
        `JsonClassifier`, or a `CsvClassifier`, depending on which field is present).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_classifier)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_classifier)
        """

    def update_column_statistics_for_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionValues: Sequence[str],
        ColumnStatisticsList: Sequence[ColumnStatisticsTypeDef],
        CatalogId: str = ...
    ) -> UpdateColumnStatisticsForPartitionResponseTypeDef:
        """
        Creates or updates partition statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_column_statistics_for_partition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_column_statistics_for_partition)
        """

    def update_column_statistics_for_table(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        ColumnStatisticsList: Sequence[ColumnStatisticsTypeDef],
        CatalogId: str = ...
    ) -> UpdateColumnStatisticsForTableResponseTypeDef:
        """
        Creates or updates table statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_column_statistics_for_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_column_statistics_for_table)
        """

    def update_connection(
        self, *, Name: str, ConnectionInput: ConnectionInputTypeDef, CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a connection definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_connection)
        """

    def update_crawler(
        self,
        *,
        Name: str,
        Role: str = ...,
        DatabaseName: str = ...,
        Description: str = ...,
        Targets: CrawlerTargetsTypeDef = ...,
        Schedule: str = ...,
        Classifiers: Sequence[str] = ...,
        TablePrefix: str = ...,
        SchemaChangePolicy: SchemaChangePolicyTypeDef = ...,
        RecrawlPolicy: RecrawlPolicyTypeDef = ...,
        LineageConfiguration: LineageConfigurationTypeDef = ...,
        LakeFormationConfiguration: LakeFormationConfigurationTypeDef = ...,
        Configuration: str = ...,
        CrawlerSecurityConfiguration: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a crawler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_crawler)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_crawler)
        """

    def update_crawler_schedule(self, *, CrawlerName: str, Schedule: str = ...) -> Dict[str, Any]:
        """
        Updates the schedule of a crawler using a `cron` expression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_crawler_schedule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_crawler_schedule)
        """

    def update_data_quality_ruleset(
        self, *, Name: str, Description: str = ..., Ruleset: str = ...
    ) -> UpdateDataQualityRulesetResponseTypeDef:
        """
        Updates the specified data quality ruleset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_data_quality_ruleset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_data_quality_ruleset)
        """

    def update_database(
        self, *, Name: str, DatabaseInput: DatabaseInputTypeDef, CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Updates an existing database definition in a Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_database)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_database)
        """

    def update_dev_endpoint(
        self,
        *,
        EndpointName: str,
        PublicKey: str = ...,
        AddPublicKeys: Sequence[str] = ...,
        DeletePublicKeys: Sequence[str] = ...,
        CustomLibraries: DevEndpointCustomLibrariesTypeDef = ...,
        UpdateEtlLibraries: bool = ...,
        DeleteArguments: Sequence[str] = ...,
        AddArguments: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Updates a specified development endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_dev_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_dev_endpoint)
        """

    def update_job(self, *, JobName: str, JobUpdate: JobUpdateTypeDef) -> UpdateJobResponseTypeDef:
        """
        Updates an existing job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_job)
        """

    def update_job_from_source_control(
        self,
        *,
        JobName: str = ...,
        Provider: SourceControlProviderType = ...,
        RepositoryName: str = ...,
        RepositoryOwner: str = ...,
        BranchName: str = ...,
        Folder: str = ...,
        CommitId: str = ...,
        AuthStrategy: SourceControlAuthStrategyType = ...,
        AuthToken: str = ...
    ) -> UpdateJobFromSourceControlResponseTypeDef:
        """
        Synchronizes a job from the source control repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_job_from_source_control)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_job_from_source_control)
        """

    def update_ml_transform(
        self,
        *,
        TransformId: str,
        Name: str = ...,
        Description: str = ...,
        Parameters: TransformParametersTypeDef = ...,
        Role: str = ...,
        GlueVersion: str = ...,
        MaxCapacity: float = ...,
        WorkerType: WorkerTypeType = ...,
        NumberOfWorkers: int = ...,
        Timeout: int = ...,
        MaxRetries: int = ...
    ) -> UpdateMLTransformResponseTypeDef:
        """
        Updates an existing machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_ml_transform)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_ml_transform)
        """

    def update_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionValueList: Sequence[str],
        PartitionInput: PartitionInputTypeDef,
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a partition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_partition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_partition)
        """

    def update_registry(
        self, *, RegistryId: RegistryIdTypeDef, Description: str
    ) -> UpdateRegistryResponseTypeDef:
        """
        Updates an existing registry which is used to hold a collection of schemas.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_registry)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_registry)
        """

    def update_schema(
        self,
        *,
        SchemaId: SchemaIdTypeDef,
        SchemaVersionNumber: SchemaVersionNumberTypeDef = ...,
        Compatibility: CompatibilityType = ...,
        Description: str = ...
    ) -> UpdateSchemaResponseTypeDef:
        """
        Updates the description, compatibility setting, or version checkpoint for a
        schema set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_schema)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_schema)
        """

    def update_source_control_from_job(
        self,
        *,
        JobName: str = ...,
        Provider: SourceControlProviderType = ...,
        RepositoryName: str = ...,
        RepositoryOwner: str = ...,
        BranchName: str = ...,
        Folder: str = ...,
        CommitId: str = ...,
        AuthStrategy: SourceControlAuthStrategyType = ...,
        AuthToken: str = ...
    ) -> UpdateSourceControlFromJobResponseTypeDef:
        """
        Synchronizes a job to the source control repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_source_control_from_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_source_control_from_job)
        """

    def update_table(
        self,
        *,
        DatabaseName: str,
        TableInput: TableInputTypeDef,
        CatalogId: str = ...,
        SkipArchive: bool = ...,
        TransactionId: str = ...,
        VersionId: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a metadata table in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_table)
        """

    def update_trigger(
        self, *, Name: str, TriggerUpdate: TriggerUpdateTypeDef
    ) -> UpdateTriggerResponseTypeDef:
        """
        Updates a trigger definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_trigger)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_trigger)
        """

    def update_user_defined_function(
        self,
        *,
        DatabaseName: str,
        FunctionName: str,
        FunctionInput: UserDefinedFunctionInputTypeDef,
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Updates an existing function definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_user_defined_function)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_user_defined_function)
        """

    def update_workflow(
        self,
        *,
        Name: str,
        Description: str = ...,
        DefaultRunProperties: Mapping[str, str] = ...,
        MaxConcurrentRuns: int = ...
    ) -> UpdateWorkflowResponseTypeDef:
        """
        Updates an existing workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_workflow)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#update_workflow)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_classifiers"]) -> GetClassifiersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_connections"]) -> GetConnectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_crawler_metrics"]
    ) -> GetCrawlerMetricsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_crawlers"]) -> GetCrawlersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_databases"]) -> GetDatabasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_dev_endpoints"]
    ) -> GetDevEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_job_runs"]) -> GetJobRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_jobs"]) -> GetJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_partition_indexes"]
    ) -> GetPartitionIndexesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_partitions"]) -> GetPartitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_policies"]
    ) -> GetResourcePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_security_configurations"]
    ) -> GetSecurityConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_table_versions"]
    ) -> GetTableVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_tables"]) -> GetTablesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_triggers"]) -> GetTriggersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_user_defined_functions"]
    ) -> GetUserDefinedFunctionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_registries"]) -> ListRegistriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_schema_versions"]
    ) -> ListSchemaVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_schemas"]) -> ListSchemasPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/client/#get_paginator)
        """
