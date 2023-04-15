#!/usr/bin/env python3

import sys
import os
import shutil
import subprocess

filename = sys.argv[1]
n_pages = subprocess.check_output(f'pdftk {filename} dump_data | grep "NumberOfPages" | cut -d":" -f2',
                                  shell=True)
n_pages = int(n_pages.decode().strip())
shutil.copy(filename, 'tmp.pdf')

# if not divisible by 4, we need to add blank pages
if (n_pages % 4) != 0:
    page_size = subprocess.check_output(f'pdftk {filename} dump_data | grep "PageMediaDimensions" | cut -d":" -f2',
                                        shell=True)
    # converting to int and back to str is just to check we got the right thing
    page_size = [str(int(x)) for x in page_size.decode().strip().split(' ')]
    subprocess.run(f'convert xc:none -page {"x".join(page_size)} blank.pdf', shell=True)
    n_blank_pages = 4 - (n_pages % 4)
    blank_str = 'B1 ' * n_blank_pages
    subprocess.run(f'pdftk A={filename} B=blank.pdf cat A1-end {blank_str} output tmp.pdf',
                   shell=True)
    n_pages += n_blank_pages
    os.remove('blank.pdf')

pages = []
curr_page = n_pages
for i in range(n_pages // 4):
    pages.extend([curr_page, 2*i+1, 2*i+2, curr_page-1])
    curr_page -= 2

pages = ' '.join([str(x) for x in pages])
subprocess.run(f'pdftk tmp.pdf cat {pages} output booklet.pdf', shell=True)
os.remove('tmp.pdf')
