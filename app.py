import sqlite3
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from utilities import sales, accounts_receivable, profit_and_loss
from functions import get_pl_sales, get_pl_other_rev, get_pl_cogs, get_pl_expenses, get_pl_taxes, \
    get_top_ten_customers, get_top_ten_vendors, get_expenses_breakdown
import plotly.graph_objects as go
import pandas as pd

sales = sales()

background_color = 'lightgray'

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
)
server = app.server

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(
                src=app.get_asset_url('logo.png'),
                className='logo',
            )
        ])
    ]
    ),
    html.Div([
        dcc.Tabs(
            id='tabs',
            value='Sales',
            children=[
                dcc.Tab(
                    label='Profit & Loss',
                    value='Profit & Loss'
                ),
                dcc.Tab(
                    label='AR',
                    value='AR'
                )
            ]
        )
    ]
    ),
    html.Div(
        id='tab-content'
    )
]
)

@app.callback(
    Output(
        'tab-content',
        'children'
    ),
    [
        Input(
            'tabs',
            'value'
        )
    ]
)
def render_content(tab):
    if tab == 'Profit & Loss':
        return html.Div([
            profit_and_loss()
        ])
    elif tab == 'AR':
        return html.Div([
            accounts_receivable()
        ])
# @app.callback([
#     Output(
#         'sales-total-kpi',
#         'figure'
#     ),
#     Output(
#         'sales-average-kpi',
#         'figure'
#     ),
#     Output(
#         'invoice-count-kpi',
#         'figure'
#     ),
#     Output(
#         'customer-count-kpi',
#         'figure'
#     )
# ],
# [
#     Input(
#         'date-picker-range',
#         'start_date'
#     ),
#     Input(
#         'date-picker-range',
#         'end_date'
#     )
# ]
# )
# def update_output(start, end):
#
#     conn = sqlite3.connect('database/bds_dash.db')
#     c = conn.cursor()
#
#     sales_sql = '''
#         SELECT SUM(jtd.CreditAmount - jtd.DebitAmount)
#         FROM journalTransactionDetails as jtd
#         INNER JOIN journalTransactions as jt ON jtd.BatchNbr = jt.BatchNbr
#         LEFT JOIN accounts as a ON a.AccountCD = jtd.Account
#         WHERE jt.TransactionDate >= ? and jt.TransactionDate <= ? and a.AccountClass = 'SALES'
#         '''
#
#     average_sql = '''
#         SELECT AVG(jtd.CreditAmount - jtd.DebitAmount)
#         FROM journalTransactionDetails as jtd
#         INNER JOIN journalTransactions as jt ON jtd.BatchNbr = jt.BatchNbr
#         LEFT JOIN accounts as a ON a.AccountCD = jtd.Account
#         WHERE jt.TransactionDate >= ? and jt.TransactionDate <= ? and a.AccountClass = 'SALES'
#         '''
#
#     invoice_count_sql = '''
#         SELECT COUNT(DISTINCT jtd.ReferenceNbr)
#         FROM journalTransactionDetails as jtd
#         INNER JOIN journalTransactions as jt ON jtd.BatchNbr = jt.BatchNbr
#         LEFT JOIN accounts as a ON a.AccountCD = jtd.Account
#         WHERE jt.TransactionDate >= ? and jt.TransactionDate <= ? and a.AccountClass = 'SALES'
#         '''
#
#     customer_count_sql = '''
#         SELECT COUNT(DISTINCT jtd.VendorOrCustomer)
#         FROM journalTransactionDetails as jtd
#         INNER JOIN journalTransactions as jt ON jtd.BatchNbr = jt.BatchNbr
#         LEFT JOIN accounts as a ON a.AccountCD = jtd.Account
#         WHERE jt.TransactionDate >= ? and jt.TransactionDate <= ? and a.AccountClass = 'SALES'
#         '''
#
#     c.execute(sales_sql, (start, end))
#
#     sales_sql_result = [row for row in c][0][0]
#
#     sales_fig = {
#         'data':[
#             go.Indicator(
#                 mode='number',
#                 value=sales_sql_result,
#                 number={
#                     'font':{
#                         'size': 48
#                     }
#                 }
#             )
#         ],
#         'layout':go.Layout(
#             title='Sales',
#             height=200,
#             paper_bgcolor='white'
#         )
#     }
#
#     c.execute(average_sql, (start, end))
#
#     average_sql_result = [row for row in c][0][0]
#
#     average_fig = {
#         'data': [
#             go.Indicator(
#                 mode='number',
#                 value=average_sql_result,
#                 number={
#                     'font': {
#                         'size': 48
#                     }
#                 }
#             )
#         ],
#         'layout': go.Layout(
#             title='Average',
#             height=200,
#             paper_bgcolor='white'
#         )
#     }
#
#     c.execute(invoice_count_sql, (start, end))
#
#     invoice_count_sql_result = [row for row in c][0][0]
#
#     invoice_count_fig = {
#         'data': [
#             go.Indicator(
#                 mode='number',
#                 value=invoice_count_sql_result,
#                 number={
#                     'font': {
#                         'size': 48
#                     }
#                 }
#             )
#         ],
#         'layout': go.Layout(
#             title='Invoice Count',
#             height=200,
#             paper_bgcolor='white'
#         )
#     }
#
#     c.execute(customer_count_sql, (start, end))
#
#     customer_count_sql_result = [row for row in c][0][0]
#
#     customer_count_fig = {
#         'data': [
#             go.Indicator(
#                 mode='number',
#                 value=customer_count_sql_result,
#                 number={
#                     'font': {
#                         'size': 48
#                     }
#                 }
#             )
#         ],
#         'layout': go.Layout(
#             title='Customer Count',
#             height=200,
#             paper_bgcolor='white'
#         )
#     }
#
#     c.close()
#
#     return sales_fig, average_fig, invoice_count_fig, customer_count_fig

