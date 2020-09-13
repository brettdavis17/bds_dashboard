import sqlite3
import pandas as pd
from database_functions import get_customers, get_customer_locations, get_vendors, get_accounts, \
    get_inventory, get_journal_transaction_details, get_invoices, get_open_invoices, get_subaccounts, \
    get_periods

conn = sqlite3.connect('bds_dash.db')
c = conn.cursor()

customers = get_customers()
customer_locations = get_customer_locations()
vendors = get_vendors()
accounts = get_accounts()
inventory = get_inventory()
journal_transaction_details = get_journal_transaction_details()
invoices = get_invoices()
open_invoices = get_open_invoices()
subaccounts = get_subaccounts()
periods = get_periods()

data = []
columns = []

for customer in customers:

    row_data = [
        v['value'] if isinstance(v, dict) and v != {} else \
            None if v == {} else \
                v \
        for k, v in customer.items()
    ]

    data.append(row_data)

    columns = [
        k for k, v in customer.items()
    ]

customers_df = pd.DataFrame(
    data=data,
    columns=columns
).drop(columns=[
    'files',
    'id',
    'rowNumber',
    'note',
    'custom'
]
)

print('customers_df done')

data = []

for location in customer_locations:

    created_date_time = str(location['CreatedDateTime']['value'])
    customer_id = location['Customer']['value']
    last_modified_date_time = str(location['LastModifiedDateTime']['value'])
    location_id = customer_id + '_' + location['LocationID']['value']
    address_line_1 = location['LocationContact']['Address']['AddressLine1']['value'] \
        if location['LocationContact']['Address']['AddressLine1'] != {} \
            else None
    address_line_2 = location['LocationContact']['Address']['AddressLine2']['value'] \
        if location['LocationContact']['Address']['AddressLine2'] != {} \
            else None
    city = location['LocationContact']['Address']['City']['value'] \
        if location['LocationContact']['Address']['City'] != {} \
            else None
    country = location['LocationContact']['Address']['Country']['value']
    postal_code = location['LocationContact']['Address']['PostalCode']['value'] \
        if location['LocationContact']['Address']['PostalCode'] != {} \
            else None
    state = location['LocationContact']['Address']['State']['value'] \
        if location['LocationContact']['Address']['State'] != {} \
            else None

    row_data = [
        created_date_time,
        customer_id,
        last_modified_date_time,
        location_id,
        address_line_1,
        address_line_2,
        city,
        country,
        postal_code,
        state
    ]

    data.append(row_data)

customer_location_df = pd.DataFrame(
    data=data,
    columns=[
        'CreatedDateTime',
        'CustomerID',
        'LastModifiedDateTime',
        'LocationID',
        'AddressLine1',
        'AddressLine2',
        'City',
        'Country',
        'PostalCode',
        'State'
    ]
)

print('customer_location_df done')

data = []
columns = []

for period in periods:
    for d in period['Details']:

        row_data = [
            v['value'] if isinstance(v, dict) and v != {} else \
                None if v != {} else \
                    v
            for k, v in d.items()
        ]

        columns = [
            k for k, v in d.items()
        ]

        data.append(row_data)

periods_df = pd.DataFrame(
    data=data,
    columns=columns
).drop(columns=[
    'files',
    'id',
    'rowNumber',
    'note',
    'custom'
]
)

print('periods_df done')

data = []

for account in accounts:

    account_cd = account['AccountCD']['value']
    account_class = account['AccountClass']['value'] if account['AccountClass'] != {} else None
    account_id = account['AccountID']['value']
    created_date_time = account['CreatedDateTime']['value']
    description = account['Description']['value'] if account['Description'] != {} else None
    last_modified_date_time = account['LastModifiedDateTime']['value']
    type = account['Type']['value']

    row_data = [
        account_cd,
        account_class,
        account_id,
        created_date_time,
        description,
        last_modified_date_time,
        type
    ]

    data.append(row_data)

accounts_df = pd.DataFrame(
    data=data,
    columns=[
        'AccountCD',
        'AccountClass',
        'AccountID',
        'CreatedDateTime',
        'Description',
        'LastModifiedDateTime',
        'Type'
    ]
)

