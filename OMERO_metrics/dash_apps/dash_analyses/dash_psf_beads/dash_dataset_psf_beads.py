import dash
from dash import dcc, html
from django_plotly_dash import DjangoDash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from linkml_runtime.dumpers import YAMLDumper, JSONDumper
from OMERO_metrics.styles import THEME, HEADER_PAPER_STYLE, MANTINE_THEME
from OMERO_metrics import views
from time import sleep
import math
from OMERO_metrics.styles import TABLE_MANTINE_STYLE
import OMERO_metrics.dash_apps.dash_utils.omero_metrics_components as my_components
from OMERO_metrics.tools import load


def get_icon(icon, size=20, color=None):
    return DashIconify(icon=icon, height=size, color=color)


dashboard_name = "omero_dataset_psf_beads"

omero_dataset_psf_beads = DjangoDash(
    name=dashboard_name,
    serve_locally=True,
    external_stylesheets=dmc.styles.ALL,
)


omero_dataset_psf_beads.layout = dmc.MantineProvider(
    theme=MANTINE_THEME,
    children=[
        dmc.NotificationProvider(position="top-center"),
        html.Div(id="notifications-container"),
        dmc.Modal(
            title="Confirm Delete",
            id="confirm_delete",
            children=[
                dmc.Text(
                    "Are you sure you want to delete this dataset outputs?"
                ),
                dmc.Space(h=20),
                dmc.Group(
                    [
                        dmc.Button(
                            "Submit",
                            id="modal-submit-button",
                            color="red",
                        ),
                        dmc.Button(
                            "Close",
                            color="gray",
                            variant="outline",
                            id="modal-close-button",
                        ),
                    ],
                    justify="flex-end",
                ),
            ],
        ),
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
                                            "PSF Beads",
                                            c=THEME["primary"],
                                            size="h2",
                                        ),
                                        dmc.Text(
                                            "PSF Beads Analysis Dashboard",
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
                                my_components.download_group,
                                my_components.delete_button,
                                dmc.Badge(
                                    "PSF Beads Analysis",
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
                html.Div(id="blank-input"),
                dmc.Paper(
                    shadow="xs",
                    p="md",
                    radius="md",
                    mt="md",
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
                                        dmc.Group(
                                            [
                                                my_components.download_table,
                                                dmc.Tooltip(
                                                    label="Statistical measurements for all the channels presented in the dataset",
                                                    children=[
                                                        get_icon(
                                                            "material-symbols:info-outline",
                                                            color=THEME[
                                                                "primary"
                                                            ],
                                                        )
                                                    ],
                                                ),
                                            ]
                                        ),
                                    ],
                                    justify="space-between",
                                ),
                                dmc.ScrollArea(
                                    [
                                        dmc.Table(
                                            id="key_values_psf",
                                            striped=True,
                                            highlightOnHover=True,
                                            className="table table-striped table-bordered",
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
                                    ]
                                ),
                            ],
                            gap="xl",
                        ),
                    ],
                ),
            ],
            size="xl",
            p="md",
            style={"backgroundColor": THEME["surface"]},
        ),
    ],
)


@omero_dataset_psf_beads.expanded_callback(
    dash.dependencies.Output("key_values_psf", "data"),
    dash.dependencies.Output("pagination", "total"),
    [
        dash.dependencies.Input("pagination", "value"),
    ],
)
def func_psf_callback(pagination_value, **kwargs):
    table_km = load.get_km_mm_metrics_dataset(
        mm_dataset=kwargs["session_state"]["context"]["mm_dataset"],
        table_name="key_measurements",
    )
    page = int(pagination_value)
    kkm = [
        "channel_name",
        "considered_valid_count",
        "intensity_max_median",
        "intensity_max_std",
        "intensity_min_mean",
        "intensity_min_median",
        "intensity_min_std",
        "intensity_std_mean",
        "intensity_std_median",
        "intensity_std_std",
    ]
    table_kkm = table_km[kkm].copy()
    table_kkm = table_kkm.round(3)
    table_kkm.columns = table_kkm.columns.str.replace("_", " ").str.title()
    total = math.ceil(len(table_kkm) / 4)
    start_idx = (page - 1) * 4
    end_idx = start_idx + 4
    table_page = table_kkm.iloc[start_idx:end_idx]
    data = {
        "head": table_page.columns.tolist(),
        "body": table_page.values.tolist(),
        "caption": "Key Measurements for the selected dataset",
    }
    return data, total


