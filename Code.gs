// Blue colors
const NavyBlue = '#05445E';
const BlueGrotto = '#189AB4';
const BlueGreen = '#75E6DA';
const BabyBlue1 = '#D4F1F4';
const BabyBlue2 = '#B1D4E0';

// Red Colors
const Cream = '#F9F1F0';
const RoseQuartz = '#FADCD9';
const DustyRose = '#F8AFA6';
const Coral = '#F79489';

// Green Colors
const OliveGreen = '#3D550C';
const LimeGreen = '#81B622';
const YellowGreen = '#ECF87F';
const Green = '#59981A';

// Delimiters
const CoolGray = '#E4E5E8';
const GunmetalGrey = '#53565A';
const BurgundyRedGrey = '#4D0011';
const OliveGreenGray  = '#4B443C';

// The main categories will have only formulas in the google sheet they will only consolidate the data below them
var defaultMainCategories = ['Monthly Bills',
                            'Everyday Expenses',
                            'Rainy Day Funds',
                            'Savings Goals',
                            'Debt'];

// categoryMatrix Array constructs the structure of the data categories and subcategories to be able to calculate the offsets inside the sheet
// it needs to be triggered each time as the data is not persistent betweeen calls from the google spreadsheet
var categoryMatrixArray = [];


// Function that populates with 2 colors each alternate month inside the google sheet
function getAlternatingBackgroundColor(i){
  if((i/3)%2 == 0)
  {
    return BabyBlue1;
  } else
  {
    return BabyBlue2;
  }
}

// Function used to get the names of each month to populate them at the header of the google sheet
function getMonthNames(i) {
  var monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  return monthNames[i];
}

// function used to debug the scripts creates the posibility to report out from the server runing of the scripts
function appendToLogSheet(message,value) {
  // Access the active spreadsheet
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  
  // Get the sheet named 'Log'
  var logSheet = spreadsheet.getSheetByName('Log');
  
  // Check if the 'Log' sheet exists
  if (logSheet) {
    // Data to append; replace with your actual data
    var rowData = [message, value];
    
    // Append the data as a new row
    logSheet.appendRow(rowData);
    
    // Optional: Log a message to confirm the action
    Logger.log('Row appended successfully.');
  } else {
    // If the 'Log' sheet doesn't exist, log an error message
    Logger.log("Sheet named 'Log' not found.");
  }
}

// Creates a black line as a separator inside the sheet used instead of the borders function for the horizontal lines
function setDelimiterRow(i,colorTone) {
  const sheet = SpreadsheetApp.getActiveSheet();
  sheet.getRange(i, 1, 1, 37).setBackground(GunmetalGrey);
  sheet.setRowHeight(i,2);
}


// main function executed on the initial opening of the sheet 
// creates a main menu that can be used to utilize the application
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  //create budget menu
  ui.createMenu('Budget')
    .addItem('Initialize spreadsheet', 'formatSheet')
    .addItem('Process categories', 'processCategories')
    .addItem('Process formulas', 'populateFormulas')
    .addItem('Import new tranzactions from ING','importNewTransactions')
    .addItem('Process transactions','processTransactions')
    .addToUi();

  processCategories();
}

// find row by cell value 
// used to make bold the main categories that have been created
function findRowByValue(searchValue) {
  // Access the active spreadsheet and the "YNGSB" sheet
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = spreadsheet.getSheetByName("YNGSB");

  // Create a TextFinder to search for the value in column A
  var textFinder = sheet.createTextFinder(searchValue);
  var foundRange = textFinder.findNext();

  // Check if the value was found
  if (foundRange) {
    // Get the row number of the found value
    var rowNumber = foundRange.getRow();
    Logger.log('Value found at row: ' + rowNumber);
    return rowNumber;
  } else {
    Logger.log('Value not found.');
    return -1; // Return -1 if the value is not found
  }
}