print('accounts_df done')

data = []
columns = []

for s in subaccounts:

    row_data = [
        v['value'] if isinstance(v, dict) and v != {} else \
            None if v == {} else \
                v
        for k, v in s.items()
    ]

    columns = [
        k for k, v in s.items()
    ]

    data.append(row_data)

subaccounts_df = pd.DataFrame(
    data=data,
    columns=columns
).drop(columns=[
    'files',
    'id',
    'rowNumber',
    'note',
    'custom'
]
)

print('subaccounts_df done')

data = []
columns = []

for account in accounts:

    row_data = [
        v['value'] if isinstance(v, dict) and v != {} else \
            None if v == {} else \
                v \
        for k, v in account.items()
    ]

    columns = [
        k for k, v in account.items()
    ]

    data.append(row_data)

account_df = pd.DataFrame(
    data=data,
    columns=columns
).drop(columns=[
    'files',
    'id',
    'rowNumber',
    'note',
    'custom'
]
)

print('account_df done')

data = []
columns = []

for i in inventory:

    row_data = [
        v['value'] if isinstance(v, dict) and v != {} else \
            None if v == {} else \
                v
        for k, v in i.items()
    ]

    columns = [
        k for k, v in i.items()
    ]

    data.append(row_data)

inventory_df = pd.DataFrame(
    data=data,
    columns=columns
).drop(columns=[
    'files',
    'id',
    'rowNumber',
    'note',
    'custom'
]
)

print('inventory_df done')

data = []
columns = []

for vendor in vendors:

    row_data = [
        v['value'] if isinstance(v, dict) and v != {} else \
            None if v == {} else \
                v
        for k, v in vendor.items()
    ]

    columns = [
        k for k, v in vendor.items()
    ]

vendors_df = pd.DataFrame(
    data=data,
    columns=columns
).drop(columns=[
    'files',
    'id',
    'rowNumber',
    'note',
    'custom'
]
)

print('vendors_df done')

trans_data = []

for t in journal_transaction_details:

    batch_nbr = t['BatchNbr']['value']
    created_date_time = t['CreatedDateTime']['value']
    last_modified_date_time = t['LastModifiedDateTime']['value']
    ledger_id = t['LedgerID']['value']
    module = t['Module']['value']
    post_period = t['PostPeriod']['value']
    status = t['Status']['value']
    transaction_date = t['TransactionDate']['value']

    trans_row_data = [
        batch_nbr,
        created_date_time,
        last_modified_date_time,
        ledger_id,
        module,
        post_period,
        status,
        transaction_date
    ]

    trans_data.append(trans_row_data)

detail_data = []

for t in journal_transaction_details:
    for d in t['Details']:

        account = d['Account']['value'] if d['Account'] != {} else None
        batch_nbr = t['BatchNbr']['value'] if t['BatchNbr'] != {} else None
        credit_amount = d['CreditAmount']['value'] if d['CreditAmount'] != {} else None
        debit_amount = d['DebitAmount']['value'] if d['DebitAmount'] != {} else None
        description = d['Description']['value'] if d['Description'] != {} else None
        inventory_id = d['InventoryID']['value'] if d['InventoryID'] != {} else None
        line_nbr = batch_nbr + '_' + str(d['LineNbr']['value'])
        qty = d['Qty']['value'] if d['Qty'] != {} else None
        reference_nbr = d['ReferenceNbr']['value'] if d['ReferenceNbr'] != {} else None
        subaccount = d['Subaccount']['value'] if d['Subaccount'] != {} else None
        trans_description = d['TransactionDescription']['value'] if d['TransactionDescription'] != {} else None
        uom = d['UOM']['value'] if d['UOM'] != {} else None
        vendor_or_cust = d['VendorOrCustomer']['value'] if d['VendorOrCustomer'] != {} else None

        detail_row_data = [
            account,
            batch_nbr,
            credit_amount,
            debit_amount,
            description,
            inventory_id,
            line_nbr,
            qty,
            reference_nbr,
            subaccount,
            trans_description,
            uom,
            vendor_or_cust
        ]

        detail_data.append(detail_row_data)

