from ASCIICompressor import *
import os

test_folder = 'tests'

def testCompression(compressor,infile):

    print("Testing "+os.path.basename(infile))

    in_prefix = infile.split('.txt')[0]
    compressor.encodeAndWrite(infile)
    compressor.decodeAndWrite(in_prefix+'_compressed.txt', in_prefix+'_decompressed.txt')

    comp_ratio = float(os.path.getsize(in_prefix+'_compressed.txt'))/float(os.path.getsize(infile))
    print("Compressed file is %.3f times the size of the original." % comp_ratio)

    if open(in_prefix+'_decompressed.txt').read() == open(infile).read():
        print("Lossless compression!\n")
    else:
        print("Error--compression was not lossless.\n")
    #os.remove(in_prefix+'_decompressed.txt')
    #os.remove(in_prefix+'_compressed.txt')

if __name__ == "__main__":

    print("Begin unit tests of ASCIICompressor.py:\n")

    test_files = [f for f in os.listdir(test_folder) if f.endswith('.txt') and 'compressed' not in f]
    compressor = ASCIICompressor()

    # test _getCharAndCount() helper method
    char,reps,next = compressor._getCharAndCount("AAAARFA#rFASD")
    if char == 'A' and reps == '4' and next == 4:
        print("_getCharAndCount test passed\n")
    else:
        print("_getCharAndCount test failed\n")

    # a test count array
    test_counts = ['','3','4','','2','','','','','2']

    # the expected result of running _compressCounts() on test_counts
    correct_comp = ['','3','4','','2','o4','2']

    # test _compressCounts()
    comp_counts = compressor._compressCounts(test_counts)
    if comp_counts == correct_comp:
        print("_compressCounts test passed\n")
    else:
        print("_compressCounts test failed\n")

    # test _decompressCounts
    decomp_counts = compressor._decompressCounts(comp_counts)

    # Note that the correctly decompressed version replaces
    # empty strings with 1s, and thus does not return the original
    # uncompressed counts. Admittedly this is bad naming/strategy,
    # and I will probably change it in the future.
    correct_decomp = ['1','3','4','1','2','1','1','1','1','2']
    if decomp_counts == correct_decomp:
        print("_decompressCounts test passed\n")
    else:
        print("_decompressCounts test failed\n")

    # test compression, decompression, and file output functions
    for test_file in test_files:
        testCompression(compressor,'/'.join([test_folder,test_file]))
