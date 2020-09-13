import sqlite3
import numpy as np
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import datetime
import plotly.graph_objects as go
import plotly.express as px
from functions import get_balance_sql_result, get_past_due_sql_result, get_current_sql_result, \
    get_zero_to_thirty_sql_result, get_thirty_to_sixty_sql_result, get_sixty_to_ninety_sql_result, \
    get_over_ninety_sql_result, get_barchart_df, get_treemap_df, get_scatter_graph_df, build_hierarchical_dataframe

def sales():
    return html.Div([
        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=datetime.date.today() - relativedelta(months=1),
                end_date=datetime.date.today()
            )
        ]
        ),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='sales-total-kpi'
                ),
                dcc.Graph(
                    id='sales-average-kpi'
                )
            ], className='six columns'
            ),
            html.Div([
                dcc.Graph(
                    id='invoice-count-kpi'
                ),
                dcc.Graph(
                    id='customer-count-kpi'
                )
            ], className='six columns'
            )
        ], className='container six columns'
        )
    ])

df1 = get_treemap_df()

df1['amount'] = df1['amount'].astype(int)

conditions = [
    (df1['PastDueStatus'] == 'Current'),
    (df1['PastDueStatus'] == '0-30'),
    (df1['PastDueStatus'] == '31-60'),
    (df1['PastDueStatus'] == '61-90'),
    (df1['PastDueStatus'] == 'Over 90')
]

values = [
    df1['Customer'] + '_0',
    df1['Customer'] + '_1',
    df1['Customer'] + '_2',
    df1['Customer'] + '_3',
    df1['Customer'] + '_4'
]

df1['graphID'] = np.select(conditions, values)

levels = ['PastDueStatus', 'status']
value_column = 'amount'

df_all_trees = build_hierarchical_dataframe(
    df1,
    levels,
    value_column
)

df_all_trees = df_all_trees[df_all_trees.id != 0]

# df_ids = df_all_trees['id'].tolist()
# print(df_ids)