@omero_dataset_psf_beads.expanded_callback(
    dash.dependencies.Output("confirm_delete", "opened"),
    dash.dependencies.Output("notifications-container", "children"),
    [
        dash.dependencies.Input("delete_data", "n_clicks"),
        dash.dependencies.Input("modal-submit-button", "n_clicks"),
        dash.dependencies.Input("modal-close-button", "n_clicks"),
        dash.dependencies.State("confirm_delete", "opened"),
    ],
    prevent_initial_call=True,
)
def delete_dataset(*args, **kwargs):
    triggered_button = kwargs["callback_context"].triggered[0]["prop_id"]
    dataset_id = kwargs["session_state"]["context"][
        "mm_dataset"
    ].data_reference.omero_object_id
    request = kwargs["request"]
    opened = not args[3]
    if triggered_button == "modal-submit-button.n_clicks" and args[0] > 0:
        sleep(1)
        msg, color = views.delete_dataset(request, dataset_id=dataset_id)
        message = dmc.Notification(
            title="Notification!",
            id="simple-notify",
            action="show",
            message=msg,
            icon=DashIconify(
                icon=(
                    "akar-icons:circle-check"
                    if color == "green"
                    else "akar-icons:circle-x"
                )
            ),
            color=color,
        )
        return opened, message
    else:
        return opened, None


@omero_dataset_psf_beads.expanded_callback(
    dash.dependencies.Output("download", "data"),
    [
        dash.dependencies.Input("download-yaml", "n_clicks"),
        dash.dependencies.Input("download-json", "n_clicks"),
        dash.dependencies.Input("download-text", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def download_dataset_data(_, **kwargs):
    if not kwargs["callback_context"].triggered:
        raise dash.no_update

    triggered_id = (
        kwargs["callback_context"].triggered[0]["prop_id"].split(".")[0]
    )
    mm_dataset = kwargs["session_state"]["context"]["mm_dataset"]
    file_name = mm_dataset.name
    yaml_dumper = YAMLDumper()
    json_dumper = JSONDumper()
    if triggered_id == "download-yaml":
        return dict(
            content=yaml_dumper.dumps(mm_dataset), filename=f"{file_name}.yaml"
        )

    elif triggered_id == "download-json":
        return dict(
            content=json_dumper.dumps(mm_dataset), filename=f"{file_name}.json"
        )

    elif triggered_id == "download-text":
        return dict(
            content=yaml_dumper.dumps(mm_dataset), filename=f"{file_name}.txt"
        )

    raise dash.no_update


@omero_dataset_psf_beads.expanded_callback(
    dash.dependencies.Output("table-download", "data"),
    [
        dash.dependencies.Input("table-download-csv", "n_clicks"),
        dash.dependencies.Input("table-download-xlsx", "n_clicks"),
        dash.dependencies.Input("table-download-json", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def download_table_data(_, **kwargs):
    if not kwargs["callback_context"].triggered:
        raise dash.no_update

    triggered_id = (
        kwargs["callback_context"].triggered[0]["prop_id"].split(".")[0]
    )
    table_km = load.get_km_mm_metrics_dataset(
        mm_dataset=kwargs["session_state"]["context"]["mm_dataset"],
        table_name="key_measurements",
    )
    kkm = [
        "channel_name",
        "considered_valid_count",
        "intensity_max_median",
        "intensity_max_std",
        "intensity_min_mean",
        "intensity_min_median",
        "intensity_min_std",
        "intensity_std_mean",
        "intensity_std_median",
        "intensity_std_std",
    ]
    table_kkm = table_km[kkm].copy()
    table_kkm = table_kkm.round(3)
    table_kkm.columns = table_kkm.columns.str.replace("_", " ").str.title()
    if triggered_id == "table-download-csv":
        return dcc.send_data_frame(table_kkm.to_csv, "km_table.csv")
    elif triggered_id == "table-download-xlsx":
        return dcc.send_data_frame(table_kkm.to_excel, "km_table.xlsx")
    elif triggered_id == "table-download-json":
        return dcc.send_data_frame(table_kkm.to_json, "km_table.json")
    raise dash.no_update