transaction_df = pd.DataFrame(
    data=trans_data,
    columns=[
        'BatchNbr',
        'CreatedDateTime',
        'LastModifiedDateTime',
        'LedgerID',
        'Module',
        'PostPeriod',
        'status',
        'TransactionDate'
    ]
)

print('transaction_df done')

transaction_detail_df = pd.DataFrame(
    data=detail_data,
    columns=[
        'Account',
        'BatchNbr',
        'CreditAmount',
        'DebitAmount',
        'Description',
        'InventoryID',
        'LineNbr',
        'Qty',
        'ReferenceNbr',
        'Subaccount',
        'TransactionDescription',
        'UOM',
        'VendorOrCustomer'
    ]
)

print('transaction_detail_df done')

data = []

for invoice in invoices:

    amount = invoice['Amount']['value']
    created_date_time = invoice['CreatedDateTime']['value'] if invoice['CreatedDateTime'] != {} else None
    customer = invoice['Customer']['value'] if invoice['Customer'] != {} else None
    customer_order = invoice['CustomerOrder']['value'] if invoice['CustomerOrder'] != {} else None
    date = invoice['Date']['value'] if invoice['Date'] != {} else None
    due_date = invoice['DueDate']['value'] if invoice['DueDate'] != {} else None
    last_modified_date_time = invoice['LastModifiedDateTime']['value'] if invoice['LastModifiedDateTime'] != {} else None
    location_id = customer + '_' + invoice['LocationID']['value'] if invoice['LocationID'] != {} else None
    post_period = invoice['PostPeriod']['value'] if invoice['PostPeriod'] != {} else None
    reference_nbr = invoice['ReferenceNbr']['value'] if invoice['ReferenceNbr'] != {} else None
    terms = invoice['Terms']['value'] if invoice['Terms'] != {} else None
    type = invoice['Type']['value'] if invoice['Type'] != {} else None

    row_data = [
        amount,
        created_date_time,
        customer,
        customer_order,
        date,
        due_date,
        last_modified_date_time,
        location_id,
        post_period,
        reference_nbr,
        terms,
        type
    ]

    data.append(row_data)

invoices_df = pd.DataFrame(
    data=data,
    columns=[
        'Amount',
        'CreatedDateTime',
        'Customer',
        'CustomerOrder',
        'Date',
        'DueDate',
        'LastModifiedDateTime',
        'LocationID',
        'PostPeriod',
        'ReferenceNbr',
        'Terms',
        'Type'
    ]
)

print('invoices_df done')

print(invoices_df.head())

data = []

for invoice in open_invoices:

    amount = invoice['Amount']['value']
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

open_invoices_df = pd.DataFrame(
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
        'LocatdionID',
        'PostPeriod',
        'ReferenceNbr',
        'Status',
        'Terms',
        'Type'
    ]
)

print('open_invoices_df done')

customers_df.to_sql(
    'customers',
    con=conn,
    if_exists='append',
    index=False
)

customer_location_df.to_sql(
    'customerLocations',
    con=conn,
    if_exists='append',
    index=False
)

vendors_df.to_sql(
    'vendors',
    con=conn,
    if_exists='append',
    index=False
)

account_df.to_sql(
    'accounts',
    con=conn,
    if_exists='append',
    index=False
)

inventory_df.to_sql(
    'inventory',
    con=conn,
    if_exists='append',
    index=False
)

transaction_df.to_sql(
    'journalTransactions',
    con=conn,
    if_exists='append',
    index=False
)

transaction_detail_df.to_sql(
    'journalTransactionDetails',
    con=conn,
    if_exists='append',
    index=False
)

subaccounts_df.to_sql(
    'subaccounts',
    con=conn,
    if_exists='append',
    index=False
)

invoices_df.to_sql(
    'invoices',
    con=conn,
    if_exists='append',
    index=False
)

open_invoices_df.to_sql(
    'openInvoices',
    con=conn,
    if_exists='replace',
    index=False
)

periods_df.to_sql(
    'periods',
    con=conn,
    if_exists='append',
    index=False
)

conn.commit()

conn.close()