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
                   ('RO92INGB0000999905926537', 'Monthly Bills: Bona'),              # Plata bona
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
                   ('LIDL', 'Everyday Expenses: Groceries'),                         # LIDL
                   ('PICO MAG DEP  RO', 'Everyday Expenses: Groceries'),             # PiCo magazin
                   ('MARELBO', 'Everyday Expenses: Haine'),                          # Marelbo
                   ('MY EVENTS SRL RO', 'Everyday Expenses: Office food'),           # Bistro Servici
                   ('SALAD BOX', 'Everyday Expenses: Office food'),                  # Bistro Servici
                   ('MADO', 'Everyday Expenses: Office food'),                       # Bistro Servici
                   ('OSPATUL ZEILOR', 'Everyday Expenses: Office food'),             # Bistro Servici
                   ('SIMIGERIA PETRU', 'Everyday Expenses: Office food'),            # Bistro Servici
                   ('EON GAZ FURNZARE', 'Monthly Bills: EON'),                       # EON Natural Gaz
                   ('WWW.MYLINE-EON.RO', 'Monthly Bills: EON'),                      # Eon myline payment
                   ('EMAG SHOWR', 'Everyday Expenses: Household Goods'),             # EMAG
                   ('DM FIL', 'Everyday Expenses: Household Goods'),                 # DM
                   ('ALTEX', 'Everyday Expenses: Household Goods'),                  # Altex
                   ('MOL', 'Everyday Expenses: Benzina/Motorina'),                   # Benzinaria MOL
                   ('IASI ETAX', 'Yearly bills: Impozite'),                          # Taxe si impozite Iasi
                   ('ING Gold', 'Yearly bills: Impozite'),                           # ING Card
                   ('RCS AND RDS SA', 'Monthly Bills: RCS/RDS'),                     # RCS/RDS online pay
                   ('SCOALA PRIMARA EUROED DEP', 'Monthly Bills: School'),           # Euroed
                   ('NETFLIX', 'Monthly Bills: Netflix'),                            # Netflix
                   ('Google Payment', 'Monthly Bills: Google Play'),                 # Google Play
                   ('BANGGOOD', 'Monthly Bills: Atelier'),                           # Bangood
                   ('ARCADIA', 'Everyday Expenses: Medical'),                        # Arcadia Hospital
                   ('ARTIMA', 'Everyday Expenses: Medical'),                         # Farmacie ARTIMA
                   ('HELP NET FARMA', 'Everyday Expenses: Medical'),                 # Farmacie Helpnet
                   ('SMILE DENT SRL', 'Everyday Expenses: Medical'),                 # Dentist
                   ('FITERMAN', 'Everyday Expenses: Medical'),                       # Farmacie Fitterman
                   ('SENSIBLU', 'Everyday Expenses: Medical'),                       # Farmacie Sensiblu
                   ('KOTON', 'Everyday Expenses: Haine'),                            # KOTON
                   ('TAKKO', 'Everyday Expenses: Haine'),                            # TAKKO
                   ('ZARA', 'Everyday Expenses: Haine'),                             # ZARA
                   ('H&M', 'Everyday Expenses: Haine'),                              # H&M
                   ('INA IULIUS MALL', 'Everyday Expenses: Haine'),                  # INA Iulius Mall 
                   ('SIA SOF', 'Everyday Expenses: Haine'),                          # SIA SOF
                   ('HBO', 'Monthly Bills: HBOgo'),                                  # HBO GO
                   ('PASTICCERIA MONTECAT', 'Everyday Expenses: Restaurante'),       # Montecatini
                   ('PREMIER RESTAURANTS', 'Everyday Expenses: Restaurante'),        # McDonalds
                   ('MOO CAFE PALAS DEP', 'Everyday Expenses: Restaurante'),         # Moo
                   ('MAMMA MIA', 'Everyday Expenses: Restaurante'),                  # Mama mia
                   ('TUFFLI DEP RO', 'Everyday Expenses: Restaurante'),              # Tuffli
                   ('KFC', 'Everyday Expenses: Restaurante'),                        # KFC
                   ('LAVA&CUCE', 'Everyday Expenses: Curatenie & Ironing'),          # Curatatorie Iulius
                   ('BLISS BEAUTY', 'Everyday Expenses: Curatenie & Ironing'),       # Bliss
                   ('Rata Credit In contul: 9999', 'Debt: Credit apartament Buni'),  # ING Credit
                   ('Prima asigurare ING Credit', 'Debt: Credit apartament Buni'),   # Asigurare ING Credit
                   ('ORANGE ROMANIA', 'Monthly Bills: Telefon Tinel'),               # Orange Romania
                   ('LEROY MERLIN ROMANIA SRL', 'Rainy Day Funds: Home Maintenance'),# Home Maintenance
                   ('DEDEMAN', 'Rainy Day Funds: Home Maintenance'),                 # Home Maintenance
                   ('Support Auto', 'Rainy Day Funds: Car Repairs'),                 # Home Maintenance
                   ('GLOBEHOSTIN', 'Yearly bills: Site-uri'),                        # edomenii.ro
                   ('MUNICIPIUL IASI SNEP  RO', 'Yearly bills: Impozite'),           # Impozit apartament
                   ('ETAX', 'Yearly bills: Impozite'),                               # Impozit apartament ETAX
                   ('Retragere numerar', 'Everyday Expenses: Spending Money'),       # Extrageri
                   ('Transfer Home','Rainy Day Funds: Emergency Fund'),              # Saving
                   ('Realimentare Extra', 'ignore'),                                 # ignore transaction
                   ('transferata din linia de credit', 'ignore')]                    # ignore transaction

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
    with open(witeToFilename, 'wb') as csvfile:
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
                        print 'output: ' + data + ',' + detalii_tranzactie + ',"' + debit + '","' + credit + '"'
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
                    print printData
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
            print 'output: ' + data + ',' + detalii_tranzactie + ',"' + debit + '","' + credit + '"'
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
