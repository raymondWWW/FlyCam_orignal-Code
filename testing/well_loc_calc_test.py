"""
Algorithm Test for calculating well locations
using the centers of the corner wells of the well plates

Input number of rows and columns

Test 1, Row:
-Input first and last well location centers of row
-Calculate location of each well in row using input number of columns
-Output those locations

Test 2, Col:
-Input first and last well location centers of column
-Calculate location of each well in row using input number of rows
-Output those locations

Test 3, 4 Corners:
-Input 4 outer corners of well plate center locations
-Calculate location of each well in each row, save to dictionary
-Calculate location of each well in each col, save to dictionary
  -For dictionary, use row_col string index as key? or nested dictionary with row/col?
-Use loop to compare results, are they the same?
  -if they are within range of error, do an average?

Note:
- For all 3 tests, locations will have to rounded to 2 decimal places (e.g. 23.84895 is rounded to 23.85)

Ideas:
-GUI will create table length based on number of rows and columns
-Create GUI that will display editable table of well location?
-GUI that is an excel sheet, right side has "go to location button"?
-GUI that has clickable image to go to well location, and editable x/y/z?
-Save to CSV File
"""