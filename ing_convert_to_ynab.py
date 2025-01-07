# ING csv to YNAB csv converter

import csv
import glob

#configuration 


#fieldnames - the header file for the export from homebank
fieldnamesDefinition = ['Date', 'Blank1','Blank2', 'Details', 'Blank3', 'Blank4', 'Value_out','Blank5','Value_in','Blank6']
fieldnamesDefinitionPost = ['Date', 'Details', 'Value_out','Value_in']
fieldnamesDefinitionYNAB = ['Date','Payee','Category','Memo','Outflow','Inflow']
fieldnamesDefinitionCategoryManager = ['String','Substring','Category','Value_out','Value_in']

#cleanup rows
cleanRowMarkup = [
                    #Header
                    (0,'Titular cont'),
                    (0,'Sold initial'),
                    (0,'Sold final '),
                    (0,'CNP:'),
                    (0,"Str."),
                    (0,'Date'),
                    (1,'Data'),
                    (1,'Roxana Petria'),
                    (1,'Serviciu Dezvoltare'),
                    (2,'ING Bank N.V. Amsterdam'),
                    (2,'Sucursala Buc'),
                    (0,'Eliberat pentru')
]

#mapping category for the usual transfers
mappingCategory = [
                   #Savings
                   ('Detalii: Christmas','Savings Goals: Christmas'),                 # Saving
                   ('Detalii: Birthdays','Savings Goals: Birthdays'),                 # Saving
                   ('Detalii: Domains','Savings Goals: Domains'),                   # Saving
                   ('Detalii: Car replacement','Savings Goals: Car replacement'),           # Saving
                   ('Detalii: Vacation','Savings Goals: Vacation'),                  # Saving
                   ('Detalii: Car Repairs','Savings Goals: Car Repairs'),               # Saving
                   ('Detalii: Home maintanance','Savings Goals: Home Maintanance'),          # Saving
                   ('Detalii: Car Insurance','Savings Goals: Car Insurance'),             # Saving
                   ('Tranzactie Round Up','Savings Goals: Round-up'),                # Saving
                   #Monthly Bills
                   #Monthly Bills: Kindergarden&School
                   ('Scoala Primara EuroEd','Monthly Bills: Kindergarden&School'),   # KinderGarden and School - Euroed
                   #Monthly Bills: EON
                   ('EON GAZ FURNZARE', 'Monthly Bills: EON'),                       # EON Natural Gaz
                   ('WWW.EON.RO/MYLINE', 'Monthly Bills: EON'),                      # Eon myline payment
                   ('AS. DE LOCATARI FRUMOASA II','Monthly Bills: Asociatie'),       # Plata Asociatie
                   #Monthly Bills: Phone
                   ('WWW.ORANGE.RO/YOXO', 'Monthly Bills: Phone'),                   # Orange Romania
                   ('myorangefix', 'Monthly Bills: Internet'),                          # Orange Romania
                   ('ORANGE ROMANIA', 'Monthly Bills: Internet'),                          # Orange Romania
                   
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
                   ('NETFLIX', 'Monthly Bills: Netflix'),                            # Netflix
                   ('Amazon Video', 'Monthly Bills: Amazon Video'),                       # Amazon Video
                   
                   #Monthly Bills: Google Play
                   ('Google Payment', 'Monthly Bills: Google Play'),                 # Google Play
                   ('YouTubePremium', 'Monthly Bills: Google Play'),                 # Google Play
                   #Monthly Bills: Atelier
                   ('BANGGOOD', 'Monthly Bills: Atelier'),                           # Bangood
                   #Games        
                   ('PAYPAL *PATREONIREL', 'Monthly Bills: Games'),                  # Games
                   ('PAYPAL *KINGUINDIGI', 'Monthly Bills: Games'),                  # Games
                   ('PAYPAL *2CO.COM', 'Monthly Bills: Games'),                      # Games
                   ('PAYPAL *DIGITALRIVE', 'Monthly Bills: Games'),                  # Games
                   
                   
                   #Everyday Expenses
                   #Everyday Expenses: Groceries
                   ('CARREFOUR', 'Everyday Expenses: Groceries'),                    # Carrefour
                   ('MPN LOGISTICS', 'Everyday Expenses: Groceries'),                # Carrefour
                   ('Zig Delivero', 'Everyday Expenses: Groceries'),                 # Carrefour
                   ('GILCA MIHAI FITNESS', 'Everyday Expenses: Groceries'),          # Carrefour
                   ('Pantiru Mihai PFA', 'Everyday Expenses: Groceries'),          # Carrefour
                   ('LIDL', 'Everyday Expenses: Groceries'),                         # LIDL
                   ('PICO MAG DEP', 'Everyday Expenses: Groceries'),                 # PiCo magazin
                   ('CRISNIC MARKET', 'Everyday Expenses: Groceries'),               # PiCo magazin
                   ('Glovo GLOVO PRIME', 'Everyday Expenses: Groceries'),               # PiCo magazin
                   ('Auchan', 'Everyday Expenses: Groceries'),               # PiCo magazin
                   ('Terminal: Livrator  RO', 'Everyday Expenses: Groceries'),               # PiCo magazin


                   ('MY EVENTS SRL', 'Everyday Expenses: Office food'),              # Bistro Servici
                   ('SALAD BOX', 'Everyday Expenses: Office food'),                  # Bistro Servici
                   ('MADO', 'Everyday Expenses: Office food'),                       # Bistro Servici
                   ('OSPATUL ZEILOR', 'Everyday Expenses: Office food'),             # Bistro Servici
                   ('SIMIGERIA PETRU', 'Everyday Expenses: Office food'),            # Bistro Servici
                   ('BLACK DOT COFFEE', 'Everyday Expenses: Office food'),           # Bistro Servici
                   ('NEATA CAFE', 'Everyday Expenses: Office food'),           # Bistro Servici
                   
                   

                   ('EMAG SHOWR', 'Everyday Expenses: Household Goods'),             # EMAG
                   ('DM FIL', 'Everyday Expenses: Household Goods'),                 # DM
                   ('ALTEX', 'Everyday Expenses: Household Goods'),                  # Altex
                   ('DM DROGERIE MARKT SRL', 'Everyday Expenses: Household Goods'),  # DM
                   ('MOBILPAY*HAIRCARE', 'Everyday Expenses: Household Goods'),  # DM

                   ('MOL', 'Everyday Expenses: Fuel'),                               # Benzinaria MOL
                   ('OMV', 'Everyday Expenses: Fuel'),                               # Benzinaria MOL
                   

                   ('IASI ETAX', 'Yearly bills: Impozite'),                          # Taxe si impozite Iasi
                   ('ING Gold', 'Yearly bills: Impozite'),                           # ING Card
                   ('MUNICIPIUL IASI SNEP  RO', 'Yearly bills: Impozite'),           # Impozit apartament
                   ('ETAX', 'Yearly bills: Impozite'),                               # Impozit apartament ETAX




                   ('ARCADIA', 'Everyday Expenses: Medical'),                        # Arcadia Hospital
                   ('ARTIMA', 'Everyday Expenses: Medical'),                         # Farmacie ARTIMA
                   ('HELP NET FARMA', 'Everyday Expenses: Medical'),                 # Farmacie Helpnet
                   ('SMILE DENT SRL', 'Everyday Expenses: Medical'),                 # Dentist
                   ('FITERMAN', 'Everyday Expenses: Medical'),                       # Farmacie Fitterman
                   ('SENSIBLU', 'Everyday Expenses: Medical'),                       # Farmacie Sensiblu
                   ('D.D.I. RADIOLOGIE', 'Everyday Expenses: Medical'),               # DDI medical radiografii
                   ('FARMACIA FLORA', 'Everyday Expenses: Medical'),               # FARMACIA FLORA
                   ('FARMACIA DONA', 'Everyday Expenses: Medical'),               # FARMACIA Dona
                   ('ASKLEPIOS-RO', 'Everyday Expenses: Medical'),               # Onofriescu
                   ('ROPHARMA', 'Everyday Expenses: Medical'),               # ROPHARMA
                    

                   ('MARELBO', 'Everyday Expenses: Clothing'),                          # Marelbo
                   ('KOTON', 'Everyday Expenses: Clothing'),                            # KOTON
                   ('TAKKO', 'Everyday Expenses: Clothing'),                            # TAKKO
                   ('ZARA', 'Everyday Expenses: Clothing'),                             # ZARA
                   ('H&M', 'Everyday Expenses: Clothing'),                              # H&M
                   ('INA IULIUS MALL', 'Everyday Expenses: Clothing'),                  # INA Iulius Mall 
                   ('SIA SOF', 'Everyday Expenses: Clothing'),                          # SIA SOF
                   ('CCC PALAS', 'Everyday Expenses: Clothing'),                        # CCC
                   ('MELI MELO FASHION', 'Everyday Expenses: Clothing'),                # Meli Melo
                   ('ELEGANT PRICOP', 'Everyday Expenses: Clothing'),                   # Elegant Group - Camasi
                   ('ART TRADITIE', 'Everyday Expenses: Clothing'),                     # magazin ie
                   ('SOPORAN RAVECA', 'Everyday Expenses: Clothing'),                   # magazin ie
                   ('ROUMASPORT', 'Everyday Expenses: Clothing'),                       # Decathlon Botosani
                   
                   
                   ('SEDCOMLIBRIS','Everyday Expenses: Library'),                    # Librarie
                   

                   ('PASTICCERIA MONTECAT', 'Everyday Expenses: Restaurante'),       # Montecatini
                   ('PREMIER RESTAURANTS', 'Everyday Expenses: Restaurante'),        # McDonalds
                   ('MOO CAFE PALAS DEP', 'Everyday Expenses: Restaurante'),         # Moo
                   ('MAMMA MIA', 'Everyday Expenses: Restaurante'),                  # Mama mia
                   ('TUFFLI DEP RO', 'Everyday Expenses: Restaurante'),              # Tuffli
                   ('KFC', 'Everyday Expenses: Restaurante'),                        # KFC
                   ('VENETO RESTAURANT SRL', 'Everyday Expenses: Restaurante'),      # Veneto
                   ('VO CHEF SRL', 'Everyday Expenses: Restaurante'),                # Vo
                   ('EVERTOGETHER SRL', 'Everyday Expenses: Restaurante'),               
                   ('N BEES', 'Everyday Expenses: Restaurante'),               
                   ('PASTRY CASA DULCE', 'Everyday Expenses: Restaurante'),               
                   ('NOODLE PACK', 'Everyday Expenses: Restaurante'),               
                   ('CASA TRADITIEI', 'Everyday Expenses: Restaurante'),               
                   ('FRATELLI RISTORANTE', 'Everyday Expenses: Restaurante'),               
                   ('BRIO GROUP', 'Everyday Expenses: Restaurante'),                # Petru
                   ('GRAPIC ARTISAN BAKERY', 'Everyday Expenses: Restaurante'),                # Petru
                   ('COLUMBUS OPERATIONAL', 'Everyday Expenses: Restaurante'),                # Petru
                   ('YOYOUGURT', 'Everyday Expenses: Restaurante'),                # Petru
                   ('BETTY ICE', 'Everyday Expenses: Restaurante'),                # Petru
                   ('CORSINI PASTICCERI', 'Everyday Expenses: Restaurante'),                # Petru
                   ('STRONGMNDCORP.SR', 'Everyday Expenses: Restaurante'),                # Spartan 
                   ('DONUTERIE', 'Everyday Expenses: Restaurante'),                # Spartan 
                   ('BIO BOX SRL', 'Everyday Expenses: Restaurante'),                # Spartan 
                   ('Dinah  Aliment', 'Everyday Expenses: Restaurante'),                # Petru
                   ('Veranda  RO', 'Everyday Expenses: Restaurante'),                # Veranda
                   ('Glovo', 'Everyday Expenses: Groceries'),               # Glovo restaurante
                   

                   ('Iasi 6 Bucium', 'Everyday Expenses: Unknown'),                # Petru
                   ('DISTRIBUTION SERVICES', 'Everyday Expenses: Unknown'),                # Petru
                   ('COSTACHE M. IONUT', 'Everyday Expenses: Unknown'),                # Petru
                   ('BETTY ICE', 'Everyday Expenses: Restaurante'),                # Petru
                   ('NYX*SCINTERNATIONALCON', 'Everyday Expenses: Unknown'),                # Petru
                   ('Terminal: Timisoara 2 -Republici', 'Everyday Expenses: Unknown'),                # Petru
                   ('Piatra Neamt 2  RO', 'Everyday Expenses: Unknown'),                # Petru
                   ('Terminal: Curier Robert  RO', 'Everyday Expenses: Unknown'),                # Petru
                   ('Terminal: CTELOG 2022', 'Everyday Expenses: Unknown'),                # Petru
                   ('Terminal: ZOLSPORT 5', 'Everyday Expenses: Unknown'),                # Petru
                   ('PRITAX INVEST SRL', 'Everyday Expenses: Unknown'),                # Petru
                   ('NYX*ALBO-SITI', 'Everyday Expenses: Unknown'),                # Petru
                   ('ONE DISTRIBUTION COMPANY', 'Everyday Expenses: Unknown'),                # Petru
                   ('Gheorgheni - Kossuth', 'Everyday Expenses: Unknown'),                # Petru
                   ('COVASNICIUC DANIELA I.I.', 'Everyday Expenses: Unknown'),                # Petru
                   ('BEST REFLEX SRL', 'Everyday Expenses: Unknown'),                # Petru
                   

                   ('EUROSERVICE TECHNOLOGY', 'Monthly Bills: Washing'),                # Petru

                   ('UBER', 'Everyday Expenses: Taxi'),                # Petru
                   

                   ('Unorthodox Roa', 'Giving: Presents'),                # Cadouri Iulia
                   ('AMZNMktplace  GB', 'Giving: Presents'),                # Cadouri Iulia
                   ('DON SERAFIM', 'Giving: Presents'),                # Jewlery
                   ('EP*bilet.ro', 'Giving: Presents'),                # Concerte
                   ('PAYU*IABILET', 'Giving: Presents'),                # Concerte
                   ('GOPAY  *BAVIXO.RO', 'Giving: Presents'),                # Hay clay
                   ('Super Entertaining SRL', 'Giving: Presents'),                # Superfun
                   ('EASYBOX STEFAN', 'Giving: Presents'),                # Superfun
                                      
                   ('BOAVISTA SPORT HOTEL', 'Work: Hotels'),                # Boavista Timisoara
                   ('PRITAX INVEST', 'Work: Hotels'),                       # Pritax Sibiu 
                   
                   
                   ('LAVA&CUCE', 'Everyday Expenses: Curatenie & Ironing'),          # Curatatorie Iulius

                   ('IULIUS MANAGEMENT CENTER','Everyday Expenses: Parcare'),        # Parcare Iulius
                   ('IULIUS PALAS7A ENT','Everyday Expenses: Parcare'),              # Parcare Iulius
                   ('ATTRIUS DEVELOPMENTS','Everyday Expenses: Parcare'),            # Parcare Iulius

                   ('BLISS BEAUTY', 'Everyday Expenses: Look&Feel'),                 # Bliss

                   ('ORANGE ROMANIA', 'Monthly Bills: Phone'),                       # Orange Romania
                   
                   ('PROZ.COM', 'Monthly Bills: Carti'),                           # Proz
                   ('MOBILPAY*EDITURA-ART', 'Monthly Bills: Carti'),                           # Proz
                   ('Kindle Svcs', 'Monthly Bills: Carti'),                           # Proz
                   
                   

                   ('NORIEL TOYS', 'Monthly Bills: Toys'),                           # Noriel
                   ('CINEMA CITY', 'Monthly Bills: Cinema'),                         # Noriel
                   
                   

                   ('LEROY MERLIN ROMANIA SRL', 'Savings Goals: Home Maintanance'),# Home Maintenance
                   ('KITCHEN SHOP', 'Savings Goals: Home Maintanance'),            # Home Maintenance
                   ('DEDEMAN', 'Savings Goals: Home Maintanance'),                 # Home Maintenance
                   ('ARABESQUE', 'Savings Goals: Home Maintanance'),               # Home Maintenance    
                   ('PAYU*EMAG.RO', 'Savings Goals: Home Maintanance'),            # Home Maintenance    

                   ('Support Auto', 'Rainy Day Funds: Car Repairs'),                 # Home Maintenance

                   ('GLOBEHOSTIN', 'Yearly bills: Site-uri'),                        # edomenii.ro

                   ('Retragere numerar', 'Everyday Expenses: Retragere'),            # Extrageri

                   ('Allianz-Tiriac','Yearly bills: Asigurari'),                     # Allianz-Tiriac

                   ('Realimentare Extra', 'ignore'),                                 # ignore transaction
                   ('transferata din linia de credit', 'ignore'),                    # ignore transaction
                   ('Detalii tranzactie', 'ignore')]                                 # ignore transaction

