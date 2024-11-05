import dash
import pandas as pd
from dash import html, dash_table, dcc
from django_plotly_dash import DjangoDash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from OMERO_metrics import views
from time import sleep
from django.urls import reverse

dashboard_name = "omero_group_dash"
dash_app_group = DjangoDash(
    name=dashboard_name,
    serve_locally=True,
    external_stylesheets=dmc.styles.ALL,
)

# Theme configuration
THEME = {
    "primary": "#189A35",
    "secondary": "#189A35",
    "background": "#f8fafc",
    "surface": "#ffffff",
    "border": "#e2e8f0",
    "success": "#10b981",
    "error": "#ef4444",
}

dash_app_group.layout = dmc.MantineProvider(
    theme={
        "colorScheme": "light",
        "primaryColor": "green",
        "components": {
            "Button": {"styles": {"root": {"fontWeight": 500}}},
            "Title": {"styles": {"root": {"letterSpacing": "-0.5px"}}},
        },
    },
    children=[
        dmc.NotificationProvider(position="top-center"),
        html.Div(id="notifications-container"),
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.TabsTab(
                            "Microscope Health",
                            leftSection=DashIconify(icon="tabler:microscope"),
                            value="microscope_health",
                            color=THEME["primary"],
                            style={
                                "fontSize": "1.1rem",
                                "fontWeight": "bold",
                                "color": THEME["primary"],
                            },
                        ),
                        dmc.TabsTab(
                            "History",
                            leftSection=DashIconify(icon="bx:history"),
                            value="history",
                            color=THEME["primary"],
                            style={
                                "fontSize": "1.1rem",
                                "fontWeight": "bold",
                                "color": THEME["primary"],
                            },
                        ),
                    ],
                    grow=True,
                    justify="space-around",
                    variant="light",
                    style={"backgroundColor": THEME["surface"]},
                ),
                dmc.TabsPanel(
                    dmc.Container(
                        [
                            dmc.Paper(
                                children=[
                                    dmc.Group(
                                        [
                                            html.Img(
                                                src="/static/OMERO_metrics/images/microscope.png",
                                                style={
                                                    "width": "100px",
                                                    "objectFit": "contain",
                                                },
                                            ),
                                            dmc.Stack(
                                                [
                                                    dmc.Title(
                                                        "Microscope Health Dashboard",
                                                        c=THEME["primary"],
                                                        size="h3",
                                                    ),
                                                    dmc.Text(
                                                        "View information about your microscope group",
                                                        c="dimmed",
                                                        size="sm",
                                                    ),
                                                ],
                                                gap=5,
                                            ),
                                        ],
                                        justify="space-between",
                                        align="center",
                                    ),
                                    dmc.Divider(mb="md"),
                                    html.Div(id="microscope_info"),
                                ],
                                withBorder=True,
                                shadow="sm",
                                radius="md",
                                p="lg",
                                style={
                                    "width": "100%",
                                    "maxWidth": "600px",
                                    "margin": "auto",
                                },
                            ),
                        ],
                        fluid=True,
                        style={
                            "backgroundColor": THEME["background"],
                            "margin": "10px",
                            "borderRadius": "0.5rem",
                            "padding": "10px",
                        },
                    ),
                    value="microscope_health",
                ),
                dmc.TabsPanel(
                    dmc.Container(
                        children=[
                            dmc.Paper(
                                children=[
                                    dmc.Group(
                                        [
                                            dmc.Button(
                                                id="download_table",
                                                children=[
                                                    DashIconify(
                                                        icon="ic:round-download"
                                                    ),
                                                    "Download",
                                                ],
                                                variant="gradient",
                                                gradient={
                                                    "from": THEME["secondary"],
                                                    "to": THEME["primary"],
                                                    "deg": 105,
                                                },
                                                w="auto",
                                            ),
                                            dcc.Download(id="download"),
                                            dmc.DatePicker(
                                                id="date-picker",
                                                label="Select Date Range",
                                                valueFormat="DD-MM-YYYY",
                                                type="range",
                                                w=250,
                                                leftSection=DashIconify(
                                                    icon="clarity:date-line"
                                                ),
                                            ),
                                            dmc.Select(
                                                id="select_mimetype",
                                                label="Mime Type",
                                                value="0",
                                                w=250,
                                                allowDeselect=False,
                                            ),
                                            dmc.Button(
                                                id="delete-all",
                                                children=[
                                                    DashIconify(
                                                        icon="ic:round-delete-forever"
                                                    ),
                                                    "Delete All",
                                                ],
                                                variant="gradient",
                                                gradient={
                                                    "from": THEME["error"],
                                                    "to": THEME["primary"],
                                                    "deg": 105,
                                                },
                                                w=250,
                                            ),
                                            dmc.Modal(
                                                title="Confirm Delete",
                                                id="confirm_delete",
                                                children=[
                                                    dmc.Text(
                                                        "Are you sure you want to delete all annotations including ROIs?"
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
                                        ],
                                        justify="space-between",
                                        align="flex-end",
                                    ),
                                    dmc.Space(h=20),
                                    dmc.Divider(mb="md"),
                                    dmc.Space(h=20),
                                    dmc.Text(
                                        "File Annotations",
                                        c=THEME["primary"],
                                        size="xl",
                                    ),
                                    html.Div(
                                        id="project_file_annotations_table",
                                        style={"margin": "10px"},
                                    ),
                                    dmc.Divider(mb="md"),
                                    dmc.Text(
                                        "Map Annotations",
                                        c=THEME["primary"],
                                        size="xl",
                                    ),
                                    html.Div(
                                        id="project_map_annotations_table",
                                        style={"margin": "10px"},
                                    ),
                                    html.Div(id="blank-input"),
                                    html.Div(id="result"),
                                ],
                                withBorder=True,
                                shadow="sm",
                                radius="md",
                                p="lg",
                            ),
                        ],
                        fluid=True,
                        style={
                            "backgroundColor": THEME["background"],
                            "margin": "10px",
                            "borderRadius": "0.5rem",
                            "padding": "10px",
                        },
                    ),
                    value="history",
                ),
            ],
            value="microscope_health",
        ),
    ],
)


