# ING csv to YNAB csv converter

import csv
import glob

mappingCategory = [
                   #Monthly Bills
                   #Monthly Bills: Kindergarden&School
                   ('Scoala Primara EuroEd','Monthly Bills: Kindergarden&School'),   # KinderGarden and School - Euroed
                   ('SCOALA PRIMARA EUROED DEP', 'Monthly Bills: School'),           # Euroed
                   ('NETFLIX', 'Monthly Bills: Netflix'),                            # Netflix
                   #Monthly Bills: EON
                   ('EON GAZ FURNZARE', 'Monthly Bills: EON'),                       # EON Natural Gaz
                   ('WWW.MYLINE-EON.RO', 'Monthly Bills: EON'),                      # Eon myline payment
                   #Monthly Bills: Phone
                   ('ORANGE', 'Monthly Bills: Phone'),                               # Orange Romania
                   #Monthly Bills: Maintanance&Water
                   #Monthly Bills: EON Buni
                   #Monthly Bills: Buni
                   #Monthly Bills: Bona
                   #Monthly Bills: HBOgo
                   ('HBO', 'Monthly Bills: HBOgo'),                                  # HBO GO
                   #Monthly Bills: RCS/RDS
                   ('RCS AND RDS SA', 'Monthly Bills: RCS/RDS'),                     # RCS/RDS online pay
                   #Monthly Bills: Netflix
                   #Monthly Bills: Google Play
                   ('Google Payment', 'Monthly Bills: Google Play'),                 # Google Play
                   #Monthly Bills: Atelier
                   ('BANGGOOD', 'Monthly Bills: Atelier'),                           # Bangood        

                   #Everyday Expenses
                   #Everyday Expenses: Groceries
                   ('CARREFOUR', 'Everyday Expenses: Groceries'),                    # Carrefour
                   ('MPN LOGISTICS', 'Everyday Expenses: Groceries'),                # Carrefour
                   ('Zig Delivero', 'Everyday Expenses: Groceries'),                 # Carrefour
                   ('ROUMASPORT', 'Everyday Expenses: Groceries'),                   # Carrefour Bringo
                   ('RAILEANU TRANSPORT', 'Everyday Expenses: Groceries'),           # Carrefour Bringo
                   ('CRISNIC MARKET', 'Everyday Expenses: Groceries'),               # Pico
                   ('LIDL', 'Everyday Expenses: Groceries'),                         # LIDL
                   ('PICO MAG DEP  RO', 'Everyday Expenses: Groceries'),             # PiCo magazin
                   #Everyday Expenses: Fuel
                   ('MOL', 'Everyday Expenses: Fuel'),                               # Benzinaria MOL
                   #Everyday Expenses: Spending Money Tinel
                   ('STEAM GAMES', 'Everyday Expenses: Spending Money Tinel'),       # Joace
                   ('Retragere numerar', 'Everyday Expenses: Spending Money Tinel'),       # Extrageri        
                   #Everyday Expenses: Spending Money Monica
                   #Everyday Expenses: Office food
                   ('MY EVENTS SRL', 'Everyday Expenses: Office food'),              # Bistro Servici
                   ('SALAD BOX', 'Everyday Expenses: Office food'),                  # Bistro Servici
                   ('MADO', 'Everyday Expenses: Office food'),                       # Bistro Servici
                   ('OSPATUL ZEILOR', 'Everyday Expenses: Office food'),             # Bistro Servici
                   ('SIMIGERIA PETRU', 'Everyday Expenses: Office food'),            # Bistro Servici
                   #Everyday Expenses: Restaurants
                   ('Dinah  Aliment', 'Everyday Expenses: Restaurants'),             # Restaurante
                   ('VO CHEF', 'Everyday Expenses: Restaurants'),                    # Restaurante
                   ('CARTOFISSERIE', 'Everyday Expenses: Restaurants'),              # Restaurante
                   ('CANTINA STUDENTEASCA', 'Everyday Expenses: Restaurants'),       # Restaurante
                   ('MESOPOTAMIA', 'Everyday Expenses: Restaurants'),                # Restaurante
                   ('CORSO', 'Everyday Expenses: Restaurants'),                      # Restaurante
                   ('PASTICCERIA MONTECAT', 'Everyday Expenses: Restaurants'),       # Montecatini
                   ('PREMIER RESTAURANTS', 'Everyday Expenses: Restaurants'),        # McDonalds
                   ('MOO CAFE PALAS DEP', 'Everyday Expenses: Restaurants'),         # Moo
                   ('MAMMA MIA', 'Everyday Expenses: Restaurants'),                  # Mama mia
                   ('TUFFLI DEP RO', 'Everyday Expenses: Restaurants'),              # Tuffli
                   ('KFC', 'Everyday Expenses: Restaurants'),                        # KFC
                   #Everyday Expenses: Medical
                   ('ARCADIA', 'Everyday Expenses: Medical'),                        # Arcadia Hospital
                   ('ARTIMA', 'Everyday Expenses: Medical'),                         # Farmacie ARTIMA
                   ('ROPHARMA', 'Everyday Expenses: Medical'),                       # Farmacie ROPHARMA
                   ('HELP NET FARMA', 'Everyday Expenses: Medical'),                 # Farmacie Helpnet
                   ('SMILE DENT SRL', 'Everyday Expenses: Medical'),                 # Dentist
                   ('FITERMAN', 'Everyday Expenses: Medical'),                       # Farmacie Fitterman
                   ('SENSIBLU', 'Everyday Expenses: Medical'),                       # Farmacie Sensiblu
                   #Everyday Expenses: Clothing
                   ('MARELBO', 'Everyday Expenses: Clothing'),                       # Marelbo
                   ('KOTON', 'Everyday Expenses: Clothing'),                         # KOTON
                   ('TAKKO', 'Everyday Expenses: Clothing'),                         # TAKKO
                   ('ZARA', 'Everyday Expenses: Clothing'),                          # ZARA
                   ('H&M', 'Everyday Expenses: Clothing'),                           # H&M
                   ('INA IULIUS MALL', 'Everyday Expenses: Clothing'),               # INA Iulius Mall 
                   ('SIA SOF', 'Everyday Expenses: Clothing'),                       # SIA SOF
                   #Everyday Expenses: Household Goods
                   ('EMAG SHOWR', 'Everyday Expenses: Household Goods'),             # EMAG
                   ('DM FIL', 'Everyday Expenses: Household Goods'),                 # DM
                   ('ALTEX', 'Everyday Expenses: Household Goods'),                  # Altex
                   #Everyday Expenses: Toys
                   ('VARUNA', 'Everyday Expenses: Toys'),                            # Magazin Jucarii
                   #Everyday Expenses: Cleaning & Ironing
                   ('LAVA&CUCE', 'Everyday Expenses: Cleaning & Ironing'),          # Curatatorie Iulius
                   ('BLISS BEAUTY', 'Everyday Expenses: Cleaning & Ironing'),       # Bliss

                   #Rainy Day Funds
                   #Rainy Day Funds: Car Repairs
                   ('Support Auto', 'Rainy Day Funds: Car Repairs'),                 # Home Maintenance
                   #Rainy Day Funds: Home Maintenance
                   ('LEROY MERLIN ROMANIA SRL', 'Rainy Day Funds: Home Maintenance'),# Home Maintenance
                   ('DEDEMAN', 'Rainy Day Funds: Home Maintenance'),                 # Home Maintenance
                   #Rainy Day Funds: Car Insurance
                   #Rainy Day Funds: Birthdays
                   #Rainy Day Funds: Christmas

                   #Savings Goals
                   #Savings Goals: Car Replacement
                   #Savings Goals: Domains
                   ('GLOBEHOSTIN', 'Savings Goals: Domains'),                        # edomenii.ro
                   #Savings Goals: Vacation
                   #Savings Goals: Restaurants
                   #Savings Goals: Taxes
                   ('IASI ETAX', 'Yearly bills: Taxes'),                          # Taxe si impozite Iasi
                   ('ING Gold', 'Yearly bills: Taxes'),                           # ING Card
                   ('MUNICIPIUL IASI SNEP  RO', 'Yearly bills: Taxes'),              # Impozit apartament
                   ('ETAX', 'Yearly bills: Taxes'),                                  # Impozit apartament ETAX

                   #Debt
                   #Debt: Emergency Fund
                   ('Tranzactie Round Up','Debt: Emergency Fund'),                   # Saving
                   #Debt: Apartment payment
                   ('Rata Credit In contul: 9999', 'Debt: Apartment payment'),       # ING Credit
                   ('Prima asigurare ING Credit', 'Debt: Apartment payment'),        # Asigurare ING Credit

                   #ignored entries
                   ('Realimentare Extra', 'ignore'),                                 # ignore transaction
                   ('transferata din linia de credit', 'ignore'),                    # ignore transaction
                   ('Detalii tranzactie', 'ignore')]                                 # ignore transaction
                   

