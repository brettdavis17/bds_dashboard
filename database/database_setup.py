import sqlite3

conn = sqlite3.connect('bds_dash.db')
c = conn.cursor()

customers_sql = '''
    CREATE TABLE customers (
        CreatedDateTime TEXT,
        CustomerID TEXT,
        CustomerName TEXT,
        LastModifiedDateTime TEXT,
        Terms TEXT,
        PRIMARY KEY(CustomerID)
    )
'''

customer_location_sql = '''
    CREATE TABLE customerLocations (
        CreatedDateTime TEXT,
        CustomerID TEXT,
        LastModifiedDateTime TEXT,
        LocationID TEXT,
        AddressLine1 TEXT,
        AddressLine2 TEXT,
        City TEXT,
        Country TEXT,
        PostalCode TEXT,
        State TEXT,
        PRIMARY KEY(LocationID),
        FOREIGN KEY(CustomerID) REFERENCES customers(CustomerID)
    )
'''

inventory_sql = '''
    CREATE TABLE inventory (
        Description TEXT,
        InventoryID TEXT,
        ItemClass TEXT,
        LastModified TEXT,
        PostingClass TEXT,
        PRIMARY KEY(InventoryID)
    )
'''

vendors_sql = '''
    CREATE TABLE vendors (
        CreatedDateTime TEXT,
        LastModifiedDateTime TEXT,
        VendorID TEXT,
        VendorName TEXT,
        PRIMARY KEY(VendorID)
    )
'''

accounts_sql = '''
    CREATE TABLE accounts (
        AccountCD TEXT,
        AccountClass TEXT,
        AccountID INTEGER,
        CreatedDateTime TEXT,
        Description TEXT,
        LastModifiedDateTime TEXT,
        Type TEXT,
        PRIMARY KEY(AccountCD)
    )
'''

journal_transaction_sql = '''
    CREATE TABLE journalTransactions (
        BatchNbr TEXT,
        CreatedDateTime TEXT,
        LastModifiedDateTime TEXT,
        LedgerID TEXT,
        Module TEXT,
        PostPeriod TEXT,
        Status TEXT,
        TransactionDate TEXT,
        PRIMARY KEY(BatchNbr)
        FOREIGN KEY(PostPeriod) REFERENCES periods(FinancialPeriodID)
    )
'''

journal_transaction_details_sql = '''
    CREATE TABLE journalTransactionDetails (
        Account TEXT,
        BatchNbr TEXT,
        CreditAmount REAL,
        DebitAmount REAL,
        Description TEXT,
        InventoryID,
        LineNbr TEXT,
        Qty REAL,
        ReferenceNbr TEXT,
        Subaccount TEXT,
        TransactionDescription TEXT,
        UOM TEXT,
        VendorOrCustomer TEXT,
        PRIMARY KEY(LineNbr),
        FOREIGN KEY(InventoryID) REFERENCES inventory(InventoryID),
        FOREIGN KEY(Account) REFERENCES accounts(AccountCD),
        FOREIGN KEY(BatchNbr) REFERENCES journalTransactions(BatchNbr)
        FOREIGN KEY(ReferenceNbr) REFERENCES invoices(ReferenceNbr)
        FOREIGN KEY(Subaccount) REFERENCES subaccounts(SubaccountCD)
    )
'''

invoices_sql = '''
    CREATE TABLE invoices (
        Amount REAL,
        CreatedDateTime TEXT,
        Customer TEXT,
        CustomerOrder TEXT,
        Date TEXT,
        DueDate TEXT,
        LastModifiedDateTime TEXT,
        LocationID TEXT,
        PostPeriod TEXT,
        ReferenceNbr TEXT,
        Terms TEXT,
        Type TEXT,
        PRIMARY KEY(ReferenceNbr),
        FOREIGN KEY(Customer) REFERENCES customers(CustomerID),
        FOREIGN KEY(LocationID) REFERENCES customerLocations(LocationID),
        FOREIGN KEY(PostPeriod) REFERENCES periods(FinancialPeriodID)
    )
'''

open_invoices_sql = '''
    CREATE TABLE openInvoices (
        Amount REAL
        CreatedDateTime TEXT,
        Customer TEXT
        CustomerOrder TEXT,
        Date TEXT,
        DueDate TEXT,
        LastModifiedDateTime TEXT,
        LocationID TEXT,
        PostPeriod TEXT,
        ReferenceNbr TEXT,
        Status TEXT
        Terms TEXT,
        Type TEXT,
        PRIMARY KEY(ReferenceNbr),
        FOREIGN KEY(ReferenceNbr) REFERENCES invoices(ReferenceNbr)
        FOREIGN KEY(Customer) REFERENCES customers(CustomerID),
        FOREIGN KEY(LocationID) REFERENCES customerLocations(LocationID),
        FOREIGN KEY(PostPeriod) REFERENCES periods(FinancialPeriodID)
    )
'''

periods_sql = '''
    CREATE TABLE periods (
        Active INTEGER,
        AdjustmentPeriod INTEGER,
        ClosedInAP INTEGER,
        ClosedInAR INTEGER,
        ClosedInCA INTEGER,
        ClosedInFA INTEGER,
        ClosedInGL INTEGER,
        ClosedInIN INTEGER,
        ClosedInPR INTEGER,
        Description TEXT,
        EndDate TEXT,
        FinancialPeriodID TEXT,
        LengthInDays INTEGER,
        PeriodNbr TEXT,
        StartDate TEXT,
        PRIMARY KEY(FinancialPeriodID)
    )
'''

subaccounts_sql = '''
    CREATE TABLE subaccounts (
        Active INTEGER,
        Description TEXT,
        Secured INTEGER,
        SubaccountCD TEXT,
        SubaccountID INTEGER,
        PRIMARY KEY(SubaccountCD)
    )
'''

c.execute(customers_sql)
c.execute(customer_location_sql)
c.execute(inventory_sql)
c.execute(vendors_sql)
c.execute(accounts_sql)
c.execute(journal_transaction_sql)
c.execute(journal_transaction_details_sql)
c.execute(invoices_sql)
c.execute(open_invoices_sql)
c.execute(periods_sql)
c.execute(subaccounts_sql)

conn.commit()

conn.close()