@dash_app_group.expanded_callback(
    dash.dependencies.Output("date-picker", "value"),
    dash.dependencies.Output("date-picker", "minDate"),
    dash.dependencies.Output("date-picker", "maxDate"),
    [dash.dependencies.Input("blank-input", "children")],
)
def update_date_range(*args, **kwargs):
    df = kwargs["session_state"]["context"]["file_ann"]
    min_date = df.Date.min()
    max_date = df.Date.max()
    return [min_date, max_date], min_date, max_date


@dash_app_group.expanded_callback(
    dash.dependencies.Output("select_mimetype", "data"),
    [dash.dependencies.Input("blank-input", "children")],
)
def update_mimetype(*args, **kwargs):
    df = kwargs["session_state"]["context"]["file_ann"]
    mimetype = df.Mimetype.unique()
    data = [{"label": mt, "value": f"{i+1}"} for i, mt in enumerate(mimetype)]
    data = [{"label": "All", "value": "0"}] + data
    return data


@dash_app_group.expanded_callback(
    dash.dependencies.Output("microscope_info", "children"),
    dash.dependencies.Input("blank-input", "children"),
)
def render_content(*args, **kwargs):
    group_name = kwargs["session_state"]["context"]["group_name"]
    group_id = kwargs["session_state"]["context"]["group_id"]
    group_description = kwargs["session_state"]["context"]["group_description"]
    return dmc.Stack(
        [
            dmc.Title("Microscope Information", c=THEME["primary"], order=4),
            dmc.Text(f"Group Name: {group_name}", size="sm"),
            dmc.Text(f"Group ID: {group_id}", size="sm"),
            dmc.Text(f"Group Description: {group_description}", size="sm"),
        ],
        align="flex-start",
        gap="xs",
    )