detalii_tranzactie = ""
debit = ""
credit = ""
category = ""

# map category to usual stores
# eg. Lidl, Everyday Expenses: Groceries


def findCategory(memoString):
    for stringMapping, mappedCategory in mappingCategory:
        if memoString.find(stringMapping) >= 0:
            return mappedCategory
    return ""


# convert each csv file in the folder
for filename in glob.glob('*.csv'):
    witeToFilename = "ynab_" + filename
    # create a file by appending ynab_ in front of the opened filename
    data = ""
    with open(witeToFilename, 'w') as csvfile:
        fieldnames = ['Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # process the file opened
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Data']:
                    # reached the end of a segment. start of a segment is marked by populated date.
                    # end of a segmend considered when another segment begins
                    if data:
                        print ('output: ' + data + ',' + detalii_tranzactie + ',"' + debit + '","' + credit + '"')
                        # try to identify category
                        category = findCategory(detalii_tranzactie)
                        # if category is ignore do not write something
                        if category.find('ignore') < 0:
                            # write the entry in YNAB csv
                            writer.writerow({'Date': data,
                                             'Memo': detalii_tranzactie,
                                             'Outflow': debit,
                                             'Inflow': credit,
                                             'Category': category})
                    printData = '----->' + row['Data'] + ','
                    printData += row['Detalii tranzactie'] + ',"'
                    printData += row['Debit'] + '","' + row['Credit'] + '"'
                    print (printData)
                    data = row['Data']
                    # Replace the romanian month by the number of the month
                    data = data.replace(" ianuarie ", "/01/")
                    data = data.replace(" februarie ", "/02/")
                    data = data.replace(" martie ", "/03/")
                    data = data.replace(" aprilie ", "/04/")
                    data = data.replace(" mai ", "/05/")
                    data = data.replace(" iunie ", "/06/")
                    data = data.replace(" iulie ", "/07/")
                    data = data.replace(" august ", "/08/")
                    data = data.replace(" septembrie ", "/09/")
                    data = data.replace(" octombrie ", "/10/")
                    data = data.replace(" noiembrie ", "/11/")
                    data = data.replace(" decembrie ", "/12/")
                    detalii_tranzactie = row['Detalii tranzactie']
                    debit = row['Debit']
                    credit = row['Credit']
                else:
                    detalii_tranzactie = detalii_tranzactie + \
                        ' ' + row['Detalii tranzactie']
            # catch also the last entry inside the import file
            print ('output: ' + data + ',' + detalii_tranzactie + ',"' + debit + '","' + credit + '"')
            # try to identify category
            category = findCategory(detalii_tranzactie)
            # write the entry in YNAB csv
            # if category is ignore do not write something
            if category.find('ignore') < 0:
                #write entry to file
                writer.writerow({'Date': data,
                                 'Memo': detalii_tranzactie,
                                 'Outflow': debit,
                                 'Inflow': credit,
                                 'Category': category})
