import dash
from dash import dcc, html, dash_table
import plotly.graph_objs as go
import numpy as np
from django_plotly_dash import DjangoDash
import plotly.express as px
import dash_mantine_components as dmc

c1 = "#d8f3dc"
c2 = "#eceff1"
c3 = "#189A35"

dashboard_name = 'omero_dataset_metrics'
dash_app_dataset = DjangoDash(name=dashboard_name, serve_locally=True, )

dash_app_dataset.layout = dmc.MantineProvider([dmc.Container(
    [
        dmc.Center(
            dmc.Text(
                id='title',
                c="#189A35",
                mb=30,
                style={"margin-top": "20px", "fontSize": 40},
            )
        ),
        dmc.Stack(
            [
                dmc.Grid([
                    dmc.GridCol([dmc.Title("Intensity Map", c="#189A35", size="h3", mb=10),
                                 dcc.Dropdown(value="Channel 0", id="channel_ddm"),
                                 dcc.Graph(id="dataset_image_graph", figure={},
                                           style={'display': 'inline-block', 'width': '100%', 'height': '100%;'}),
                                 ], span="6"),
                    dmc.GridCol([
                        dmc.Title("Intensity Profile", c="#189A35", size="h3", mb=10),
                        dcc.Graph(id="intensity_profile", figure={},
                                  style={'display': 'inline-block', 'width': '100%', 'height': '100%;'}),
                    ], span="6"),

                ]),

                dmc.Stack(
                    [
                        dmc.Title(
                            "Key Measurements", c="#189A35", size="h3", mb=10
                        ),
                        dash_table.DataTable(
                            id="table",
                            page_size=10,
                            sort_action="native",
                            sort_mode="multi",
                            sort_as_null=["", "No"],
                            sort_by=[{"column_id": "pop", "direction": "asc"}],
                            editable=False,
                            style_cell={
                                "textAlign": "left",
                                "fontSize": 10,
                                "font-family": "sans-serif",
                            },
                            style_header={
                                "backgroundColor": "#189A35",
                                "fontWeight": "bold",
                                "fontSize": 15,
                            },
                        ),
                    ]
                )
            ]),
    ],
    fluid=True,
)])


@dash_app_dataset.expanded_callback(dash.dependencies.Output('dataset_image_graph', 'figure'),
                                    dash.dependencies.Output('channel_ddm', 'options'),
                                    dash.dependencies.Output('title', 'children'),
                                    dash.dependencies.Output('table', 'data'),
                                    dash.dependencies.Output('intensity_profile', 'figure'),
                                    [dash.dependencies.Input('channel_ddm', 'value')])
def dataset_callback_intensity_map(*args, **kwargs):
    title = kwargs['session_state']['title']
    table = kwargs['session_state']['key_values_df']
    images = kwargs['session_state']['images']
    df_intensity_profiles = kwargs['session_state']['intensity_profiles']
    labels = table.columns[1:].to_list()
    imaaa = images[0, 0, :, :, int(args[0][-1])] / 255
    channel_list = [{'label': labels[i], 'value': f"channel {i}"} for i in range(len(labels))]
    fig = px.imshow(imaaa, zmin=imaaa.min(), zmax=imaaa.max(), color_continuous_scale="gray")
    C = 'Ch0' + args[0][-1]
    df_profile = df_intensity_profiles[df_intensity_profiles.columns[df_intensity_profiles.columns.str.startswith(C)]
    ].copy()
    df_profile.columns = df_profile.columns.str.replace("Ch\d{2}_", "", regex=True)
    df_profile.columns = df_profile.columns.str.replace("_", " ", regex=True)
    df_profile.columns = df_profile.columns.str.title()
    fig_ip = px.line(df_profile, markers=True)
    return fig, channel_list, title, table.to_dict('records'), fig_ip