#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 13:06:22 2022

@author: m102324
"""

import sys
from cobindability.BED import bed_genomic_size, bed_overlap_size
from cobindability.BED import bed_to_list, bed_counts
from os.path import basename
import logging
import numpy as np
import pandas as pd
from random import sample
from cobindability import version


__author__ = "Liguo Wang"
__copyright__ = "Copyleft"
__credits__ = []
__license__ = "MIT"
__version__ = version.version
__maintainer__ = "Liguo Wang"
__email__ = "wang.liguo@mayo.edu"
__status__ = "Development"


def bootstrap_coef(file1, file2, score_func, size_factor, name1=None,
                   name2=None, n_draws=20, fraction=0.75, bg_size=1.4e9):
    """
    Calculate the following indices:
    - Collocation coefficient,
    - Jaccard's coefficient
        (https://en.wikipedia.org/wiki/Jaccard_index),
    - Szymkiewicz–Simpson coefficient
        (https://en.wikipedia.org/wiki/Overlap_coefficient),
    - Sørensen–Dice coefficient
        (https://en.wikipedia.org/wiki/Sørensen–Dice_coefficient),
    - Pointwise mutual information
        (https://en.wikipedia.org/wiki/Pointwise_mutual_information),

    Parameters
    ----------
    file1 : str
        Genomic regions in BED (Browser Extensible Data,
        https://genome.ucsc.edu/FAQ/FAQformat.html#format1), BED-like or
        BigBed format. The BED-like format includes 'bed3','bed4','bed6',
        'bed12','bedgraph','narrowpeak', 'broadpeak','gappedpeak'. BED and
        BED-like format can be plain text, compressed (.gz, .z, .bz, .bz2,
        .bzip2) or remote (http://, https://, ftp://) files. Do not compress
        BigBed foramt. BigBed file can also be a remote file.
    file2 : str
        Genomic regions in BED (Browser Extensible Data,
        https://genome.ucsc.edu/FAQ/FAQformat.html#format1), BED-like or
        BigBed format. The BED-like format includes 'bed3','bed4','bed6',
        'bed12','bedgraph','narrowpeak', 'broadpeak','gappedpeak'. BED and
        BED-like format can be plain text, compressed (.gz, .z, .bz, .bz2,
        .bzip2) or remote (http://, https://, ftp://) files. Do not compress
        BigBed foramt. BigBed file can also be a remote file.
    score_func : function
        Function to calculate overlap index. Include ov_coef, ov_jaccard,
        ov_ss, ov_sd, pmi_value, npmi_value
    size_factor : float
        Set to the reciprocal of resampling fraction.
    name1 : str, optional
        Name to represent the 1st set of genomic intervals.
    name2 : str, optional
        Name to represent the 2nd set of genomic intervals.
    n_draws : int, optional
        Times of drawing samples with replacement. Set to '0' to turn off
        bootstraping.  The default is 20.
    fraction : float, optional
        The fraction of subsample. The default is 0.75 (75% of the orignal
        genomic reginos will be selected).
    bg_size : int, optional
        The effective background genome size. The default is 1.4e9.

    Note
    ----
        For the bootstrap process works properly, the overlapped genomic
        intervals in file1 and file2 must be merged.

    Returns
    -------
    pandas.Series
        Pandas Series of 'coef_obs', 'coef_exp','coef_ratio', 'coef_ratio_low',
        'coef_ratio_high'.
        'coef_obs' :
            Observed overlap coefficient between two BED files.
        'coef_exp' :
            Expected overlap coefficient between two BED files.
        'coef_ratio' :
            Ratio between 'coef_obs' and 'coef_exp'.
        'coef_ratio_low' :
            The lower bound of 95% confidence interval of 'coef_ratio'.
        'coef_ratio_high' :
            The upper bound of 95% confidence interval of 'coef_ratio'.

    """

    results = {}

    file1_lst = bed_to_list(file1)
    file2_lst = bed_to_list(file2)
    if name1 is None:
        results['A.name'] = basename(file1)
    else:
        results['A.name'] = name1
    if name2 is None:
        results['B.name'] = basename(file2)
    else:
        results['B.name'] = name2

    # calculate interval counts
    logging.debug("Calculating bed counts ...")
    totalCount1, totalCount2 = bed_counts(file1, file2)
    results['A.interval_count'] = totalCount1
    results['B.interval_count'] = totalCount2

    # calculate overall overlap coef
    logging.info("Calculating coefficient ...")
    (uniqBase1, uniqBase2) = bed_genomic_size(file1_lst, file2_lst)

    overlapBases = bed_overlap_size(file1_lst, file2_lst)
    overlapBases_exp = uniqBase1*uniqBase2/bg_size
    [unionBases] = bed_genomic_size(file1_lst + file2_lst)

    results['A.size'] = uniqBase1
    results['B.size'] = uniqBase2
    results['A_or_B.size'] = unionBases
    results['A_and_B.size'] = overlapBases
    results['Coef'] = score_func(uniqBase1, uniqBase2, overlapBases, bg_size)
    results['Coef(expected)'] = score_func(
        uniqBase1, uniqBase2, overlapBases_exp, bg_size)

    if n_draws > 0:
        if fraction > 0 and fraction < 1:
            resample_size1 = int(totalCount1 * fraction)
            resample_size2 = int(totalCount2 * fraction)
        else:
            logging.error("Fraction must be > 0 and < 1.")
            sys.exit(0)
        logging.debug("Bootstraping is on. Iterate %d times. " % n_draws)
        tmp = []
        for i in range(n_draws):
            logging.debug("Bootstrap resampling %d ..." % i)
            sample_1 = sample(file1_lst, resample_size1)
            sample_2 = sample(file2_lst, resample_size2)

            sample_overlapBases = bed_overlap_size(sample_1, sample_2)
            if size_factor != 1:
                sample_overlapBases = sample_overlapBases * size_factor
            (sample1_size, sample2_size) = bed_genomic_size(sample_1, sample_2)
            sample_ovcoef = score_func(
                sample1_size, sample2_size, sample_overlapBases, bg_size)
            tmp.append(sample_ovcoef)
        ci_lower = np.percentile(np.array(tmp), 2.5)
        ci_upper = np.percentile(np.array(tmp), 97.5)
        results['Coef(95% CI)'] = '[%.4f,%.4f]' % (ci_lower, ci_upper)
    else:
        logging.info("Bootstraping is off ...")
        results['Coef(95% CI)'] = '[NA,NA]'

    return pd.Series(data=results)


def bootstrap_npmi(file1, file2, score_func, size_factor, name1=None,
                   name2=None, n_draws=20, fraction=0.75, bg_size=1.4e9):
    """
    Calculate the following indices:
    - Normalized pointwise mutual information.

    Parameters
    ----------
    file1 : str
        Genomic regions in BED (Browser Extensible Data,
        https://genome.ucsc.edu/FAQ/FAQformat.html#format1), BED-like or
        BigBed format. The BED-like format includes 'bed3','bed4','bed6',
        'bed12','bedgraph','narrowpeak', 'broadpeak','gappedpeak'. BED and
        BED-like format can be plain text, compressed (.gz, .z, .bz, .bz2,
        .bzip2) or remote (http://, https://, ftp://) files. Do not compress
        BigBed foramt. BigBed file can also be a remote file.
    file2 : str
        Genomic regions in BED (Browser Extensible Data,
        https://genome.ucsc.edu/FAQ/FAQformat.html#format1), BED-like or
        BigBed format. The BED-like format includes 'bed3','bed4','bed6',
        'bed12','bedgraph','narrowpeak', 'broadpeak','gappedpeak'. BED and
        BED-like format can be plain text, compressed (.gz, .z, .bz, .bz2,
        .bzip2) or remote (http://, https://, ftp://) files. Do not compress
        BigBed foramt. BigBed file can also be a remote file.
    score_func : function
        Function to calculate overlap index. Include ov_coef, ov_jaccard,
        ov_ss, ov_sd, pmi_value, npmi_value
    size_factor : float
        Set to the reciprocal of resampling fraction.
    name1 : str, optional
        Name to represent the 1st set of genomic intervals.
    name2 : str, optional
        Name to represent the 2nd set of genomic intervals.
    n_draws : int, optional
        Times of drawing samples with replacement. Set to '0' to turn off
        bootstraping.  The default is 20.
    fraction : float, optional
        The fraction of subsample. The default is 0.75 (75% of the orignal
        genomic reginos will be selected).
    bg_size : int, optional
        The effective background genome size. The default is 1.4e9.

    Returns
    -------
    pandas.Series
        Pandas Series of 'coef_obs', 'coef_exp','coef_ratio',
        'coef_ratio_low', 'coef_ratio_high'.
        'coef_obs' :
            Observed overlap coefficient between two BED files.
        'coef_exp' :
            Expected overlap coefficient between two BED files.
        'coef_ratio' :
            Ratio between 'coef_obs' and 'coef_exp'.
        'coef_ratio_low' :
            The lower bound of 95% confidence interval of 'coef_ratio'.
        'coef_ratio_high' :
            The upper bound of 95% confidence interval of 'coef_ratio'.
    """

    results = {}

    file1_lst = bed_to_list(file1)
    file2_lst = bed_to_list(file2)

    if name1 is None:
        results['A.name'] = basename(file1)
    else:
        results['A.name'] = name1
    if name2 is None:
        results['B.name'] = basename(file2)
    else:
        results['B.name'] = name2

    # calculate interval counts
    logging.debug("Calculating bed counts ...")
    totalCount1, totalCount2 = bed_counts(file1, file2)
    results['A.interval_count'] = totalCount1
    results['B.interval_count'] = totalCount2

    # calculate overall overlap coef
    logging.info("Calculating coefficient ...")
    (uniqBase1, uniqBase2) = bed_genomic_size(file1_lst, file2_lst)

    overlapBases = bed_overlap_size(file1_lst, file2_lst)
    overlapBases_exp = uniqBase1*uniqBase2/bg_size
    [unionBases] = bed_genomic_size(file1_lst + file2_lst)

    results['A.size'] = uniqBase1
    results['B.size'] = uniqBase2
    results['A_or_B.size'] = unionBases
    results['A_and_B.size'] = overlapBases
    results['Coef'] = score_func(uniqBase1, uniqBase2, overlapBases, bg_size)
    results['Coef(expected)'] = score_func(
        uniqBase1, uniqBase2, overlapBases_exp, bg_size)

    if n_draws > 0:
        if fraction > 0 and fraction < 1:
            resample_size1 = int(totalCount1 * fraction)
            resample_size2 = int(totalCount2 * fraction)
        else:
            logging.error("Fraction must be > 0 and < 1.")
            sys.exit(0)
        logging.debug("Bootstraping is on. Iterate %d times. " % n_draws)
        tmp = []
        for i in range(n_draws):
            logging.debug("Bootstrap resampling %d ..." % i)
            sample_1 = sample(file1_lst, resample_size1)
            sample_2 = sample(file2_lst, resample_size2)

            sample_overlapBases = bed_overlap_size(sample_1, sample_2)
            if size_factor != 1:
                sample_overlapBases = sample_overlapBases * size_factor
            (sample1_size, sample2_size) = bed_genomic_size(sample_1, sample_2)
            sample_ovcoef = score_func(
                sample1_size, sample2_size,
                sample_overlapBases, bg_size*fraction)
            tmp.append(sample_ovcoef)
        ci_lower = np.percentile(np.array(tmp), 2.5)
        ci_upper = np.percentile(np.array(tmp), 97.5)
        results['Coef(95% CI)'] = '[%.4f,%.4f]' % (ci_lower, ci_upper)
    else:
        logging.info("Bootstraping is off ...")
        results['Coef(95% CI)'] = '[NA,NA]'

    return pd.Series(data=results)
