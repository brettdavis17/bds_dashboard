import os
import requests
import json
import sqlite3
import pandas as pd

token_url = os.environ.get('TOKEN_URL')
token_payload = os.environ.get('TOKEN_PAYLOAD')
base_url = os.environ.get('BASE_URL')

def get_token():

    url = token_url

    payload = token_payload
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    token = json.loads(response.text)['token_type'] + ' ' + json.loads(response.text)['access_token']

    return token

def get_customers():

    token = get_token()

    url = base_url + "Customer?$select=CustomerID,CustomerName,CreatedDateTime,LastModifiedDateTime,Terms"

    payload = {}
    headers = {
        'Accept': 'application/json, text/json',
        'Authorization': token,
        'Cookie': 'UserBranch=4; requestid=38702; Locale=Culture=en-US&TimeZone=GMTM0600G; CompanyID=Bob Davis'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    customers = json.loads(response.text)

    return customers

def get_customer_locations():

    token = get_token()

    url = base_url + "CustomerLocation?$expand=LocationContact/Address"

    payload = {}
    headers = {
        'Accept': 'application/json, text/json',
        'Authorization': token,
        'Cookie': 'UserBranch=4; requestid=38702; Locale=Culture=en-US&TimeZone=GMTM0600G; CompanyID=Bob Davis'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    customer_locations = json.loads(response.text)

    return customer_locations

def get_accounts():

    token = get_token()

    url = base_url + "Account?$Select=AccountCD,AccountClass,AccountID,CreatedDateTime,LastModifiedDateTime,Type"

    payload = {}
    headers = {
        'Accept': 'application/json, text/json',
        'Authorization': token,
        'Cookie': 'UserBranch=4; requestid=38702; Locale=Culture=en-US&TimeZone=GMTM0600G; CompanyID=Bob Davis'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    accounts = json.loads(response.text)

    return accounts

def get_inventory():

    token = get_token()

    url = base_url + "StockItem?$filter=ItemClass eq 'BDS'&$Select=Description,InventoryID,ItemClass,"\
        "LastModified,PostingClass"

    payload = {}
    headers = {
        'Accept': 'application/json, text/json',
        'Authorization': token,
        'Cookie': 'UserBranch=4; requestid=38702; Locale=Culture=en-US&TimeZone=GMTM0600G; CompanyID=Bob Davis'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    inventory = json.loads(response.text)

    return inventory

def get_vendors():

    token = get_token()

    url = base_url + "Vendor?$Select=CreatedDateTime,LastModifiedDateTime,VendorID,VendorName"

    payload = {}
    headers = {
        'Accept': 'application/json, text/json',
        'Authorization': token,
        'Cookie': 'UserBranch=4; requestid=38702; Locale=Culture=en-US&TimeZone=GMTM0600G; CompanyID=Bob Davis'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    vendors = json.loads(response.text)

    return vendors

def get_journal_transaction_details():

    token = get_token()

    url = base_url + "JournalTransaction?$expand=Details&$filter=TransactionDate ge datetimeoffset'2020-01-01'"

    payload = {}
    headers = {
        'Accept': 'application/json, text/json',
        'Authorization': token,
        'Cookie': 'UserBranch=4; requestid=38702; Locale=Culture=en-US&TimeZone=GMTM0600G; CompanyID=Bob Davis'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    journal_transaction_details = json.loads(response.text)

    return journal_transaction_details

def get_invoices():

    token = get_token()

    url = base_url + "Invoice?$select=Amount,Balance,CreatedDateTime,Customer,CustomerOrder,Date,DueDate," \
                    "LastModifiedDateTime,LocationID,PostPeriod,ReferenceNbr,Status,Terms,Type" \
                    "&$filter=Date ge datetimeoffset'2020-01-01'"

    payload = {}
    headers = {
        'Accept': 'application/json, text/json',
        'Authorization': token,
        'Cookie': 'UserBranch=4; requestid=38702; Locale=Culture=en-US&TimeZone=GMTM0600G; CompanyID=Bob Davis'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    invoices = json.loads(response.text)

    return invoices

def get_open_invoices():

    token = get_token()

    url = base_url + "Invoice?$select=Amount,Balance,CreatedDateTime,Customer,CustomerOrder,Date,DueDate," \
                    "LastModifiedDateTime,LocationID,PostPeriod,ReferenceNbr,Status,Terms,Type" \
                    "&$filter=Date ge datetimeoffset'2020-01-01'&$filter=Status eq 'Open'"

    payload = {}
    headers = {
        'Accept': 'application/json, text/json',
        'Authorization': token,
        'Cookie': 'UserBranch=4; requestid=38702; Locale=Culture=en-US&TimeZone=GMTM0600G; CompanyID=Bob Davis'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    open_invoices = json.loads(response.text)

    return open_invoices

def get_subaccounts():

    token = get_token()

    url = base_url + "Subaccount"

    payload = {}
    headers = {
        'Accept': 'application/json, text/json',
        'Authorization': token,
        'Cookie': 'UserBranch=4; requestid=38702; Locale=Culture=en-US&TimeZone=GMTM0600G; CompanyID=Bob Davis'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    subaccounts = json.loads(response.text)

    return subaccounts

def get_periods():

    token = get_token()

    url = base_url + "FinancialPeriod?$expand=Details"

    payload = {}
    headers = {
        'Accept': 'application/json, text/json',
        'Authorization': token,
        'Cookie': 'UserBranch=4; requestid=38702; Locale=Culture=en-US&TimeZone=GMTM0600G; CompanyID=Bob Davis'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    periods = json.loads(response.text)

    return periods

def get_balance_sql_result():
    conn = sqlite3.connect('database/bds_dash.db')

    balance_sql = '''
        SELECT SUM(Balance) as totalBalance
        FROM openInvoices
        GROUP BY Status
        HAVING Status = 'Open'
    '''

    df = pd.read_sql(
        balance_sql,
        con=conn
    )

    conn.close()

    return sum(df['totalBalance'].tolist())

def get_past_due_sql_result():
    conn = sqlite3.connect('database/bds_dash.db')

    past_due_sql = '''
        SELECT SUM(Balance) as balance
        FROM openInvoices
        WHERE julianday('now') - julianday(DueDate) > 0
        GROUP BY Status
        HAVING Status = 'Open'
    '''

    df = pd.read_sql(
        past_due_sql,
        con=conn
    )

    conn.close()

    return sum(df['balance'].tolist())

def get_current_sql_result():
    conn = sqlite3.connect('database/bds_dash.db')

    current_sql = '''
        SELECT SUM(Balance) as balance
        FROM openInvoices
        WHERE julianday('now') - julianday(DueDate) <= 0
        GROUP BY Status
        HAVING Status = 'Open'
    '''

    df = pd.read_sql(
        current_sql,
        con=conn
    )

    conn.close()

    return sum(df['balance'].tolist())

def get_zero_to_thirty_sql_result():
    conn = sqlite3.connect('database/bds_dash.db')

    zero_to_thirty_sql = '''
        SELECT SUM(Balance) as balance
        FROM openInvoices
        WHERE julianday('now') - julianday(DueDate) > 0 AND julianday('now') - julianday(DueDate) < 30
        GROUP BY Status
        HAVING Status = 'Open'
    '''

    df = pd.read_sql(
        zero_to_thirty_sql,
        con=conn
    )

    conn.close()

    return sum(df['balance'].tolist())

def get_thirty_to_sixty_sql_result():
    conn = sqlite3.connect('database/bds_dash.db')

    thirty_to_sixty_sql = '''
        SELECT SUM(Balance) as balance
        FROM openInvoices
        WHERE julianday('now') - julianday(DueDate) >= 30 AND julianday('now') - julianday(DueDate) < 60
        GROUP BY Status
        HAVING Status = 'Open'
    '''

    df = pd.read_sql(
        thirty_to_sixty_sql,
        con=conn
    )

    conn.close()

    return sum(df['balance'].tolist())

def get_sixty_to_ninety_sql_result():
    conn = sqlite3.connect('database/bds_dash.db')

    sixty_to_ninety_sql = '''
        SELECT SUM(Balance) as balance
        FROM openInvoices
        WHERE julianday('now') - julianday(DueDate) >= 60 AND julianday('now') - julianday(DueDate) < 90
        GROUP BY Status
        HAVING Status = 'Open'
    '''

    df = pd.read_sql(
        sixty_to_ninety_sql,
        con=conn
    )

    conn.close()

    return sum(df['balance'].tolist())

def get_over_ninety_sql_result():
    conn = sqlite3.connect('database/bds_dash.db')

    over_ninety_sql = '''
        SELECT SUM(Balance) as balance
        FROM openInvoices
        WHERE julianday('now') - julianday(DueDate) >= 90
        GROUP BY Status
        HAVING Status = 'Open'
    '''

    df = pd.read_sql(
        over_ninety_sql,
        con=conn
    )

    conn.close()

    return sum(df['balance'].tolist())

print(get_over_ninety_sql_result())

def get_barchart_df():
    conn = sqlite3.connect('database/bds_dash.db')

    ar_group_graph_sql = '''
        SELECT SUM(Balance) as balance,
    	CASE
    	    WHEN (julianday('now') - julianday(DueDate)) > 90 THEN 'Over 90'
    	    WHEN (julianday('now') - julianday(DueDate)) > 60 THEN '60-90'
    		WHEN (julianday('now') - julianday(DueDate)) > 30 THEN '30-60'
    		WHEN (julianday('now') - julianday(DueDate)) > 0 THEN '0-30'
    		WHEN (julianday('now') - julianday(DueDate)) < 0 THEN 'Current'
    	END as PastDue
        FROM openInvoices
        WHERE Type = 'Invoice'
        GROUP BY PastDue
        ORDER BY
    	CASE PastDue
    		WHEN 'Current' THEN 5
    		WHEN '0-30' THEN 4
    		WHEN '30-60' THEN 3
    		WHEN '60-90' THEN 2
    		WHEN 'Over 90' THEN 1
    	END
    '''

    df = pd.read_sql(
        ar_group_graph_sql,
        con=conn
    )

    conn.close()

    return df

print(get_barchart_df())

def get_treemap_df():
    conn = sqlite3.connect('database/bds_dash.db')

    ar_customer_share_graph_sql = '''
        SELECT inv.Customer, (jtd.CreditAmount - jtd.DebitAmount) as amount, inv.Status as status,
    	CASE
    	    WHEN (julianday('now') - julianday(inv.DueDate)) > 90 THEN 'Over 90'
    	    WHEN (julianday('now') - julianday(inv.DueDate)) > 60 THEN '60-90'
    		WHEN (julianday('now') - julianday(inv.DueDate)) > 30 THEN '30-60'
    		WHEN (julianday('now') - julianday(inv.DueDate)) > 0 THEN '0-30'
    		WHEN (julianday('now') - julianday(inv.DueDate)) < 0 THEN 'Current'
    		WHEN inv.Type = 'Credit Memo' THEN 'Current'
    	END as PastDueStatus
        FROM journalTransactionDetails as jtd
        LEFT JOIN openInvoices as inv ON inv.ReferenceNbr = jtd.ReferenceNbr
        LEFT JOIN accounts as a ON a.AccountCD = jtd.Account
        WHERE Status = 'Open' and a.AccountClass = 'SALES' and inv.Date > '2020-02-01'
        GROUP BY PastDueStatus, Customer
    '''

    df1 = pd.read_sql(
        ar_customer_share_graph_sql,
        con=conn
    )

    conn.close()

    return df1

def get_scatter_graph_df():
    conn = sqlite3.connect('database/bds_dash.db')

    ar_scatter_graph_sql = '''
        SELECT (jtd.DebitAmount - jtd.CreditAmount) as amount, jtd.ReferenceNbr as refNbr, inv.Customer, c.CustomerName,
        CASE
            WHEN (julianday('now') - julianday(inv.DueDate)) > 120 THEN 120
    	    WHEN (julianday('now') - julianday(inv.DueDate)) < -30 THEN -30
    	    ELSE (julianday('now') - julianday(inv.DueDate))
    	END as days
    	FROM journalTransactionDetails as jtd
    	LEFT JOIN openInvoices as inv ON inv.ReferenceNbr = jtd.ReferenceNbr
    	LEFT JOIN customers as c ON c.CustomerID = inv.Customer
    	WHERE inv.Type = 'Invoice'
    	GROUP BY refNbr
    '''

    df2 = pd.read_sql(
        ar_scatter_graph_sql,
        con=conn
    )

    conn.close()

    return df2

def build_hierarchical_dataframe(df, levels, value_column):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value'])
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value'])
        dfg = df.groupby(levels[i:]).sum()
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'total'
        df_tree['value'] = dfg[value_column]
        df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
    total = pd.Series(dict(id='total', parent='',
                              value=df[value_column].sum()))
    df_all_trees = df_all_trees.append(total, ignore_index=True)
    return df_all_trees

def get_pl_sales(start, end):

    conn = sqlite3.connect('database/bds_dash.db')
    c = conn.cursor()

    pl_sales_sql = '''
        SELECT SUM(jtd.CreditAmount - jtd.DebitAmount)
        FROM journalTransactionDetails as jtd
        LEFT JOIN accounts as a ON a.AccountCD = jtd.Account
        LEFT JOIN journalTransactions as jt ON jt.BatchNbr = jtd.BatchNbr
        WHERE jt.TransactionDate >= ? and jt.TransactionDate <= ?
        GROUP BY a.AccountClass
        HAVING a.AccountClass = 'SALES'
    '''

    c.execute(pl_sales_sql, (start, end))

    result = [row for row in c]

    pl_sales_sql_result = result[0][0] if result != [] else 0

    c.close()

    return pl_sales_sql_result

def get_pl_other_rev(start, end):

    conn = sqlite3.connect('database/bds_dash.db')
    c = conn.cursor()

    pl_other_rev_sql = '''
        SELECT SUM(jtd.CreditAmount - jtd.DebitAmount)
        FROM journalTransactionDetails as jtd
        LEFT JOIN accounts as a ON a.AccountCD = jtd.Account
        LEFT JOIN journalTransactions as jt ON jt.BatchNbr = jtd.BatchNbr
        WHERE jt.TransactionDate >= ? and jt.TransactionDate <= ?
        GROUP BY a.AccountCD
        HAVING a.AccountCD = '7150'
    '''

    c.execute(pl_other_rev_sql, (start, end))

    result = [row for row in c]

    pl_other_rev_sql_result = result[0][0] if result != [] else 0

    c.close()

    return pl_other_rev_sql_result

def get_pl_cogs(start, end):

    conn = sqlite3.connect('database/bds_dash.db')
    c = conn.cursor()

    pl_cogs_sql = '''
        SELECT SUM(jtd.CreditAmount - jtd.DebitAmount)
        FROM journalTransactionDetails as jtd
        LEFT JOIN accounts as a ON a.AccountCD = jtd.Account
        LEFT JOIN journalTransactions as jt ON jt.BatchNbr = jtd.BatchNbr
        WHERE jt.TransactionDate >= ? and jt.TransactionDate <= ?
        GROUP BY a.AccountClass
        HAVING a.AccountClass = 'COGS'
    '''

    c.execute(pl_cogs_sql, (start, end))

    result = [row for row in c]

    pl_cogs_sql_result = result[0][0] if result != [] else 0

    c.close()

    return pl_cogs_sql_result

def get_pl_expenses(start, end):

    conn = sqlite3.connect('database/bds_dash.db')
    c = conn.cursor()

    #

    pl_expenses_sql = '''
        SELECT sum(jtd.CreditAmount - jtd.DebitAmount) as turnover
        FROM journalTransactionDetails as jtd
        LEFT JOIN journalTransactions as jt ON jt.BatchNbr = jtd.BatchNbr
        LEFT JOIN accounts as a ON a.AccountCD = jtd.Account
        WHERE jt.TransactionDate >= ? AND jt.TransactionDate <= ? AND a.AccountClass LIKE 'EX%' AND 
            a.AccountClass != 'COGS'|'EXTAX'
        GROUP BY a.Type = 'Expense'
    '''

    c.execute(pl_expenses_sql, (start, end))

    result = [row for row in c]

    pl_expenses_sql_result = result[0][0] if result != [] else 0

    c.close()

    return pl_expenses_sql_result

def get_pl_taxes(start, end):

    conn = sqlite3.connect('database/bds_dash.db')
    c = conn.cursor()

    pl_taxes_sql = '''
            SELECT sum(jtd.CreditAmount - jtd.DebitAmount) as turnover
            FROM journalTransactionDetails as jtd
            LEFT JOIN journalTransactions as jt ON jt.BatchNbr = jtd.BatchNbr
            LEFT JOIN accounts as a ON a.AccountCD = jtd.Account
            WHERE jt.TransactionDate >= ? AND jt.TransactionDate <= ?
            GROUP BY accountClass
            HAVING accountClass = 'EXTAX'
        '''

    c.execute(pl_taxes_sql, (start, end))

    result = [row for row in c]

    pl_taxes_sql_result = result[0][0] if result != [] else 0

    c.close()

    return pl_taxes_sql_result

def get_top_ten_customers(start, end):

    conn = sqlite3.connect('database/bds_dash.db')

    top_ten_customers_sql = '''
        SELECT jtd.VendorOrCustomer as customer, SUM(jtd.CreditAmount - jtd.DebitAmount) as turnover
        FROM journalTransactionDetails as jtd
        LEFT JOIN accounts as a ON a.AccountCD = jtd.Account
        LEFT JOIN journalTransactions as jt ON jt.BatchNbr = jtd.BatchNbr
        WHERE jt.TransactionDate >= ? AND jt.TransactionDate <= ? and a.AccountClass = 'SALES' AND a.AccountCD != '4280'
        GROUP BY customer
        ORDER BY turnover DESC
        LIMIT 10
    '''

    top_ten_customers_df = pd.read_sql(
        top_ten_customers_sql,
        con=conn,
        params=(start, end)
    ).sort_values(by='turnover')

    return top_ten_customers_df

def get_top_ten_vendors(start, end):

    conn = sqlite3.connect('database/bds_dash.db')

    top_ten_vendors_sql = '''
        SELECT jtd.VendorOrCustomer as vendor, SUM(jtd.CreditAmount - jtd.DebitAmount) as turnover
        FROM journalTransactionDetails as jtd
        LEFT JOIN accounts as a ON a.AccountCD = jtd.Account
        LEFT JOIN journalTransactions as jt ON jt.BatchNbr = jtd.BatchNbr
        WHERE jt.TransactionDate >= ? AND jt.TransactionDate <= ? and jtd.Account = '2050'
        GROUP BY vendor
        ORDER BY turnover ASC
        LIMIT 10
    '''

    top_ten_customers_df = pd.read_sql(
        top_ten_vendors_sql,
        con=conn,
        params=(start, end)
    ).sort_values(by='turnover', ascending=False)

    return top_ten_customers_df

def get_expenses_breakdown(start, end):

    conn = sqlite3.connect('database/bds_dash.db')

    expenses_breakdown_sql = '''
        SELECT jtd.Account as account, a.Description as desc, SUM(jtd.CreditAmount - jtd.DebitAmount) as turnover
        FROM journalTransactionDetails as jtd
        LEFT JOIN accounts as a on a.AccountCD = jtd.Account
        LEFT JOIN journalTransactions as jt ON jt.BatchNbr = jtd.BatchNbr
        WHERE jt.TransactionDate >= ? AND jt.TransactionDate <= ? AND a.AccountClass LIKE 'EX%' AND a.AccountClass != 'EXTAX'
        GROUP BY account
        ORDER BY turnover ASC
    '''

    expenses_breakdown_df = pd.read_sql(
        expenses_breakdown_sql,
        con=conn,
        params=(
            start,
            end
        )
    )

    return expenses_breakdown_df