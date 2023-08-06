# Description
Converts a list of json objects to a csv with optional filtering, sorting and date formatting.

# installation
This commands installs the package and an application script: json2csv. 
```bash
pip install json-to-csv-filter
```

# Usage
```bash
usage: json_to_csv.py [-h] [-i [INCLUDE ...]] [-e [EXCLUDE ...]] [-o [ORDER ...]] [-n [NUMBER]] [-d [DATE_FIELDS ...]] [-df [DATE_FORMAT]]
                      [infile] [outfile]

Convert list of json objects to csv

positional arguments:
  infile                Input file, defaults to STDIN
  outfile               Output file, defaults to STDOUT

optional arguments:
  -h, --help            show this help message and exit
  -i [INCLUDE ...], --include [INCLUDE ...]
                        Include fields, defaults to all
  -e [EXCLUDE ...], --exclude [EXCLUDE ...]
                        Exclude fields, defaults to none
  -o [ORDER ...], --order [ORDER ...]
                        Order fields, defaults to none
  -n [NUMBER], --number [NUMBER]
                        Number of records to process, defaults to all
  -d [DATE_FIELDS ...], --date-fields [DATE_FIELDS ...]
                        Date fields, defaults to none
  -df [DATE_FORMAT], --date-format [DATE_FORMAT]
                        Datetime format, defaults to none
```

# Examples
## convert a json file to standard out
```bash
json2csv -i ais-messages.txt
```