// should be triggered only once when creating a new budget
function formatSheet() {
  const sheet = SpreadsheetApp.getActiveSheet();
  var i;
  // cagegories column should be 100px
  sheet.setColumnWidth(1,150); 
  //each month is composed of a column of 150px and one of 100px
  // set key formulas
  sheet.getRange(1,1).setValue('Keys');
  sheet.getRange(1,1).setFontWeight("bold");
  sheet.getRange(1,1).setFontColor(GunmetalGrey);
  sheet.getRange(1,1).setBackground(CoolGray);
  sheet.getRange(1,1).setHorizontalAlignment('center');
  sheet.getRange(1,1).setFontSize(14);

  // Sum of all transactions
  targetCell = sheet.getRange(4,1,1,1);
  rangeFormulaString = '=SUM(Transactions!E2:E1000)';
  targetCell.setFormula(rangeFormulaString);
  // sum of all income
  targetCell = sheet.getRange(6,1,1,1);
  rangeFormulaString = '=SUM(Transactions!F2:F1000)';
  targetCell.setFormula(rangeFormulaString);

  for(i=0;i<36;i=i+3)
  {
    // set column colors
    
    sheet.getRange(1,2+i,100,3).setBackground(getAlternatingBackgroundColor(i));

    sheet.getRange(1,2+i).setValue(getMonthNames(i/3));
    sheet.getRange(1,2+i).setFontWeight("bold");
    sheet.getRange(1,2+i).setFontColor(GunmetalGrey);
    sheet.getRange(1,2+i).setBackground(CoolGray);
    sheet.getRange(1,2+i,1,3).mergeAcross();
    sheet.getRange(1,2+i,1,3).setHorizontalAlignment('center');
    sheet.getRange(1,2+i).setFontSize(14);

    setDelimiterRow(2,GunmetalGrey);

    sheet.getRange(3,2+i).setValue("Not Budgeted");
    sheet.getRange(3,2+i).setFontWeight("bold");
    sheet.getRange(3,2+i).setFontSize(8);
    sheet.getRange(3,2+i).setFontColor(NavyBlue);
    sheet.getRange(3,3+i,1,2).mergeAcross();

    sheet.getRange(4,2+i).setValue("Spent");
    sheet.getRange(4,2+i).setFontWeight("bold");
    sheet.getRange(4,2+i).setFontSize(8);
    sheet.getRange(4,2+i).setFontColor(NavyBlue);
    sheet.getRange(4,3+i,1,2).mergeAcross();

    sheet.getRange(5,2+i).setValue("Remaining");
    sheet.getRange(5,2+i).setFontWeight("bold");
    sheet.getRange(5,2+i).setFontSize(8);
    sheet.getRange(5,2+i).setFontColor(NavyBlue);
    sheet.getRange(5,3+i,1,2).mergeAcross();

    sheet.getRange(6,2+i).setValue("Overall income");
    sheet.getRange(6,2+i).setFontWeight("bold");
    sheet.getRange(6,2+i).setFontSize(8);
    sheet.getRange(6,2+i).setFontColor(NavyBlue);
    sheet.getRange(6,3+i,1,2).mergeAcross();

    sheet.getRange(7,2+i).setValue("Budgeted");
    sheet.getRange(7,2+i).setFontWeight("bold");
    sheet.getRange(7,2+i).setFontSize(8);
    sheet.getRange(7,2+i).setFontColor(BurgundyRedGrey);
    sheet.getRange(7,3+i,1,2).mergeAcross();

    sheet.getRange(8,2+i).setValue("Available");
    sheet.getRange(8,2+i).setFontWeight("bold");
    sheet.getRange(8,2+i).setFontSize(10);
    sheet.getRange(8,2+i).setFontColor(Green);
    sheet.getRange(8,3+i,1,2).mergeAcross();

    sheet.setColumnWidth(2+i,100); 
    sheet.setColumnWidth(3+i,50); 
    sheet.setColumnWidth(4+i,50); 

    setDelimiterRow(9,GunmetalGrey);

    sheet.getRange(10,1).setBackground(NavyBlue);;
    sheet.getRange(10,1).setValue("Categories");
    sheet.getRange(10,1).setFontSize(8);
    sheet.getRange(10,1).setFontWeight("bold");
    sheet.getRange(10,1).setFontColor('white');
    
    sheet.getRange(10,2+i).setValue("Budget");
    sheet.getRange(10,3+i).setValue("Out");
    sheet.getRange(10,4+i).setValue("Diff");
    sheet.getRange(10,2+i,1,3).setFontSize(8);
    sheet.getRange(10,2+i,1,3).setFontWeight("bold");
    sheet.getRange(10,2+i,1,3).setFontColor('white');
    sheet.getRange(10,2+i,1,3).setBackground(NavyBlue);
    sheet.getRange(10,2+i,100,3).setHorizontalAlignment('center');
    sheet.getRange(10,2+i,100,3).setHorizontalAlignment('center');

    setDelimiterRow(11,GunmetalGrey);

    sheet.setFrozenColumns(1);
    sheet.setFrozenRows(11);

    sheet.getRange(12,2+i,100,1).setBackground('white');
  }

  //populate with initial categories
  var defaultCategories = ['Monthly Bills','Rent/Mortgage','Phone','Internet','Cable TV','Electricity','Water','Hidroelectrica','Streaming','Bani buni', 'Transport','Software','EON',
                            'Everyday Expenses','Groceries','Fuel','Medical','Clothing','Household Goods','Pets','Pocket Money Tinel','Pocket Money Monica','Atelier', 'Transactions', 'Education','Parcare','Restaurante','Round-up',
                            'Rainy Day Funds','Emergency Fund','Car Repairs','Home Maintanance','Car Insurance','Life Insurance','Health Insurance','Birthdays','Christmas',
                            'Savings Goals','Car Replacement','Vacation',
                            'Debt','Car Payment','Personal Loan Payment'];
  var data = defaultCategories.map(function(category) {
      return [category];
    });                   

  // set default formating         
  var range = sheet.getRange(12,1,data.length, 1);
  range.setValues(data);
  range.setHorizontalAlignment('right');
  range.setFontWeight('normal');


  // Make bold the main categories in the sheet aligned left and all the subcategories will remain aligned right
  var rowNumberOfCategory;
  // parse the defaultCategories and mark them
  // to be able to identify them inside the parser of categories also will Mark them with 1 at column 38
  // delete the column 8 before
  var startRow = 12; // Row to start deletion
  var column = 38; // Column to delete (38 corresponds to column AL)
  var lastRow = sheet.getLastRow(); // Get the last row with data in the sheet
  sheet.getRange(startRow, column, lastRow - startRow + 1, 1).clearContent();

  //format the main categories
  for(var icnt = 0;icnt<defaultMainCategories.length;icnt++)
  {
    rowNumberOfCategory = findRowByValue(defaultMainCategories[icnt]);
    sheet.getRange(rowNumberOfCategory,1).setFontWeight('bold');
    sheet.getRange(rowNumberOfCategory,1).setHorizontalAlignment('left');
    sheet.getRange(rowNumberOfCategory,38).setValue(1);
    sheet.getRange(rowNumberOfCategory,1,1,38).setBackground(BlueGreen);
  }
  ////mark 'Monthly bills' as Main
  //rowNumberOfCategory = findRowByValue('Monthly bills');
  //sheet.getRange(rowNumberOfCategory,1).setFontWeight('bold');
  //sheet.getRange(rowNumberOfCategory,1).setHorizontalAlignment('left');
  //sheet.getRange(rowNumberOfCategory,38).setValue(1);
//
  ////mark 'Everyday Expenses' as Main
  //rowNumberOfCategory = findRowByValue('Everyday Expenses');
  //sheet.getRange(rowNumberOfCategory,1).setFontWeight('bold');
  //sheet.getRange(rowNumberOfCategory,1).setHorizontalAlignment('left');
  //sheet.getRange(rowNumberOfCategory,38).setValue(1);
//
  ////mark 'Rainy Day Funds' as Main
  //rowNumberOfCategory = findRowByValue('Rainy Day Funds');
  //sheet.getRange(rowNumberOfCategory,1).setFontWeight('bold');
  //sheet.getRange(rowNumberOfCategory,1).setHorizontalAlignment('left');
  //sheet.getRange(rowNumberOfCategory,38).setValue(1);
//
  ////mark 'Saving Goals' as Main
  //rowNumberOfCategory = findRowByValue('Savings Goals');
  //sheet.getRange(rowNumberOfCategory,1).setFontWeight('bold');
  //sheet.getRange(rowNumberOfCategory,1).setHorizontalAlignment('left');
  //sheet.getRange(rowNumberOfCategory,38).setValue(1);
//
  ////mark 'Debt' as Main
  //rowNumberOfCategory = findRowByValue('Debt');
  //sheet.getRange(rowNumberOfCategory,1).setFontWeight('bold');
  //sheet.getRange(rowNumberOfCategory,1).setHorizontalAlignment('left');
  //sheet.getRange(rowNumberOfCategory,38).setValue(1);
}