def accounts_receivable():
    return html.Div([
        html.Br(),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(
                            figure={
                                'data':[
                                    go.Indicator(
                                        mode='number',
                                        value=get_balance_sql_result(),
                                        number={
                                            'font':{
                                                'size': 42
                                            }
                                        }
                                    )
                                ],
                                'layout':go.Layout(
                                    title='Total AR',
                                    height=200,
                                    paper_bgcolor='white'
                                )
                            }
                        )
                    ], className='three columns'
                    ),
                    html.Div([
                        dcc.Graph(
                            figure={
                                'data': [
                                    go.Indicator(
                                        mode='number',
                                        value=get_current_sql_result(),
                                        number={
                                            'font': {
                                                'size': 42
                                            }
                                        }
                                    )
                                ],
                                'layout': go.Layout(
                                    title='Total Current',
                                    height=200,
                                    paper_bgcolor='white'
                                )
                            }
                        )
                    ], className='three columns'
                    ),
                    html.Div([
                        dcc.Graph(
                            figure={
                                'data': [
                                    go.Indicator(
                                        mode='number',
                                        value=get_past_due_sql_result(),
                                        number={
                                            'font': {
                                                'size': 42
                                            }
                                        }
                                    )
                                ],
                                'layout': go.Layout(
                                    title='Total Past Due',
                                    height=200,
                                    paper_bgcolor='white'
                                )
                            }
                        )
                    ], className='three columns'
                    ),
                    html.Div([
                        dcc.Graph(
                            figure={
                                'data': [
                                    go.Indicator(
                                        mode='number',
                                        value=(get_past_due_sql_result() / get_balance_sql_result()) * 100,
                                        number={
                                            'font': {
                                                'size': 42
                                            },
                                            'suffix': '%'
                                        }
                                    )
                                ],
                                'layout': go.Layout(
                                    title='Percent Past Due',
                                    height=200,
                                    paper_bgcolor='white'
                                )
                            }
                        )
                    ], className='three columns'
                    ),
                ], className='row'
                ),
                html.Br(),
                html.Br(),
                html.Div([
                    html.Div([
                        dcc.Graph(
                            figure={
                                'data': [
                                    go.Indicator(
                                        mode='number',
                                        value=get_zero_to_thirty_sql_result(),
                                        number={
                                            'font': {
                                                'size': 42
                                            }
                                        }
                                    )
                                ],
                                'layout': go.Layout(
                                    title='0-30 Days',
                                    height=200,
                                    paper_bgcolor='white'
                                )
                            }
                        )
                    ], className='three columns'
                    ),
                    html.Div([
                        dcc.Graph(
                            figure={
                                'data': [
                                    go.Indicator(
                                        mode='number',
                                        value=get_thirty_to_sixty_sql_result(),
                                        number={
                                            'font': {
                                                'size': 42
                                            }
                                        }
                                    )
                                ],
                                'layout': go.Layout(
                                    title='30-60 Days',
                                    height=200,
                                    paper_bgcolor='white'
                                )
                            }
                        )
                    ], className='three columns'
                    ),
                    html.Div([
                        dcc.Graph(
                            figure={
                                'data': [
                                    go.Indicator(
                                        mode='number',
                                        value=get_sixty_to_ninety_sql_result(),
                                        number={
                                            'font': {
                                                'size': 42
                                            }
                                        }
                                    )
                                ],
                                'layout': go.Layout(
                                    title='60-90 Days',
                                    height=200,
                                    paper_bgcolor='white'
                                )
                            }
                        )
                    ], className='three columns'
                    ),
                    html.Div([
                        dcc.Graph(
                            figure={
                                'data': [
                                    go.Indicator(
                                        mode='number',
                                        value=get_over_ninety_sql_result(),
                                        number={
                                            'font': {
                                                'size': 42
                                            }
                                        }
                                    )
                                ],
                                'layout': go.Layout(
                                    title='Over 90 Days',
                                    height=200,
                                    paper_bgcolor='white'
                                )
                            }
                        )
                    ], className='three columns'
                    )
                ], className='row'
                )
            ], className='eight columns'
            ),
            html.Div([
                dcc.Graph(
                    figure={
                        'data': [
                            go.Bar(
                                x=get_barchart_df()['balance'],
                                y=get_barchart_df()['PastDue'],
                                orientation='h'
                            )
                        ],
                        'layout': go.Layout(
                            title='Open Invoices By Past Due Status'
                        )
                    }
                )
            ], className='four columns'
            )
        ], className='row'
        ),
        html.Br(),
        html.Div([
            html.Div([
                dcc.Graph(
                    figure={
                        'data': [
                            go.Scatter(
                                x=get_scatter_graph_df()['days'],
                                y=get_scatter_graph_df()['amount'],
                                mode='markers',
                                text=get_scatter_graph_df()['refNbr'],
                                hovertemplate='<b>INVOICE %{text}</b><br>' +
                                              '<br>Customer: ' + get_scatter_graph_df()['Customer'] +
                                              '<br>Amount: %{y}' +
                                              '<br>DaysPastDue: %{x}'
                            )
                        ],
                        'layout': go.Layout(
                            title='All Open Invoices',
                            xaxis={
                                'title': 'Days Past Due'
                            },
                            yaxis={
                                'title': 'Invoice Amount'
                            },
                            hoverdistance=-1,
                            hovermode='closest'
                        )
                    }
                )
            ], className='twelve columns'
            )
        ], className='row'
        ),
        html.Br(),
        html.Br(),
        html.Div([
            html.Div([
                dcc.Graph(
                    figure={
                        'data': [
                            go.Treemap(
                                labels=df_all_trees['id'],
                                parents=df_all_trees['parent'],
                                values=df_all_trees['value'],
                                branchvalues='total'
                            )
                        ],
                        'layout': go.Layout(
                            title='Past Due Status Share'
                        )
                    }
                )
            ], className='twelve columns'
            )
        ], className='row'
        )
    ]
    )

def profit_and_loss():
    return html.Div([
        html.Div([
            html.Div([
                dcc.DatePickerRange(
                    id='pl-date-picker-range',
                    start_date=datetime.date.today().replace(day=1),
                    end_date=datetime.date.today()
                )
            ], className='six columns'
            ),
            html.Div([], className='six columns')
        ], className='row'
        ),
        html.Br(),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='pl-sales'
                    )
                ], className='twelve columns'
                ),
                html.Div([
                    dcc.Graph(
                        id='pl-cogs'
                    )
                ], className='twelve columns'
                ),
                html.Div([
                    dcc.Graph(
                        id='pl-profit'
                    )
                ], className='twelve columns'
                ),
                html.Div([
                    dcc.Graph(
                        id='pl-margin'
                    )
                ], className='twelve columns'
                )
            ], className='three columns'
            ),
            html.Div([
                dcc.Graph(
                    id='pl-waterfall'
                )
            ], className='six columns'
            ),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='pl-expenses'
                    )
                ], className='twelve columns'
                ),
                html.Div([
                    dcc.Graph(
                        id='pl-taxes'
                    )
                ], className='twelve columns'
                ),
                html.Div([
                    dcc.Graph(
                        id='pl-income'
                    )
                ], className='twelve columns'
                ),
                html.Div([
                    dcc.Graph(
                        id='pl-income-percent'
                    )
                ], className='twelve columns'
                )
            ], className='three columns'
            )
        ], className='row'
        ),
        html.Br(),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='expenses-bar'
                )
            ], className='twelve columns'
            )
        ], className='row'
        ),
        html.Br(),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='pl-top-customers'
                )
            ], className='six columns'
            ),
            html.Div([
                dcc.Graph(
                    id='pl-top-vendors'
                )
            ], className='six columns'
            )
        ], className='row'
        )
    ]#page
    )

def rig_report():
    return html.Div([
        html.Div([
            html.Div
        ], className='row'
        )
    ] #page
    )