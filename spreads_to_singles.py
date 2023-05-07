#!/usr/bin/env python3

import sys
import os
import shutil
import subprocess

filename = sys.argv[1]

dims = subprocess.check_output(f'pdftk {filename} dump_data | grep "Dimensions" | cut -d":" -f2',
                               shell=True)
dims = [x.strip().split(' ') for x in dims.decode().strip().split('\n')]
dims = [(float(x[0]), float(x[1])) for x in dims]
if len(set(dims)) != 1:
    # order dims by frequency, hopefully most frequent is the one we want
    dims = sorted(dims, key=lambda x: dims.count(x), reverse=True )
dims = dims[0]
half_horiz = int(dims[0] // 2)
full_height = int(dims[1])

left_fp = os.path.splitext(filename)[0] + '-left.pdf'
right_fp = os.path.splitext(filename)[0] + '-right.pdf'
single_fp = os.path.splitext(filename)[0] + '-single.pdf'

# from https://superuser.com/a/235401, though I had to reverse left and right?
subprocess.run(f'gs -o {left_fp} -sDEVICE=pdfwrite -g{half_horiz*10}x{full_height*10} -c "<</PageOffset [0 0]>> setpagedevice" -f {filename}',
               shell=True)
subprocess.run(f'gs -o {right_fp} -sDEVICE=pdfwrite -g{half_horiz*10}x{full_height*10} -c "<</PageOffset [-{half_horiz} 0]>> setpagedevice" -f {filename}',
               shell=True)
subprocess.run(f'pdftk B={right_fp} A={left_fp} shuffle A B output {single_fp} verbose', shell=True)
os.remove(left_fp)
os.remove(right_fp)
