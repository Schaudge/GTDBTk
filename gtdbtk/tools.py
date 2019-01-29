# import prodigal
import math
import time
import random
import os
import hashlib

from itertools import islice
from biolib_lite.seq_io import read_fasta
from biolib_lite.common import remove_extension


##################################################
############MISC UTILITIES########################
##################################################

def add_ncbi_prefix(refname):
    if refname.startswith("GCF_"):
        return "RS_" + refname
    elif refname.startswith("GCA_"):
        return "GB_" + refname
    else:
        return refname


def splitchunks(d, n):
    chunksize = int(math.ceil(len(d) / float(n)))
    it = iter(d)
    for _ in xrange(0, len(d), chunksize):
        yield {k: d[k] for k in islice(it, chunksize)}


def splitchunks_list(l, n):
    """Yield successive n-sized chunks from l."""
    chunksize = int(math.ceil(len(l) / float(n)))
    for i in range(0, len(l), chunksize):
        yield l[i:i + chunksize]


def generateTempTableName():
    rng = random.SystemRandom()
    suffix = ''
    for _ in range(0, 10):
        suffix += rng.choice(
            'abcefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return "TEMP" + suffix + str(int(time.time()))


def list_genomes_dir(userdir):
    """List fasta files in a specified directory

    Parameters
    ----------
    userdir : str
        Directory path where all fasta files are

    Returns
    -------
    dict
        Dictionary indicating the genomic file for each genome.
    """
    if not os.path.exists(userdir):
        raise ValueError('{0} does not exist.'.format(userdir))
    else:
        onlygenomefiles = {f: os.path.join(userdir, f) for f in os.listdir(
            userdir) if os.path.isfile(os.path.join(userdir, f))}
        for potential_file in onlygenomefiles:
            try:
                read_fasta(os.path.join(userdir, potential_file))
            except:
                raise IOError("{0} is not a fasta file." .format(
                    os.path.join(userdir, potential_file)))
        return onlygenomefiles


def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z


def sha256(input_file):
    """Determine SHA256 hash for file.
    Parameters
    ----------
    input_file : str
        Name of file.
    Returns
    -------
    str
        SHA256 hash.
    """

    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(input_file, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)

    return hasher.hexdigest()