detalii_tranzactie = ""
debit = ""
credit = ""
category = ""


#replace the data with the right type
def replaceDateING(dateString):
    dateString = dateString.replace(" ianuarie ", "/01/")
    dateString = dateString.replace(" februarie ", "/02/")
    dateString = dateString.replace(" martie ", "/03/")
    dateString = dateString.replace(" aprilie ", "/04/")
    dateString = dateString.replace(" mai ", "/05/")
    dateString = dateString.replace(" iunie ", "/06/")
    dateString = dateString.replace(" iulie ", "/07/")
    dateString = dateString.replace(" august ", "/08/")
    dateString = dateString.replace(" septembrie ", "/09/")
    dateString = dateString.replace(" octombrie ", "/10/")
    dateString = dateString.replace(" noiembrie ", "/11/")
    dateString = dateString.replace(" decembrie ", "/12/")
    return dateString


# map category to usual stores
# eg. Lidl, Everyday Expenses: Groceries


def findCategory(memoString):
    for stringMapping, mappedCategory in mappingCategory:
        if memoString.find(stringMapping) >= 0:
            return mappedCategory
    return ""

def findCategoryMapping(memoString):
    for stringMapping, mappedCategory in mappingCategory:
        if memoString.find(stringMapping) >= 0:
            return stringMapping
    return ""

