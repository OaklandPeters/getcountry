import os
from getcounty.pipeline import processing


def process_file(infile):
    assert(os.path.exists(infile))
    
    # Create outfile path-string    
    in_dir, in_name_ext = os.path.split(infile)
    in_name, in_ext = os.path.splitext(in_name_ext)
    out_name = in_name + "_processed" + in_ext
    outfile = os.path.join(in_dir, out_name)
    
    if os.path.exists(outfile):
        os.remove(outfile)
    assert(not os.path.exists(outfile))

    # Process outfile    
    processing.pipeline(infile, outfile)
    
    assert(os.path.exists(outfile))
    
    #n_unfilled = len(list(processing.find_unfilled(outfile, 'Home of Record County')))
    n_unfilled = count_unfilled_counties(outfile)
    
    print("\n---------")
    print("For '{0}'".format(outfile))
    print("  # Unfilled Counties == {0}".format(n_unfilled))

def count_unfilled_counties(filepath):
    return processing.count_unfilled(filepath, 'Home of Record County')

def run_task():
    """Run task on pre-defined set of files."""
    # testdir is the directory containing final_processing.py
    testdir = os.path.split(os.path.abspath(__file__))[0]
    ticketdir = os.path.join(testdir, '..', 'ticket-files')
    infiles = [
        os.path.join(ticketdir, 'ONDNames_of_Fallen__1___1_.csv'),
        os.path.join(ticketdir, 'OIFNames_of_Fallen__1___1_.csv'),
        os.path.join(ticketdir, 'OEFNames_of_Fallen.csv')
    ]
    
    for infile in infiles:
        process_file(infile)
    

if __name__ == "__main__":
    run_task()

