# Converter from ING csv format to YNAB csv format

## ING csv format
'''
Data,,,Detalii_tranzactie,,Debit,Credit
23 martie 2018,,,Cumparare POS,,"xx,xx",
,,,Nr. card: xxxx xxxx xxxx xxxx,,,
,,,Terminal: Numele companiei,,,
24 martie 2018,,,Cumparare POS,,"xx,xx",
,,,Terminal: Numele companiei,,,
'''

## Ynab CSV format
What does YNAB look for in a CSV file?
In order to import a CSV file into YNAB it must follow a specific structure. The 3 line example below outlines exactly how a file might look if it contained only 2 transactions.

Date,Payee,Category,Memo,Outflow,Inflow
01/25/12,Sample Payee,,Sample Memo for an outflow,100.00,
01/26/12,Sample Payee 2,,Sample memo for an inflow,,500.00

To format your file the way YNAB requires, open it in a text editor and make your transactions look like the sample ones above.

You'll notice every field is separated by a comma so it's important that every field is present in each line, even if your transactions don't fill every field. Always include the "Date,Payee,Category,Memo,Outflow,Inflow" line at the very top as it is required. 

Any field can be left blank except the date. Valid date formats:

DD/MM/YY
DD/MM/YYYY
DD/MM//YYYY
MM/DD/YY
MM/DD/YYYY
MM/DD//YYYY

Categories will only import if the category already exists in your budget file with the exact same name. Otherwise the categories will be ignored when importing the file.  Also, make sure that the categories are listed with the master category, followed by a colon, then the sub category.  For example Everyday Expenses: Groceries