# preprocess the file from ING
def preProcessIngExport(filename):
    #create a new file to have the original intact
    writeFilePreProcessName = "ynab_pre_" + filename
    #add the header to the csv file
    with open(writeFilePreProcessName, 'w') as csvfile:
        # add the field names to the file
        writer = csv.DictWriter(csvfile, fieldnames=fieldnamesDefinition)
        writer.writeheader()
        #filter all the unnecessary rows from the file
        with open(filename) as csvfile:
             reader = csv.reader(csvfile)
             for row in reader:
                #skip all the empty rows
                #print(row)
                row = dict(zip(fieldnamesDefinition, row))
                # skip all the unecessary rows
                writeToFile = True
                #eliminate the unnecessary data from the file
                for rowNumber, stringToIgnore in cleanRowMarkup:
                    #skip all the clean-up marked rows
                    #if line is a header do not treat it
                    #print(row)
                    if len(row) == 0: 
                        writeToFile = False
                        break
                    #print(""+fieldnamesDefinition[rowNumber] + " " + row[fieldnamesDefinition[rowNumber]] + " " + str(row[fieldnamesDefinition[rowNumber]].find(stringToIgnore)))
                    if row[fieldnamesDefinition[rowNumber]].find(stringToIgnore) >= 0: 
                        writeToFile = False
                        break
                #print(writeToFile)
                if writeToFile: writer.writerow(row)
