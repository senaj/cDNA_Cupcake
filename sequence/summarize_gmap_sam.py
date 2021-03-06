#!/usr/bin/env python

import os, sys
from collections import defaultdict
from Bio import SeqIO
import BioReaders

def type_fa_or_fq(file):
    file = file.upper()
    if file.endswith('.FA') or file.endswith('.FASTA'): return 'fasta'
    else: return 'fastq'

def summarize_GMAP_sam(input_fa_or_fq, input_sam):
    d = dict((r.id, len(r.seq)) for r in SeqIO.parse(open(input_fa_or_fq), type_fa_or_fq(input_fa_or_fq)))

    map_count = defaultdict(lambda: 0)
    for r in BioReaders.GMAPSAMReader(input_sam, True):
        map_count[r.qID] += 1
    multi = filter(lambda x: map_count[x]>1, map_count)

    f = open(input_sam + '.summary.txt', 'w')
    f.write("id\tqLength\tqCoverage\tidentity\tunique\n")
    for r in BioReaders.GMAPSAMReader(input_sam, True, query_len_dict=d):
        if r.sID == '*': continue
        if r.qID in multi: uni = 'N'
        else: uni = 'Y'
        f.write("{0}\t{1}\t{2:.4f}\t{3:.4f}\t{4}\n".format(r.qID, d[r.qID], r.qCoverage, r.identity, uni))
    f.close()

    print >> sys.stderr, "Output written to:", f.name

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser("Summarize GMAP SAM file in tab-delimited file.")
    parser.add_argument("input_fa_or_fq", help="Input fasta/fastq filename")
    parser.add_argument("sam_file", help="(GMAP) SAM filename")

    args = parser.parse_args()
    summarize_GMAP_sam(args.input_fa_or_fq, args.sam_file)
