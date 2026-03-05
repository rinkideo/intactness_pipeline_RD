# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 00:29:42 2017

@author: Ce Gao
@author: Rong Chen
"""
# pylint: disable=C0103
# Disable module level constant name checking

import argparse  #RD
import sys
import logging
import datetime

# Local module
from .view import View
from .sequence import Sequences
from .configs import configs
from .blast import blast
from .muscle import muscle
from .gag_codon import gag_codon
from .primer import primer
from .hypermut import hypermut
from .psc import psc
from .defect import defect
from .summary import summary
#from .GeneCutter import process_GC

logger = logging.getLogger('pipe')
logger.setLevel(logging.INFO)

import os
mod_path = os.path.dirname(os.path.abspath(__file__))
parser = argparse.ArgumentParser(add_help=True)  #RD
parser.add_argument('--plasmid', action='store_true',  #RD
                    help='Plasmidsaurus run: force primer=Yes')  #RD
parser.add_argument('--input', dest='input_fasta',  #RD
                    help='Input FASTA file to analyze')  #RD
args = parser.parse_args()  #RD

cfg = configs(os.path.join(mod_path, 'default.cfg'))
if args.input_fasta:  #RD
    cfg['Main']['file_qry'] = args.input_fasta  #RD
    cfg['Query']['file_seq'] = args.input_fasta  #RD
    cfg['BLAST']['file_qry'] = args.input_fasta  #RD
    input_base = os.path.splitext(os.path.basename(args.input_fasta))[0]  #RD
    cfg['Main']['path_out'] = os.path.join(cfg['Main']['path_dat'], f"seqs_{input_base}")  #RD
    os.makedirs(cfg['Main']['path_out'], exist_ok=True)  #RD
if args.plasmid:  #RD
    cfg['Primer']['plasmidsaurus_force_primer'] = '1'  #RD

# Logging: initialize handlers after final output path is resolved.
os.makedirs(cfg['Main']['path_out'], exist_ok=True)
date_tag = datetime.datetime.now().strftime("%Y-%b-%d_%H-%M-%S")
file_log = "{}/run_{}.log".format(cfg['Main']['path_out'], date_tag)
fmtr = logging.Formatter('%(asctime)s\t\t%(name)s\t\t%(message)s')

fh = logging.FileHandler(file_log)
fh.setLevel(logging.INFO)
fh.setFormatter(fmtr)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(fmtr)
logger.addHandler(ch)

seqs = Sequences(cfg['Query'], cfg['Reference'])

primer(cfg['Primer'], seqs)

blast(cfg['BLAST'], seqs)

View(cfg['View']).run()

muscle(cfg['MSA'])

gag_codon(cfg['Codon'], seqs)

hypermut(cfg['Hypermut'], seqs)

psc(cfg['PSC'], seqs)

defect(cfg['Defect'], seqs)

summary(cfg['Summary'], seqs)

print('\nPipeline finished. Good bye!\n')
