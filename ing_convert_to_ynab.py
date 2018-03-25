# ING csv to YNAB csv converter

import csv
import glob

mappingCategory = [('CARREFOUR ROMANIA', 'Everyday Expenses: Mancare'),              # Carrefour
                   ('LIDL', 'Everyday Expenses: Mancare'),                           # LIDL
                   ('EON GAZ FURNZARE', 'Monthly Bills: Gaz'),                       # EON GAZ
                   ('WWW.MYLINE-EON.RO', 'Monthly Bills: Gaz'),                      # Eon myline payment
                   ('DEDEMAN', 'Everyday Expenses: Household Goods'),                # Dedeman
                   ('EMAG SHOWR', 'Everyday Expenses: Household Goods'),             # EMAG
                   ('DM FIL', 'Everyday Expenses: Household Goods'),                 # DM
                   ('MOL', 'Everyday Expenses: Benzina/Motorina'),                   # Benzinaria MOL
                   ('IASI ETAX', 'Yearly bills: Impozite'),                          # Taxe si impozite Iasi
                   ('ING Gold', 'Yearly bills: Impozite'),                           # ING Card
                   ('digicare.rcs-rds.ro', 'Monthly Bills: RCS/RDS'),                # RCS/RDS online pay
                   ('Netflix', 'Monthly Bills: Netflix'),                            # Netflix
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
                   ('HBOEUROPESRO', 'Monthly Bills: HBOgo'),                         # HBO GO
                   ('PASTICCERIA MONTECAT', 'Everyday Expenses: Restaurante'),       # Montecatini
                   ('PREMIER RESTAURANTS', 'Everyday Expenses: Restaurante'),        # McDonalds
                   ('KFC', 'Everyday Expenses: Restaurante'),                        # KFC
                   ('LAVA&CUCE', 'Everyday Expenses: Curatenie & Ironing'),          # Curatatorie Iulius
                   ('Rata Credit In contul: 9999', 'Debt: Credit apartament Buni'),  # ING Credit
                   ('Prima asigurare ING Credit', 'Debt: Credit apartament Buni'),   # Asigurare ING Credit
                   ('ORANGE ROMANIA', 'Monthly Bills: Telefon Tinel'),               # Orange Romania
                   ('GLOBEHOSTIN', 'Yearly bills: Site-uri')]                        # edomenii.ro

detalii_tranzactie = ""
debit = ""
credit = ""
category = ""

# map category to usual stores
# eg. Lidl, Everyday Expenses: Mancare


def findCategory(memoString):
    for stringMapping, mappedCategory in mappingCategory:
        if memoString.find(stringMapping) > 0:
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
            writer.writerow({'Date': data,
                             'Memo': detalii_tranzactie,
                             'Outflow': debit,
                             'Inflow': credit,
                             'Category': category})