function insertDate() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var cell = sheet.getRange('A1');
  cell.setValue(new Date());
}

function processCategories() {
  // Access the active spreadsheet and the desired sheet
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  // Get the last row with data in column A
  var lastRow = sheet.getLastRow();
  
  // Define the range from row 12 to the last row in column A
  var range = sheet.getRange(12, 1, lastRow - 11, 1);
  
  // Get the values in the range as a 2D array
  var values = range.getValues();
  
  // Initialize variables to store the matrix array and current main category

  var currentMainCategory = null;
  
  // Iterate through the values to categorize them
  for (var i = 0; i < values.length; i++) {
    var cellValue = values[i][0];
    
    // Check if the cell value is a main category
    if (isMainCategory(cellValue,12+i)) {
      // Start a new main category
      currentMainCategory = [cellValue];
      categoryMatrixArray.push(currentMainCategory);
    } else if (currentMainCategory) {
      // Add subcategory to the current main category
      currentMainCategory.push(cellValue);
    }
  }
  
  // Log the resulting matrix array
  Logger.log(categoryMatrixArray);
  //appendToLogSheet("Found main category length",categoryMatrixArray[0].length);
}

// Helper function to determine if a cell value is a main category
function isMainCategory(cellValue,row) {
  // Implement your logic to identify main categories
  return cellValue && cellValue.trim() !== '' && isInMainCategoryArray(cellValue,row);
}

