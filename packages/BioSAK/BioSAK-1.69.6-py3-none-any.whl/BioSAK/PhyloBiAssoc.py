import os
import argparse
from BioSAK.BioSAK_config import config_dict


PhyloBiAssoc_usage = '''
=========== PhyloBiAssoc example commands ===========

BioSAK PhyloBiAssoc -t demo.tre -d demo.txt

# https://www.rdocumentation.org/packages/ape/versions/5.7-1/topics/binaryPGLMM

# Note: the header for the first two columns has to be "ID" and "cate".

# Output example
# gene_1  phylosig        7.973475e-26    binaryPGLMM     0.03255813
# gene_2  phylosig        1       chisq.test      0.7183411
# gene_3  phylosig        2.66378e-08     binaryPGLMM     0.5969282
# gene_4  phylosig        7.169588e-08    binaryPGLMM     0.999338

=====================================================
'''

'''
cd /Users/songweizhi/Desktop/test
Rscript /Users/songweizhi/PycharmProjects/BioSAK/BioSAK/PhyloBiAssoc.R -t Soil2.tre -d Soil2_bin.tab

cd /Users/songweizhi/Desktop/test
Rscript /Users/songweizhi/PycharmProjects/BioSAK/BioSAK/PhyloBiAssoc.R -t demo.tre -d demo.txt
Rscript /Users/songweizhi/PycharmProjects/BioSAK/BioSAK/PhyloBiAssoc.R -t Soil2.tre -d Soil2_bin.txt

'''


def PhyloBiAssoc(args):

    tree_file        = args['t']
    data_file        = args['d']
    PhyloBiAssoc_R   = config_dict['PhyloBiAssoc_R']
    PhyloBiAssoc_cmd = 'Rscript %s -t %s -d %s' % (PhyloBiAssoc_R, tree_file, data_file)

    os.system(PhyloBiAssoc_cmd)


if __name__ == "__main__":
    PhyloBiAssoc_parser = argparse.ArgumentParser()
    PhyloBiAssoc_parser.add_argument('-t', required=True, help='tree file')
    PhyloBiAssoc_parser.add_argument('-d', required=True, help='data file')
    args = vars(PhyloBiAssoc_parser.parse_args())
    PhyloBiAssoc(args)
