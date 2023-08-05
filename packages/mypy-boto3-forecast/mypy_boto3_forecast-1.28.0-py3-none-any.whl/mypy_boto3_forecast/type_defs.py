"""
Type annotations for forecast service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecast/type_defs/)

Usage::

    ```python
    from mypy_boto3_forecast.type_defs import ActionTypeDef

    data: ActionTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AttributeTypeType,
    AutoMLOverrideStrategyType,
    ConditionType,
    DatasetTypeType,
    DayOfWeekType,
    DomainType,
    EvaluationTypeType,
    FilterConditionStringType,
    ImportModeType,
    MonthType,
    OperationType,
    OptimizationMetricType,
    ScalingTypeType,
    StateType,
    TimePointGranularityType,
    TimeSeriesGranularityType,
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
    "ActionTypeDef",
    "AdditionalDatasetTypeDef",
    "AttributeConfigTypeDef",
    "BaselineMetricTypeDef",
    "CategoricalParameterRangeTypeDef",
    "ContinuousParameterRangeTypeDef",
    "EncryptionConfigTypeDef",
    "MonitorConfigTypeDef",
    "TagTypeDef",
    "TimeAlignmentBoundaryTypeDef",
    "CreateAutoPredictorResponseTypeDef",
    "CreateDatasetGroupResponseTypeDef",
    "CreateDatasetImportJobResponseTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateExplainabilityExportResponseTypeDef",
    "ExplainabilityConfigTypeDef",
    "CreateExplainabilityResponseTypeDef",
    "CreateForecastExportJobResponseTypeDef",
    "CreateForecastResponseTypeDef",
    "CreateMonitorResponseTypeDef",
    "CreatePredictorBacktestExportJobResponseTypeDef",
    "EvaluationParametersTypeDef",
    "CreatePredictorResponseTypeDef",
    "CreateWhatIfAnalysisResponseTypeDef",
    "CreateWhatIfForecastExportResponseTypeDef",
    "CreateWhatIfForecastResponseTypeDef",
    "S3ConfigTypeDef",
    "DatasetGroupSummaryTypeDef",
    "DatasetSummaryTypeDef",
    "DeleteDatasetGroupRequestRequestTypeDef",
    "DeleteDatasetImportJobRequestRequestTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DeleteExplainabilityExportRequestRequestTypeDef",
    "DeleteExplainabilityRequestRequestTypeDef",
    "DeleteForecastExportJobRequestRequestTypeDef",
    "DeleteForecastRequestRequestTypeDef",
    "DeleteMonitorRequestRequestTypeDef",
    "DeletePredictorBacktestExportJobRequestRequestTypeDef",
    "DeletePredictorRequestRequestTypeDef",
    "DeleteResourceTreeRequestRequestTypeDef",
    "DeleteWhatIfAnalysisRequestRequestTypeDef",
    "DeleteWhatIfForecastExportRequestRequestTypeDef",
    "DeleteWhatIfForecastRequestRequestTypeDef",
    "DescribeAutoPredictorRequestRequestTypeDef",
    "ExplainabilityInfoTypeDef",
    "MonitorInfoTypeDef",
    "ReferencePredictorSummaryTypeDef",
    "DescribeDatasetGroupRequestRequestTypeDef",
    "DescribeDatasetGroupResponseTypeDef",
    "DescribeDatasetImportJobRequestRequestTypeDef",
    "StatisticsTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeExplainabilityExportRequestRequestTypeDef",
    "DescribeExplainabilityRequestRequestTypeDef",
    "DescribeForecastExportJobRequestRequestTypeDef",
    "DescribeForecastRequestRequestTypeDef",
    "DescribeMonitorRequestRequestTypeDef",
    "DescribePredictorBacktestExportJobRequestRequestTypeDef",
    "DescribePredictorRequestRequestTypeDef",
    "DescribeWhatIfAnalysisRequestRequestTypeDef",
    "DescribeWhatIfForecastExportRequestRequestTypeDef",
    "DescribeWhatIfForecastRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ErrorMetricTypeDef",
    "FeaturizationMethodTypeDef",
    "FilterTypeDef",
    "ForecastSummaryTypeDef",
    "GetAccuracyMetricsRequestRequestTypeDef",
    "SupplementaryFeatureTypeDef",
    "IntegerParameterRangeTypeDef",
    "ListDatasetGroupsRequestListDatasetGroupsPaginateTypeDef",
    "ListDatasetGroupsRequestRequestTypeDef",
    "ListDatasetsRequestListDatasetsPaginateTypeDef",
    "ListDatasetsRequestRequestTypeDef",
    "MonitorSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "WhatIfAnalysisSummaryTypeDef",
    "WhatIfForecastSummaryTypeDef",
    "MetricResultTypeDef",
    "WeightedQuantileLossTypeDef",
    "MonitorDataSourceTypeDef",
    "PaginatorConfigTypeDef",
    "PredictorEventTypeDef",
    "TestWindowSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "ResumeResourceRequestRequestTypeDef",
    "SchemaAttributeTypeDef",
    "StopResourceRequestRequestTypeDef",
    "TimeSeriesConditionTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDatasetGroupRequestRequestTypeDef",
    "DataConfigTypeDef",
    "PredictorBaselineTypeDef",
    "CreateDatasetGroupRequestRequestTypeDef",
    "CreateMonitorRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ExplainabilitySummaryTypeDef",
    "DataDestinationTypeDef",
    "DataSourceTypeDef",
    "ListDatasetGroupsResponseTypeDef",
    "ListDatasetsResponseTypeDef",
    "PredictorSummaryTypeDef",
    "FeaturizationTypeDef",
    "ListDatasetImportJobsRequestListDatasetImportJobsPaginateTypeDef",
    "ListDatasetImportJobsRequestRequestTypeDef",
    "ListExplainabilitiesRequestListExplainabilitiesPaginateTypeDef",
    "ListExplainabilitiesRequestRequestTypeDef",
    "ListExplainabilityExportsRequestListExplainabilityExportsPaginateTypeDef",
    "ListExplainabilityExportsRequestRequestTypeDef",
    "ListForecastExportJobsRequestListForecastExportJobsPaginateTypeDef",
    "ListForecastExportJobsRequestRequestTypeDef",
    "ListForecastsRequestListForecastsPaginateTypeDef",
    "ListForecastsRequestRequestTypeDef",
    "ListMonitorEvaluationsRequestListMonitorEvaluationsPaginateTypeDef",
    "ListMonitorEvaluationsRequestRequestTypeDef",
    "ListMonitorsRequestListMonitorsPaginateTypeDef",
    "ListMonitorsRequestRequestTypeDef",
    "ListPredictorBacktestExportJobsRequestListPredictorBacktestExportJobsPaginateTypeDef",
    "ListPredictorBacktestExportJobsRequestRequestTypeDef",
    "ListPredictorsRequestListPredictorsPaginateTypeDef",
    "ListPredictorsRequestRequestTypeDef",
    "ListWhatIfAnalysesRequestListWhatIfAnalysesPaginateTypeDef",
    "ListWhatIfAnalysesRequestRequestTypeDef",
    "ListWhatIfForecastExportsRequestListWhatIfForecastExportsPaginateTypeDef",
    "ListWhatIfForecastExportsRequestRequestTypeDef",
    "ListWhatIfForecastsRequestListWhatIfForecastsPaginateTypeDef",
    "ListWhatIfForecastsRequestRequestTypeDef",
    "ListForecastsResponseTypeDef",
    "InputDataConfigTypeDef",
    "ParameterRangesTypeDef",
    "ListMonitorsResponseTypeDef",
    "ListWhatIfAnalysesResponseTypeDef",
    "ListWhatIfForecastsResponseTypeDef",
    "MetricsTypeDef",
    "PredictorMonitorEvaluationTypeDef",
    "PredictorExecutionTypeDef",
    "SchemaTypeDef",
    "TimeSeriesTransformationTypeDef",
    "CreateAutoPredictorRequestRequestTypeDef",
    "DescribeAutoPredictorResponseTypeDef",
    "BaselineTypeDef",
    "ListExplainabilitiesResponseTypeDef",
    "CreateExplainabilityExportRequestRequestTypeDef",
    "CreateForecastExportJobRequestRequestTypeDef",
    "CreatePredictorBacktestExportJobRequestRequestTypeDef",
    "CreateWhatIfForecastExportRequestRequestTypeDef",
    "DescribeExplainabilityExportResponseTypeDef",
    "DescribeForecastExportJobResponseTypeDef",
    "DescribePredictorBacktestExportJobResponseTypeDef",
    "DescribeWhatIfForecastExportResponseTypeDef",
    "ExplainabilityExportSummaryTypeDef",
    "ForecastExportJobSummaryTypeDef",
    "PredictorBacktestExportJobSummaryTypeDef",
    "WhatIfForecastExportSummaryTypeDef",
    "CreateDatasetImportJobRequestRequestTypeDef",
    "DatasetImportJobSummaryTypeDef",
    "DescribeDatasetImportJobResponseTypeDef",
    "ListPredictorsResponseTypeDef",
    "FeaturizationConfigTypeDef",
    "HyperParameterTuningJobConfigTypeDef",
    "WindowSummaryTypeDef",
    "ListMonitorEvaluationsResponseTypeDef",
    "PredictorExecutionDetailsTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "CreateExplainabilityRequestRequestTypeDef",
    "DescribeDatasetResponseTypeDef",
    "DescribeExplainabilityResponseTypeDef",
    "TimeSeriesIdentifiersTypeDef",
    "TimeSeriesReplacementsDataSourceTypeDef",
    "DescribeMonitorResponseTypeDef",
    "ListExplainabilityExportsResponseTypeDef",
    "ListForecastExportJobsResponseTypeDef",
    "ListPredictorBacktestExportJobsResponseTypeDef",
    "ListWhatIfForecastExportsResponseTypeDef",
    "ListDatasetImportJobsResponseTypeDef",
    "CreatePredictorRequestRequestTypeDef",
    "EvaluationResultTypeDef",
    "DescribePredictorResponseTypeDef",
    "TimeSeriesSelectorTypeDef",
    "CreateWhatIfForecastRequestRequestTypeDef",
    "DescribeWhatIfForecastResponseTypeDef",
    "GetAccuracyMetricsResponseTypeDef",
    "CreateForecastRequestRequestTypeDef",
    "CreateWhatIfAnalysisRequestRequestTypeDef",
    "DescribeForecastResponseTypeDef",
    "DescribeWhatIfAnalysisResponseTypeDef",
)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "AttributeName": str,
        "Operation": OperationType,
        "Value": float,
    },
)

_RequiredAdditionalDatasetTypeDef = TypedDict(
    "_RequiredAdditionalDatasetTypeDef",
    {
        "Name": str,
    },
)
_OptionalAdditionalDatasetTypeDef = TypedDict(
    "_OptionalAdditionalDatasetTypeDef",
    {
        "Configuration": Mapping[str, Sequence[str]],
    },
    total=False,
)


class AdditionalDatasetTypeDef(
    _RequiredAdditionalDatasetTypeDef, _OptionalAdditionalDatasetTypeDef
):
    pass


AttributeConfigTypeDef = TypedDict(
    "AttributeConfigTypeDef",
    {
        "AttributeName": str,
        "Transformations": Mapping[str, str],
    },
)

BaselineMetricTypeDef = TypedDict(
    "BaselineMetricTypeDef",
    {
        "Name": str,
        "Value": float,
    },
    total=False,
)

CategoricalParameterRangeTypeDef = TypedDict(
    "CategoricalParameterRangeTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
)

_RequiredContinuousParameterRangeTypeDef = TypedDict(
    "_RequiredContinuousParameterRangeTypeDef",
    {
        "Name": str,
        "MaxValue": float,
        "MinValue": float,
    },
)
_OptionalContinuousParameterRangeTypeDef = TypedDict(
    "_OptionalContinuousParameterRangeTypeDef",
    {
        "ScalingType": ScalingTypeType,
    },
    total=False,
)


class ContinuousParameterRangeTypeDef(
    _RequiredContinuousParameterRangeTypeDef, _OptionalContinuousParameterRangeTypeDef
):
    pass


EncryptionConfigTypeDef = TypedDict(
    "EncryptionConfigTypeDef",
    {
        "RoleArn": str,
        "KMSKeyArn": str,
    },
)

MonitorConfigTypeDef = TypedDict(
    "MonitorConfigTypeDef",
    {
        "MonitorName": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

TimeAlignmentBoundaryTypeDef = TypedDict(
    "TimeAlignmentBoundaryTypeDef",
    {
        "Month": MonthType,
        "DayOfMonth": int,
        "DayOfWeek": DayOfWeekType,
        "Hour": int,
    },
    total=False,
)

CreateAutoPredictorResponseTypeDef = TypedDict(
    "CreateAutoPredictorResponseTypeDef",
    {
        "PredictorArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateDatasetGroupResponseTypeDef = TypedDict(
    "CreateDatasetGroupResponseTypeDef",
    {
        "DatasetGroupArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateDatasetImportJobResponseTypeDef = TypedDict(
    "CreateDatasetImportJobResponseTypeDef",
    {
        "DatasetImportJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateDatasetResponseTypeDef = TypedDict(
    "CreateDatasetResponseTypeDef",
    {
        "DatasetArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateExplainabilityExportResponseTypeDef = TypedDict(
    "CreateExplainabilityExportResponseTypeDef",
    {
        "ExplainabilityExportArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ExplainabilityConfigTypeDef = TypedDict(
    "ExplainabilityConfigTypeDef",
    {
        "TimeSeriesGranularity": TimeSeriesGranularityType,
        "TimePointGranularity": TimePointGranularityType,
    },
)

CreateExplainabilityResponseTypeDef = TypedDict(
    "CreateExplainabilityResponseTypeDef",
    {
        "ExplainabilityArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateForecastExportJobResponseTypeDef = TypedDict(
    "CreateForecastExportJobResponseTypeDef",
    {
        "ForecastExportJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateForecastResponseTypeDef = TypedDict(
    "CreateForecastResponseTypeDef",
    {
        "ForecastArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateMonitorResponseTypeDef = TypedDict(
    "CreateMonitorResponseTypeDef",
    {
        "MonitorArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreatePredictorBacktestExportJobResponseTypeDef = TypedDict(
    "CreatePredictorBacktestExportJobResponseTypeDef",
    {
        "PredictorBacktestExportJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EvaluationParametersTypeDef = TypedDict(
    "EvaluationParametersTypeDef",
    {
        "NumberOfBacktestWindows": int,
        "BackTestWindowOffset": int,
    },
    total=False,
)

CreatePredictorResponseTypeDef = TypedDict(
    "CreatePredictorResponseTypeDef",
    {
        "PredictorArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateWhatIfAnalysisResponseTypeDef = TypedDict(
    "CreateWhatIfAnalysisResponseTypeDef",
    {
        "WhatIfAnalysisArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateWhatIfForecastExportResponseTypeDef = TypedDict(
    "CreateWhatIfForecastExportResponseTypeDef",
    {
        "WhatIfForecastExportArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateWhatIfForecastResponseTypeDef = TypedDict(
    "CreateWhatIfForecastResponseTypeDef",
    {
        "WhatIfForecastArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredS3ConfigTypeDef = TypedDict(
    "_RequiredS3ConfigTypeDef",
    {
        "Path": str,
        "RoleArn": str,
    },
)
_OptionalS3ConfigTypeDef = TypedDict(
    "_OptionalS3ConfigTypeDef",
    {
        "KMSKeyArn": str,
    },
    total=False,
)


class S3ConfigTypeDef(_RequiredS3ConfigTypeDef, _OptionalS3ConfigTypeDef):
    pass


DatasetGroupSummaryTypeDef = TypedDict(
    "DatasetGroupSummaryTypeDef",
    {
        "DatasetGroupArn": str,
        "DatasetGroupName": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

DatasetSummaryTypeDef = TypedDict(
    "DatasetSummaryTypeDef",
    {
        "DatasetArn": str,
        "DatasetName": str,
        "DatasetType": DatasetTypeType,
        "Domain": DomainType,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

DeleteDatasetGroupRequestRequestTypeDef = TypedDict(
    "DeleteDatasetGroupRequestRequestTypeDef",
    {
        "DatasetGroupArn": str,
    },
)

DeleteDatasetImportJobRequestRequestTypeDef = TypedDict(
    "DeleteDatasetImportJobRequestRequestTypeDef",
    {
        "DatasetImportJobArn": str,
    },
)

DeleteDatasetRequestRequestTypeDef = TypedDict(
    "DeleteDatasetRequestRequestTypeDef",
    {
        "DatasetArn": str,
    },
)

DeleteExplainabilityExportRequestRequestTypeDef = TypedDict(
    "DeleteExplainabilityExportRequestRequestTypeDef",
    {
        "ExplainabilityExportArn": str,
    },
)

DeleteExplainabilityRequestRequestTypeDef = TypedDict(
    "DeleteExplainabilityRequestRequestTypeDef",
    {
        "ExplainabilityArn": str,
    },
)

DeleteForecastExportJobRequestRequestTypeDef = TypedDict(
    "DeleteForecastExportJobRequestRequestTypeDef",
    {
        "ForecastExportJobArn": str,
    },
)

DeleteForecastRequestRequestTypeDef = TypedDict(
    "DeleteForecastRequestRequestTypeDef",
    {
        "ForecastArn": str,
    },
)

DeleteMonitorRequestRequestTypeDef = TypedDict(
    "DeleteMonitorRequestRequestTypeDef",
    {
        "MonitorArn": str,
    },
)

DeletePredictorBacktestExportJobRequestRequestTypeDef = TypedDict(
    "DeletePredictorBacktestExportJobRequestRequestTypeDef",
    {
        "PredictorBacktestExportJobArn": str,
    },
)

DeletePredictorRequestRequestTypeDef = TypedDict(
    "DeletePredictorRequestRequestTypeDef",
    {
        "PredictorArn": str,
    },
)

DeleteResourceTreeRequestRequestTypeDef = TypedDict(
    "DeleteResourceTreeRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DeleteWhatIfAnalysisRequestRequestTypeDef = TypedDict(
    "DeleteWhatIfAnalysisRequestRequestTypeDef",
    {
        "WhatIfAnalysisArn": str,
    },
)

DeleteWhatIfForecastExportRequestRequestTypeDef = TypedDict(
    "DeleteWhatIfForecastExportRequestRequestTypeDef",
    {
        "WhatIfForecastExportArn": str,
    },
)

DeleteWhatIfForecastRequestRequestTypeDef = TypedDict(
    "DeleteWhatIfForecastRequestRequestTypeDef",
    {
        "WhatIfForecastArn": str,
    },
)

DescribeAutoPredictorRequestRequestTypeDef = TypedDict(
    "DescribeAutoPredictorRequestRequestTypeDef",
    {
        "PredictorArn": str,
    },
)

ExplainabilityInfoTypeDef = TypedDict(
    "ExplainabilityInfoTypeDef",
    {
        "ExplainabilityArn": str,
        "Status": str,
    },
    total=False,
)

MonitorInfoTypeDef = TypedDict(
    "MonitorInfoTypeDef",
    {
        "MonitorArn": str,
        "Status": str,
    },
    total=False,
)

ReferencePredictorSummaryTypeDef = TypedDict(
    "ReferencePredictorSummaryTypeDef",
    {
        "Arn": str,
        "State": StateType,
    },
    total=False,
)

DescribeDatasetGroupRequestRequestTypeDef = TypedDict(
    "DescribeDatasetGroupRequestRequestTypeDef",
    {
        "DatasetGroupArn": str,
    },
)

DescribeDatasetGroupResponseTypeDef = TypedDict(
    "DescribeDatasetGroupResponseTypeDef",
    {
        "DatasetGroupName": str,
        "DatasetGroupArn": str,
        "DatasetArns": List[str],
        "Domain": DomainType,
        "Status": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDatasetImportJobRequestRequestTypeDef = TypedDict(
    "DescribeDatasetImportJobRequestRequestTypeDef",
    {
        "DatasetImportJobArn": str,
    },
)

StatisticsTypeDef = TypedDict(
    "StatisticsTypeDef",
    {
        "Count": int,
        "CountDistinct": int,
        "CountNull": int,
        "CountNan": int,
        "Min": str,
        "Max": str,
        "Avg": float,
        "Stddev": float,
        "CountLong": int,
        "CountDistinctLong": int,
        "CountNullLong": int,
        "CountNanLong": int,
    },
    total=False,
)

DescribeDatasetRequestRequestTypeDef = TypedDict(
    "DescribeDatasetRequestRequestTypeDef",
    {
        "DatasetArn": str,
    },
)

DescribeExplainabilityExportRequestRequestTypeDef = TypedDict(
    "DescribeExplainabilityExportRequestRequestTypeDef",
    {
        "ExplainabilityExportArn": str,
    },
)

DescribeExplainabilityRequestRequestTypeDef = TypedDict(
    "DescribeExplainabilityRequestRequestTypeDef",
    {
        "ExplainabilityArn": str,
    },
)

DescribeForecastExportJobRequestRequestTypeDef = TypedDict(
    "DescribeForecastExportJobRequestRequestTypeDef",
    {
        "ForecastExportJobArn": str,
    },
)

DescribeForecastRequestRequestTypeDef = TypedDict(
    "DescribeForecastRequestRequestTypeDef",
    {
        "ForecastArn": str,
    },
)

DescribeMonitorRequestRequestTypeDef = TypedDict(
    "DescribeMonitorRequestRequestTypeDef",
    {
        "MonitorArn": str,
    },
)

DescribePredictorBacktestExportJobRequestRequestTypeDef = TypedDict(
    "DescribePredictorBacktestExportJobRequestRequestTypeDef",
    {
        "PredictorBacktestExportJobArn": str,
    },
)

DescribePredictorRequestRequestTypeDef = TypedDict(
    "DescribePredictorRequestRequestTypeDef",
    {
        "PredictorArn": str,
    },
)

DescribeWhatIfAnalysisRequestRequestTypeDef = TypedDict(
    "DescribeWhatIfAnalysisRequestRequestTypeDef",
    {
        "WhatIfAnalysisArn": str,
    },
)

DescribeWhatIfForecastExportRequestRequestTypeDef = TypedDict(
    "DescribeWhatIfForecastExportRequestRequestTypeDef",
    {
        "WhatIfForecastExportArn": str,
    },
)

DescribeWhatIfForecastRequestRequestTypeDef = TypedDict(
    "DescribeWhatIfForecastRequestRequestTypeDef",
    {
        "WhatIfForecastArn": str,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ErrorMetricTypeDef = TypedDict(
    "ErrorMetricTypeDef",
    {
        "ForecastType": str,
        "WAPE": float,
        "RMSE": float,
        "MASE": float,
        "MAPE": float,
    },
    total=False,
)

_RequiredFeaturizationMethodTypeDef = TypedDict(
    "_RequiredFeaturizationMethodTypeDef",
    {
        "FeaturizationMethodName": Literal["filling"],
    },
)
_OptionalFeaturizationMethodTypeDef = TypedDict(
    "_OptionalFeaturizationMethodTypeDef",
    {
        "FeaturizationMethodParameters": Mapping[str, str],
    },
    total=False,
)


class FeaturizationMethodTypeDef(
    _RequiredFeaturizationMethodTypeDef, _OptionalFeaturizationMethodTypeDef
):
    pass


FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Key": str,
        "Value": str,
        "Condition": FilterConditionStringType,
    },
)

ForecastSummaryTypeDef = TypedDict(
    "ForecastSummaryTypeDef",
    {
        "ForecastArn": str,
        "ForecastName": str,
        "PredictorArn": str,
        "CreatedUsingAutoPredictor": bool,
        "DatasetGroupArn": str,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

GetAccuracyMetricsRequestRequestTypeDef = TypedDict(
    "GetAccuracyMetricsRequestRequestTypeDef",
    {
        "PredictorArn": str,
    },
)

SupplementaryFeatureTypeDef = TypedDict(
    "SupplementaryFeatureTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

_RequiredIntegerParameterRangeTypeDef = TypedDict(
    "_RequiredIntegerParameterRangeTypeDef",
    {
        "Name": str,
        "MaxValue": int,
        "MinValue": int,
    },
)
_OptionalIntegerParameterRangeTypeDef = TypedDict(
    "_OptionalIntegerParameterRangeTypeDef",
    {
        "ScalingType": ScalingTypeType,
    },
    total=False,
)


class IntegerParameterRangeTypeDef(
    _RequiredIntegerParameterRangeTypeDef, _OptionalIntegerParameterRangeTypeDef
):
    pass


ListDatasetGroupsRequestListDatasetGroupsPaginateTypeDef = TypedDict(
    "ListDatasetGroupsRequestListDatasetGroupsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDatasetGroupsRequestRequestTypeDef = TypedDict(
    "ListDatasetGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListDatasetsRequestListDatasetsPaginateTypeDef = TypedDict(
    "ListDatasetsRequestListDatasetsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDatasetsRequestRequestTypeDef = TypedDict(
    "ListDatasetsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

MonitorSummaryTypeDef = TypedDict(
    "MonitorSummaryTypeDef",
    {
        "MonitorArn": str,
        "MonitorName": str,
        "ResourceArn": str,
        "Status": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

WhatIfAnalysisSummaryTypeDef = TypedDict(
    "WhatIfAnalysisSummaryTypeDef",
    {
        "WhatIfAnalysisArn": str,
        "WhatIfAnalysisName": str,
        "ForecastArn": str,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

WhatIfForecastSummaryTypeDef = TypedDict(
    "WhatIfForecastSummaryTypeDef",
    {
        "WhatIfForecastArn": str,
        "WhatIfForecastName": str,
        "WhatIfAnalysisArn": str,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

MetricResultTypeDef = TypedDict(
    "MetricResultTypeDef",
    {
        "MetricName": str,
        "MetricValue": float,
    },
    total=False,
)

WeightedQuantileLossTypeDef = TypedDict(
    "WeightedQuantileLossTypeDef",
    {
        "Quantile": float,
        "LossValue": float,
    },
    total=False,
)

MonitorDataSourceTypeDef = TypedDict(
    "MonitorDataSourceTypeDef",
    {
        "DatasetImportJobArn": str,
        "ForecastArn": str,
        "PredictorArn": str,
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

PredictorEventTypeDef = TypedDict(
    "PredictorEventTypeDef",
    {
        "Detail": str,
        "Datetime": datetime,
    },
    total=False,
)

TestWindowSummaryTypeDef = TypedDict(
    "TestWindowSummaryTypeDef",
    {
        "TestWindowStart": datetime,
        "TestWindowEnd": datetime,
        "Status": str,
        "Message": str,
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

ResumeResourceRequestRequestTypeDef = TypedDict(
    "ResumeResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

SchemaAttributeTypeDef = TypedDict(
    "SchemaAttributeTypeDef",
    {
        "AttributeName": str,
        "AttributeType": AttributeTypeType,
    },
    total=False,
)

StopResourceRequestRequestTypeDef = TypedDict(
    "StopResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

TimeSeriesConditionTypeDef = TypedDict(
    "TimeSeriesConditionTypeDef",
    {
        "AttributeName": str,
        "AttributeValue": str,
        "Condition": ConditionType,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateDatasetGroupRequestRequestTypeDef = TypedDict(
    "UpdateDatasetGroupRequestRequestTypeDef",
    {
        "DatasetGroupArn": str,
        "DatasetArns": Sequence[str],
    },
)

_RequiredDataConfigTypeDef = TypedDict(
    "_RequiredDataConfigTypeDef",
    {
        "DatasetGroupArn": str,
    },
)
_OptionalDataConfigTypeDef = TypedDict(
    "_OptionalDataConfigTypeDef",
    {
        "AttributeConfigs": Sequence[AttributeConfigTypeDef],
        "AdditionalDatasets": Sequence[AdditionalDatasetTypeDef],
    },
    total=False,
)


class DataConfigTypeDef(_RequiredDataConfigTypeDef, _OptionalDataConfigTypeDef):
    pass


PredictorBaselineTypeDef = TypedDict(
    "PredictorBaselineTypeDef",
    {
        "BaselineMetrics": List[BaselineMetricTypeDef],
    },
    total=False,
)

_RequiredCreateDatasetGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetGroupRequestRequestTypeDef",
    {
        "DatasetGroupName": str,
        "Domain": DomainType,
    },
)
_OptionalCreateDatasetGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetGroupRequestRequestTypeDef",
    {
        "DatasetArns": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDatasetGroupRequestRequestTypeDef(
    _RequiredCreateDatasetGroupRequestRequestTypeDef,
    _OptionalCreateDatasetGroupRequestRequestTypeDef,
):
    pass


_RequiredCreateMonitorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMonitorRequestRequestTypeDef",
    {
        "MonitorName": str,
        "ResourceArn": str,
    },
)
_OptionalCreateMonitorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMonitorRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateMonitorRequestRequestTypeDef(
    _RequiredCreateMonitorRequestRequestTypeDef, _OptionalCreateMonitorRequestRequestTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
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

ExplainabilitySummaryTypeDef = TypedDict(
    "ExplainabilitySummaryTypeDef",
    {
        "ExplainabilityArn": str,
        "ExplainabilityName": str,
        "ResourceArn": str,
        "ExplainabilityConfig": ExplainabilityConfigTypeDef,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

DataDestinationTypeDef = TypedDict(
    "DataDestinationTypeDef",
    {
        "S3Config": S3ConfigTypeDef,
    },
)

DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "S3Config": S3ConfigTypeDef,
    },
)

ListDatasetGroupsResponseTypeDef = TypedDict(
    "ListDatasetGroupsResponseTypeDef",
    {
        "DatasetGroups": List[DatasetGroupSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDatasetsResponseTypeDef = TypedDict(
    "ListDatasetsResponseTypeDef",
    {
        "Datasets": List[DatasetSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PredictorSummaryTypeDef = TypedDict(
    "PredictorSummaryTypeDef",
    {
        "PredictorArn": str,
        "PredictorName": str,
        "DatasetGroupArn": str,
        "IsAutoPredictor": bool,
        "ReferencePredictorSummary": ReferencePredictorSummaryTypeDef,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

_RequiredFeaturizationTypeDef = TypedDict(
    "_RequiredFeaturizationTypeDef",
    {
        "AttributeName": str,
    },
)
_OptionalFeaturizationTypeDef = TypedDict(
    "_OptionalFeaturizationTypeDef",
    {
        "FeaturizationPipeline": Sequence[FeaturizationMethodTypeDef],
    },
    total=False,
)


class FeaturizationTypeDef(_RequiredFeaturizationTypeDef, _OptionalFeaturizationTypeDef):
    pass


ListDatasetImportJobsRequestListDatasetImportJobsPaginateTypeDef = TypedDict(
    "ListDatasetImportJobsRequestListDatasetImportJobsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDatasetImportJobsRequestRequestTypeDef = TypedDict(
    "ListDatasetImportJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListExplainabilitiesRequestListExplainabilitiesPaginateTypeDef = TypedDict(
    "ListExplainabilitiesRequestListExplainabilitiesPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListExplainabilitiesRequestRequestTypeDef = TypedDict(
    "ListExplainabilitiesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListExplainabilityExportsRequestListExplainabilityExportsPaginateTypeDef = TypedDict(
    "ListExplainabilityExportsRequestListExplainabilityExportsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListExplainabilityExportsRequestRequestTypeDef = TypedDict(
    "ListExplainabilityExportsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListForecastExportJobsRequestListForecastExportJobsPaginateTypeDef = TypedDict(
    "ListForecastExportJobsRequestListForecastExportJobsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListForecastExportJobsRequestRequestTypeDef = TypedDict(
    "ListForecastExportJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListForecastsRequestListForecastsPaginateTypeDef = TypedDict(
    "ListForecastsRequestListForecastsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListForecastsRequestRequestTypeDef = TypedDict(
    "ListForecastsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

_RequiredListMonitorEvaluationsRequestListMonitorEvaluationsPaginateTypeDef = TypedDict(
    "_RequiredListMonitorEvaluationsRequestListMonitorEvaluationsPaginateTypeDef",
    {
        "MonitorArn": str,
    },
)
_OptionalListMonitorEvaluationsRequestListMonitorEvaluationsPaginateTypeDef = TypedDict(
    "_OptionalListMonitorEvaluationsRequestListMonitorEvaluationsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListMonitorEvaluationsRequestListMonitorEvaluationsPaginateTypeDef(
    _RequiredListMonitorEvaluationsRequestListMonitorEvaluationsPaginateTypeDef,
    _OptionalListMonitorEvaluationsRequestListMonitorEvaluationsPaginateTypeDef,
):
    pass


_RequiredListMonitorEvaluationsRequestRequestTypeDef = TypedDict(
    "_RequiredListMonitorEvaluationsRequestRequestTypeDef",
    {
        "MonitorArn": str,
    },
)
_OptionalListMonitorEvaluationsRequestRequestTypeDef = TypedDict(
    "_OptionalListMonitorEvaluationsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)


class ListMonitorEvaluationsRequestRequestTypeDef(
    _RequiredListMonitorEvaluationsRequestRequestTypeDef,
    _OptionalListMonitorEvaluationsRequestRequestTypeDef,
):
    pass


ListMonitorsRequestListMonitorsPaginateTypeDef = TypedDict(
    "ListMonitorsRequestListMonitorsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListMonitorsRequestRequestTypeDef = TypedDict(
    "ListMonitorsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListPredictorBacktestExportJobsRequestListPredictorBacktestExportJobsPaginateTypeDef = TypedDict(
    "ListPredictorBacktestExportJobsRequestListPredictorBacktestExportJobsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListPredictorBacktestExportJobsRequestRequestTypeDef = TypedDict(
    "ListPredictorBacktestExportJobsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListPredictorsRequestListPredictorsPaginateTypeDef = TypedDict(
    "ListPredictorsRequestListPredictorsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListPredictorsRequestRequestTypeDef = TypedDict(
    "ListPredictorsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListWhatIfAnalysesRequestListWhatIfAnalysesPaginateTypeDef = TypedDict(
    "ListWhatIfAnalysesRequestListWhatIfAnalysesPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListWhatIfAnalysesRequestRequestTypeDef = TypedDict(
    "ListWhatIfAnalysesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListWhatIfForecastExportsRequestListWhatIfForecastExportsPaginateTypeDef = TypedDict(
    "ListWhatIfForecastExportsRequestListWhatIfForecastExportsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListWhatIfForecastExportsRequestRequestTypeDef = TypedDict(
    "ListWhatIfForecastExportsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListWhatIfForecastsRequestListWhatIfForecastsPaginateTypeDef = TypedDict(
    "ListWhatIfForecastsRequestListWhatIfForecastsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListWhatIfForecastsRequestRequestTypeDef = TypedDict(
    "ListWhatIfForecastsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListForecastsResponseTypeDef = TypedDict(
    "ListForecastsResponseTypeDef",
    {
        "Forecasts": List[ForecastSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredInputDataConfigTypeDef = TypedDict(
    "_RequiredInputDataConfigTypeDef",
    {
        "DatasetGroupArn": str,
    },
)
_OptionalInputDataConfigTypeDef = TypedDict(
    "_OptionalInputDataConfigTypeDef",
    {
        "SupplementaryFeatures": Sequence[SupplementaryFeatureTypeDef],
    },
    total=False,
)


class InputDataConfigTypeDef(_RequiredInputDataConfigTypeDef, _OptionalInputDataConfigTypeDef):
    pass


ParameterRangesTypeDef = TypedDict(
    "ParameterRangesTypeDef",
    {
        "CategoricalParameterRanges": Sequence[CategoricalParameterRangeTypeDef],
        "ContinuousParameterRanges": Sequence[ContinuousParameterRangeTypeDef],
        "IntegerParameterRanges": Sequence[IntegerParameterRangeTypeDef],
    },
    total=False,
)

ListMonitorsResponseTypeDef = TypedDict(
    "ListMonitorsResponseTypeDef",
    {
        "Monitors": List[MonitorSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListWhatIfAnalysesResponseTypeDef = TypedDict(
    "ListWhatIfAnalysesResponseTypeDef",
    {
        "WhatIfAnalyses": List[WhatIfAnalysisSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListWhatIfForecastsResponseTypeDef = TypedDict(
    "ListWhatIfForecastsResponseTypeDef",
    {
        "WhatIfForecasts": List[WhatIfForecastSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MetricsTypeDef = TypedDict(
    "MetricsTypeDef",
    {
        "RMSE": float,
        "WeightedQuantileLosses": List[WeightedQuantileLossTypeDef],
        "ErrorMetrics": List[ErrorMetricTypeDef],
        "AverageWeightedQuantileLoss": float,
    },
    total=False,
)

PredictorMonitorEvaluationTypeDef = TypedDict(
    "PredictorMonitorEvaluationTypeDef",
    {
        "ResourceArn": str,
        "MonitorArn": str,
        "EvaluationTime": datetime,
        "EvaluationState": str,
        "WindowStartDatetime": datetime,
        "WindowEndDatetime": datetime,
        "PredictorEvent": PredictorEventTypeDef,
        "MonitorDataSource": MonitorDataSourceTypeDef,
        "MetricResults": List[MetricResultTypeDef],
        "NumItemsEvaluated": int,
        "Message": str,
    },
    total=False,
)

PredictorExecutionTypeDef = TypedDict(
    "PredictorExecutionTypeDef",
    {
        "AlgorithmArn": str,
        "TestWindows": List[TestWindowSummaryTypeDef],
    },
    total=False,
)

SchemaTypeDef = TypedDict(
    "SchemaTypeDef",
    {
        "Attributes": Sequence[SchemaAttributeTypeDef],
    },
    total=False,
)

TimeSeriesTransformationTypeDef = TypedDict(
    "TimeSeriesTransformationTypeDef",
    {
        "Action": ActionTypeDef,
        "TimeSeriesConditions": Sequence[TimeSeriesConditionTypeDef],
    },
    total=False,
)

_RequiredCreateAutoPredictorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAutoPredictorRequestRequestTypeDef",
    {
        "PredictorName": str,
    },
)
_OptionalCreateAutoPredictorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAutoPredictorRequestRequestTypeDef",
    {
        "ForecastHorizon": int,
        "ForecastTypes": Sequence[str],
        "ForecastDimensions": Sequence[str],
        "ForecastFrequency": str,
        "DataConfig": DataConfigTypeDef,
        "EncryptionConfig": EncryptionConfigTypeDef,
        "ReferencePredictorArn": str,
        "OptimizationMetric": OptimizationMetricType,
        "ExplainPredictor": bool,
        "Tags": Sequence[TagTypeDef],
        "MonitorConfig": MonitorConfigTypeDef,
        "TimeAlignmentBoundary": TimeAlignmentBoundaryTypeDef,
    },
    total=False,
)


class CreateAutoPredictorRequestRequestTypeDef(
    _RequiredCreateAutoPredictorRequestRequestTypeDef,
    _OptionalCreateAutoPredictorRequestRequestTypeDef,
):
    pass


DescribeAutoPredictorResponseTypeDef = TypedDict(
    "DescribeAutoPredictorResponseTypeDef",
    {
        "PredictorArn": str,
        "PredictorName": str,
        "ForecastHorizon": int,
        "ForecastTypes": List[str],
        "ForecastFrequency": str,
        "ForecastDimensions": List[str],
        "DatasetImportJobArns": List[str],
        "DataConfig": DataConfigTypeDef,
        "EncryptionConfig": EncryptionConfigTypeDef,
        "ReferencePredictorSummary": ReferencePredictorSummaryTypeDef,
        "EstimatedTimeRemainingInMinutes": int,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "OptimizationMetric": OptimizationMetricType,
        "ExplainabilityInfo": ExplainabilityInfoTypeDef,
        "MonitorInfo": MonitorInfoTypeDef,
        "TimeAlignmentBoundary": TimeAlignmentBoundaryTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BaselineTypeDef = TypedDict(
    "BaselineTypeDef",
    {
        "PredictorBaseline": PredictorBaselineTypeDef,
    },
    total=False,
)

ListExplainabilitiesResponseTypeDef = TypedDict(
    "ListExplainabilitiesResponseTypeDef",
    {
        "Explainabilities": List[ExplainabilitySummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateExplainabilityExportRequestRequestTypeDef = TypedDict(
    "_RequiredCreateExplainabilityExportRequestRequestTypeDef",
    {
        "ExplainabilityExportName": str,
        "ExplainabilityArn": str,
        "Destination": DataDestinationTypeDef,
    },
)
_OptionalCreateExplainabilityExportRequestRequestTypeDef = TypedDict(
    "_OptionalCreateExplainabilityExportRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "Format": str,
    },
    total=False,
)


class CreateExplainabilityExportRequestRequestTypeDef(
    _RequiredCreateExplainabilityExportRequestRequestTypeDef,
    _OptionalCreateExplainabilityExportRequestRequestTypeDef,
):
    pass


_RequiredCreateForecastExportJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateForecastExportJobRequestRequestTypeDef",
    {
        "ForecastExportJobName": str,
        "ForecastArn": str,
        "Destination": DataDestinationTypeDef,
    },
)
_OptionalCreateForecastExportJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateForecastExportJobRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "Format": str,
    },
    total=False,
)


class CreateForecastExportJobRequestRequestTypeDef(
    _RequiredCreateForecastExportJobRequestRequestTypeDef,
    _OptionalCreateForecastExportJobRequestRequestTypeDef,
):
    pass


_RequiredCreatePredictorBacktestExportJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePredictorBacktestExportJobRequestRequestTypeDef",
    {
        "PredictorBacktestExportJobName": str,
        "PredictorArn": str,
        "Destination": DataDestinationTypeDef,
    },
)
_OptionalCreatePredictorBacktestExportJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePredictorBacktestExportJobRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "Format": str,
    },
    total=False,
)


class CreatePredictorBacktestExportJobRequestRequestTypeDef(
    _RequiredCreatePredictorBacktestExportJobRequestRequestTypeDef,
    _OptionalCreatePredictorBacktestExportJobRequestRequestTypeDef,
):
    pass


_RequiredCreateWhatIfForecastExportRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWhatIfForecastExportRequestRequestTypeDef",
    {
        "WhatIfForecastExportName": str,
        "WhatIfForecastArns": Sequence[str],
        "Destination": DataDestinationTypeDef,
    },
)
_OptionalCreateWhatIfForecastExportRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWhatIfForecastExportRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
        "Format": str,
    },
    total=False,
)


class CreateWhatIfForecastExportRequestRequestTypeDef(
    _RequiredCreateWhatIfForecastExportRequestRequestTypeDef,
    _OptionalCreateWhatIfForecastExportRequestRequestTypeDef,
):
    pass


DescribeExplainabilityExportResponseTypeDef = TypedDict(
    "DescribeExplainabilityExportResponseTypeDef",
    {
        "ExplainabilityExportArn": str,
        "ExplainabilityExportName": str,
        "ExplainabilityArn": str,
        "Destination": DataDestinationTypeDef,
        "Message": str,
        "Status": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "Format": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeForecastExportJobResponseTypeDef = TypedDict(
    "DescribeForecastExportJobResponseTypeDef",
    {
        "ForecastExportJobArn": str,
        "ForecastExportJobName": str,
        "ForecastArn": str,
        "Destination": DataDestinationTypeDef,
        "Message": str,
        "Status": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "Format": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribePredictorBacktestExportJobResponseTypeDef = TypedDict(
    "DescribePredictorBacktestExportJobResponseTypeDef",
    {
        "PredictorBacktestExportJobArn": str,
        "PredictorBacktestExportJobName": str,
        "PredictorArn": str,
        "Destination": DataDestinationTypeDef,
        "Message": str,
        "Status": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "Format": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeWhatIfForecastExportResponseTypeDef = TypedDict(
    "DescribeWhatIfForecastExportResponseTypeDef",
    {
        "WhatIfForecastExportArn": str,
        "WhatIfForecastExportName": str,
        "WhatIfForecastArns": List[str],
        "Destination": DataDestinationTypeDef,
        "Message": str,
        "Status": str,
        "CreationTime": datetime,
        "EstimatedTimeRemainingInMinutes": int,
        "LastModificationTime": datetime,
        "Format": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ExplainabilityExportSummaryTypeDef = TypedDict(
    "ExplainabilityExportSummaryTypeDef",
    {
        "ExplainabilityExportArn": str,
        "ExplainabilityExportName": str,
        "Destination": DataDestinationTypeDef,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

ForecastExportJobSummaryTypeDef = TypedDict(
    "ForecastExportJobSummaryTypeDef",
    {
        "ForecastExportJobArn": str,
        "ForecastExportJobName": str,
        "Destination": DataDestinationTypeDef,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

PredictorBacktestExportJobSummaryTypeDef = TypedDict(
    "PredictorBacktestExportJobSummaryTypeDef",
    {
        "PredictorBacktestExportJobArn": str,
        "PredictorBacktestExportJobName": str,
        "Destination": DataDestinationTypeDef,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

WhatIfForecastExportSummaryTypeDef = TypedDict(
    "WhatIfForecastExportSummaryTypeDef",
    {
        "WhatIfForecastExportArn": str,
        "WhatIfForecastArns": List[str],
        "WhatIfForecastExportName": str,
        "Destination": DataDestinationTypeDef,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

_RequiredCreateDatasetImportJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetImportJobRequestRequestTypeDef",
    {
        "DatasetImportJobName": str,
        "DatasetArn": str,
        "DataSource": DataSourceTypeDef,
    },
)
_OptionalCreateDatasetImportJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetImportJobRequestRequestTypeDef",
    {
        "TimestampFormat": str,
        "TimeZone": str,
        "UseGeolocationForTimeZone": bool,
        "GeolocationFormat": str,
        "Tags": Sequence[TagTypeDef],
        "Format": str,
        "ImportMode": ImportModeType,
    },
    total=False,
)


class CreateDatasetImportJobRequestRequestTypeDef(
    _RequiredCreateDatasetImportJobRequestRequestTypeDef,
    _OptionalCreateDatasetImportJobRequestRequestTypeDef,
):
    pass


DatasetImportJobSummaryTypeDef = TypedDict(
    "DatasetImportJobSummaryTypeDef",
    {
        "DatasetImportJobArn": str,
        "DatasetImportJobName": str,
        "DataSource": DataSourceTypeDef,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "ImportMode": ImportModeType,
    },
    total=False,
)

DescribeDatasetImportJobResponseTypeDef = TypedDict(
    "DescribeDatasetImportJobResponseTypeDef",
    {
        "DatasetImportJobName": str,
        "DatasetImportJobArn": str,
        "DatasetArn": str,
        "TimestampFormat": str,
        "TimeZone": str,
        "UseGeolocationForTimeZone": bool,
        "GeolocationFormat": str,
        "DataSource": DataSourceTypeDef,
        "EstimatedTimeRemainingInMinutes": int,
        "FieldStatistics": Dict[str, StatisticsTypeDef],
        "DataSize": float,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "Format": str,
        "ImportMode": ImportModeType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPredictorsResponseTypeDef = TypedDict(
    "ListPredictorsResponseTypeDef",
    {
        "Predictors": List[PredictorSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredFeaturizationConfigTypeDef = TypedDict(
    "_RequiredFeaturizationConfigTypeDef",
    {
        "ForecastFrequency": str,
    },
)
_OptionalFeaturizationConfigTypeDef = TypedDict(
    "_OptionalFeaturizationConfigTypeDef",
    {
        "ForecastDimensions": Sequence[str],
        "Featurizations": Sequence[FeaturizationTypeDef],
    },
    total=False,
)


class FeaturizationConfigTypeDef(
    _RequiredFeaturizationConfigTypeDef, _OptionalFeaturizationConfigTypeDef
):
    pass


HyperParameterTuningJobConfigTypeDef = TypedDict(
    "HyperParameterTuningJobConfigTypeDef",
    {
        "ParameterRanges": ParameterRangesTypeDef,
    },
    total=False,
)

WindowSummaryTypeDef = TypedDict(
    "WindowSummaryTypeDef",
    {
        "TestWindowStart": datetime,
        "TestWindowEnd": datetime,
        "ItemCount": int,
        "EvaluationType": EvaluationTypeType,
        "Metrics": MetricsTypeDef,
    },
    total=False,
)

ListMonitorEvaluationsResponseTypeDef = TypedDict(
    "ListMonitorEvaluationsResponseTypeDef",
    {
        "NextToken": str,
        "PredictorMonitorEvaluations": List[PredictorMonitorEvaluationTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PredictorExecutionDetailsTypeDef = TypedDict(
    "PredictorExecutionDetailsTypeDef",
    {
        "PredictorExecutions": List[PredictorExecutionTypeDef],
    },
    total=False,
)

_RequiredCreateDatasetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetRequestRequestTypeDef",
    {
        "DatasetName": str,
        "Domain": DomainType,
        "DatasetType": DatasetTypeType,
        "Schema": SchemaTypeDef,
    },
)
_OptionalCreateDatasetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetRequestRequestTypeDef",
    {
        "DataFrequency": str,
        "EncryptionConfig": EncryptionConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDatasetRequestRequestTypeDef(
    _RequiredCreateDatasetRequestRequestTypeDef, _OptionalCreateDatasetRequestRequestTypeDef
):
    pass


_RequiredCreateExplainabilityRequestRequestTypeDef = TypedDict(
    "_RequiredCreateExplainabilityRequestRequestTypeDef",
    {
        "ExplainabilityName": str,
        "ResourceArn": str,
        "ExplainabilityConfig": ExplainabilityConfigTypeDef,
    },
)
_OptionalCreateExplainabilityRequestRequestTypeDef = TypedDict(
    "_OptionalCreateExplainabilityRequestRequestTypeDef",
    {
        "DataSource": DataSourceTypeDef,
        "Schema": SchemaTypeDef,
        "EnableVisualization": bool,
        "StartDateTime": str,
        "EndDateTime": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateExplainabilityRequestRequestTypeDef(
    _RequiredCreateExplainabilityRequestRequestTypeDef,
    _OptionalCreateExplainabilityRequestRequestTypeDef,
):
    pass


DescribeDatasetResponseTypeDef = TypedDict(
    "DescribeDatasetResponseTypeDef",
    {
        "DatasetArn": str,
        "DatasetName": str,
        "Domain": DomainType,
        "DatasetType": DatasetTypeType,
        "DataFrequency": str,
        "Schema": SchemaTypeDef,
        "EncryptionConfig": EncryptionConfigTypeDef,
        "Status": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeExplainabilityResponseTypeDef = TypedDict(
    "DescribeExplainabilityResponseTypeDef",
    {
        "ExplainabilityArn": str,
        "ExplainabilityName": str,
        "ResourceArn": str,
        "ExplainabilityConfig": ExplainabilityConfigTypeDef,
        "EnableVisualization": bool,
        "DataSource": DataSourceTypeDef,
        "Schema": SchemaTypeDef,
        "StartDateTime": str,
        "EndDateTime": str,
        "EstimatedTimeRemainingInMinutes": int,
        "Message": str,
        "Status": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TimeSeriesIdentifiersTypeDef = TypedDict(
    "TimeSeriesIdentifiersTypeDef",
    {
        "DataSource": DataSourceTypeDef,
        "Schema": SchemaTypeDef,
        "Format": str,
    },
    total=False,
)

_RequiredTimeSeriesReplacementsDataSourceTypeDef = TypedDict(
    "_RequiredTimeSeriesReplacementsDataSourceTypeDef",
    {
        "S3Config": S3ConfigTypeDef,
        "Schema": SchemaTypeDef,
    },
)
_OptionalTimeSeriesReplacementsDataSourceTypeDef = TypedDict(
    "_OptionalTimeSeriesReplacementsDataSourceTypeDef",
    {
        "Format": str,
        "TimestampFormat": str,
    },
    total=False,
)


class TimeSeriesReplacementsDataSourceTypeDef(
    _RequiredTimeSeriesReplacementsDataSourceTypeDef,
    _OptionalTimeSeriesReplacementsDataSourceTypeDef,
):
    pass


DescribeMonitorResponseTypeDef = TypedDict(
    "DescribeMonitorResponseTypeDef",
    {
        "MonitorName": str,
        "MonitorArn": str,
        "ResourceArn": str,
        "Status": str,
        "LastEvaluationTime": datetime,
        "LastEvaluationState": str,
        "Baseline": BaselineTypeDef,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "EstimatedEvaluationTimeRemainingInMinutes": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListExplainabilityExportsResponseTypeDef = TypedDict(
    "ListExplainabilityExportsResponseTypeDef",
    {
        "ExplainabilityExports": List[ExplainabilityExportSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListForecastExportJobsResponseTypeDef = TypedDict(
    "ListForecastExportJobsResponseTypeDef",
    {
        "ForecastExportJobs": List[ForecastExportJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPredictorBacktestExportJobsResponseTypeDef = TypedDict(
    "ListPredictorBacktestExportJobsResponseTypeDef",
    {
        "PredictorBacktestExportJobs": List[PredictorBacktestExportJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListWhatIfForecastExportsResponseTypeDef = TypedDict(
    "ListWhatIfForecastExportsResponseTypeDef",
    {
        "WhatIfForecastExports": List[WhatIfForecastExportSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDatasetImportJobsResponseTypeDef = TypedDict(
    "ListDatasetImportJobsResponseTypeDef",
    {
        "DatasetImportJobs": List[DatasetImportJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreatePredictorRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePredictorRequestRequestTypeDef",
    {
        "PredictorName": str,
        "ForecastHorizon": int,
        "InputDataConfig": InputDataConfigTypeDef,
        "FeaturizationConfig": FeaturizationConfigTypeDef,
    },
)
_OptionalCreatePredictorRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePredictorRequestRequestTypeDef",
    {
        "AlgorithmArn": str,
        "ForecastTypes": Sequence[str],
        "PerformAutoML": bool,
        "AutoMLOverrideStrategy": AutoMLOverrideStrategyType,
        "PerformHPO": bool,
        "TrainingParameters": Mapping[str, str],
        "EvaluationParameters": EvaluationParametersTypeDef,
        "HPOConfig": HyperParameterTuningJobConfigTypeDef,
        "EncryptionConfig": EncryptionConfigTypeDef,
        "Tags": Sequence[TagTypeDef],
        "OptimizationMetric": OptimizationMetricType,
    },
    total=False,
)


class CreatePredictorRequestRequestTypeDef(
    _RequiredCreatePredictorRequestRequestTypeDef, _OptionalCreatePredictorRequestRequestTypeDef
):
    pass


EvaluationResultTypeDef = TypedDict(
    "EvaluationResultTypeDef",
    {
        "AlgorithmArn": str,
        "TestWindows": List[WindowSummaryTypeDef],
    },
    total=False,
)

DescribePredictorResponseTypeDef = TypedDict(
    "DescribePredictorResponseTypeDef",
    {
        "PredictorArn": str,
        "PredictorName": str,
        "AlgorithmArn": str,
        "AutoMLAlgorithmArns": List[str],
        "ForecastHorizon": int,
        "ForecastTypes": List[str],
        "PerformAutoML": bool,
        "AutoMLOverrideStrategy": AutoMLOverrideStrategyType,
        "PerformHPO": bool,
        "TrainingParameters": Dict[str, str],
        "EvaluationParameters": EvaluationParametersTypeDef,
        "HPOConfig": HyperParameterTuningJobConfigTypeDef,
        "InputDataConfig": InputDataConfigTypeDef,
        "FeaturizationConfig": FeaturizationConfigTypeDef,
        "EncryptionConfig": EncryptionConfigTypeDef,
        "PredictorExecutionDetails": PredictorExecutionDetailsTypeDef,
        "EstimatedTimeRemainingInMinutes": int,
        "IsAutoPredictor": bool,
        "DatasetImportJobArns": List[str],
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "OptimizationMetric": OptimizationMetricType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TimeSeriesSelectorTypeDef = TypedDict(
    "TimeSeriesSelectorTypeDef",
    {
        "TimeSeriesIdentifiers": TimeSeriesIdentifiersTypeDef,
    },
    total=False,
)

_RequiredCreateWhatIfForecastRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWhatIfForecastRequestRequestTypeDef",
    {
        "WhatIfForecastName": str,
        "WhatIfAnalysisArn": str,
    },
)
_OptionalCreateWhatIfForecastRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWhatIfForecastRequestRequestTypeDef",
    {
        "TimeSeriesTransformations": Sequence[TimeSeriesTransformationTypeDef],
        "TimeSeriesReplacementsDataSource": TimeSeriesReplacementsDataSourceTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateWhatIfForecastRequestRequestTypeDef(
    _RequiredCreateWhatIfForecastRequestRequestTypeDef,
    _OptionalCreateWhatIfForecastRequestRequestTypeDef,
):
    pass


DescribeWhatIfForecastResponseTypeDef = TypedDict(
    "DescribeWhatIfForecastResponseTypeDef",
    {
        "WhatIfForecastName": str,
        "WhatIfForecastArn": str,
        "WhatIfAnalysisArn": str,
        "EstimatedTimeRemainingInMinutes": int,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "TimeSeriesTransformations": List[TimeSeriesTransformationTypeDef],
        "TimeSeriesReplacementsDataSource": TimeSeriesReplacementsDataSourceTypeDef,
        "ForecastTypes": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetAccuracyMetricsResponseTypeDef = TypedDict(
    "GetAccuracyMetricsResponseTypeDef",
    {
        "PredictorEvaluationResults": List[EvaluationResultTypeDef],
        "IsAutoPredictor": bool,
        "AutoMLOverrideStrategy": AutoMLOverrideStrategyType,
        "OptimizationMetric": OptimizationMetricType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateForecastRequestRequestTypeDef = TypedDict(
    "_RequiredCreateForecastRequestRequestTypeDef",
    {
        "ForecastName": str,
        "PredictorArn": str,
    },
)
_OptionalCreateForecastRequestRequestTypeDef = TypedDict(
    "_OptionalCreateForecastRequestRequestTypeDef",
    {
        "ForecastTypes": Sequence[str],
        "Tags": Sequence[TagTypeDef],
        "TimeSeriesSelector": TimeSeriesSelectorTypeDef,
    },
    total=False,
)


class CreateForecastRequestRequestTypeDef(
    _RequiredCreateForecastRequestRequestTypeDef, _OptionalCreateForecastRequestRequestTypeDef
):
    pass


_RequiredCreateWhatIfAnalysisRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWhatIfAnalysisRequestRequestTypeDef",
    {
        "WhatIfAnalysisName": str,
        "ForecastArn": str,
    },
)
_OptionalCreateWhatIfAnalysisRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWhatIfAnalysisRequestRequestTypeDef",
    {
        "TimeSeriesSelector": TimeSeriesSelectorTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateWhatIfAnalysisRequestRequestTypeDef(
    _RequiredCreateWhatIfAnalysisRequestRequestTypeDef,
    _OptionalCreateWhatIfAnalysisRequestRequestTypeDef,
):
    pass


DescribeForecastResponseTypeDef = TypedDict(
    "DescribeForecastResponseTypeDef",
    {
        "ForecastArn": str,
        "ForecastName": str,
        "ForecastTypes": List[str],
        "PredictorArn": str,
        "DatasetGroupArn": str,
        "EstimatedTimeRemainingInMinutes": int,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "TimeSeriesSelector": TimeSeriesSelectorTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeWhatIfAnalysisResponseTypeDef = TypedDict(
    "DescribeWhatIfAnalysisResponseTypeDef",
    {
        "WhatIfAnalysisName": str,
        "WhatIfAnalysisArn": str,
        "ForecastArn": str,
        "EstimatedTimeRemainingInMinutes": int,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
        "TimeSeriesSelector": TimeSeriesSelectorTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
