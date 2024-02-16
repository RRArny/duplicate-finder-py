import hashlib
from pathlib import Path
import sys

def hash(f : "Path") -> "SHA-256 digest for argument":
    '''Calculates the SHA-256 digest of a file.
    
    Argument:
        f: Path - path to the file
    '''
    BLOCKSIZE = 65536
    if(not f.exists()):
        print("File '{}' does not exist!".format(f))
        raise IOError(str(f))
    
    hasher = hashlib.sha256()
    with open(str(f), 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()

def equal(f1 : "Path", f2 : "Path") -> "True if content equal, else false":
    '''Compares two files by their content
    
    Arguments:
        f1: Path - 1st file
        f2: Path - 2nd file
    '''
    BLOCKSIZE = 65536
    if(hash(f1) != hash(f2)):
        return False
    with open(str(f1), 'rb') as file1:
        with open(str(f2), 'rb') as file2:
            buf1 = file1.read(BLOCKSIZE)
            buf2 = file2.read(BLOCKSIZE)
            while (len(buf1) > 0 or len(buf2) > 0):
                if(buf1 != buf2):
                    return False
                buf1 = file1.read(BLOCKSIZE)
                buf2 = file2.read(BLOCKSIZE)
            return buf1 == buf2

def _removeDuplicates(dir : "String", verb : "Boolean" = True) -> "Number of deleted files":
    '''Helper function, DO NOT USE THIS!
    
    Arguments:
        dir: String - Path of the directory
        verb: Boolean - Verbose
        
    For really not obvious reasons this function deletes at most 50 duplicate files.
    So battle plan is to call it until no new duplicates are found...
    '''
    files = [x for x in Path(dir).iterdir() if not x.is_dir()]
    files.sort()

    counter = 0

    for f1 in files:
        files.remove(f1)
        for f2 in files:
            if (equal(f1, f2)):
                if(verb):
                    print("'{}' and '{}' are equal.".format(f1, f2))
                    print("Deleting '{}'...\n".format(f2))
                files.remove(f2)
                os.remove(str(f2))
                f2.unlink()
                counter += 1
                
    return counter

def removeDuplicates(dir : "String", verb : "Boolean" = True, rec : "Boolean" = False) -> "Number of deleted files":
    '''Searches directory for duplicates
    
    Arguments:
        dir: String - Path to the directory
        verb: Boolean - Verbose
        rec: Boolean - Recursive
    '''
    count = 0
    deltac = _removeDuplicates(dir, verb)
    while( deltac != 0):
        count += deltac
        deltac = _removeDuplicates(dir, verb)
        
    if (rec):            
        for d in [x for x in Path(dir).iterdir() if x.is_dir()]:
            counter += removeDuplicates(str(d), verb, rec)
        
    return count

### Main begins here: ###

if(__name__ == "__main__"):
    
    directory = ""
    verbose = ""
    rec = ""

    if ("r" in sys.argv or "+r" in sys.argv or "-r" in sys.argv):
        rec = True
    
    if ("v" in sys.argv or "+v" in sys.argv or "-v" in sys.argv):
        verbose = True
        
    if ("vr" in sys.argv or "+vr" in sys.argv or "rv" in sys.argv or "+rv" in sys.argv or "-vr" in sys.argv or "-rv" in sys.argv):    
        verbose = True
        rec = True
    
    '''
    while(verbose == ""):
        answ = input("Do you want extensive output? [y/n]")
        if(answ in {"y", "yes"}):
            verbose = True
        elif (answ in {"n", "no"}):
            verbose = False
            
    while (rec == ""):
        answ = input("Do you want to search recursively? [y/n]")
        if(answ in {"y", "yes"}):
            rec = True
        elif (answ in {"n", "no"}):
            rec = False
    '''
    
    verbose = (verbose == True)
    rec = (rec == True)
    
    for f in sys.argv[1:]:
        if Path(f).exists():
            if (not Path(directory).is_dir()):
                print("'{}' is not a directory!\n".format(directory))
            else:
                directory = f
                break
    
    while (directory == ""):
        directory = input("Enter a directory ('.' for current working directory, enter 'exit' to quit):\n")
    
        if(directory == "exit"):
            sys.exit()
            
        elif (directory == "."):
            directory = str(Path.cwd())
            break
            
        elif (not Path(directory).is_dir()):
            print("'{}' is not a directory!\n".format(directory))
            directory = ""
            
        else:
            break
            
    print("Checking {}...".format(directory))
    
    counter = removeDuplicates(directory, verbose, rec)
    
    if (counter == 0):
        print("Done, no duplicates found.")
    elif (counter == 1): 
        print("Done, 1 file removed.")
    else:
        print("Done, {} files removed.".format(counter))
         