// Helper function to check if the cell value is in bold font
function isInMainCategoryArray(cellValue,row) {
  // Implement logic to check if the cell's font is bold
  // This is a placeholder function; actual implementation may vary
  // Note: Accessing font styles may require the Sheets API
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var cellValueCat = sheet.getRange(row,38).getValue();
  
  if(cellValueCat == 1)
  {
    //appendToLogSheet("Found main category",cellValue);
    //appendToLogSheet("Found main category cell value",cellValueCat);
    //appendToLogSheet("Found main category cel row",row);
    return true;
  }
  else
  {
    //appendToLogSheet("Found secondary category",cellValue);
    //appendToLogSheet("Found secondary category value",cellValueCat);
    //appendToLogSheet("Found secondary category row",row);
    return false; // Replace with actual implementation
  }
}

function getColumnLetter(columnIndex) {
  var columnLetter = '';
  while (columnIndex > 0) {
    var modulo = (columnIndex - 1) % 26;
    columnLetter = String.fromCharCode(65 + modulo) + columnLetter;
    columnIndex = Math.floor((columnIndex - modulo) / 26);
  }
  return columnLetter;
}


function populateHeaderMonth(sheet,numberOfEntries,categoryMatrixArray)
{
  for(var i = 1; i < 12+1; i++)
  {
     var targetCell;
     var rangeFormulaString;
     // not budgeted
     if(i>1)
     {
     // appendToLogSheet("current column",i*3);
      targetCell = sheet.getRange(3,3*i,1,1);
      rangeFormulaString = '=' + getColumnLetter(3*(i-1)) + '8';
      targetCell.setFormula(rangeFormulaString);
     }
    // Spent
    var currentRow = 12;
    //appendToLogSheet("current column",i*3);
    targetCell = sheet.getRange(4,3*i,1,1);
    var numberOfCategories = categoryMatrixArray.length;
    rangeFormulaString = '=' + getColumnLetter(i*3) + '12';
    for(var j=0;j<numberOfCategories - 1;j++)
    {
        currentRow = currentRow + categoryMatrixArray[j].length;
        rangeFormulaString = rangeFormulaString + '+' + getColumnLetter(i*3) + currentRow;
    }
    targetCell.setFormula(rangeFormulaString);
    //Remaining
    var currentRow = 12;
    //appendToLogSheet("current column",i*3);
    targetCell = sheet.getRange(5,3*i,1,1);
    var numberOfCategories = categoryMatrixArray.length;
    rangeFormulaString = '=' + getColumnLetter(i*3) + '3-'+ getColumnLetter(i*3) + '4+'+ getColumnLetter(i*3) + '6' ;
    targetCell.setFormula(rangeFormulaString);
    // Budgeted
    var currentRow = 12;
    //appendToLogSheet("current column",i*3);
    targetCell = sheet.getRange(7,3*i,1,1);
    var numberOfCategories = categoryMatrixArray.length;
    rangeFormulaString = '=' + getColumnLetter(i*3-1) + '12';
    for(var j=0;j<numberOfCategories - 1;j++)
    {
        currentRow = currentRow + categoryMatrixArray[j].length;
        rangeFormulaString = rangeFormulaString + '+' + getColumnLetter(i*3-1) + currentRow;
    }
    targetCell.setFormula(rangeFormulaString);
    //available
    var currentRow = 12;
    //appendToLogSheet("current column",i*3);
    targetCell = sheet.getRange(8,3*i,1,1);
    rangeFormulaString = '=' + getColumnLetter(i*3) + '6-' + getColumnLetter(i*3) + '7+' + getColumnLetter(i*3) + '3';
    targetCell.setFormula(rangeFormulaString);
  }
}

