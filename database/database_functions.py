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

    url = base_url + "Account?$Select=AccountCD,AccountClass,AccountID,CreatedDateTime," + \
          "Description,LastModifiedDateTime,Type"

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

    url = base_url + "JournalTransaction?$expand=Details&$filter=LastModifiedDateTime gt datetimeoffset'2020-07-01'"

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
                    "&$filter=LastModifiedDateTime gt datetimeoffset'2020-07-01'"

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
                    "&$filter=LastModifiedDateTime gt datetimeoffset'2020-07-01' and Status eq 'Open'"

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
