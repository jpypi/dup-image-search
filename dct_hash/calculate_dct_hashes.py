import sys
import os
import fast_dct_hash

try:
    base_directory = sys.argv[1]
    directories = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
                   "n","o","p","q","r","s","t","the","u","v","w","x","y"]

    for d in directories:
        print "Calculating hashes for the {} directory.".format(d)
        fast_dct_hash.hash_directory(base_directory+os.sep+d)

# IndexError will occur if we're missing the bas directory arg
except IndexError:
    print "{0}: Syntax: {0} <album covers base directory>".format(sys.argv[0])
    sys.exit(0)