function populateFormulasMonth(sheet,currentColumn,currentRow,numberOfSubCategories)
{
  // populate all the sums for each category
  var targetCell = sheet.getRange(currentRow,currentColumn,1,1); 
  var rangeFormulaString = '=SUM(' + getColumnLetter(currentColumn) + (currentRow+1) + ':' + getColumnLetter(currentColumn) + (numberOfSubCategories + currentRow - 1) + ')';
  targetCell.setFormula(rangeFormulaString);
  //appendToLogSheet("Formula",rangeFormulaString);
  // create the values for the difference

  if((currentColumn-1)%3==0){
    //appendToLogSheet("current column",currentColumn);
    // insert the formula to get the budget vs speding (out)
    for(var i=0;i<numberOfSubCategories-1;i++)
    {
        targetCell = sheet.getRange(currentRow+i+1,currentColumn,1,1); 
        var rangeFormulaString = '=' + getColumnLetter(currentColumn-2) + (currentRow+i+1) + '-' + getColumnLetter(currentColumn-1) + (currentRow+i+1);
        targetCell.setFormula(rangeFormulaString);
    }
  }
}

// populates all the formulas inside the sheet does not touch the data inserted
function populateFormulas() {
  //process categories to get the category matrix
  var numberOfEntries = 0;
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  processCategories();
  var numberOfCategories = categoryMatrixArray.length;
  
  //appendToLogSheet("Number of categories",numberOfCategories);
  var currentRow = 12;
  for(var i=0; i<numberOfCategories; i++)
  {
    var numberOfSubCategories = categoryMatrixArray[i].length;
    numberOfEntries = numberOfEntries + numberOfSubCategories;
    //appendToLogSheet("Number of subcategories",numberOfSubCategories);
    // Budget categories sum 
    for(var j=2;j<38;j++)
    {
      var currentColumn = j;
      populateFormulasMonth(sheet,currentColumn,currentRow,numberOfSubCategories);
    }
    currentRow = currentRow + numberOfSubCategories;
  }

  // insert conditional formating for the spreadsheet
    
     // Clear all conditional format rules
    sheet.clearConditionalFormatRules();
    // insert conditional formating for the cells to be bold and red if the difference is negative for each diff in each month
    for(var i=1; i<12+1; i++)
    {
      
      var range = sheet.getRange(12, 1+3*i, sheet.getLastRow(), 1); // Adjust the range as needed
      // Create a conditional format rule
      var rule = SpreadsheetApp.newConditionalFormatRule()
        .whenNumberLessThan(0) // Condition: value is less than 0
        .setFontColor('red') // Font color: red
        .setBold(true) // Font style: bold
        .setRanges([range]) // Apply to the specified range
        .build();

      // Get existing rules and add the new rule
      var rules = sheet.getConditionalFormatRules();
      rules.push(rule);

      // Set the new rules back to the sheet
      sheet.setConditionalFormatRules(rules);
      // set conditional formating also on the header of each month
      var range = sheet.getRange(3, 1+3*i-1, 6, 2); // Adjust the range as needed
      // Create a conditional format rule
      var rule = SpreadsheetApp.newConditionalFormatRule()
        .whenNumberLessThan(0) // Condition: value is less than 0
        .setFontColor('red') // Font color: red
        .setBold(true) // Font style: bold
        .setRanges([range]) // Apply to the specified range
        .build();

      // Get existing rules and add the new rule
      var rules = sheet.getConditionalFormatRules();
      rules.push(rule);

      // Set the new rules back to the sheet
      sheet.setConditionalFormatRules(rules);

      // set decimal places to 0
      var range = sheet.getRange(3, 1+3*i, sheet.getLastRow(), 1); // Adjust the range as needed
      range.setNumberFormat('0');
      var range = sheet.getRange(3, 1+3*i-1, sheet.getLastRow(), 1); // Adjust the range as needed
      range.setNumberFormat('0');
      var range = sheet.getRange(3, 1+3*i-2, sheet.getLastRow(), 1); // Adjust the range as needed
      range.setNumberFormat('0');
    }
  // populate headers
  populateHeaderMonth(sheet,numberOfEntries,categoryMatrixArray);
}