@app.callback([
    Output(
        'pl-sales',
        'figure'
    ),
    Output(
        'pl-cogs',
        'figure'
    ),
    Output(
        'pl-profit',
        'figure'
    ),
    Output(
        'pl-margin',
        'figure'
    ),
Output(
        'pl-expenses',
        'figure'
    ),
    Output(
        'pl-taxes',
        'figure'
    ),
    Output(
        'pl-income',
        'figure'
    ),
    Output(
        'pl-income-percent',
        'figure'
    ),
    Output(
        'pl-waterfall',
        'figure'
    ),
    Output(
        'pl-top-customers',
        'figure'
    ),
    Output(
        'pl-top-vendors',
        'figure'
    ),
    Output(
        'expenses-bar',
        'figure'
    )
],
[
    Input(
        'pl-date-picker-range',
        'start_date'
    ),
    Input(
        'pl-date-picker-range',
        'end_date'
    )
]
)
def update_pl(start, end):

    profit = sum([
        get_pl_sales(start, end),
        get_pl_other_rev(start, end),
        get_pl_cogs(start, end)
    ])

    margin = profit / get_pl_sales(start, end)

    income = sum([
        profit,
        get_pl_expenses(start, end),
        get_pl_taxes(start, end)
    ])

    income_percent = income / get_pl_sales(start, end)

    pl_sales_fig = {
        'data': [
            go.Indicator(
                mode='number',
                value=get_pl_sales(start, end) + get_pl_other_rev(start, end),
                number={
                    'font': {
                        'size': 36
                    }
                }
            )
        ],
        'layout': go.Layout(
            title='Sales',
            height=100,
            paper_bgcolor='white'
        )
    }

    pl_cogs_fig = {
        'data': [
            go.Indicator(
                mode='number',
                value=abs(get_pl_cogs(start, end)),
                number={
                    'font': {
                        'size': 36
                    }
                }
            )
        ],
        'layout': go.Layout(
            title='COGS',
            height=100,
            paper_bgcolor='white'
        )
    }

    pl_profit_fig = {
        'data': [
            go.Indicator(
                mode='number',
                value=profit,
                number={
                    'font': {
                        'size': 36
                    }
                }
            )
        ],
        'layout': go.Layout(
            title='Gross Profit',
            height=100,
            paper_bgcolor='white'
        )
    }

    pl_margin_fig = {
        'data': [
            go.Indicator(
                mode='number',
                value=margin * 100,
                number={
                    'font': {
                        'size': 36
                    },
                    'suffix': '%'
                }
            )
        ],
        'layout': go.Layout(
            title='Profit Margin',
            height=100,
            paper_bgcolor='white'
        )
    }

    pl_expenses_fig = {
        'data': [
            go.Indicator(
                mode='number',
                value=abs(get_pl_expenses(start, end)),
                number={
                    'font': {
                        'size': 32
                    }
                }
            )
        ],
        'layout': go.Layout(
            title='Operating Expenses',
            height=100,
            paper_bgcolor='white'
        )
    }

    pl_taxes_fig = {
        'data': [
            go.Indicator(
                mode='number',
                value=abs(get_pl_taxes(start, end)),
                number={
                    'font': {
                        'size': 36
                    }
                }
            )
        ],
        'layout': go.Layout(
            title='Taxes',
            height=100,
            paper_bgcolor='white'
        )
    }

    pl_income_fig = {
        'data': [
            go.Indicator(
                mode='number',
                value=income,
                number={
                    'font': {
                        'size': 36
                    }
                }
            )
        ],
        'layout': go.Layout(
            title='Net Income',
            height=100,
            paper_bgcolor='white'
        )
    }

    pl_income_percent_fig = {
        'data': [
            go.Indicator(
                mode='number',
                value=income_percent * 100,
                number={
                    'font': {
                        'size': 36
                    },
                    'suffix': '%'
                }
            )
        ],
        'layout': go.Layout(
            title='Income Percent',
            height=100,
            paper_bgcolor='white'
        )
    }

    waterfall_x_list = [
        'SALES',
        'OTHER<BR>REVENUE',
        'COGS',
        'GROSS PROFIT',
        'EXPENSES',
        'TAXES',
        'NET INCOME'
    ]

    waterfall_y_list = [
        get_pl_sales(start, end),
        get_pl_other_rev(start, end),
        get_pl_cogs(start, end),
        profit,
        get_pl_expenses(start, end),
        get_pl_taxes(start, end),
        income
    ]

    measure = [
        'relative',
        'relative',
        'relative',
        'total',
        'relative',
        'relative',
        'total'
    ]

    waterfall_fig = {
        'data': [
            go.Waterfall(
                orientation='v',
                measure=measure,
                x=waterfall_x_list,
                y=waterfall_y_list,
                base=0
            )
        ],
        'layout': go.Layout(
            title='Profit & Loss Waterfall'
        )
    }

    pl_top_ten_customers_fig = {
        'data': [
            go.Bar(
                x=get_top_ten_customers(start, end)['turnover'],
                y=get_top_ten_customers(start, end)['customer'],
                orientation='h'
            )
        ],
        'layout': go.Layout(
            title='Top Ten Customers'
        )
    }

    pl_top_ten_vendors_fig = {
        'data': [
            go.Bar(
                x=abs(get_top_ten_vendors(start, end)['turnover']),
                y=get_top_ten_vendors(start, end)['vendor'],
                orientation='h'
            )
        ],
        'layout': go.Layout(
            title='Top Ten Vendors'
        )
    }

    expense_breakdown_traces = []

    counter = 0

    expense_value_list = get_expenses_breakdown(start, end)['turnover'].tolist()
    expense_sub_category_list = get_expenses_breakdown(start, end)['desc'].tolist()
    expense_category_list = ['expense'] * len(expense_value_list)

    for v in expense_value_list:

        trace = go.Bar(
            x=[abs(v)],
            y=[expense_category_list[counter]],
            name=expense_sub_category_list[counter],
            orientation='h',
            hoverinfo='name'
        )

        expense_breakdown_traces.append(trace)

        counter += 1

    pl_expenses_breakdown_fig = {
        'data': expense_breakdown_traces,
        'layout': go.Layout(
            title='Operating Expenses Breakdown',
            barmode='stack',
            yaxis={
                'visible': False
            }
        )
    }

    return pl_sales_fig, pl_cogs_fig, pl_profit_fig, pl_margin_fig, pl_expenses_fig, pl_taxes_fig, \
        pl_income_fig, pl_income_percent_fig, waterfall_fig, pl_top_ten_customers_fig, pl_top_ten_vendors_fig, \
        pl_expenses_breakdown_fig


if __name__ == '__main__':
    app.run_server(debug=True)