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
                   ('Detalii: Christmas'            ,'Christmas'),                 # Saving
                   ('Detalii: Birthdays'            ,'Birthdays'),                 # Saving
                   ('Detalii: Domains'              ,'Domains'),                   # Saving
                   ('Detalii: Car replacement'      ,'Car replacement'),           # Saving
                   ('Detalii: Vacation'             ,'Vacation'),                  # Saving
                   ('Detalii: Car Repairs'          ,'Car Repairs'),               # Saving
                   ('Detalii: Home maintanance'     ,'Home Maintanance'),          # Saving
                   ('Detalii: Car Insurance'        ,'Car Insurance'),             # Saving
                   ('Tranzactie Round Up'           ,'Round-up'),                # Saving
                   #Monthly Bills   
                   #Kindergarden&School 
                   ('Scoala Primara EuroEd'         ,'Kindergarden&School'),   # KinderGarden and School - Euroed
                   #EON 
                   ('EON GAZ FURNZARE'              , 'EON'),                       # EON Natural Gaz
                   ('WWW.EON.RO/MYLINE'             , 'EON'),                      # Eon myline payment
                   ('E.ON'                          , 'EON'),                       # EON Natural Gaz   
                   ('AS. DE LOCATARI FRUMOASA II'   ,'Asociatie'),       # Plata Asociatie
                   #Phone
                   ('WWW.ORANGE.RO/YOXO'            , 'Phone'),                   # Orange Romania
                   ('myorangefix'                   , 'Internet'),                          # Orange Romania
                   ('ORANGE ROMANIA'                , 'Internet'),                          # Orange Romania
                   
                   #Maintanance&Water
                   #EON Buni
                   #Buni
                   #Bona
                   ('RO92INGB0000999905926537'      , 'Bona'),              # Plata bona
                   #HBOgo
                   ('HBO'                           , 'Streaming'),                                  # HBO GO
                   #RCS/RDS
                   ('RCS AND RDS SA'                , 'RCS/RDS'),                     # RCS/RDS online pay
                   #Netflix
                   ('NETFLIX'                       , 'Streaming'),                            # Netflix
                   ('Amazon Video'                  , 'Streaming'),                       # Amazon Video
                   
                   #Google Play
                   ('Google Payment'                , 'Google Play'),                 # Google Play
                   ('YouTubePremium'                , 'Streaming'),                 # Google Play
                   #Atelier
                   ('BANGGOOD'                      , 'Atelier'),                           # Bangood
                   ('ALIEXPRES'                    , 'Atelier'),                          # Aliexpress
                   #Games        
                   ('PAYPAL *PATREONIREL'           , 'Games'),                  # Games
                   ('PAYPAL *KINGUINDIGI'           , 'Games'),                  # Games
                   ('PAYPAL *2CO.COM'               , 'Games'),                      # Games
                   ('PAYPAL *DIGITALRIVE'           , 'Games'),                  # Games
                   
                   
                   #Everyday Expenses
                   #Everyday Expenses: Groceries
                   ('CARREFOUR'                     , 'Groceries'),                    # Carrefour
                   ('MPN LOGISTICS'                 , 'Groceries'),                # Carrefour
                   ('Zig Delivero'                  , 'Groceries'),                 # Carrefour
                   ('GILCA MIHAI FITNESS'           , 'Groceries'),          # Carrefour
                   ('Pantiru Mihai PFA'             , 'Groceries'),          # Carrefour
                   ('LIDL'                          , 'Groceries'),                         # LIDL
                   ('Lidl Discount'                , 'Groceries'),                 # LIDL
                   ('PICO MAG DEP'                  , 'Groceries'),                 # PiCo magazin
                   ('CRISNIC MARKET'                , 'Groceries'),               # Crisnic magazin
                   ('Glovo GLOVO PRIME'             , 'Groceries'),               # Glovo magazin
                   ('Auchan'                        , 'Groceries'),               # Auchan magazin
                   ('Terminal: Livrator  RO'        , 'Groceries'),               # Bringo magazin
                   ('MARYO S EAST '                 ,'Groceries'),               # 2 Pasi magazin
                   ('PENNY '                        ,'Groceries'),               # Penny magazin
                   ('MCS STORE'             ,'Groceries'),               # Meat concept Iasi


                   ('MY EVENTS SRL'                 , 'Office food'),              # Bistro Servici
                   ('SALAD BOX'                     , 'Office food'),                  # Bistro Servici
                   ('MADO'                          , 'Office food'),                       # Bistro Servici
                   ('OSPATUL ZEILOR'                , 'Office food'),             # Bistro Servici
                   ('SIMIGERIA PETRU'               , 'Office food'),            # Bistro Servici
                   ('BLACK DOT COFFEE'              , 'Office food'),           # Bistro Servici
                   ('NEATA CAFE'                    , 'Office food'),           # Bistro Servici
                   
                   

                   ('EMAG SHOWR'                    , 'Household Goods'),             # EMAG
                   ('DM FIL'                        , 'Household Goods'),                 # DM
                   ('ALTEX'                         , 'Household Goods'),                  # Altex
                   ('DM DROGERIE MARKT SRL'         , 'Household Goods'),  # DM
                   ('MOBILPAY*HAIRCARE'             , 'Household Goods'),  # DM

                   ('MOL'                           , 'Fuel'),                               # Benzinaria MOL
                   ('OMV'                           , 'Fuel'),                               # Benzinaria MOL
                   

                   ('IASI ETAX'                     , 'Impozite'),                          # Taxe si impozite Iasi
                   ('ING Gold'                      , 'Impozite'),                           # ING Card
                   ('MUNICIPIUL IASI SNEP  RO'      , 'Impozite'),           # Impozit apartament
                   ('ETAX'                          , 'Impozite'),                               # Impozit apartament ETAX




                   ('ARCADIA'                       , 'Medical'),                        # Arcadia Hospital
                   ('ARTIMA'                        , 'Medical'),                         # Farmacie ARTIMA
                   ('HELP NET FARMA'                , 'Medical'),                 # Farmacie Helpnet
                   ('SMILE DENT SRL'                , 'Medical'),                 # Dentist
                   ('FITERMAN'                      , 'Medical'),                       # Farmacie Fitterman
                   ('SENSIBLU'                      , 'Medical'),                       # Farmacie Sensiblu
                   ('D.D.I. RADIOLOGIE'             , 'Medical'),               # DDI medical radiografii
                   ('FARMACIA FLORA'                , 'Medical'),               # FARMACIA FLORA
                   ('FARMACIA DONA'                 , 'Medical'),               # FARMACIA Dona
                   ('ASKLEPIOS-RO'                  , 'Medical'),               # Onofriescu
                   ('ROPHARMA'                      , 'Medical'),               # ROPHARMA
                   ('LARA FARM'                     , 'Medical'),               # Lara Farm
                   ('ANA PHARM'                    , 'Medical'),               # Ana Pharm
                    

                   ('MARELBO'                       , 'Clothing'),                          # Marelbo
                   ('KOTON'                         , 'Clothing'),                            # KOTON
                   ('TAKKO'                         , 'Clothing'),                            # TAKKO
                   ('ZARA'                          , 'Clothing'),                             # ZARA
                   ('H&M'                           , 'Clothing'),                              # H&M
                   ('INA IULIUS MALL'               , 'Clothing'),                  # INA Iulius Mall 
                   ('SIA SOF'                       , 'Clothing'),                          # SIA SOF
                   ('CCC PALAS'                     , 'Clothing'),                        # CCC
                   ('MELI MELO FASHION'             , 'Clothing'),                # Meli Melo
                   ('ELEGANT PRICOP'                , 'Clothing'),                   # Elegant Group - Camasi
                   ('ART TRADITIE'                  , 'Clothing'),                     # magazin ie
                   ('SOPORAN RAVECA'                , 'Clothing'),                   # magazin ie
                   ('ROUMASPORT'                    , 'Clothing'),                       # Decathlon Botosani
                   ('HM Hennes'                     , 'Clothing'),                        # H&M
                   ('Zara.com'                      , 'Clothing'),                        # Zara.com    
                   ('SAMEDAY.RO'                    , 'Clothing'),                        # SameDay.ro
                   ('MAXI PET IASI '                     ,'Pets'),                    # Petshop
                   ('MPVET IASI'                        ,'Pets'),                    # Petshop

                   ('SEDCOMLIBRIS'                  ,'Library'),                    # Librarie
                   

                   ('PASTICCERIA MONTECAT'          , 'Restaurante'),       # Montecatini
                   ('PREMIER RESTAURANTS'           , 'Restaurante'),        # McDonalds
                   ('MOO CAFE PALAS DEP'            , 'Restaurante'),         # Moo
                   ('MAMMA MIA'                     , 'Restaurante'),                  # Mama mia
                   ('TUFFLI DEP RO'                 , 'Restaurante'),              # Tuffli
                   ('KFC'                           , 'Restaurante'),                        # KFC
                   ('VENETO RESTAURANT SRL'         , 'Restaurante'),      # Veneto
                   ('VO CHEF SRL'                   , 'Restaurante'),                # Vo
                   ('EVERTOGETHER SRL'              , 'Restaurante'),               
                   ('N BEES'                        , 'Restaurante'),               
                   ('PASTRY CASA DULCE'             , 'Restaurante'),               
                   ('NOODLE PACK'                   , 'Restaurante'),               
                   ('CASA TRADITIEI'                , 'Restaurante'),               
                   ('FRATELLI RISTORANTE'           , 'Restaurante'),               
                   ('BRIO GROUP'                    , 'Restaurante'),                # Petru
                   ('GRAPIC ARTISAN BAKERY'         , 'Restaurante'),                # Petru
                   ('COLUMBUS OPERATIONAL'          , 'Restaurante'),                # Petru
                   ('YOYOUGURT'                     , 'Restaurante'),                # MU
                   ('BETTY ICE'                     , 'Restaurante'),                # Petru
                   ('CORSINI PASTICCERI'            , 'Restaurante'),                # Petru
                   ('STRONGMNDCORP.SR'              , 'Restaurante'),                # Spartan 
                   ('DONUTERIE'                     , 'Restaurante'),                # Spartan 
                   ('BIO BOX SRL'                   , 'Restaurante'),                # Spartan 
                   ('Dinah  Aliment'                , 'Restaurante'),                # Petru
                   ('Veranda  RO'                   , 'Restaurante'),                # Veranda
                   ('ABI CONCEPT SAPTE'             , 'Restaurante'),                # Abi Concept
                   ('CARTOFISSERIE'                 , 'Restaurante'),                # Cartofisserie
                   ('SMART BUSINESS'                , 'Restaurante'),                # Smart Business  

                   ('Glovo'                         , 'Groceries'),               # Glovo restaurante
                   

                   ('Iasi 6 Bucium'                 , 'Unknown'),                # Petru
                   ('DISTRIBUTION SERVICES'         , 'Unknown'),                # Petru
                   ('COSTACHE M. IONUT'             , 'Unknown'),                # Petru
                   ('BETTY ICE'                     , 'Restaurante'),                # Petru
                   ('Beneficiar:De Basm'           , 'Education'),                # Educatie Cristina
                   

                   ('EUROSERVICE TECHNOLOGY'        , 'Washing'),                # Petru

                   ('UBER'                          , 'Taxi'),                # Petru
                   

                   ('Unorthodox Roa'                , 'Presents'),                # Cadouri Iulia
                   ('AMZNMktplace  GB'              , 'Presents'),                # Cadouri Iulia
                   ('DON SERAFIM'                   , 'Presents'),                # Jewlery
                   ('EP*bilet.ro'                   , 'Presents'),                # Concerte
                   ('PAYU*IABILET'                  , 'Presents'),                # Concerte
                   ('GOPAY  *BAVIXO.RO'             , 'Presents'),                # Hay clay
                   ('Super Entertaining SRL'        , 'Presents'),                # Superfun
                   ('EASYBOX STEFAN'                , 'Presents'),                # Superfun
                                      
                   ('BOAVISTA SPORT HOTEL'          , 'Hotels'),                # Boavista Timisoara
                   ('PRITAX INVEST'                 , 'Hotels'),                       # Pritax Sibiu 
                   
                   
                   ('LAVA&CUCE'                     , 'Curatenie & Ironing'),          # Curatatorie Iulius

                   ('IULIUS MANAGEMENT CENTER'      ,'Parcare'),        # Parcare Iulius
                   ('IULIUS PALAS7A ENT'            ,'Parcare'),              # Parcare Iulius
                   ('ATTRIUS DEVELOPMENTS'          ,'Parcare'),            # Parcare Iulius

                   ('BLISS BEAUTY'                  , 'Look&Feel'),                 # Bliss

                   ('ORANGE ROMANIA'                , 'Phone'),                       # Orange Romania
                   
                   ('PROZ.COM'                      , 'Carti'),                           # Proz
                   ('MOBILPAY*EDITURA-ART'          , 'Carti'),                           # Proz
                   ('Kindle Svcs'                   , 'Carti'),                           # Proz
                   
                   

                   ('NORIEL TOYS'                   , 'Toys'),                           # Noriel
                   ('CINEMA CITY'                   , 'Cinema'),                         # Noriel
                   
                   

                   ('LEROY MERLIN ROMANIA SRL'      , 'Home Maintanance'),# Home Maintenance
                   ('KITCHEN SHOP'                  , 'Home Maintanance'),            # Home Maintenance
                   ('DEDEMAN'                       , 'Home Maintanance'),                 # Home Maintenance
                   ('ARABESQUE'                     , 'Home Maintanance'),               # Home Maintenance    
                   ('PAYU*EMAG.RO'                  , 'Home Maintanance'),            # Home Maintenance    

                   ('Support Auto'                  , 'Car Repairs'),                 # Home Maintenance

                   ('GLOBEHOSTIN'                   , 'Site-uri'),                        # edomenii.ro

                   ('Retragere numerar'             , 'Retragere'),            # Extrageri

                   ('Allianz-Tiriac'                ,'Asigurari'),                     # Allianz-Tiriac

                   ('ALENTEJO'                      ,'Pocket Money Monica'),                     # Alentejo Pocket Money Monica
                   (' asigurare de viata'           ,'Health Insurance'),                     # Life Insurance
                   ('WALLET'                         ,'Software'),                     # Softare purchases
                   ('Scribd'                         ,'Software'),                     # Scribd

                   ('Realimentare Extra'            , 'ignore'),                                 # ignore transaction
                   ('transferata din linia de credit', 'ignore'),                    # ignore transaction
                   ('Detalii tranzactie'            , 'ignore')]                                 # ignore transaction

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
                                                'Outflow': row['Value_out'].replace('.', '').replace(',', '.'),
                                                'Inflow': row['Value_in'].replace('.', '').replace(',', '.')
                                                })

                        #categories ['String','Substring','Category','Found']
                        #do not write the blank categories to the file -> part of the pending tranzactions
                        if row['Details'].isspace() != True:
                            writerCategory.writerow({'String': row['Details'],
                                                    'Substring': findCategoryMapping(row['Details']),
                                                    'Category': category,
                                                    'Value_out': row['Value_out'].replace(',', '.'),
                                                    'Value_in': row['Value_in'].replace(',', '.')
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