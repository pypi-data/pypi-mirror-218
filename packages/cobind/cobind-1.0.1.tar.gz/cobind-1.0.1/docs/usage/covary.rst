Covary
============

Description
-------------
Evaluate the signal correlations (`Pearson's r <https://en.wikipedia.org/wiki/Pearson_correlation_coefficient>`_
, `Spearman's 𝜌 <https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient>`_, 
and `Kendall's 𝜏 <https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient>`_) between two sets of genomic intervals. 


Usage
-----

:code:`cobind.py covary -h`

::
 
 usage: cobind.py covary [-h] [--nameA NAMEA] [--nameB NAMEB] [--na NA_LABEL]
                         [--type {mean,min,max}] [--topx TOP_X]
                         [--min_sig MIN_SIGNAL] [--exact] [--keepna]
                         [-l log_file] [-d]
                         input_A.bed input_A.bw input_B.bed input_B.bw
                         output_prefix
 
 positional arguments:
   input_A.bed           Genomic regions in BED, BED-like or bigBed format. The
                         BED-like format includes:'bed3', 'bed4', 'bed6',
                         'bed12', 'bedgraph', 'narrowpeak', 'broadpeak',
                         'gappedpeak'. BED and BED-like format can be plain
                         text, compressed (.gz, .z, .bz, .bz2, .bzip2) or
                         remote (http://, https://, ftp://) files. Do not
                         compress BigBed foramt. BigBed file can also be a
                         remote file.
   input_A.bw            Input bigWig file matched to 'input_A.bed'. BigWig
                         file can be local or remote. Note: the chromosome IDs
                         must be consistent between BED and bigWig files.
   input_B.bed           Genomic regions in BED, BED-like or bigBed format. The
                         BED-like format includes:'bed3', 'bed4', 'bed6',
                         'bed12', 'bedgraph', 'narrowpeak', 'broadpeak',
                         'gappedpeak'. BED and BED-like format can be plain
                         text, compressed (.gz, .z, .bz, .bz2, .bzip2) or
                         remote (http://, https://, ftp://) files. Do not
                         compress BigBed foramt. BigBed file can also be a
                         remote file.
   input_B.bw            Input bigWig file matched to 'input_B.bed'. BigWig
                         file can be local or remote. Note: the chromosome IDs
                         must be consistent between BED and bigWig files.
   output_prefix         Prefix of output files. Three files will be generated:
                         "output_prefix_bedA_unique.tsv" (input_A.bed specific
                         regions and their bigWig scores),
                         "output_prefix_bedB_unique.tsv" (input_B.bed specific
                         regions and their bigWig scores), and
                         "output_prefix_common.tsv"(input_A.bed and input_B.bed
                         overlapped regions and their bigWig scores).

 options:
   -h, --help            show this help message and exit
   --nameA NAMEA         Name of the 1st set of genomic interval, if not
                         proviced, "bedA" will be used. Only affects the name
                         of output file.
   --nameB NAMEB         Name of the 2nd set of genomic interval, if not
                         proviced, "bedB" will be used. Only affects the name
                         of output file.
   --na NA_LABEL         Symbols used to represent the missing values.
                         (default: nan)
   --type {mean,min,max}
                         Summary statistic score type ('min','mean' or 'max')
                         of a genomic region. (default: mean)
   --topx TOP_X          Fraction (if 0 < top_X <= 1) or number (if top_X > 1)
                         of genomic regions used to calculate Pearson,
                         Spearman, Kendall's correlations. If TOP_X == 1 (i.e.,
                         100%), all the genomic regions will be used to
                         calculate correlations. (default: 1.0)
   --min_sig MIN_SIGNAL  Genomic region with summary statistic score <= this
                         will be removed. (default: 0)
   --exact               If set, calculate the "exact" summary statistic score
                         rather than "zoom-level" score for each genomic
                         region.
   --keepna              If set, a genomic region will be kept even it does not
                         have summary statistical score in either of the two
                         bigWig files. This flag only affects the output TSV
                         files.
   -l log_file, --log log_file
                         This file is used to save the log information. By
                         default, if no file is specified (None), the log
                         information will be printed to the screen.
   -d, --debug           Print detailed information for debugging.

Example
-------

::
 
 cobind.py covary CTCF_ENCFF660GHM.bed3 CTCF_ENCFF682MFJ_FC.bigWig RAD21_ENCFF057JFH.bed3 
 RAD21_ENCFF130GMP.bigWig output


::
 
 2022-01-20 02:56:53 [INFO]  Read and union BED file: "CTCF_ENCFF660GHM.bed3"
 2022-01-20 02:56:54 [INFO]  Unioned regions of "CTCF_ENCFF660GHM.bed3" : 58584
 2022-01-20 02:56:54 [INFO]  Read and union BED file: "RAD21_ENCFF057JFH.bed3"
 2022-01-20 02:56:54 [INFO]  Unioned regions of "RAD21_ENCFF057JFH.bed3" : 31955
 ...
                Correlation  P-value
 Pearson_cor:        0.6378   0.0000
 Spearman_rho:       0.6355   0.0000
 Kendall_tau:        0.4406   0.0000
 2022-01-20 02:57:06 [INFO]  Calculate covariabilities of "CTCF_ENCFF660GHM.bed3"
                             unique regions ...
 2022-01-20 02:57:16 [INFO]  Sort dataframe by summary statistical scores ...
 2022-01-20 02:57:16 [INFO]  Save dataframe to: "output_bedA_unique.tsv"
 2022-01-20 02:57:16 [INFO]  Select 30347 regions ...
                Correlation  P-value
 Pearson_cor:        0.3356   0.0000
 Spearman_rho:       0.3667   0.0000
 Kendall_tau:        0.2489   0.0000
 2022-01-20 02:57:16 [INFO]  Calculate covariabilities of "RAD21_ENCFF057JFH.bed3"
                             unique regions ...
 2022-01-20 02:57:18 [INFO]  Sort dataframe by summary statistical scores ...
 2022-01-20 02:57:18 [INFO]  Save dataframe to: "output_bedB_unique.tsv"
 2022-01-20 02:57:18 [INFO]  Select 3822 regions ...
                Correlation  P-value
 Pearson_cor:        0.2511   0.0000
 Spearman_rho:       0.2261   0.0000
 Kendall_tau:        0.1534   0.0000



