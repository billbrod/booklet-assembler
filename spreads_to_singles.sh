#!/usr/bin/env bash
set -euo pipefail

# from https://superuser.com/a/235401, though I had to reverse left and right?
gs -o left-sections.pdf -sDEVICE=pdfwrite -g4210x5950 -c "<</PageOffset [0 0]>> setpagedevice" -f $1
gs -o right-sections.pdf -sDEVICE=pdfwrite -g4210x5950 -c "<</PageOffset [-421 0]>> setpagedevice" -f $1
pdftk B=right-sections.pdf A=left-sections.pdf shuffle A B output ./singles.pdf verbose
rm left-sections.pdf right-sections.pdf