# postprocess the file from ING
def postProcessIngExport(filename):
    writeFilePreProcessName = "ynab_pre_" + filename
    writeFilePostProcessName = "ynab_post_" + filename
    #repack all the rows into a single entry
    with open(writeFilePreProcessName) as csvfile:
            reader = csv.DictReader(csvfile)
            # add the field names to the file
            with open(writeFilePostProcessName, 'w', newline='') as csvWritefile:
                # add the field names to the file
                writer = csv.DictWriter(csvWritefile, fieldnames=fieldnamesDefinitionPost)
                writer.writeheader()
                detailsRow = ""
                dateValue = ""
                value_out = ""
                value_in = ""
                
                firstOccurence = True
                numberOfRows = 0
                for row in open(writeFilePreProcessName):
                    numberOfRows += 1
                lineCounter = 0
            
                for row in reader:
                    if row['Date'] != "":
                        #print onto the file
                        if firstOccurence == False:
                            #['Date', 'Details', 'Value_out','Value_in']                        
                            writer.writerow({'Date': dateValue,
                                            'Details': detailsRow,
                                            'Value_out': value_out,
                                            'Value_in': value_in
                                            })
                        #print(row['Date'])
                        #print(detailsRow)
                        dateValue = replaceDateING(row['Date'])
                        value_out = row['Value_out']
                        value_in = row['Value_in']
                        firstOccurence = False
                        detailsRow = row['Details']
                    else:
                        #add to the string value
                        detailsRow = detailsRow + " " + row['Details']
                    lineCounter = lineCounter + 1
                    #last row is marked by 'Sold ini"
                    if row['Date'].find('Sold ini') >= 0:  break
                    if lineCounter == numberOfRows:
                        #write last row
                        writer.writerow({'Date': dateValue,
                                        'Details': detailsRow,
                                        'Value_out': value_out,
                                        'Value_in': value_in
                                        })

