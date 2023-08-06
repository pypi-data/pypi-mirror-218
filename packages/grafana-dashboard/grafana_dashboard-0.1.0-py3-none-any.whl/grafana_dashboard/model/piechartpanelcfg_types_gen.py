# AUTO GENERATED, PLEASE DO NOT MODIFY BY HAND
from __future__ import annotations

from pydantic import Field

from grafana_dashboard.extracted_generated_common_models import *
from grafana_dashboard.utils import MyBaseModel


class HideSeriesConfig(MyBaseModel):
    tooltip: bool
    legend: bool
    viz: bool


class HideableFieldConfig(MyBaseModel):
    hideFrom: Optional[HideSeriesConfig] = None


class PieChartLabels(Enum):
    name = 'name'
    value = 'value'
    percent = 'percent'


class PieChartLegendValues(Enum):
    value = 'value'
    percent = 'percent'


class PieChartType(Enum):
    pie = 'pie'
    donut = 'donut'


class ReduceDataOptions(MyBaseModel):
    values: Optional[bool] = Field(None, description='If true show each row value')
    limit: Optional[float] = Field(None, description='if showing all values limit')
    calcs: List[str] = Field(
        [], description='When !values, pick one value for the whole field'  # NOTE MODIFIED
    )
    fields: Optional[str] = Field(
        None,
        description='Which fields to show.  By default this is only numeric fields',
    )


class VizOrientation(Enum):
    auto = 'auto'
    vertical = 'vertical'
    horizontal = 'horizontal'


class VizTextDisplayOptions(MyBaseModel):
    titleSize: Optional[float] = Field(None, description='Explicit title text size')
    valueSize: Optional[float] = Field(None, description='Explicit value text size')


class OptionsWithTextFormatting(MyBaseModel):
    text: Optional[VizTextDisplayOptions] = None


class OptionsWithTooltip(MyBaseModel):
    tooltip: VizTooltipOptions = VizTooltipOptions()  # NOTE MODIFIED


class PieChartLegendOptions(VizLegendOptions):
    values: List[PieChartLegendValues] = []  # NOTE MODIFIED


class SingleStatBaseOptions(OptionsWithTextFormatting):
    reduceOptions: Optional[ReduceDataOptions] = ReduceDataOptions()  # NOTE MODIFIED
    orientation: Optional[VizOrientation] = None  # NOTE MODIFIED


class PanelOptions(OptionsWithTooltip, SingleStatBaseOptions):
    pieType: PieChartType = PieChartType.pie  # NOTE MODIFIED
    displayLabels: List[PieChartLabels] = []  # NOTE MODIFIED
    legend: PieChartLegendOptions = PieChartLegendOptions()  # NOTE MODIFIED


class PieChartPanelCfg(MyBaseModel):
    PieChartType: PieChartType = Field(
        ..., description='Select the pie chart display style.'
    )
    PieChartLabels: PieChartLabels = Field(
        ...,
        description='Select labels to display on the pie chart.\n - Name - The series or field name.\n - Percent - The percentage of the whole.\n - Value - The raw numerical value.',
    )
    PieChartLegendValues: PieChartLegendValues = Field(
        ...,
        description='Select values to display in the legend.\n - Percent: The percentage of the whole.\n - Value: The raw numerical value.',
    )
    PieChartLegendOptions: PieChartLegendOptions
    PanelOptions: PanelOptions
    PanelFieldConfig: HideableFieldConfig
