# Converter from ING csv (homebank.ro) format to YNAB csv format

## How to use

### Executing the windows application
Get the latest release from https://github.com/tinel-c/ing-csv-to-ynab-csv/releases

Follow the steps each time you want to import:

1. Place the csv file in the same folder with ing_covert_to_ynab.exe
2. Execute ing_convert_to_ynab.exe by double clicking on it
3. Import to YNGSB the resulted csv file ynab_.csv 

YNAB is not supporting the classic application. Ported the YNAB application to google spreadsheet.

### Executing python code
Before use:
* open ing_convert_to_ynab.py with your favorite editor and edit your usual store and categories.
* Install python on your PC.

Follow the steps each time you want to import:

1. Export transactions to a csv file from homebank.ro (-filename-.csv)
2. Place the py script in the same folder
3. Execute the py script to output ynab_-filename-.csv
4. Import to YNGSB the resulted csv file ynab_.csv 

### Creating the google sheet application

Follow the the steps:

1. Create a new sheet in google sheets and name it to your needs
2. Create the following sheets YNGSB , Transactions , Import , Log
3. Go to Extentions -> Apps Script
4. Copy the code from Code.gs
5. Save and reload the browser in the google sheet tab
6. A new Menu will apear Budget
7. Click Budget -> Initialize spreadsheet while having YNGSB selected
8. Click Budget -> Process formulas 

Interface ready to track the budget like in the classic YNAB.

How to import:
1. After running the python script copy all entries toghether with the header inside the Import sheet
2. Budget -> Import new transactions from ING
3. Budget -> Process transactions


## ING csv format
```
Data,,,Detalii_tranzactie,,Debit,Credit
23 martie 2018,,,Cumparare POS,,"xx,xx",
,,,Nr. card: xxxx xxxx xxxx xxxx,,,
,,,Terminal: Numele companiei,,,
24 martie 2018,,,Cumparare POS,,"xx,xx",
,,,Terminal: Numele companiei,,,
```

## YNAB csv format
What does YNAB look for in a CSV file?
In order to import a CSV file into YNAB it must follow a specific structure. The 3 line example below outlines exactly how a file might look if it contained only 2 transactions.

```
Date,Payee,Category,Memo,Outflow,Inflow
01/25/12,Sample Payee,,Sample Memo for an outflow,100.00,
01/26/12,Sample Payee 2,,Sample memo for an inflow,,500.00
```

To format your file the way YNAB requires, open it in a text editor and make your transactions look like the sample ones above.

You'll notice every field is separated by a comma so it's important that every field is present in each line, even if your transactions don't fill every field. Always include the "Date,Payee,Category,Memo,Outflow,Inflow" line at the very top as it is required. 

Any field can be left blank except the date. Valid date formats:

```
DD/MM/YY
DD/MM/YYYY
DD/MM//YYYY
MM/DD/YY
MM/DD/YYYY
MM/DD//YYYY
```

Categories will only import if the category already exists in your budget file with the exact same name. Otherwise the categories will be ignored when importing the file.  Also, make sure that the categories are listed with the master category, followed by a colon, then the sub category.  For example Everyday Expenses: Groceries

# Release

Converter for pyton 3 to exe:

```
$ pip install auto-py-to-exe
```
Then to run it, execute the following in the terminal:

```
$ auto-py-to-exe
```