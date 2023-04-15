# booklet-assembler

Tools to turn RPG PDFs into booklets for printing, inspired by [this
article](https://www.creativegamelife.com/printing-and-binding-rpg-zines). The
article does a lot manually and uses Adobe, so I figured I could do better.

Basically, the goal is to get the PDF into a bunch of single pages, which we
then rearrange into the proper order, and print as a booklet using LibreOffice.

1. If the PDF only comes as "spreads" (with two content pages side-by-side on a
   single pdf page), we need to split them in half: `spreads_to_singles.sh
   NAME_OF_FILE.pdf`. This will create a new file, `singles.pdf`, wherever you
   ran the script from.
   - Note this assumes that the page before splitting is letter size (8.5in x 11
     in) in landscape rotation. If that assumption is false, will need to change
     the `-g` option passed to `gs`. If you have this issue, open an issue and
     we can try and come up with a more general solution.
2. The single pages need to be reorganized so that they can be assembled in the
   proper order: `n 1 2 n-1 n-2 3 4 n-3 n-4 5 6 n-5 n-6 ...`:
   `rearrange_singles.py NAME_OF_SINGLES.pdf`. This will create a new file,
   `booklet.pdf`, for printing
3. These are then printed using LibreOffice, following [this
   article](https://help.ubuntu.com/stable/ubuntu-help/printing-booklet-duplex.html.en)
   (skiping the steps about printing in the specific order, steps 3 and 4).
   Pasting the steps below for posterity. First, open the pdf in LibreOffice,
   then:
   
>    Open the print dialog. This can normally be done through Print in the menu or using the Ctrl+P keyboard shortcut.
>
>    Click the Properties… button
>
>    In the Orientation drop-down list, make sure that Landscape is selected.
>
>    In the Duplex drop-down list, select Short Edge.
>
>    Click OK to go back to the print dialog.
>
>    ~~Under Range and Copies, choose Pages.~~
>
>    ~~Type the numbers of the pages in this order (n is the total number of pages, and a multiple of 4):~~
>
>    ~~n, 1, 2, n-1, n-2, 3, 4, n-3, n-4, 5, 6, n-5, n-6, 7, 8, n-7, n-8, 9, 10, n-9, n-10, 11, 12, n-11...~~
>
>    ~~Examples:~~
>
>        ~~4 page booklet: Type 4,1,2,3~~
>
>        ~~8 page booklet: Type 8,1,2,7,6,3,4,5~~
>
>        ~~20 page booklet: Type 20,1,2,19,18,3,4,17,16,5,6,15,14,7,8,13,12,9,10,11~~
>
>    Choose the Page Layout tab.
>
>    Under Layout, select Brochure.
>
>    Under Page Sides, in the Include drop-down list, select All pages.
>
>    Click Print.

# Requirements

- ghostscript for `spreads_to_singles.sh`. This was already installed on my
  system, see [docs](https://ghostscript.readthedocs.io/en/latest/Install.html)
  for how to install your own.
- `pdftk` for `spreads_to_singles.sh`, `rearrange_singles.py`. Also already
  installed for me, probably install from package manager.
- Python 3 for `rearrange_singles.py` because I find arithmatic and constructing
  arrays difficult in bash.
- ImageMagick for `rearrange_singles.py` to create blank files. You may get an
  error about permissions if it's used, in which case see
  [here](https://askubuntu.com/questions/1081895/trouble-with-batch-conversion-of-png-to-pdf-using-convert)
- LibreOffice for printing the booklet.
