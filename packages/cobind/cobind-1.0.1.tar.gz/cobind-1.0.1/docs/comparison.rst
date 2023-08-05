
Compare different metrics
--------------------------

The table below gives the lower and upper bounds of the 6 metrics and their major drawbacks if any.


.. list-table::
   :widths: 5,20,20,35
   :header-rows: 1

   * - *Metric*
     - *Lower bound*
     - *Upper bound*
     - *Comments*
   * - C(A,B)
     - 0 (no overlap)
     - 1 (A = B)
     -   
   * - J(A,B)
     - 0 (no overlap)
     - 1 (A = B)
     - Bias towards the **larger** interval
   * - SD(A,B)
     - 0 (no overlap)
     - 1 (A = B)
     - Bias towards the **larger** interval
   * - SS(A,B)
     - 0 (no overlap)
     - 1 (A = B, A ∈ B, or B ∈ A)
     - Bias towards the **smaller** interval
   * - PMI
     - -inf (no overlap)
     - min(-log(p(A)), -log(p(B)))
     - No fixed bound
   * - NPMI
     - -1 (no overlap)
     - 1 (A = B)
     -   

The table below compares the intersection-based metrics. **C**, **J**, **SD**, and **SS**. All the four metrics are bounded by 0 and 1. When the size of the two genomic intervals are significanlty different, **C** is less sensitive to the extreme, and gives a compromised score compared to **J**/**SD** and **SS**.

.. list-table:: **C(A,B)** vs **J(A,B)** vs **SD(A,B)** vs **SS(A,B)**
   :widths: 15,15,15,15,15,15,15,15,20
   :header-rows: 1

   * - *SROG*
     - \|A\|
     - \|B\|
     - \|A ∩ B\|
     - \|A ∪ B\|
     - *C*
     - *J*
     - *SD*
     - *SS*
   * - A equals B
     - 1000
     - 1000
     - 1000
     - 1000
     - 1
     - 1
     - 1
     - 1
   * - A disjoint B 
     - 1000
     - 1000
     - 0
     - 2000
     - 0
     - 0
     - 0
     - 0
   * - A overlaps B 
     - 100
     - 1000
     - 50
     - 1050
     - 0.158
     - 0.0476
     - 0.0909
     - 0.5
   * - A within B 
     - 100
     - 1000
     - 100
     - 1000
     - 0.316
     - 0.1
     - 0.182
     - 1




CTCF: Demonstration
-------------------

70-95% of `CTCF <https://en.wikipedia.org/wiki/CTCF>`_ binding sites are also bound by `cohesin <https://en.wikipedia.org/wiki/Cohesin>`_ complex (including SMC1, SMC3, RAD21/SCC1, STAG1/SA1, STAG2/SA2) to establish chromatin loops and regulate gene expression [#f1]_, [#f2]_. 

We used CTCF-cohesin as a positive control to evaluate the performance of the six collocation measurements (including C, J, SD, SS, PMI and NPMI).  We first calculated the scores of these metrics between all the binding sites (defined as cistrome) of `CTCF <https://en.wikipedia.org/wiki/CTCF>`_ with those cistromes of 1207 TFs curated in the `ReMap <https://remap2022.univ-amu.fr/>`_ database. Then, we calculate the `Zscore <https://cobind.readthedocs.io/en/latest/usage/zscore.html>`_ as an overall measurement of the cobindability. Please note, TRIM22 is not part of the cohesin complex, but multiple studies have identified TRIM22 as a critical regulator of chromatin structure. TRIM22 bindings are highly enriched at chromatin contact domain boundaries [#f3]_, [#f4]_. 

.. image:: _static/CTCF.png
  :width: 800
  :alt: Alternative text


**(A)** Collocation between CTCF binding sites and the binding sites of 1207 TFs were evaluated uing the six measurements as well as the zscore. Only the top 20 TFs were displayed.



.. [#f1] Pugacheva EM, Kubo N, Loukinov D, et al. CTCF mediates chromatin looping via N-terminal domain-dependent cohesin retention. Proc Natl Acad Sci U S A. 2020;117(4):2020-2031. doi:10.1073/pnas.1911708117
.. [#f2] Xiao T, Li X, Felsenfeld G. The Myc-associated zinc finger protein (MAZ) works together with CTCF to control cohesin positioning and genome organization. Proc Natl Acad Sci U S A. 2021;118(7):e2023127118. doi:10.1073/pnas.2023127118
.. [#f3] Chen F, Li G, Zhang MQ, Chen Y. HiCDB: a sensitive and robust method for detecting contact domain boundaries. Nucleic Acids Res. 2018;46(21):11239-11250. doi:10.1093/nar/gky789
.. [#f4] Di Pierro M, Cheng RR, Lieberman Aiden E, Wolynes PG, Onuchic JN. De novo prediction of human chromosome structures: Epigenetic marking patterns encode genome architecture. Proc Natl Acad Sci U S A. 2017;114(46):12126-12131. doi:10.1073/pnas.1714980114
