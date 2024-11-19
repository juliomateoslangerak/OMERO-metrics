import dash
from dash import dcc, html
from django_plotly_dash import DjangoDash
import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import logging
import pandas as pd
from dash_iconify import DashIconify

from OMERO_metrics.tools.data_preperation import (
    crop_bead_index,
    mip_graphs,
    fig_mip,
)
from OMERO_metrics.styles import THEME, MANTINE_THEME, HEADER_PAPER_STYLE


def get_icon(icon, size=20, color=None):
    return DashIconify(icon=icon, height=size, color=color)


logger = logging.getLogger(__name__)
dashboard_name = "omero_image_psf_beads"

omero_image_psf_beads = DjangoDash(
    name=dashboard_name, external_scripts=dmc.styles.ALL
)

omero_image_psf_beads.layout = dmc.MantineProvider(
    theme=MANTINE_THEME,
    children=[
        # Header Section
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
                                            "PSF Beads Analysis",
                                            c=THEME["primary"],
                                            size="h2",
                                        ),
                                        dmc.Text(
                                            "Advanced Microscopy Image Analysis",
                                            c=THEME["text"]["secondary"],
                                            size="sm",
                                        ),
                                    ],
                                    gap="xs",
                                ),
                            ],
                            gap="md",
                        ),
                        dmc.Badge(
                            "Interactive Analysis",
                            color=THEME["primary"],
                            variant="dot",
                            size="lg",
                        ),
                    ],
                    justify="space-between",
                ),
            ],
            **HEADER_PAPER_STYLE,
        ),
        # Main Content
        dmc.Container(
            [
                html.Div(id="blank-input"),
                # Main Content
                dmc.Stack(
                    [
                        dmc.Grid(
                            children=[
                                dmc.GridCol(
                                    [
                                        dmc.Paper(
                                            [
                                                dmc.Group(
                                                    [
                                                        dmc.Text(
                                                            "Bead Distribution Map",
                                                            size="lg",
                                                            fw=500,
                                                            c=THEME["primary"],
                                                        ),
                                                        dmc.Tooltip(
                                                            label="Click on a bead in the image to view its MIP",
                                                            children=[
                                                                get_icon(
                                                                    "material-symbols:info",
                                                                    color=THEME[
                                                                        "primary"
                                                                    ],
                                                                )
                                                            ],
                                                        ),
                                                    ],
                                                    justify="space-between",
                                                ),
                                                dcc.Graph(
                                                    figure={},
                                                    style={"height": "400px"},
                                                    id="psf_image_graph",
                                                ),
                                            ],
                                            p="md",
                                            radius="md",
                                            withBorder=True,
                                            shadow="sm",
                                            h="100%",
                                        ),
                                    ],
                                    span=8,
                                ),
                                dmc.GridCol(
                                    [
                                        dmc.Paper(
                                            h="100%",
                                            shadow="xs",
                                            p="md",
                                            radius="md",
                                            children=[
                                                dmc.Stack(
                                                    [
                                                        dmc.Text(
                                                            "Visualization Controls",
                                                            size="lg",
                                                            fw=500,
                                                            c=THEME["primary"],
                                                        ),
                                                        dmc.Divider(
                                                            label="Channel Selection",
                                                            labelPosition="center",
                                                        ),
                                                        dmc.Select(
                                                            id="channel_selector_psf_image",
                                                            label="Channel",
                                                            w="100%",
                                                            value="0",
                                                            allowDeselect=False,
                                                            leftSection=get_icon(
                                                                "material-symbols:layers"
                                                            ),
                                                            rightSection=get_icon(
                                                                "radix-icons:chevron-down"
                                                            ),
                                                        ),
                                                        dmc.Divider(
                                                            label="Display Options",
                                                            labelPosition="center",
                                                            mt="md",
                                                        ),
                                                        dmc.SegmentedControl(
                                                            id="beads_info_segmented",
                                                            value="beads_info",
                                                            data=[
                                                                {
                                                                    "value": "beads_info",
                                                                    "label": "Show Beads",
                                                                },
                                                                {
                                                                    "value": "None",
                                                                    "label": "Hide Beads",
                                                                },
                                                            ],
                                                            fullWidth=True,
                                                            color=THEME[
                                                                "primary"
                                                            ],
                                                            # w='auto'
                                                        ),
                                                        dmc.Stack(
                                                            [
                                                                dmc.Checkbox(
                                                                    id="contour_checkbox_psf_image",
                                                                    label="Enable Contour View",
                                                                    checked=False,
                                                                    color=THEME[
                                                                        "primary"
                                                                    ],
                                                                ),
                                                                dmc.Checkbox(
                                                                    id="roi_checkbox_psf_image",
                                                                    label="Show ROI Boundaries",
                                                                    checked=False,
                                                                    color=THEME[
                                                                        "primary"
                                                                    ],
                                                                ),
                                                            ],
                                                            gap="xs",
                                                        ),
                                                        dmc.Divider(
                                                            label="Color Settings",
                                                            labelPosition="center",
                                                            mt="md",
                                                        ),
                                                        dmc.Select(
                                                            id="color_selector_psf_image",
                                                            label="Color Scheme",
                                                            allowDeselect=False,
                                                            data=[
                                                                {
                                                                    "value": "Hot",
                                                                    "label": "Hot",
                                                                },
                                                                {
                                                                    "value": "Viridis",
                                                                    "label": "Viridis",
                                                                },
                                                                {
                                                                    "value": "Inferno",
                                                                    "label": "Inferno",
                                                                },
                                                            ],
                                                            value="Hot",
                                                            leftSection=get_icon(
                                                                "material-symbols:palette"
                                                            ),
                                                            rightSection=get_icon(
                                                                "radix-icons:chevron-down"
                                                            ),
                                                        ),
                                                        dmc.Switch(
                                                            id="color_switch_psf_image",
                                                            label="Invert Colors",
                                                            checked=False,
                                                            size="md",
                                                            color=THEME[
                                                                "primary"
                                                            ],
                                                        ),
                                                    ],
                                                    gap="sm",
                                                ),
                                            ],
                                        ),
                                    ],
                                    span=4,
                                ),
                            ],
                        ),
                        dmc.Paper(
                            id="paper_mip",
                            shadow="sm",
                            p="md",
                            radius="md",
                            children=[
                                dmc.Grid(
                                    [
                                        # MIP Section
                                        dmc.GridCol(
                                            [
                                                dmc.Group(
                                                    [
                                                        dmc.Text(
                                                            "Maximum Intensity Projection",
                                                            size="lg",
                                                            fw=500,
                                                            c=THEME["primary"],
                                                        ),
                                                    ],
                                                    justify="space-between",
                                                ),
                                                dcc.Graph(
                                                    id="mip_image",
                                                    figure={},
                                                    style={"height": "400px"},
                                                ),
                                            ],
                                            span=6,
                                        ),
                                        dmc.GridCol(
                                            [
                                                dmc.Stack(
                                                    [
                                                        dmc.Group(
                                                            [
                                                                dmc.Text(
                                                                    "Intensity Profiles",
                                                                    size="lg",
                                                                    fw=500,
                                                                    c=THEME[
                                                                        "primary"
                                                                    ],
                                                                ),
                                                                dmc.Select(
                                                                    data=[
                                                                        {
                                                                            "label": "X Axis",
                                                                            "value": "x",
                                                                        },
                                                                        {
                                                                            "label": "Y Axis",
                                                                            "value": "y",
                                                                        },
                                                                        {
                                                                            "label": "Z Axis",
                                                                            "value": "z",
                                                                        },
                                                                    ],
                                                                    value="x",
                                                                    allowDeselect=False,
                                                                    id="axis_image_psf",
                                                                    rightSection=get_icon(
                                                                        "radix-icons:chevron-down"
                                                                    ),
                                                                    leftSection=get_icon(
                                                                        icon="mdi:axis-x-arrow"
                                                                    ),
                                                                ),
                                                            ],
                                                            justify="space-between",
                                                        ),
                                                        dcc.Graph(
                                                            id="mip_chart_image",
                                                            figure={},
                                                            style={
                                                                "height": "400px"
                                                            },
                                                        ),
                                                    ],
                                                    gap="md",
                                                ),
                                            ],
                                            span=6,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                    gap="md",
                ),
            ],
            size="xl",
            p="md",
            style={"backgroundColor": THEME["surface"]},
        ),
    ],
)


@omero_image_psf_beads.expanded_callback(
    dash.dependencies.Output("axis_image_psf", "leftSection"),
    [dash.dependencies.Input("axis_image_psf", "value")],
)
def update_icon(*args, **kwargs):
    icon = f"mdi:axis-{args[0]}-arrow"
    return get_icon(icon=icon)


@omero_image_psf_beads.expanded_callback(
    dash.dependencies.Output("psf_image_graph", "figure"),
    [
        dash.dependencies.Input("channel_selector_psf_image", "value"),
        dash.dependencies.Input("color_selector_psf_image", "value"),
        dash.dependencies.Input("color_switch_psf_image", "checked"),
        dash.dependencies.Input("contour_checkbox_psf_image", "checked"),
        dash.dependencies.Input("roi_checkbox_psf_image", "checked"),
        dash.dependencies.Input("beads_info_segmented", "value"),
    ],
)
def update_image(*args, **kwargs):
    try:
        image_omero = kwargs["session_state"]["context"]["image"]
        channel_index = int(args[0])
        color = args[1]
        invert = args[2]
        contour = args[3]
        roi = args[4]
        beads_info = args[5]

        min_distance = kwargs["session_state"]["context"]["min_distance"]
        bead_properties_df = kwargs["session_state"]["context"][
            "bead_properties_df"
        ]

        df_beads_location = bead_properties_df[
            bead_properties_df["channel_nr"] == channel_index
        ][
            [
                "channel_nr",
                "bead_id",
                "considered_axial_edge",
                "considered_valid",
                "considered_self_proximity",
                "considered_lateral_edge",
                "considered_intensity_outlier",
                "center_z",
                "center_y",
                "center_x",
            ]
        ].copy()

        beads, roi_rect = get_beads_info(df_beads_location, min_distance)

        if invert:
            color = color + "_r"

        stack = image_omero[0, :, :, :, channel_index]
        mip_z = np.max(stack, axis=0)

        fig = px.imshow(
            mip_z,
            zmin=mip_z.min(),
            zmax=mip_z.max(),
            color_continuous_scale=color,
        )

        fig.add_trace(beads)

        if roi:
            fig.update_layout(shapes=roi_rect)
        else:
            fig.update_layout(shapes=None)

        if contour:
            fig.plotly_restyle({"type": "contour"}, 0)
            fig.update_yaxes(autorange="reversed")

        if beads_info == "beads_info":
            fig.update_traces(
                visible=True, selector=dict(name="Beads Locations")
            )
        else:
            fig.update_traces(
                visible=False, selector=dict(name="Beads Locations")
            )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False),
            xaxis1=dict(showgrid=False, zeroline=False, visible=False),
            yaxis1=dict(showgrid=False, zeroline=False, visible=False),
            coloraxis_colorbar=dict(
                thickness=15,
                len=0.7,
                title=dict(text="Intensity", side="right"),
                tickfont=dict(size=10),
            ),
        )

        return fig

    except Exception as e:
        logger.error(f"Error updating image: {str(e)}")
        return px.imshow([[0]], title="Error loading image")


@omero_image_psf_beads.expanded_callback(
    dash.dependencies.Output("channel_selector_psf_image", "data"),
    [dash.dependencies.Input("blank-input", "children")],
)
def update_channels_psf_image(*args, **kwargs):
    channel_names = kwargs["session_state"]["context"]["channel_names"]
    channel_options = [
        {"label": c.name, "value": f"{i}"}
        for i, c in enumerate(channel_names.channels)
    ]
    return channel_options


@omero_image_psf_beads.expanded_callback(
    dash.dependencies.Output("mip_image", "figure"),
    dash.dependencies.Output("mip_chart_image", "figure"),
    [
        dash.dependencies.Input("psf_image_graph", "clickData"),
        dash.dependencies.Input("axis_image_psf", "value"),
        dash.dependencies.Input("channel_selector_psf_image", "value"),
    ],
    prevent_initial_call=True,
)
def callback_mip(*args, **kwargs):
    point = args[0]["points"][0]
    axis = args[1].lower()
    channel_index = int(args[2])
    stack = kwargs["session_state"]["context"]["image"][
        0, :, :, :, channel_index
    ]
    bead_properties_df = kwargs["session_state"]["context"][
        "bead_properties_df"
    ]
    df_beads_location = bead_properties_df[
        bead_properties_df["channel_nr"] == channel_index
    ][
        [
            "channel_nr",
            "bead_id",
            "considered_axial_edge",
            "center_z",
            "center_x",
            "center_y",
        ]
    ].copy()
    min_dist = int(kwargs["session_state"]["context"]["min_distance"])
    if point["curveNumber"] == 1:
        bead_index = point["pointNumber"]
        # title = (
        #     f"MIP for bead number: {bead_index} in channel: {channel_index}"
        # )
        bead = df_beads_location[
            df_beads_location["bead_id"] == bead_index
        ].copy()
        x0, xf, y0, yf = crop_bead_index(bead, min_dist, stack)
        mip_x, mip_y, mip_z = mip_graphs(x0, xf, y0, yf, stack)
        fig_mip_go = fig_mip(mip_x, mip_y, mip_z)
        fig_mip_go.update_layout(
            coloraxis={
                "colorbar": dict(
                    thickness=15,
                    len=0.7,
                    title=dict(text="Intensity", side="right"),
                    tickfont=dict(size=10),
                ),
            },
            margin={"l": 20, "r": 20, "t": 30, "b": 20},
            plot_bgcolor=THEME["background"],
            paper_bgcolor=THEME["background"],
            # xaxis_title="X Position (pixels)",
            # yaxis_title="Y Position (pixels)",
            font={"color": THEME["text"]["primary"]},
        )
        return (
            fig_mip_go,
            line_graph_axis(bead_index, channel_index, axis, kwargs),
        )
    else:
        return dash.no_update


def line_graph_axis(bead_index, channel_index, axis, kwargs):
    df_axis = kwargs["session_state"]["context"][f"bead_{axis}_profiles_df"]
    image_id = kwargs["session_state"]["context"]["image_id"]
    df_axis_3d = df_axis[
        df_axis.columns[df_axis.columns.str.startswith(str(image_id))]
    ]
    df_meta_x = pd.DataFrame(
        data=[
            [
                int(col.split("_")[-3]),
                int(col.split("_")[-4]),
                col.split("_")[-1],
                col,
            ]
            for col in df_axis_3d.columns
        ],
        columns=["bead_id", "channel_nr", "type", "name"],
    )
    cols_x = df_meta_x[
        (
            (df_meta_x["bead_id"] == bead_index)
            & (df_meta_x["channel_nr"] == channel_index)
        )
    ]["name"].values
    df_x = df_axis_3d[cols_x].copy()
    df_x.columns = df_x.columns.str.split("_").str[-1]
    fig_ip_x = px.line(df_x)
    fig_ip_x.update_traces(
        patch={"line": {"dash": "dot"}}, selector={"name": "fitted"}
    )
    fig_ip_x.update_layout(
        plot_bgcolor=THEME["background"],
        paper_bgcolor=THEME["background"],
        font={"color": THEME["text"]["primary"]},
    )
    return fig_ip_x


def get_beads_info(df, min_distance):
    color_map = {"Yes": "green", "No": "red"}
    df["considered_axial_edge"] = df["considered_axial_edge"].map(
        {"False": "No", "True": "Yes"}
    )
    df["considered_valid"] = df["considered_valid"].map(
        {"False": "No", "True": "Yes"}
    )
    df["considered_self_proximity"] = df["considered_self_proximity"].map(
        {"False": "No", "True": "Yes"}
    )
    df["considered_lateral_edge"] = df["considered_lateral_edge"].map(
        {"False": "No", "True": "Yes"}
    )
    df["considered_intensity_outlier"] = df[
        "considered_intensity_outlier"
    ].map({"False": "No", "True": "Yes"})
    df["color"] = df["considered_valid"].map(color_map)
    beads_location_plot = go.Scatter(
        y=df["center_y"],
        x=df["center_x"],
        mode="markers",
        name="Beads Locations",
        marker=dict(
            size=0.001,
            opacity=0.01,
            color=df["considered_valid"].map(color_map),
        ),
        text=df["channel_nr"],
        customdata=np.stack(
            (
                df["bead_id"],
                df["considered_axial_edge"],
                df["considered_valid"],
                df["considered_self_proximity"],
                df["considered_lateral_edge"],
                df["considered_intensity_outlier"],
            ),
            axis=-1,
        ),
        hovertemplate="<b>Bead Number:</b>  %{customdata[0]} <br>"
        + "<b>Channel Number:</b>  %{text} <br>"
        + "<b>Considered valid:</b>  %{customdata[2]}<br>"
        + "<b>Considered self proximity:</b>  %{customdata[3]}<br>"
        + "<b>Considered lateral edge:</b>  %{customdata[4]}<br>"
        + "<b>Considered intensity outlier:</b>  %{customdata[5]}<br>"
        + "<b>Considered Axial Edge:</b> %{customdata[1]} <br><extra></extra>",
    )
    corners = [
        dict(
            type="rect",
            x0=row.center_x - min_distance,
            y0=row.center_y - min_distance,
            x1=row.center_x + min_distance,
            y1=row.center_y + min_distance,
            xref="x",
            yref="y",
            line=dict(
                color=row["color"],
                width=3,
            ),
        )
        for i, row in df.iterrows()
    ]
    return beads_location_plot, corners