// process inports from ING bank to the spreadsheet
function generateSHA256Hashes(sheet) {
  // Determine the number of rows with data
  var numRows = sheet.getLastRow();
  
  // Retrieve values from columns A to F
  var dataRange = sheet.getRange(2, 1, numRows-1, 6);
  var data = dataRange.getValues();
  
  // Iterate over each row
  for (var i = 0; i < data.length; i++) {
    // Concatenate values from columns A to F
    var concatenatedString = data[i].join('');
    
    // Generate a SHA-256 hash of the concatenated string
    var hash = generateSHA256Hash(concatenatedString);
    
    // Write the hash to column G
    sheet.getRange(i + 2, 7).setValue(hash);
  }
}

// Helper function to generate a SHA-256 hash
function generateSHA256Hash(input) {
  // Compute the digest as a byte array
  var digest = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, input);
  
  // Convert the byte array to a hexadecimal string
  var hash = digest.map(function(byte) {
    // Convert byte to unsigned 8-bit integer and then to hexadecimal
    var hex = (byte < 0 ? byte + 256 : byte).toString(16);
    // Ensure two characters by padding with leading zero if necessary
    return ('0' + hex).slice(-2);
  }).join('');
  
  return hash;
}

function importNewTransactions() {
  
  // Open the active spreadsheet
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // Access the 'Import' and 'Transactions' sheets
  var importSheet = ss.getSheetByName('Import');
  var transactionsSheet = ss.getSheetByName('Transactions');
  generateSHA256Hashes(importSheet);
  // Get the data from the 'Import' sheet starting from row 2
  var importData = importSheet.getRange(2, 1, importSheet.getLastRow() - 1, importSheet.getLastColumn()).getValues();
  var noEntriesinTransactions = true;
  //appendToLogSheet("Number of lines in Transactions",transactionsSheet.getLastRow());
  if(transactionsSheet.getLastRow() > 2)
  {
    // Get the existing hashes from the 'Transactions' sheet
    var transactionHashes = transactionsSheet.getRange(2, 7, transactionsSheet.getLastRow() - 1, 1).getValues().flat();
    
    // Create a set of existing hashes for quick lookup
    var existingHashes = new Set(transactionHashes);
    noEntriesinTransactions = false;
  } 
  // Initialize an array to hold new rows to be added to 'Transactions'
  var newRows = [];
  
  // Iterate over the import data
  for (var i = 0; i < importData.length; i++) {
    var row = importData[i];
    var hash = row[6]; // Column G (index 6)
    
    // Check if the hash already exists in 'Transactions'
    if(noEntriesinTransactions == false)
      if (existingHashes.has(hash)) {
        // Mark as 'Already Imported' in column H (index 7)
        importSheet.getRange(i + 2, 8).setValue('Already Imported');
      } else {
        // Add the row to the newRows array
        newRows.push(row);
        // Mark as 'Imported' in column H (index 7)
        importSheet.getRange(i + 2, 8).setValue('Imported');
      }
    else
    {
      //just copy everything
      // Add the row to the newRows array
      newRows.push(row);
      // Mark as 'Imported' in column H (index 7)
      importSheet.getRange(i + 2, 8).setValue('Imported');
    }
  }
  
  // Append new rows to the 'Transactions' sheet if there are any
  if (newRows.length > 0) {
    transactionsSheet.getRange(transactionsSheet.getLastRow() + 1, 1, newRows.length, newRows[0].length).setValues(newRows);
  }
  insertDate();
}

