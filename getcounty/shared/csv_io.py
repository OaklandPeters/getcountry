import os
import csv

def read_csv_rows(infile):
    assert(isinstance(infile, basestring))
    assert(os.path.exists(infile))
    assert(os.path.isfile(infile))
    
    with open(infile, mode='rbU') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            yield row

def get_headers(infile):
    assert(isinstance(infile, basestring))
    assert(os.path.exists(infile))
    assert(os.path.isfile(infile))
    with open(infile, mode='rbU') as csvfile:
        rows = csv.reader(csvfile)
        headers = rows.next()
    return headers

def read_csv_dict_rows(infile):
    """Read as a dict."""
    assert(isinstance(infile, basestring))
    assert(os.path.exists(infile))
    assert(os.path.isfile(infile))
    
    with open(infile, mode='rbU') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            yield row

def write_csv_rows(outfile, iterable, headers=None):
    """Write iterable of rows into outfile."""
    assert(isinstance(outfile, basestring))

    with open(outfile, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        if headers is not None:
            writer.writerow(headers)        
        writer.writerows(iterable)

def write_csv_rows_enumerated(outfile, iterable, headers=None):
    """Write iterable of rows into outfile."""
    assert(isinstance(outfile, basestring))

    with open(outfile, 'wb') as csvfile:
        writer = csv.writer(csvfile)        
        if headers is not None:
            writer.writerow(headers)
        
        for i, row in enumerate(iterable):
            print(i)
            writer.writerow(row)


            
    