# convert to YNAB format
def convertToYNAB(filename):
    writeFilePostProcessName = "ynab_post_" + filename
    writeFilePostProcessNameYNAB = "ynab_import_" + filename
    writeFileCategoryManager = 'ynab_categoryManager_'+filename
    payeeName = 'Not known'
    #if filename contains "890227" then payee is Tinel
    if filename.find("890227") >= 0:
        payeeName = 'Tinel'
    #if filename contains "883376" then payee is Monica
    if filename.find("883376") >= 0:
        payeeName = 'Monica'
        
    with open(writeFileCategoryManager, 'w', newline='') as csvWriteCategoryfile:
        writerCategory = csv.DictWriter(csvWriteCategoryfile, fieldnames=fieldnamesDefinitionCategoryManager)
        writerCategory.writeheader()
        #repack all the rows into a single entry
        with open(writeFilePostProcessName) as csvfile:
                reader = csv.DictReader(csvfile)
                # add the field names to the file
                with open(writeFilePostProcessNameYNAB, 'w', newline='') as csvWritefile:
                    # add the field names to the file
                    writer = csv.DictWriter(csvWritefile, fieldnames=fieldnamesDefinitionYNAB)
                    writer.writeheader()
                    for row in reader:                
                        #fieldnamesDefinitionYNAB = ['Date','Payee','Category','Memo','Outflow','Inflow']
                        #try to identify category

                        category = findCategory(row['Details'])
                        # if category is ignore do not write something
                        if category.find('ignore') < 0:
                            # write the entry in YNAB csv
                            #do not write the blank categories to the file -> part of the pending tranzactions
                            if row['Details'].isspace() != True:
                                writer.writerow({'Date': row['Date'],
                                                'Payee': payeeName, #Monica
                                                'Category': category,
                                                'Memo': row['Details'],
                                                'Outflow': row['Value_out'],
                                                'Inflow': row['Value_in']
                                                })

                        #categories ['String','Substring','Category','Found']
                        #do not write the blank categories to the file -> part of the pending tranzactions
                        if row['Details'].isspace() != True:
                            writerCategory.writerow({'String': row['Details'],
                                                    'Substring': findCategoryMapping(row['Details']),
                                                    'Category': category,
                                                    'Value_out': row['Value_out'],
                                                    'Value_in': row['Value_in']
                                                    })

