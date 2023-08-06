""".. Line to protect from pydocstyle D205, D400.

Cutadapt
--------

Remove adapter sequences from reads in FASTQ file.
"""

import os
import shutil
import subprocess
import tempfile

import iCount
from iCount.files.fastq import get_qual_encoding, ENCODING_TO_OFFSET


def get_version():
    """Get cutadapt version."""
    args = ['cutadapt', '--version']
    try:
        ver = subprocess.check_output(args, shell=False, universal_newlines=True)
        return str(ver).rstrip('\n\r')
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def run(reads,
        adapter,
        reads_trimmed=None,
        overwrite=False,
        qual_trim=None,
        minimum_length=None,
        overlap=None,
        untrimmed_output=None,
        error_rate=None,
        ):
    """
    Remove adapter sequences from high-throughput sequencing reads.

    Parameters
    ----------
    reads : str
        Input FASTQ file.
    adapter : str
        Sequence of an adapter ligated to the 3' end.
    reads_trimmed : str
        Output FASTQ file containing trimmed reads. If not provided
    overwrite : bool
        If true, overwrite input file (reads) with trimmed file.
    qual_trim : int
        Trim low-quality bases before adapter removal.
    minimum_length : int
        Discard trimmed reads that are shorter than `minimum_length`.
    overlap : int
        Require ``overlap`` overlap between read and adapter for an
        adapter to be found.
    untrimmed_output : str
        Write reads that do not contain any adapter to this file.
    error_rate : float
        Maximum allowed error rate (no. of errors divided by the length
        of the matching region).

    Returns
    -------
    int
        Return code of the `cutadapt` program.

    """
    args = [
        'cutadapt',
        '--quiet',
        '-a', adapter,
    ]
    qual_base = ENCODING_TO_OFFSET.get(get_qual_encoding(reads), 33)
    args.extend(['--quality-base={}'.format(qual_base)])

    if reads_trimmed is None:
        # Auto-generate output name:
        extension = '.gz' if reads.endswith('.gz') else ''
        name = next(tempfile._get_candidate_names()) + '.fq' + extension  # pylint: disable=protected-access
        reads_trimmed = os.path.join(iCount.TMP_ROOT, name)
    if qual_trim is not None:
        args.extend(['-q', '{:d}'.format(qual_trim)])
    if minimum_length is not None:
        args.extend(['-m', '{:d}'.format(minimum_length)])
    if overlap is not None:
        args.extend(['--overlap', '{:d}'.format(overlap)])
    if untrimmed_output is not None:
        args.extend(['--untrimmed-output', '{}'.format(untrimmed_output)])
    if error_rate is not None:
        args.extend(['--error-rate', '{}'.format(error_rate)])
    args.extend(['-o', reads_trimmed, reads])

    rcode = subprocess.call(args, shell=False)

    if overwrite:
        shutil.move(reads_trimmed, reads)

    return rcode
