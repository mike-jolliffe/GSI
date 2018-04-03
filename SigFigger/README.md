# SigFigger

This program will convert values in a specific column, `GSI_Result`, to their correct number of significant figures,
based on a second column, `SigFigs`. Results are written to a new sheet in the same workbook.

It utilizes `to_precision.py`, which is available on [GitHub](https://github.com/BebeSparkelSparkel/to-precision).

### Prerequisites

SigFigger is built with `Python 3.6` and the following packages:

`et-xmlfile (1.0.1)`
`jdcal (1.3)`
`openpyxl (2.5.1)`

These can be installed using `pip install -r requirements.txt` at the command line.

### Running the program

When you `set_sig_figs.py` with Python at the command line, you will be prompted
for a `filepath` and and `worksheet`. The filepath should just be the full filepath
to the .xlsx workbook you want to modify (e.g., `C:\\Documents\\workbook.xlsx`).
For the `worksheet` input, just provide the name of the worksheet containing the
values to be modified (e.g., `Sheet1`).

At this point, the program will look for two columns of data: first, a column with
the header `SigFigs`, which holds a number representing the sig figs to modify
that row's result to. The result to be modified is in a column entitled `GSI_Result`.
Operations are performed row by row, with the program modifying a given row's result
by that row's `SigFigs` value.

Column headers can be changed by opening `set_sig_figs.py` and modifying the
`SIG_FIGS_HDR` and `RESULTS_HDR` variables to a different set of header strings.   