function processTransactions(){
  var today = new Date(); // Get the current date and time
  var month = today.getMonth() + 1; // getMonth() returns 0-11, so add 1 to get 1-12
  //appendToLogSheet("Month number",month);
  processTransactionsByMonth(month);
}

function processTransactionsByMonth(month) {
    var sumsByKey = sumValuesByUniqueKey();
    updateTransactionsSheet(sumsByKey,month);
    var missingKeys = findMissingKeys(sumsByKey);
    for(var i=0;i<missingKeys.length;i++)
    {
      appendToLogSheet("Missing keys",missingKeys[i]);
    }
}

// finds all the keys from transactions that do not have an equivalent in the budget categories
function findMissingKeys(dataStructure) {
  // Access the active spreadsheet and the "YNGSB" sheet
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = spreadsheet.getSheetByName("YNGSB");

  // Get the values from column A (starting from row 12)
  var dataRange = sheet.getRange(12, 1, sheet.getLastRow() - 11, 1);
  var values = dataRange.getValues();

  // Flatten the 2D array to a 1D array
  var existingKeys = values.flat();

  // Initialize an array to hold the missing keys
  var missingKeys = [];

  // Iterate through the keys in the data structure
  for (var key in dataStructure) {
    if (dataStructure.hasOwnProperty(key)) {
      // Check if the key is not in the existing keys
      if (!existingKeys.includes(key)) {
        missingKeys.push(key);
      }
    }
  }

  // Log the missing keys to the console
  Logger.log(missingKeys);

  // Return the missing keys
  return missingKeys;
}

function updateTransactionsSheet(dataStructure,month) {
    // Access the active spreadsheet and the "Transactions" sheet
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = spreadsheet.getSheetByName("YNGSB");

  // Get the last row with data in column A
  var lastRow = sheet.getLastRow();

  // Iterate through each row in column A
  for (var i = 1; i <= lastRow; i++) {
    var cellValue = sheet.getRange(i, 1).getValue(); // Get value from column A (1)
    //appendToLogSheet("Cell value",cellValue);
    //appendToLogSheet("Has own prop:",dataStructure.hasOwnProperty(cellValue));
    if (dataStructure.hasOwnProperty(cellValue)) {
      var correspondingValue = dataStructure[cellValue];
      //appendToLogSheet("Has value:",correspondingValue);
      sheet.getRange(i, 3*month).setValue(correspondingValue); // Set value in column C (3)
    }
  }
}

function sumValuesByUniqueKey() {
  // Access the active spreadsheet
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  
  // Get the "Transactions" sheet
  var sheet = spreadsheet.getSheetByName("Transactions");
  
  // Get the range of data in the sheet
  var dataRange = sheet.getDataRange();
  
  // Fetch all the data as a 2D array
  var data = dataRange.getValues();
  
  // Initialize an object to hold the sums for each unique key
  var sumsByKey = {};
  
  // Iterate over the rows, starting from the second row to skip headers
  for (var i = 1; i < data.length; i++) {
    var key = data[i][2]; // Column C (index 2)
    var value = data[i][4]; // Column E (index 4)
    
    // Ensure the value is a number before adding
    if (typeof value === 'number') {
      if (sumsByKey[key]) {
        sumsByKey[key] += value;
      } else {
        sumsByKey[key] = value;
      }
    }
  }
  
  // Log the result to the console (for debugging purposes)
  console.log(sumsByKey);
  
  // Return the resulting object
  return sumsByKey;
}