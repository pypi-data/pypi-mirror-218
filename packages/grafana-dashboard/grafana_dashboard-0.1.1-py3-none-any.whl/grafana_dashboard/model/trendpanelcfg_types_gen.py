# AUTO GENERATED, PLEASE DO NOT MODIFY BY HAND
from __future__ import annotations

from typing import Union

from pydantic import Field

from grafana_dashboard.extracted_generated_common_models import *
from grafana_dashboard.utils import MyBaseModel


class AxisColorMode(Enum):
    text = 'text'
    series = 'series'


class AxisPlacement(Enum):
    auto = 'auto'
    top = 'top'
    right = 'right'
    bottom = 'bottom'
    left = 'left'
    hidden = 'hidden'


class BarAlignment(Enum):
    integer__1 = -1
    integer_0 = 0
    integer_1 = 1


class BarConfig(MyBaseModel):
    barAlignment: Optional[BarAlignment] = None
    barWidthFactor: Optional[float] = None
    barMaxWidth: Optional[float] = None


class FillConfig(MyBaseModel):
    fillColor: Optional[str] = None
    fillOpacity: Optional[float] = None
    fillBelowTo: Optional[str] = None


class GraphDrawStyle(Enum):
    line = 'line'
    bars = 'bars'
    points = 'points'


class GraphGradientMode(Enum):
    none = 'none'
    opacity = 'opacity'
    hue = 'hue'
    scheme = 'scheme'


class GraphTransform(Enum):
    constant = 'constant'
    negative_Y = 'negative-Y'


class GraphTresholdsStyleMode(Enum):
    off = 'off'
    line = 'line'
    dashed = 'dashed'
    area = 'area'
    line_area = 'line+area'
    dashed_area = 'dashed+area'
    series = 'series'


class HideSeriesConfig(MyBaseModel):
    tooltip: bool
    legend: bool
    viz: bool


class HideableFieldConfig(MyBaseModel):
    hideFrom: Optional[HideSeriesConfig] = None


class LineInterpolation(Enum):
    linear = 'linear'
    smooth = 'smooth'
    stepBefore = 'stepBefore'
    stepAfter = 'stepAfter'


class Fill(Enum):
    solid = 'solid'
    dash = 'dash'
    dot = 'dot'
    square = 'square'


class LineStyle(MyBaseModel):
    fill: Optional[Fill] = None
    dash: Optional[List[float]] = None


class ScaleDistribution(Enum):
    linear = 'linear'
    log = 'log'
    ordinal = 'ordinal'
    symlog = 'symlog'


class ScaleDistributionConfig(MyBaseModel):
    type: ScaleDistribution
    log: Optional[float] = None
    linearThreshold: Optional[float] = None


class StackingMode(Enum):
    none = 'none'
    normal = 'normal'
    percent = 'percent'


class VisibilityMode(Enum):
    auto = 'auto'
    never = 'never'
    always = 'always'


class AxisConfig(MyBaseModel):
    axisPlacement: Optional[AxisPlacement] = None
    axisColorMode: Optional[AxisColorMode] = None
    axisLabel: Optional[str] = None
    axisWidth: Optional[float] = None
    axisSoftMin: Optional[float] = None
    axisSoftMax: Optional[float] = None
    axisGridShow: Optional[bool] = None
    scaleDistribution: Optional[ScaleDistributionConfig] = None
    axisCenteredZero: Optional[bool] = None


class GraphThresholdsStyleConfig(MyBaseModel):
    mode: GraphTresholdsStyleMode


class LineConfig(MyBaseModel):
    lineColor: Optional[str] = None
    lineWidth: Optional[float] = None
    lineInterpolation: Optional[LineInterpolation] = None
    lineStyle: Optional[LineStyle] = None
    spanNulls: Optional[Union[bool, float]] = Field(
        None,
        description='Indicate if null values should be treated as gaps or connected.\nWhen the value is a number, it represents the maximum delta in the\nX axis that should be considered connected.  For timeseries, this is milliseconds',
    )


class PointsConfig(MyBaseModel):
    showPoints: Optional[VisibilityMode] = None
    pointSize: Optional[float] = None
    pointColor: Optional[str] = None
    pointSymbol: Optional[str] = None


class StackingConfig(MyBaseModel):
    mode: Optional[StackingMode] = None
    group: Optional[str] = None


class PanelOptions(MyBaseModel):
    legend: VizLegendOptions
    tooltip: VizTooltipOptions
    xField: Optional[str] = Field(
        None, description='Name of the x field to use (defaults to first number)'
    )


class StackableFieldConfig(MyBaseModel):
    stacking: Optional[StackingConfig] = None


class GraphFieldConfig(
    LineConfig,
    FillConfig,
    PointsConfig,
    AxisConfig,
    BarConfig,
    StackableFieldConfig,
    HideableFieldConfig,
):
    drawStyle: Optional[GraphDrawStyle] = None
    gradientMode: Optional[GraphGradientMode] = None
    thresholdsStyle: Optional[GraphThresholdsStyleConfig] = None
    transform: Optional[GraphTransform] = None


class TrendPanelCfg(MyBaseModel):
    PanelOptions: PanelOptions = Field(
        ...,
        description='Identical to timeseries... except it does not have timezone settings',
    )
    PanelFieldConfig: GraphFieldConfig
