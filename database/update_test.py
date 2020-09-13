import os
import requests
import json
import sqlite3
import pandas as pd
from functions import get_invoices

test_invoice = get_invoices()

test_invoice_list = []

test_invoice_list.append(test_invoice)

conn = sqlite3.connect('bds_dash.db')
c = conn.cursor()

data = []

for invoice in test_invoice_list:

    row_data = []
    amount = invoice['Amount']['value'] if invoice['Amount'] != {} else None
    balance = invoice['Balance']['value'] if invoice['Balance'] != {} else None
    created_date_time = invoice['CreatedDateTime']['value'] if invoice['CreatedDateTime'] != {} else None
    customer = invoice['Customer']['value'] if invoice['Customer'] != {} else None
    customer_order = invoice['CustomerOrder']['value'] if invoice['CustomerOrder'] != {} else None
    date = invoice['Date']['value'] if invoice['Date'] != {} else None
    due_date = invoice['DueDate']['value'] if invoice['DueDate'] != {} else None
    last_modified_date_time = invoice['LastModifiedDateTime']['value'] if invoice['LastModifiedDateTime'] != {} else None
    location_id = customer + '_' + invoice['LocationID']['value'] if invoice['LocationID'] != {} else None
    post_period = invoice['PostPeriod']['value'] if invoice['PostPeriod'] != {} else None
    reference_nbr = invoice['ReferenceNbr']['value'] if invoice['ReferenceNbr'] != {} else None
    status = invoice['Status']['value'] if invoice['Status'] != {} else None
    terms = invoice['Terms']['value'] if invoice['Terms'] != {} else None
    type = invoice['Type']['value'] if invoice['Type'] != {} else None

    row_data = [
        amount,
        balance,
        created_date_time,
        customer,
        customer_order,
        date,
        due_date,
        last_modified_date_time,
        location_id,
        post_period,
        reference_nbr,
        status,
        terms,
        type
    ]

    data.append(row_data)

invoices_df = pd.DataFrame(
    data=data,
    columns=[
        'Amount',
        'Balance',
        'CreatedDateTime',
        'Customer',
        'CustomerOrder',
        'Date',
        'DueDate',
        'LastModifiedDateTime',
        'LocationID',
        'PostPeriod',
        'ReferenceNbr',
        'Status',
        'Terms',
        'Type'
    ]
)

invoices_df.to_sql(
    'invoices',
    con=conn,
    if_exists='replace',
    index=False
)

print(test_invoice_list)