#!/usr/bin/env python3

import sys
import os
import shutil
import subprocess
import argparse

def main(filename, folio_length=None):

    n_pages = subprocess.check_output(f'pdftk {filename} dump_data | grep "NumberOfPages" | cut -d":" -f2',
                                      shell=True)
    n_pages = int(n_pages.decode().strip())

    if folio_length is not None:
        if folio_length % 4 != 0:
            raise ValueError("folio_length must be divisible by 4!")
        if folio_length > n_pages:
            raise ValueError("folio_length must be smaller than the number of pages in the pdf!")

    shutil.copy(filename, 'tmp.pdf')

    # if not divisible by 4, we need to add blank pages
    if (n_pages % 4) != 0:
        page_size = subprocess.check_output(f'pdftk {filename} dump_data | grep "PageMediaDimensions" | cut -d":" -f2',
                                            shell=True)
        # converting to float and back to str is just to check we got the right thing
        page_size = [str(float(x)) for x in page_size.decode().strip().split(' ')]
        subprocess.run(f'convert xc:none -page {"x".join(page_size)} blank.pdf', shell=True)
        n_blank_pages = 4 - (n_pages % 4)
        blank_str = 'B1 ' * n_blank_pages
        subprocess.run(f'pdftk A={filename} B=blank.pdf cat A1-end {blank_str} output tmp.pdf',
                       shell=True)
        n_pages += n_blank_pages
        os.remove('blank.pdf')

    if folio_length is None:
        folio_length = n_pages

    pages = []
    for j in range(n_pages // folio_length):
        curr_page = (j+1) * folio_length
        for i in range(folio_length // 4):
            pages.extend([curr_page, j*folio_length + 2*i+1, j*folio_length + 2*i+2, curr_page-1])
            curr_page -= 2

    pages = ' '.join([str(x) for x in pages])
    subprocess.run(f'pdftk tmp.pdf cat {pages} output booklet.pdf', shell=True)
    os.remove('tmp.pdf')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=("Rearrange single page pdfs into booklet / folio order, for printing"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("filename",
                        help="Which file to rearrange")
    parser.add_argument("--folio_length", '-l', default=None, type=int,
                        help="Length of the folio, in pages. If None, all pages will be in single folio.")
    args = vars(parser.parse_args())
    main(**args)
