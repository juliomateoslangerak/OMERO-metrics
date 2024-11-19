import dash
import pandas as pd
from dash import dcc, html
from django_plotly_dash import DjangoDash
import plotly.express as px
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from linkml_runtime.dumpers import YAMLDumper
from skimage.exposure import rescale_intensity
from OMERO_metrics.styles import (
    THEME,
    MANTINE_THEME,
    CONTAINER_STYLE,
    HEADER_PAPER_STYLE,
    CONTENT_PAPER_STYLE,
    GRAPH_STYLE,
    PLOT_LAYOUT,
    LINE_CHART_SERIES,
    INPUT_BASE_STYLES,
    TABLE_MANTINE_STYLE,
)
import math

dashboard_name = "omero_dataset_foi"
omero_dataset_foi = DjangoDash(
    name=dashboard_name,
    serve_locally=True,
    external_stylesheets=dmc.styles.ALL,
)

omero_dataset_foi.layout = dmc.MantineProvider(
    theme=MANTINE_THEME,
    children=[
        dmc.Paper(
            children=[
                dmc.Group(
                    [
                        dmc.Group(
                            [
                                html.Img(
                                    src="/static/OMERO_metrics/images/metrics_logo.png",
                                    style={
                                        "width": "120px",
                                        "height": "auto",
                                    },
                                ),
                                dmc.Stack(
                                    [
                                        dmc.Title(
                                            "Field of Illumination Dataset Analysis",
                                            c=THEME["primary"],
                                            size="h2",
                                        ),
                                        dmc.Text(
                                            "Dataset Dashboard",
                                            c=THEME["text"]["secondary"],
                                            size="sm",
                                        ),
                                    ],
                                    gap="xs",
                                ),
                            ],
                        ),
                        dmc.Group(
                            [
                                dmc.Button(
                                    id="download_dataset_data",
                                    children="Download",
                                    color="blue",
                                    variant="filled",
                                    rightSection=DashIconify(
                                        icon="line-md:download",
                                        height=20,
                                    ),
                                ),
                                dcc.Download(id="download"),
                                dmc.Button(
                                    id="delete_dataset_data",
                                    children="Delete",
                                    color="red",
                                    variant="filled",
                                    rightSection=DashIconify(
                                        icon="line-md:document-delete-twotone",
                                        height=20,
                                    ),
                                ),
                                # dmc.Select(
                                #     data=[
                                #         "Pandas",
                                #         "NumPy",
                                #         "TensorFlow",
                                #         "PyTorch",
                                #     ],
                                #     value="Pandas",
                                #     comboboxProps={
                                #         "withinPortal": False,
                                #         "zIndex": 1000,
                                #     },
                                #     style={
                                #         "backgroundColor": THEME["primary"],
                                #         "color": "green",
                                #         "background-color": "green",
                                #     },
                                #     styles={
                                #         "root": {"backgroundColor": "red"},
                                #     },
                                # ),
                                dmc.Badge(
                                    "FOI Analysis",
                                    color=THEME["primary"],
                                    variant="dot",
                                    size="lg",
                                ),
                            ]
                        ),
                    ],
                    justify="space-between",
                ),
            ],
            **HEADER_PAPER_STYLE,
        ),
        dmc.Container(
            [
                # Header Section
                # Main Content
                dmc.Grid(
                    gutter="md",
                    align="stretch",
                    children=[
                        # Left Column - Intensity Map
                        dmc.GridCol(
                            span=6,
                            children=[
                                dmc.Paper(
                                    children=[
                                        dmc.Stack(
                                            [
                                                dmc.Group(
                                                    [
                                                        dmc.Text(
                                                            "Intensity Map",
                                                            fw=500,
                                                            size="lg",
                                                        ),
                                                        dmc.Select(
                                                            id="channel_dropdown_foi",
                                                            clearable=False,
                                                            allowDeselect=False,
                                                            w="200",
                                                            value="0",
                                                            leftSection=DashIconify(
                                                                icon="material-symbols:layers",
                                                                height=20,
                                                            ),
                                                            rightSection=DashIconify(
                                                                icon="radix-icons:chevron-down",
                                                                height=20,
                                                            ),
                                                            styles=INPUT_BASE_STYLES,
                                                        ),
                                                    ],
                                                    justify="space-between",
                                                ),
                                                dcc.Graph(
                                                    id="intensity_map",
                                                    config={
                                                        "displayModeBar": True,
                                                        "scrollZoom": True,
                                                        "modeBarButtonsToRemove": [
                                                            "lasso2d",
                                                            "select2d",
                                                        ],
                                                    },
                                                    style=GRAPH_STYLE,
                                                ),
                                            ],
                                            gap="md",
                                            justify="space-between",
                                            h="100%",
                                        ),
                                    ],
                                    **CONTENT_PAPER_STYLE,
                                ),
                            ],
                        ),
                        # Right Column - Key Measurements
                        dmc.GridCol(
                            span=6,
                            children=[
                                dmc.Paper(
                                    children=[
                                        dmc.Stack(
                                            [
                                                dmc.Group(
                                                    [
                                                        dmc.Text(
                                                            "Key Measurements",
                                                            fw=500,
                                                            size="lg",
                                                        ),
                                                        dmc.Tooltip(
                                                            label="Statistical measurements for all the channels",
                                                            children=[
                                                                DashIconify(
                                                                    icon="material-symbols:info",
                                                                    height=20,
                                                                    color=THEME[
                                                                        "primary"
                                                                    ],
                                                                )
                                                            ],
                                                        ),
                                                    ],
                                                    justify="space-between",
                                                ),
                                                dmc.ScrollArea(
                                                    offsetScrollbars=True,
                                                    children=[
                                                        dmc.Table(
                                                            id="km_table",
                                                            striped=True,
                                                            highlightOnHover=True,
                                                            withTableBorder=False,
                                                            withColumnBorders=True,
                                                            fz="sm",
                                                            style=TABLE_MANTINE_STYLE,
                                                        ),
                                                        dmc.Group(
                                                            mt="md",
                                                            children=[
                                                                dmc.Pagination(
                                                                    id="pagination",
                                                                    total=0,
                                                                    value=1,
                                                                    withEdges=True,
                                                                )
                                                            ],
                                                            justify="center",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                            gap="md",
                                            justify="space-between",
                                            h="100%",
                                        ),
                                    ],
                                    **CONTENT_PAPER_STYLE,
                                ),
                            ],
                        ),
                    ],
                ),
                # Hidden element for callbacks
                html.Div(id="blank-input"),
                # Intensity Profiles Section
                dmc.Paper(
                    children=[
                        dmc.Stack(
                            [
                                dmc.Group(
                                    [
                                        dmc.Text(
                                            "Intensity Profiles",
                                            fw=500,
                                            size="lg",
                                        ),
                                        dmc.SegmentedControl(
                                            id="profile-type",
                                            data=[
                                                {
                                                    "value": "natural",
                                                    "label": "Smooth",
                                                },
                                                {
                                                    "value": "linear",
                                                    "label": "Linear",
                                                },
                                            ],
                                            value="natural",
                                            color=THEME["primary"],
                                        ),
                                    ],
                                    justify="space-between",
                                ),
                                dmc.LineChart(
                                    id="intensity_profile",
                                    h=300,
                                    dataKey="Pixel",
                                    data={},
                                    series=LINE_CHART_SERIES,
                                    xAxisLabel="Position (pixels)",
                                    yAxisLabel="Intensity",
                                    tickLine="y",
                                    gridAxis="x",
                                    withXAxis=True,
                                    withYAxis=True,
                                    withLegend=True,
                                    strokeWidth=2,
                                    withDots=False,
                                ),
                            ],
                            gap="xl",
                        ),
                    ],
                    shadow="xs",
                    p="md",
                    radius="md",
                    mt="md",
                ),
            ],
            size="xl",
            p="md",
            style=CONTAINER_STYLE,
        ),
    ],
)


@omero_dataset_foi.expanded_callback(
    dash.dependencies.Output("channel_dropdown_foi", "data"),
    [dash.dependencies.Input("blank-input", "children")],
)
def update_dropdown_menu(*args, **kwargs):
    try:
        channel = kwargs["session_state"]["context"]["channel_names"]
        return [
            {"label": f"{name}", "value": f"{i}"}
            for i, name in enumerate(channel)
        ]
    except Exception as e:
        return [{"label": "Error loading channels", "value": "0"}]


@omero_dataset_foi.expanded_callback(
    dash.dependencies.Output("km_table", "data"),
    dash.dependencies.Output("pagination", "total"),
    [
        dash.dependencies.Input("pagination", "value"),
    ],
)
def update_km_table(*args, **kwargs):
    try:
        page = int(args[0])
        table = kwargs["session_state"]["context"]["key_values_df"]
        start_idx = (page - 1) * 4
        end_idx = start_idx + 4
        metrics_df = table[
            [
                "channel_name",
                "center_region_intensity_fraction",
                "center_region_area_fraction",
                "max_intensity",
            ]
        ].copy()

        metrics_df = metrics_df.round(3)
        metrics_df.columns = metrics_df.columns.str.replace(
            "_", " ", regex=True
        ).str.title()
        page_data = metrics_df.iloc[start_idx:end_idx]
        return {
            "head": page_data.columns.tolist(),
            "body": page_data.values.tolist(),
            "caption": "Statistical measurements across channels",
        }, math.ceil(len(metrics_df) / 4)
    except Exception as e:
        return {
            "head": ["Error"],
            "body": [[str(e)]],
            "caption": "Error loading measurements",
        }, 1


@omero_dataset_foi.expanded_callback(
    dash.dependencies.Output("intensity_map", "figure"),
    [
        dash.dependencies.Input("channel_dropdown_foi", "value"),
    ],
)
def update_intensity_map(*args, **kwargs):
    try:
        channel = int(args[0])
        images = kwargs["session_state"]["context"]["image"]
        image = images[channel]
        image_channel = image[0, 0, :, :]
        image_channel = rescale_intensity(
            image_channel,
            in_range=(0, image_channel.max()),
            out_range=(0.0, 1.0),
        )
        # Create intensity map
        fig = px.imshow(
            image_channel,
            color_continuous_scale="hot",
            labels={"color": "Intensity"},
        )
        fig.update_layout(
            **PLOT_LAYOUT,
            xaxis_title="X Position (pixels)",
            yaxis_title="Y Position (pixels)",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            coloraxis_colorbar=dict(
                thickness=15,
                len=0.7,
                title=dict(text="Intensity", side="right"),
                tickfont=dict(size=10),
            ),
        )
        return fig
    except Exception as e:
        fig = px.imshow([[0]])
        fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig


@omero_dataset_foi.expanded_callback(
    dash.dependencies.Output("intensity_profile", "data"),
    dash.dependencies.Output("intensity_profile", "curveType"),
    [
        dash.dependencies.Input("channel_dropdown_foi", "value"),
        dash.dependencies.Input("profile-type", "value"),
    ],
)
def update_profile_type(*args, **kwargs):
    try:
        channel = int(args[0])
        curveType = args[1]
        df_intensity_profiles = kwargs["session_state"]["context"][
            "intensity_profiles"
        ]
        channel_regex = f"ch{channel:02d}"
        df_profile = df_intensity_profiles[
            df_intensity_profiles.columns[
                df_intensity_profiles.columns.str.startswith(channel_regex)
            ]
        ].copy()

        df_profile.columns = df_profile.columns.str.replace(
            "ch\d{2}_", "", regex=True
        )
        df_profile = restyle_dataframe(df_profile, "columns")
        df_profile = df_profile.reset_index()
        df_profile.columns = df_profile.columns.str.replace(
            "Lefttop To Rightbottom", "Diagonal (↘)"
        )
        df_profile.columns = df_profile.columns.str.replace(
            "Leftbottom To Righttop", "Diagonal (↗)"
        )
        df_profile.columns = df_profile.columns.str.replace(
            "Center Horizontal", "Horizontal (→)"
        )
        df_profile.columns = df_profile.columns.str.replace(
            "Center Vertical", "Vertical (↓)"
        )
        return df_profile.to_dict("records"), curveType

    except Exception as e:
        return [{"Pixel": 0}], "natural"


def restyle_dataframe(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Improve column names for better readability."""
    value = getattr(df, col).str.replace("_", " ", regex=True).str.title()
    setattr(df, col, value)
    return df


@omero_dataset_foi.expanded_callback(
    dash.dependencies.Output("download", "data"),
    [dash.dependencies.Input("download_dataset_data", "n_clicks")],
    prevent_initial_call=True,
)
def download_dataset_data(*args, **kwargs):
    mm_dataset = kwargs["session_state"]["context"]["mm_dataset"]
    dumper = YAMLDumper()
    return dict(content=dumper.dumps(mm_dataset), filename="dataset.yaml")
