'''
Created on Jun 21, 2022

Convert an Annovar *.avinput file to VCF
@author: pleyte
'''
import argparse
import logging
import csv

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
logging_format = '%(levelname)s: [%(filename)s:%(lineno)s - %(funcName)s()]: %(message)s'

stream_format = logging.Formatter(logging_format)
stream_handler.setFormatter(stream_format)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

class Variant(object):
    def __init__(self):        
        chromosome = None
        startPos = None
        endPos = None
        ref = None
        alt = None
        dbSnpId = None
        
def _parse_args():
    '''
    Validate and return command line arguments.
    '''
    parser = argparse.ArgumentParser(description='Read an Annovar avinput file and write out a VCF')

    parser.add_argument('-i', '--in_file',  
                        help='Annovar avinput file generated by convert2annovar.pl',
                        type=argparse.FileType('r'),
                        required=True)
    
    parser.add_argument('-o', '--out_file',  
                        help='VCF file to create',
                        type=argparse.FileType('w'),
                        required=True)    
    
    args = parser.parse_args()
    
    return args

def _read_avinput_variants(avinput_file_name: str):
    variants = list()
    
    with open(avinput_file_name) as tsv_file:
        reader = csv.reader(tsv_file, delimiter = '\t')
        for row in reader:
            if row[3] == "-" or row[4] == "-":
                continue
            variant = Variant()
            variant.chromosome = row[0].replace('chr', '', 1) 
            variant.startPos = row[1]
            variant.endPos = row[2]
            variant.ref = row[3] 
            variant.alt = row[4]
            variant.dbSnpId = row[7]
            variants.append(variant)
         
    return variants

def _write_vcf(vcf_file_name: str, variants: list):
    '''
    '''
    with open(vcf_file_name, 'w') as vcf_file:
        vcf_file.write('##fileformat=VCFv4.2\n')
        vcf_file.write('##FILTER=<ID=PASS,Description="All filters passed">\n')
        vcf_file.write('##FILTER=<ID=PON,Description="Variant found in panel of normals in 3 or more samples.">\n')
        vcf_file.write('##FILTER=<ID=PON_OV,Description="Variant found in panel of normals at low frequency, but call is at significantly higher frequency.">\n')
        vcf_file.write('##contig=<ID=1,length=249250621>\n')
        vcf_file.write('##contig=<ID=2,length=243199373>\n')
        vcf_file.write('##contig=<ID=3,length=198022430>\n')
        vcf_file.write('##contig=<ID=4,length=191154276>\n')
        vcf_file.write('##contig=<ID=5,length=180915260>\n')
        vcf_file.write('##contig=<ID=6,length=171115067>\n')
        vcf_file.write('##contig=<ID=7,length=159138663>\n')
        vcf_file.write('##contig=<ID=8,length=146364022>\n')
        vcf_file.write('##contig=<ID=9,length=141213431>\n')
        vcf_file.write('##contig=<ID=10,length=135534747>\n')
        vcf_file.write('##contig=<ID=11,length=135006516>\n')
        vcf_file.write('##contig=<ID=12,length=133851895>\n')
        vcf_file.write('##contig=<ID=13,length=115169878>\n')
        vcf_file.write('##contig=<ID=14,length=107349540>\n')
        vcf_file.write('##contig=<ID=15,length=102531392>\n')
        vcf_file.write('##contig=<ID=16,length=90354753>\n')
        vcf_file.write('##contig=<ID=17,length=81195210>\n')
        vcf_file.write('##contig=<ID=18,length=78077248>\n')
        vcf_file.write('##contig=<ID=19,length=59128983>\n')
        vcf_file.write('##contig=<ID=20,length=63025520>\n')
        vcf_file.write('##contig=<ID=21,length=48129895>\n')
        vcf_file.write('##contig=<ID=22,length=51304566>\n')
        vcf_file.write('##contig=<ID=X,length=155270560>\n')
        vcf_file.write('##contig=<ID=Y,length=59373566>\n')
        vcf_file.write('##contig=<ID=MT,length=16569>\n')
        vcf_file.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
        vcf_file.write('##INFO=<ID=x,Number=1,Type=String,Description="Placeholder">\n')
        vcf_file.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tabcd-123\n')
        
        for variant in variants:            
            vcf_file.write(f"{variant.chromosome}\t{variant.startPos}\t{variant.dbSnpId}\t{variant.ref}\t{variant.alt}\t1.0\tPON\tx=y\tGT\t0/0\t\n")

def _main():
    '''
    main function
    '''
    args = _parse_args()
    
    variants = _read_avinput_variants(args.in_file.name)
    
    logger.info(f"Read {len(variants)} variants from {args.in_file.name}")
    
    _write_vcf(args.out_file.name, variants)
    
    logger.info(f"Wrote VCF {args.out_file.name}")
    
if __name__ == '__main__':
    _main()