for filename in glob.glob('*.csv'):
    preProcessIngExport(filename)
    postProcessIngExport(filename)
    convertToYNAB(filename)

# # convert each csv file in the folder
# for filename in glob.glob('*.csv'):
#     witeToFilename = "ynab_" + filename
#     # create a file by appending ynab_ in front of the opened filename
#     data = ""
#     with open(witeToFilename, 'w') as csvfile:
#         fieldnames = ['Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         # process the file opened
#         with open(filename) as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 if row['Data']:
#                     # reached the end of a segment. start of a segment is marked by populated date.
#                     # end of a segmend considered when another segment begins
#                     if data:
#                         print ('output: ' + data + ',' + detalii_tranzactie + ',"' + debit + '","' + credit + '"')
#                         # try to identify category
#                         category = findCategory(detalii_tranzactie)
#                         # if category is ignore do not write something
#                         if category.find('ignore') < 0:
#                             # write the entry in YNAB csv
#                             writer.writerow({'Date': data,
#                                              'Memo': detalii_tranzactie,
#                                              'Outflow': debit,
#                                              'Inflow': credit,
#                                              'Category': category})
#                     printData = '----->' + row['Data'] + ','
#                     printData += row['Detalii tranzactie'] + ',"'
#                     printData += row['Debit'] + '","' + row['Credit'] + '"'
#                     print (printData)
#                     data = row['Data']
#                     # Replace the romanian month by the number of the month
#                     data = data.replace(" ianuarie ", "/01/")
#                     data = data.replace(" februarie ", "/02/")
#                     data = data.replace(" martie ", "/03/")
#                     data = data.replace(" aprilie ", "/04/")
#                     data = data.replace(" mai ", "/05/")
#                     data = data.replace(" iunie ", "/06/")
#                     data = data.replace(" iulie ", "/07/")
#                     data = data.replace(" august ", "/08/")
#                     data = data.replace(" septembrie ", "/09/")
#                     data = data.replace(" octombrie ", "/10/")
#                     data = data.replace(" noiembrie ", "/11/")
#                     data = data.replace(" decembrie ", "/12/")
#                     detalii_tranzactie = row['Detalii tranzactie']
#                     debit = row['Debit']
#                     credit = row['Credit']
#                 else:
#                     detalii_tranzactie = detalii_tranzactie + \
#                         ' ' + row['Detalii tranzactie']
#             # catch also the last entry inside the import file
#             print ('output: ' + data + ',' + detalii_tranzactie + ',"' + debit + '","' + credit + '"')
#             # try to identify category
#             category = findCategory(detalii_tranzactie)
#             # write the entry in YNAB csv
#             # if category is ignore do not write something
#             if category.find('ignore') < 0:
#                 #write entry to file
#                 writer.writerow({'Date': data,
#                                  'Memo': detalii_tranzactie,
#                                  'Outflow': debit,
#                                  'Inflow': credit,
#                                  'Category': cate