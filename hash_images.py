#!/usr/bin/env python2
from PIL import Image
import os
import csv
from simplehash import image_hash, get_similarity
from multiprocessing import Pool


album_cover_dir = "j"

cover_filenames = os.listdir(album_cover_dir)
print("N covers: %d"%len(cover_filenames))


def hashImages(filename):
    try:
        # Use PIL to open the image so it can be passed to
        # image_hash to get its simple pHash
        image = Image.open(album_cover_dir+os.sep+filename)
        # (10,10) is the thumbnail size. A larger size results in a larger hash
        # but also more accuracy.
        return (image_hash(image, (10,10)), filename)
    except IOError:
        # We might get IOErrors due to corrupted images or
        # or strange formats.
        pass


# Create a process pool then use them to run hashImages
# over all the cover filenames
pool = Pool(8)
image_hashes = pool.map(hashImages, cover_filenames)

# Write out the hashes to a file
with open("hashes-10x10.csv","w") as f:
    w=csv.writer(f)
    for fname_and_hash in image_hashes:
        # This check is needed because the function may return
        # None if an exception occured
        if fname_and_hash:
            w.writerow(fname_and_hash)


####
# An inline version
#

#image_hashes = []
#n_covers = float(len(cover_filenames))
#for i, filename in enumerate(cover_filenames):
#    try:
#        image = Image.open(album_cover_dir+os.sep+filename)
#        image_hashes.append( (image_hash(image, (10,10)), filename) )
#        if i%100==0:
#            print("%.f%%"%(i/n_covers*100))
#    except IOError,e:
#        print e
#        print filename
