# DuplicateFinder.py README

## Standalone Usage

If you plan on using the script as a standalone program,
you eather provide the directory path as command
line argument, e.g.:

`python duplicatefinder.py [-v][-r] /home/xxx/`

Add "v" or "-v" for extended console output.
The search will not include subdirectories, unless you
use eather the "r" or "-r" option.

## Library Usage

If you want to use the functionality in your own script,
copy the DuplicateFinder somewhere inside your PYTHONPATH,
import duplicatefinder
and invoke the
duplicatefinder.removeDuplicates() function.

Syntax:

```
removeDuplicates(dir,		#String: Path to the directory
		verb = True,	#Boolean: If True: extended console output, quiet if False.								
		rec = False	#Boolean: If True: recursive search
)
```

