## ING csv to YNAB csv converter
##
## What does YNAB look for in a CSV file?
## In order to import a CSV file into YNAB it must follow a specific structure. The 3 line example below outlines exactly how a file might look if it contained only 2 transactions.
##
## Date,Payee,Category,Memo,Outflow,Inflow
## 01/25/12,Sample Payee,,Sample Memo for an outflow,100.00,
## 01/26/12,Sample Payee 2,,Sample memo for an inflow,,500.00
##
## To format your file the way YNAB requires, open it in a text editor and make your transactions look like the sample ones above.
##
## You'll notice every field is separated by a comma so it's important that every field is present in each line, even if your transactions don't fill every field. Always include the "Date,Payee,Category,Memo,Outflow,Inflow" line at the very top as it is required. 
##
## Any field can be left blank except the date. Valid date formats:
##
## DD/MM/YY
## DD/MM/YYYY
## DD/MM//YYYY
## MM/DD/YY
## MM/DD/YYYY
## MM/DD//YYYY
##
## Categories will only import if the category already exists in your budget file with the exact same name. Otherwise the categories will be ignored when importing the file.  Also, make sure that the categories are listed with the master category, followed by a colon, then the sub category.  For example Everyday Expenses: Groceries
##
## FREE online conversion tools
## Custom YNAB specific tool → http://halloffame.github.io/ynab-csv/ 
## Instructions on how to use it → https://github.com/halloffame/ynab-csv/blob/gh-pages/README.md
##
## Generic CSV conversion → http://csvconverter.gginternational.net/
##
## CSV Desktop software
## Windows - CSVed - Cardware
##
## Mac - XTabulator - $19.99 USD



import csv



data = ""
detalii_tranzactie = ""
debit = ""
credit = ""
with open('ynab_format.csv', 'w') as csvfile:
        fieldnames = ['Date','Payee','Category','Memo','Outflow','Inflow']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        with open('test.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:        
                        if row['Data']:
                                if data:
                                        print 'output: '+data+','+detalii_tranzactie+',"'+debit+'","'+credit+'"'
                                        writer.writerow({'Date': data, 'Memo': detalii_tranzactie, 'Outflow': debit , 'Inflow': credit})
                                print '----->'+row['Data']+','+row['Detalii_tranzactie']+',"'+row['Debit']+'","'+row['Credit']+'"'
                                data = row['Data']
                                detalii_tranzactie = row['Detalii_tranzactie']
                                debit = row['Debit'] 
                                credit = row['Credit']
                        else:
                                detalii_tranzactie = detalii_tranzactie + ' ' + row['Detalii_tranzactie']
                print 'output: '+data+','+detalii_tranzactie+',"'+debit+'","'+credit+'"'
                writer.writerow({'Date': data, 'Memo': detalii_tranzactie, 'Outflow': debit , 'Inflow': credit})
                   
                        