@dash_app_group.expanded_callback(
    dash.dependencies.Output("project_file_annotations_table", "children"),
    dash.dependencies.Output("project_map_annotations_table", "children"),
    [
        dash.dependencies.Input("select_mimetype", "value"),
        dash.dependencies.Input("date-picker", "value"),
    ],
    prevent_initial_call=True,
)
def load_table_project(*args, **kwargs):
    file_ann = kwargs["session_state"]["context"]["file_ann"]
    data_filter = args[1]
    if data_filter is not None:
        file_ann = file_ann[
            (file_ann["Date"].dt.date >= pd.to_datetime(data_filter[0]).date())
            & (
                file_ann["Date"].dt.date
                <= pd.to_datetime(data_filter[1]).date()
            )
        ]

    else:
        pass
    if int(args[0]) > 0 and len(file_ann.Mimetype.unique()) > 0:
        file_ann = file_ann[
            file_ann.Mimetype == file_ann.Mimetype.unique()[int(args[0]) - 1]
        ]
    else:
        pass
    file_ann_subset = file_ann[
        file_ann.columns[~file_ann.columns.str.contains("ID")]
    ].copy()
    request = kwargs["request"]
    file_ann_subset.loc[file_ann_subset.index, "Download"] = [
        (
            f"[CSV]({request.build_absolute_uri(reverse(viewname='omero_table', args=[i, 'csv']))})"
            f" | [JSON]({request.build_absolute_uri(reverse(viewname='omero_table', args=[i, 'json']))}) "
            if mt == "OMERO.tables"
            else f"[YAML]({request.build_absolute_uri(reverse(viewname='download_annotation', args=[id]))})"
        )
        for i, mt, id in zip(file_ann.File_ID, file_ann.Mimetype, file_ann.ID)
    ]
    file_ann_table = dash_table.DataTable(
        id="datatable_file_ann",
        columns=[
            (
                {"id": x, "name": x, "presentation": "markdown"}
                if x == "Download"
                else {"id": x, "name": x}
            )
            for x in file_ann_subset.columns
        ],
        data=file_ann_subset.to_dict("records"),
        sort_action="native",
        sort_mode="multi",
        row_selectable="multi",
        page_action="native",
        page_current=0,
        page_size=5,
        style_table={
            "overflowX": "auto",
            "borderRadius": "0.5rem",
            "fontFamily": "'Arial', 'Helvetica', sans-serif",
            "borderCollapse": "collapse",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
            "margin": "20px 0",
            "borderLeft": "none",
            "borderRight": "none",
        },
        style_cell={
            "whiteSpace": "normal",
            "height": "30px",
            "minWidth": "100px",
            "width": "100px",
            "maxWidth": "100px",
            "textAlign": "left",
            "textOverflow": "ellipsis",
            "fontSize": "12px",
            "fontFamily": "'Arial', 'Helvetica', sans-serif",
            "color": "#333",
            "fontWeight": "500",
            "padding": "10px",
            "border": "1px solid #ddd",
            "borderLeft": "none",
            "borderRight": "none",
        },
        style_header={
            "backgroundColor": THEME["primary"],
            "fontWeight": "bold",
            "fontSize": "16px",
            "paddingTop": "12px",
            "paddingBottom": "12px",
            "color": THEME["surface"],
            "border": "1px solid #ddd",
            "borderLeft": "none",
            "borderRight": "none",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": THEME["background"],
            },
            {
                "if": {"row_index": "even"},
                "backgroundColor": THEME["surface"],
            },
        ],
    )
    map_ann = kwargs["session_state"]["context"]["map_ann"]
    map_ann_subset = map_ann[
        map_ann.columns[~map_ann.columns.str.contains("ID")]
    ]
    map_table = dash_table.DataTable(
        id="datatable-interactivity",
        columns=[{"name": i, "id": i} for i in map_ann_subset.columns],
        data=map_ann_subset.to_dict("records"),
        sort_action="native",
        sort_mode="multi",
        row_selectable="multi",
        page_action="native",
        page_current=0,
        page_size=5,
        style_table={
            "overflowX": "auto",
            "borderRadius": "0.5rem",
            "fontFamily": "'Arial', 'Helvetica', sans-serif",
            "borderCollapse": "collapse",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
            "margin": "20px 0",
            "borderLeft": "none",
            "borderRight": "none",
        },
        style_cell={
            "whiteSpace": "normal",
            "height": "30px",
            "minWidth": "100px",
            "width": "100px",
            "maxWidth": "100px",
            "textAlign": "left",
            "textOverflow": "ellipsis",
            "fontSize": "12px",
            "fontFamily": "'Arial', 'Helvetica', sans-serif",
            "color": "#333",
            "fontWeight": "500",
            "padding": "10px",
            "border": "1px solid #ddd",
            "borderLeft": "none",
            "borderRight": "none",
        },
        style_header={
            "backgroundColor": THEME["primary"],
            "fontWeight": "bold",
            "fontSize": "16px",
            "paddingTop": "12px",
            "paddingBottom": "12px",
            "color": THEME["surface"],
            "border": "1px solid #ddd",
            "borderLeft": "none",
            "borderRight": "none",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": THEME["background"],
            },
            {
                "if": {"row_index": "even"},
                "backgroundColor": THEME["surface"],
            },
        ],
    )
    return file_ann_table, map_table


@dash_app_group.expanded_callback(
    dash.dependencies.Output("confirm_delete", "opened"),
    dash.dependencies.Output("notifications-container", "children"),
    [
        dash.dependencies.Input("delete-all", "n_clicks"),
        dash.dependencies.Input("modal-submit-button", "n_clicks"),
        dash.dependencies.Input("modal-close-button", "n_clicks"),
        dash.dependencies.State("confirm_delete", "opened"),
    ],
    prevent_initial_call=True,
)
def delete_all_callback(*args, **kwargs):
    triggered_button = kwargs["callback_context"].triggered[0]["prop_id"]
    group_id = kwargs["session_state"]["context"]["group_id"]
    request = kwargs["request"]
    if triggered_button == "modal-submit-button.n_clicks" and args[0] > 0:
        sleep(1)
        views.delete_all(request, group_id=group_id)
        message = dmc.Notification(
            title="Notification!",
            id="simple-notify",
            action="show",
            message="All annotations have been deleted",
            icon=DashIconify(icon="akar-icons:circle-check"),
        )
    elif triggered_button == "modal-close-button.n_clicks" and args[1] > 0:
        message = "You have clicked the close button"
    else:
        message = "delete all button clicked"
    opened = not args[3]
    return opened, message


@dash_app_group.expanded_callback(
    dash.dependencies.Output("download", "data"),
    dash.dependencies.Input("download_table", "n_clicks"),
    dash.dependencies.State("datatable_file_ann", "data"),
    prevent_initial_call=True,
)
def download_file(*args, **kwargs):
    table_data = args[1]
    df = pd.DataFrame(table_data)
    return dcc.send_data_frame(df.to_csv, "FIle_annotation.csv")
