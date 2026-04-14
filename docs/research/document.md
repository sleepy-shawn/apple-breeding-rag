1. 哪些基因或位点与苹果果肉硬度（firmness）保持相关？请列证据。  
   回答
根据提供的证据，与苹果果肉硬度（firmness）保持相关的基因或位点信息如下：

1. **SNP位点**：证据[1]中列出了多个与感官评价（Sensory evaluation）和脆度评分（Crispness score）相关的SNP位点，包括：
   - SNP_24399345
   - SNP_8667563
   - SNP_15566229
   这些位点出现在一个与硬度（firmness_like）性状相关的基因分型数据表中。

2. **KASP基因分型位点**：证据[2]中提到了在品种“Honeycrisp”中进行KASP基因分型的两个SNP位点：
   - SNP-2,002
   - SNP-1,545
   该数据表同样被推测与硬度（firmness_like）性状相关。

**结论**：以上列出的SNP位点（SNP_24399345, SNP_8667563, SNP_15566229, SNP-2,002, SNP-1,545）与苹果果肉硬度保持相关，证据来源于相关的基因分型数据表。但需要指出，提供的证据仅为数据表格片段，未包含具体的基因名称或更详细的位点功能描述。

引用编号：[1], [2]

证据
[1] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/039_development_and_application_of_key_allel_004_Supplementary file4.xlsx; sheet: Sheet1; row_index: 1; row_text: Table S4 Genotyping of different varities: Name; col_2: SNP_24399345; col_3: SNP_8667563; col_4: SNP_15566229; col_5: Sensory evaluation; col_6: Crispness score; col_7: Marker combination; trait_guess: firmness_like; record_type: data

[2] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_004_koaf007_supplementary_data.zip::Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 277; row_text: Supplementary Table S5. KASP genotyping in SNP-2,002: Honeycrisp; col_2: A10; col_3: C; col_4: 1114.7; col_5: 151.4; col_6: FAM; col_7: 1; Supplementary Table S5. KASP genotyping in SNP-1,545: Honeycrisp; col_11: A10; col_12: A; col_13: 1067; col_14: 266.2; col_15: FAM; col_16: 1; trait_guess: firmness_like; record_type: data





2. 与苹果脆度（crispness）相关的 SNP 或 marker 有哪些？  
回答
根据提供的证据，与苹果脆度（crispness）相关的SNP标记主要有以下三个：

1. **SNP_24399345**：与果肉的机械特性（力学性质）相关。
2. **SNP_8667563**：与果肉的水分含量相关。
3. **SNP_15566229**：与细胞面积相关。

这些标记被整合为KASP分子标记，用于评估苹果脆度。特定的基因型组合与脆度表型相关联：
- **CC-CC-TT** 基因型组合代表果肉较软的苹果。
- **GG-CC/TC-TT** 基因型组合代表质地较硬的苹果。
- 其他组合（如GG-TT/TC-TC/CC）反映了脆度的复杂性。

引用编号：[1]

证据
[1] paper | 039_development_and_application_of_key_allel_001_Development and application of Key Allele-Specific PCR (KASP) molecular markers for assessing apple fruit crispness | p.16
a large number of unknown genes and various regulatory genes suggests that the key SNPs may be associated with crispness through more complex biological processes (Table S6). In general, the KASP markers developed in this study integrate aspects of cell mechanics, histology, and physiology to measure crispness, it would be a bet- ter marker for identity of flesh crisp which include three critical SNP markers: SNP_24399345 for mechanical properties, SNP_8667563 for water content, and SNP_15566229 for cell area. The combination of these markers in the CC-CC-TT genotype effectively represents soft apples, while the GG-CC/TC-TT genotype indi- cates apples with a firmer texture. The complexity of crispness is reflected in the multiple genotypic combinations of GG-TT/TC-TC/CC, which better represent the

[2] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/039_development_and_application_of_key_allel_004_Supplementary file4.xlsx; sheet: Sheet1; row_index: 1; row_text: Table S4 Genotyping of different varities: Name; col_2: SNP_24399345; col_3: SNP_8667563; col_4: SNP_15566229; col_5: Sensory evaluation; col_6: Crispness score; col_7: Marker combination; trait_guess: firmness_like; record_type: data

[3] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 277; row_text: Supplementary Table S5. KASP genotyping in SNP-2,002: Honeycrisp; col_2: A10; col_3: C; col_4: 1114.7; col_5: 151.4; col_6: FAM; col_7: 1; Supplementary Table S5. KASP genotyping in SNP-1,545: Honeycrisp; col_11: A10; col_12: A; col_13: 1067; col_14: 266.2; col_15: FAM; col_16: 1; trait_guess: firmness_like; record_type: data




3. `MdNAC18.1` 与成熟/硬度性状的关联证据有哪些？  
   回答
根据提供的证据，关于 `MdNAC18.1` 与成熟/硬度性状的关联，证据仅表明该基因在果实发育早期于不同成熟期品种中的表达情况，但未直接说明其与成熟或硬度性状的具体关联机制或数据。

具体证据显示：
- 在果实发育早期，`MdNAC18.1` 在早熟和晚熟品种中均有表达（参考附图 S2）[1][2][3][4][5][6]。

由于证据中未包含该基因如何影响成熟时间、果实硬度或相关性状的直接实验数据（如基因功能验证、性状相关性分析等），因此无法提供更具体的关联证据。

引用编号：[1][2][3][4][5][6]

证据
[1] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18 | p.2
Supplementary Figure S2. Expression of MdNAC18.1 in early- and late-ripening cultivars in the early stages of fruit development. Each sample has three biological replicates. DAP, days after pollination.

[2] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18 | p.2
Supplementary Figure S2. Expression of MdNAC18.1 in early- and late-ripening cultivars in the early stages of fruit development. Each sample has three biological replicates. DAP, days after pollination.

[3] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18 | p.2
Supplementary Figure S2. Expression of MdNAC18.1 in early- and late-ripening cultivars in the early stages of fruit development. Each sample has three biological replicates. DAP, days after pollination.

[4] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18 | p.2
Supplementary Figure S2. Expression of MdNAC18.1 in early- and late-ripening cultivars in the early stages of fruit development. Each sample has three biological replicates. DAP, days after pollination.

[5] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18 | p.2
Supplementary Figure S2. Expression of MdNAC18.1 in early- and late-ripening cultivars in the early stages of fruit development. Each sample has three biological replicates. DAP, days after pollination.

[6] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18 | p.2
Supplementary Figure S2. Expression of MdNAC18.1 in early- and late-ripening cultivars in the early stages of fruit development. Each sample has three biological replicates. DAP, days after pollination.




4. `MdNAC5` 对果实硬度或成熟差异的作用有什么证据？  

回答
根据提供的证据，关于 **MdNAC5** 对果实硬度或成熟差异的作用，证据中仅描述了 **MdNAC5A** 和 **MdNAC5T** 两种变体与 **MdERF3** 的相互作用，并提及这种差异性的相互作用调控 **MdACS1**。然而，证据中并未直接说明这种调控如何具体影响果实硬度或成熟差异，也没有提供相关的表型数据或功能验证结果。

因此，**证据不足**，无法直接回答 MdNAC5 对果实硬度或成熟差异的具体作用机制。

引用编号：[1], [2], [3], [4], [5], [6]

证据
[1] paper | 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple | p.11
Liu et al. | 11 Figure 7.MdNAC5A and MdNAC5T differentially interact with MdERF3 to regulateMdACS1.( A) The structure of MdNAC5A and MdNAC5T.( B)D o c k i n g prediction of MdNAC5A and MdNAC5T on MdERF3. (C) Luciferase complementation imaging assays showed that MdNAC5A and MdNAC5T interact with MdERF3. (D) BiFC assays showed that MdNAC5A and MdNAC5T interact with MdERF3 (indicated by the fluorescence observed in the nucleus of protoplasts). The YFP fluorescence coexpressed by MdNAC5A/MdNAC5T and MdERF3Arabidopsis thalianaprotoplasts was detected by confocal laser scanning microscope. From left to right, YFP , chloroplast, bright field, and merged field images. Bars = 10μm. (E) Y2H assays showing that MdNAC5A and MdNAC5T interact with MdERF3. The fusion vectors pGBKT7-MdNAC5A△ 175–364/MdNAC5T△ 175–364 and pGADT7-MdERF3 were co-transformed in Y2H on SD/−Leu/−Trp (−LT) medium. Single coloni

[2] paper | 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple | p.11
Liu et al. | 11 Figure 7.MdNAC5A and MdNAC5T differentially interact with MdERF3 to regulateMdACS1.( A) The structure of MdNAC5A and MdNAC5T.( B)D o c k i n g prediction of MdNAC5A and MdNAC5T on MdERF3. (C) Luciferase complementation imaging assays showed that MdNAC5A and MdNAC5T interact with MdERF3. (D) BiFC assays showed that MdNAC5A and MdNAC5T interact with MdERF3 (indicated by the fluorescence observed in the nucleus of protoplasts). The YFP fluorescence coexpressed by MdNAC5A/MdNAC5T and MdERF3Arabidopsis thalianaprotoplasts was detected by confocal laser scanning microscope. From left to right, YFP , chloroplast, bright field, and merged field images. Bars = 10μm. (E) Y2H assays showing that MdNAC5A and MdNAC5T interact with MdERF3. The fusion vectors pGBKT7-MdNAC5A△ 175–364/MdNAC5T△ 175–364 and pGADT7-MdERF3 were co-transformed in Y2H on SD/−Leu/−Trp (−LT) medium. Single coloni

[3] paper | 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple | p.11
Liu et al. | 11 Figure 7.MdNAC5A and MdNAC5T differentially interact with MdERF3 to regulateMdACS1.( A) The structure of MdNAC5A and MdNAC5T.( B)D o c k i n g prediction of MdNAC5A and MdNAC5T on MdERF3. (C) Luciferase complementation imaging assays showed that MdNAC5A and MdNAC5T interact with MdERF3. (D) BiFC assays showed that MdNAC5A and MdNAC5T interact with MdERF3 (indicated by the fluorescence observed in the nucleus of protoplasts). The YFP fluorescence coexpressed by MdNAC5A/MdNAC5T and MdERF3Arabidopsis thalianaprotoplasts was detected by confocal laser scanning microscope. From left to right, YFP , chloroplast, bright field, and merged field images. Bars = 10μm. (E) Y2H assays showing that MdNAC5A and MdNAC5T interact with MdERF3. The fusion vectors pGBKT7-MdNAC5A△ 175–364/MdNAC5T△ 175–364 and pGADT7-MdERF3 were co-transformed in Y2H on SD/−Leu/−Trp (−LT) medium. Single coloni

[4] paper | 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple | p.11
Liu et al. | 11 Figure 7.MdNAC5A and MdNAC5T differentially interact with MdERF3 to regulateMdACS1.( A) The structure of MdNAC5A and MdNAC5T.( B)D o c k i n g prediction of MdNAC5A and MdNAC5T on MdERF3. (C) Luciferase complementation imaging assays showed that MdNAC5A and MdNAC5T interact with MdERF3. (D) BiFC assays showed that MdNAC5A and MdNAC5T interact with MdERF3 (indicated by the fluorescence observed in the nucleus of protoplasts). The YFP fluorescence coexpressed by MdNAC5A/MdNAC5T and MdERF3Arabidopsis thalianaprotoplasts was detected by confocal laser scanning microscope. From left to right, YFP , chloroplast, bright field, and merged field images. Bars = 10μm. (E) Y2H assays showing that MdNAC5A and MdNAC5T interact with MdERF3. The fusion vectors pGBKT7-MdNAC5A△ 175–364/MdNAC5T△ 175–364 and pGADT7-MdERF3 were co-transformed in Y2H on SD/−Leu/−Trp (−LT) medium. Single coloni

[5] paper | 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple | p.11
Liu et al. | 11 Figure 7.MdNAC5A and MdNAC5T differentially interact with MdERF3 to regulateMdACS1.( A) The structure of MdNAC5A and MdNAC5T.( B)D o c k i n g prediction of MdNAC5A and MdNAC5T on MdERF3. (C) Luciferase complementation imaging assays showed that MdNAC5A and MdNAC5T interact with MdERF3. (D) BiFC assays showed that MdNAC5A and MdNAC5T interact with MdERF3 (indicated by the fluorescence observed in the nucleus of protoplasts). The YFP fluorescence coexpressed by MdNAC5A/MdNAC5T and MdERF3Arabidopsis thalianaprotoplasts was detected by confocal laser scanning microscope. From left to right, YFP , chloroplast, bright field, and merged field images. Bars = 10μm. (E) Y2H assays showing that MdNAC5A and MdNAC5T interact with MdERF3. The fusion vectors pGBKT7-MdNAC5A△ 175–364/MdNAC5T△ 175–364 and pGADT7-MdERF3 were co-transformed in Y2H on SD/−Leu/−Trp (−LT) medium. Single coloni

[6] paper | 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple | p.11
Liu et al. | 11 Figure 7.MdNAC5A and MdNAC5T differentially interact with MdERF3 to regulateMdACS1.( A) The structure of MdNAC5A and MdNAC5T.( B)D o c k i n g prediction of MdNAC5A and MdNAC5T on MdERF3. (C) Luciferase complementation imaging assays showed that MdNAC5A and MdNAC5T interact with MdERF3. (D) BiFC assays showed that MdNAC5A and MdNAC5T interact with MdERF3 (indicated by the fluorescence observed in the nucleus of protoplasts). The YFP fluorescence coexpressed by MdNAC5A/MdNAC5T and MdERF3Arabidopsis thalianaprotoplasts was detected by confocal laser scanning microscope. From left to right, YFP , chloroplast, bright field, and merged field images. Bars = 10μm. (E) Y2H assays showing that MdNAC5A and MdNAC5T interact with MdERF3. The fusion vectors pGBKT7-MdNAC5A△ 175–364/MdNAC5T△ 175–364 and pGADT7-MdERF3 were co-transformed in Y2H on SD/−Leu/−Trp (−LT) medium. Single coloni




5. `MdPG`、`MdACS1` 是否在文献中被报告与软化或硬度变化相关？  
回答
根据提供的证据，**无法直接回答** `MdPG` 和 `MdACS1` 是否在文献中被报告与苹果软化或硬度变化相关。

**说明：**
提供的证据（全部为同一篇论文的附图S9）仅表明转录因子 MdNAC18.1 能够直接结合到 `MdPG1` 和 `MdACS1` 基因的启动子上。这暗示 `MdPG1` 和 `MdACS1` 可能是 MdNAC18.1 调控的下游靶基因。然而，证据本身并未报告或讨论这两个基因的功能，特别是它们是否直接参与或导致了苹果果实的软化或硬度变化过程。

要回答该问题，需要提供明确描述 `MdPG`（可能指多聚半乳糖醛酸酶基因）和 `MdACS1`（可能指1-氨基环丙烷-1-羧酸合成酶基因）在苹果果实成熟软化或质地变化中作用的证据。

**引用编号：[1], [2], [3], [4], [5], [6]**

证据
[1] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18 | p.10
Supplementary Figure S9. MdNAC18.1 directly binds to the promoters of MdPG1 and MdACS1 in apples. A) Diagrams of the promoters of MdPG1. Fragment P1 and P2 contain one TTACGT motif, respectively. B) Diagrams of the promoters of MdACS1. Fragment P1 contains one TACGAG motif; fragment P2 contains one TACGTA motif. C-D) Binding of MdNAC18.1 to the MdPG1 and MdACS1 promoter as determined by ChIP–qPCR assay. Positions of fragments used for ChIP–qPCR are listed in A-B). EF1, and No-antibody serve as negative controls. Error bars indicate SD (n = 3). Student’s two-tailed t test is used for statistical analyses, and statistically significant differences are indicated by *** P < 0.001. E-F) Binding of MdNAC18.1 to the promoter of MdPG1 and MdACS1 by electrophoretic mobility shift assay analysis. Mut represents the mutant probe. Binding sites in mutant probe were replaced with AAAAAA.

[2] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18 | p.10
Supplementary Figure S9. MdNAC18.1 directly binds to the promoters of MdPG1 and MdACS1 in apples. A) Diagrams of the promoters of MdPG1. Fragment P1 and P2 contain one TTACGT motif, respectively. B) Diagrams of the promoters of MdACS1. Fragment P1 contains one TACGAG motif; fragment P2 contains one TACGTA motif. C-D) Binding of MdNAC18.1 to the MdPG1 and MdACS1 promoter as determined by ChIP–qPCR assay. Positions of fragments used for ChIP–qPCR are listed in A-B). EF1, and No-antibody serve as negative controls. Error bars indicate SD (n = 3). Student’s two-tailed t test is used for statistical analyses, and statistically significant differences are indicated by *** P < 0.001. E-F) Binding of MdNAC18.1 to the promoter of MdPG1 and MdACS1 by electrophoretic mobility shift assay analysis. Mut represents the mutant probe. Binding sites in mutant probe were replaced with AAAAAA.

[3] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18 | p.10
Supplementary Figure S9. MdNAC18.1 directly binds to the promoters of MdPG1 and MdACS1 in apples. A) Diagrams of the promoters of MdPG1. Fragment P1 and P2 contain one TTACGT motif, respectively. B) Diagrams of the promoters of MdACS1. Fragment P1 contains one TACGAG motif; fragment P2 contains one TACGTA motif. C-D) Binding of MdNAC18.1 to the MdPG1 and MdACS1 promoter as determined by ChIP–qPCR assay. Positions of fragments used for ChIP–qPCR are listed in A-B). EF1, and No-antibody serve as negative controls. Error bars indicate SD (n = 3). Student’s two-tailed t test is used for statistical analyses, and statistically significant differences are indicated by *** P < 0.001. E-F) Binding of MdNAC18.1 to the promoter of MdPG1 and MdACS1 by electrophoretic mobility shift assay analysis. Mut represents the mutant probe. Binding sites in mutant probe were replaced with AAAAAA.

[4] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18 | p.10
Supplementary Figure S9. MdNAC18.1 directly binds to the promoters of MdPG1 and MdACS1 in apples. A) Diagrams of the promoters of MdPG1. Fragment P1 and P2 contain one TTACGT motif, respectively. B) Diagrams of the promoters of MdACS1. Fragment P1 contains one TACGAG motif; fragment P2 contains one TACGTA motif. C-D) Binding of MdNAC18.1 to the MdPG1 and MdACS1 promoter as determined by ChIP–qPCR assay. Positions of fragments used for ChIP–qPCR are listed in A-B). EF1, and No-antibody serve as negative controls. Error bars indicate SD (n = 3). Student’s two-tailed t test is used for statistical analyses, and statistically significant differences are indicated by *** P < 0.001. E-F) Binding of MdNAC18.1 to the promoter of MdPG1 and MdACS1 by electrophoretic mobility shift assay analysis. Mut represents the mutant probe. Binding sites in mutant probe were replaced with AAAAAA.

[5] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18 | p.10
Supplementary Figure S9. MdNAC18.1 directly binds to the promoters of MdPG1 and MdACS1 in apples. A) Diagrams of the promoters of MdPG1. Fragment P1 and P2 contain one TTACGT motif, respectively. B) Diagrams of the promoters of MdACS1. Fragment P1 contains one TACGAG motif; fragment P2 contains one TACGTA motif. C-D) Binding of MdNAC18.1 to the MdPG1 and MdACS1 promoter as determined by ChIP–qPCR assay. Positions of fragments used for ChIP–qPCR are listed in A-B). EF1, and No-antibody serve as negative controls. Error bars indicate SD (n = 3). Student’s two-tailed t test is used for statistical analyses, and statistically significant differences are indicated by *** P < 0.001. E-F) Binding of MdNAC18.1 to the promoter of MdPG1 and MdACS1 by electrophoretic mobility shift assay analysis. Mut represents the mutant probe. Binding sites in mutant probe were replaced with AAAAAA.

[6] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18 | p.10
Supplementary Figure S9. MdNAC18.1 directly binds to the promoters of MdPG1 and MdACS1 in apples. A) Diagrams of the promoters of MdPG1. Fragment P1 and P2 contain one TTACGT motif, respectively. B) Diagrams of the promoters of MdACS1. Fragment P1 contains one TACGAG motif; fragment P2 contains one TACGTA motif. C-D) Binding of MdNAC18.1 to the MdPG1 and MdACS1 promoter as determined by ChIP–qPCR assay. Positions of fragments used for ChIP–qPCR are listed in A-B). EF1, and No-antibody serve as negative controls. Error bars indicate SD (n = 3). Student’s two-tailed t test is used for statistical analyses, and statistically significant differences are indicated by *** P < 0.001. E-F) Binding of MdNAC18.1 to the promoter of MdPG1 and MdACS1 by electrophoretic mobility shift assay analysis. Mut represents the mutant probe. Binding sites in mutant probe were replaced with AAAAAA.

6. `SNP-2,002` 和 `SNP-1,545` 与哪些性状有关？在哪些品种中出现？  
回答
根据提供的证据，无法回答您的问题。

证据中提到了 `SNP-2,002` 和 `SNP-1,545` 这两个标记，但仅限于它们在引物序列列表（证据[4]、[5]）和KASP基因分型数据表（证据[6]）中被提及。证据[6]显示在“华红”品种中对这两个SNP进行了基因分型。

然而，所有证据均未说明这两个SNP标记与任何具体的苹果性状（如果实品质、抗病性等）有关联。证据[1]、[2]、[3]虽然讨论了SNP标记和遗传图谱构建，并涉及抗病性（炭疽叶枯病、褐斑病）和果糖含量等性状，但并未提及 `SNP-2,002` 或 `SNP-1,545` 与这些性状的关联。

因此，关于这两个SNP与哪些性状有关，以及在哪些品种中出现（除“华红”外）的问题，证据不足。

[4][5][6]

证据
[1] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥 | p.30
s 565519 541798 使用Python筛选亲本间相对SNPs标记位点，过滤掉亲本中相对位置缺失的位点后 对亲本基因型进行分型，通过Python脚本将筛选出的遗传标记基因型进行转码，最终 获得共获得SNPs标记共1,865,157个，如表2-4所示，其中“hk× hk”类型标记382316个， “lm× ll”类型标记646400个，“nn× np”类型标记661642个，“cc× ab”类型标记589

[2] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥 | p.7
摘要 II 摘要 正向遗传分析是获得特定性状遗传分子标记、挖掘相关控制基因的有效方法，是 苹果等果树分子辅助育种的基础。苹果的品质、抗旱等性状多为数量性状，由多基因 控制，高质量遗传图谱是进行相关 QTL 区间定位的基础。基于 RAD-Seq 等测序技术 的 SNP 遗传图谱质量与参考基因组质量密切相关。本论文为了获得高质量的‘蜜脆’ ×‘秦冠’ 杂交 群体的 SNP 连锁遗传图谱，基于 组装更完善 的苹果基因组 GDDH13v1.1 为参考基因组对实验室前期基于GDv1.0 的遗传图谱进行了再构建，并比 较了新构建的图谱与基于 GDv1.0 参考基因组构建图谱 的差异。同时对‘蜜脆’× ‘秦冠’杂交群体的抗苹果炭疽叶枯病表型调查，使用卡方分析方法在 GDDH13v1.1 物理图谱上进行苹果抗炭疽叶枯病主效基因的定位。主要研究结果如下： 1. 利用‘蜜脆’×‘秦冠’352 个杂交群体的 RAD-seq 结果，基于苹果参考基因 组GDDH13v1.1 构建出杂交群体父母本高密度连锁遗传图谱，父本上图SNP 标记4816 个，总遗传距离1264.32 cM，母本上图标记5592 个，总遗传距离1358.73 cM，整合图 谱SNP 标记8955 个，总遗传距离1823.8 cM，连锁群平均遗传距离在0.17 cM-0.25 cM 之间。 2. 与 GDv1.0 参考基因组构建的遗传图谱相比，基于 GDDH13v1.1 参考基因组构 建的新遗传图谱SNP 标记连锁群分群和物理图谱的一致性更高，显著降低了SNP 遗传 标记所在连锁群与物理图谱不一致问题，总遗传距离缩短，连锁群标记密度增加，基 于 GDDH13v1.1 的 SNP 遗传图谱父母本标记密度分别为 0.28 cM 和 0.25 cM，高于基 于 GDv1.0 的遗传图谱的父母本的 0.35 cM 和 0.37 cM。 3. 分别使用基于 GDv1.0 参考基因组构建的遗传图谱和基于 GDDH13v1.1 新构建 的遗传图谱对子代果实果糖含量进行了QTL 定位分析，结果表明基于GDDH13v1.1 的 遗传图谱定位出更

[3] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋 | p.50
西北农林科技大学硕士学位论文 38 3.3.2‘长富2号’苹果遗传连锁图谱的构建 ‘长富 2号’苹果遗传连锁图谱由 17个连锁群组成，包含 1,082个 SNP标记，覆盖 1,114.2cM的遗传距离。在‘长富 2号’图谱中，每个连锁群包含的 SNP标记数目为：26 （LG6） ~117（LG11）。除去共分离 SNP标记，‘长富 2号’图谱共包含672个 SNP标 记，相邻标记平均距离为 1.66cM。另外，在‘长富 2号’图谱的 LG2、6、10和 17上发 现了＞10cM的相邻标记间隔。‘长富2号’遗传连锁图谱及相关信息如表 3-4和图 3-8。 表 3-4.‘长富 2号’苹果连锁图谱相关信息 Table3-4.Informationof‘NagafuNo.2’linkagemap 连锁群 LG 长度 Length(cM) 标记数目 Marker numbers 位点数目 Locus numbers 平均间隔 Averagegap (cM) 最大间隔 Largestgap (cM) LG1 63.2 65 44 1.44 7.0 LG2 74.0 72 42 1.76 15.2 LG3 63.1 73 44 1.43 8.0 LG4 57.9 68 38 1.52 5.2 LG5 58.9 67 40 1.47 7.0 LG6 50.5 26 18 2.81 10.9 LG7 71.1 56 35 2.03 6.1 LG8 68.6 75 50 1.37 5.2 LG9 68.2 55 40 1.71 6.1 LG10 38.5 32 22 1.75 15.2 LG11 69.1 117 60 1.15 4.3 LG12 60.5 64 36 1.68 5.2 LG13 58.5 41 30 1.95 9.0 LG14 78.5 70 48 1.64 8.0 LG15 93.3 91 54 1.73 9.0 LG16 77.5 51 33 2.35 7.1 LG17 62.8 59 38 1.65 10.0 共计 Total 1114.2 1082 672 1.6

[4] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S7; row_index: 31; row_text: Supplementary Table S7. List of primer sequences used in this study.: SNP-1,545 F2

[5] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S7; row_index: 28; row_text: Supplementary Table S7. List of primer sequences used in this study.: SNP-2,002 F2

[6] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 100; row_text: Supplementary Table S5. KASP genotyping in SNP-2,002: Hua Hong; col_2: 1; col_3: C; col_4: 1203.9000000000001; col_5: 326.7; col_6: FAM; col_7: 1; Supplementary Table S5. KASP genotyping in SNP-1,545: Hua Hong; col_11: 1; col_12: A; col_13: 1301.2; col_14: 362; col_15: FAM; col_16: 1


7. 哪些研究使用 KASP 标记评估苹果硬度或脆度？  
   根据提供的证据，没有直接提及使用KASP标记评估苹果硬度或脆度的具体研究。证据[1]主要讨论了遗传图谱的构建及其在苹果果实品质（如果肉硬度）QTL定位中的应用，但未说明这些研究是否使用了KASP标记技术。

引用编号：[1]

证据
[1] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥 | p.14
提高。遗传图谱广泛用于 动植物遗传性状的遗传定位，高密度连锁图谱的应用极大地促进了功能基因的发现， 通过QTL定位方法已经定位到多个果实品质、抗性等相关的QTL位点。如2015年Kujur 等人分别将3625和2177个SNP整合到八个desi和kabuli的染色体中构建特异性鹰嘴豆内 遗传连锁图（Kujur et al. 2015），童春发等人使用Populus deltoides和Populus simonii进 行杂交构建F1代杂交群体并使用限制性位点相关 DNA测序数据构，共开发出 4018个 Populus deltoides的SNP标记以及2097个Populus simonii的SNP标记并成功构建了两个亲 本特异性遗传连锁图谱，并将该遗传连锁图谱应用于QTL定位和基因组组装，改善了 689个P. simonii重叠群与染色体的锚定（Tong et al. 2020）。遗传图谱是进行苹果果实 品质、产量等相关农艺性状QTL遗传定位的基础，利用不同杂交群体和特异性遗传图 谱已经实现了对苹果果肉硬度、多酚类物质含量、火疫病的相关抗性基因以及果实糖 含量的QTL定位（Chagné et al. 2012; Peng et al. 2020; Kostick et al. 2021; Wu et al. 2021; Wang et al. 2022 ），构建更高质量的特异性遗传连锁图谱对苹果相关性状遗传学机理 深入研究具有重要意义。 1.1.1 拟测交和F1构图群体 苹果复杂的遗传背景和自交不亲和性，使得获得纯合的苹果研究材料十分困难，
   
8. 哪些文献提供了“硬度相关 SNP 明细表”（不是方法描述）？  
   回答
根据提供的证据，有两篇文献的补充材料中包含了硬度相关的SNP明细表：

1.  **文献[1]** 的补充文件4（Table S4）中提供了一个表格，标题为“Genotyping of different varities”，其中列出了多个SNP位点（如SNP_24399345、SNP_8667563、SNP_15566229）以及感官评价和脆度评分等数据，与硬度性状相关。这是一个包含具体SNP名称和基因型数据的明细表。[1]

2.  **文献[2]** 的补充表S5（Supplementary Table S5）中提供了“KASP genotyping”数据，其中包含了具体的SNP位点（如SNP-2,002、SNP-1,545）在不同样本（如Honeycrisp）中的基因型分型结果，该表也与硬度性状相关。[2]

**引用编号：[1], [2]**

证据
[1] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/039_development_and_application_of_key_allel_004_Supplementary file4.xlsx; sheet: Sheet1; row_index: 1; row_text: Table S4 Genotyping of different varities: Name; col_2: SNP_24399345; col_3: SNP_8667563; col_4: SNP_15566229; col_5: Sensory evaluation; col_6: Crispness score; col_7: Marker combination; trait_guess: firmness_like; record_type: data

[2] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_004_koaf007_supplementary_data.zip::Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 277; row_text: Supplementary Table S5. KASP genotyping in SNP-2,002: Honeycrisp; col_2: A10; col_3: C; col_4: 1114.7; col_5: 151.4; col_6: FAM; col_7: 1; Supplementary Table S5. KASP genotyping in SNP-1,545: Honeycrisp; col_11: A10; col_12: A; col_13: 1067; col_14: 266.2; col_15: FAM; col_16: 1; trait_guess: firmness_like; record_type: data

9.  关于果实成熟期（harvest date），有哪些候选基因或位点？  
回答
根据提供的证据，关于苹果果实成熟期（harvest date）的候选基因或位点信息如下：

**候选基因：**
- **MD03G1222600**：该基因编码一个NAC结构域蛋白（NAC domain containing protein 2）。证据[4]和[5]指出，该基因在苹果成熟的全基因组关联分析（GWAS）中被鉴定到，其两个位点（Chr03:30696840 和 Chr03:30696690）发生了外显子非同义突变，与成熟期显著相关。

**相关位点：**
1. **Chr03:30696840**（证据[4]）
2. **Chr03:30696690**（证据[5]）

这两个位点均位于基因MD03G1222600上，且GWAS分析显示它们与苹果成熟期显著关联（P值分别为1.19E-5和2.78E-5）。

**注意：** 其他证据（[1]、[2]、[3]、[6]）未提供与果实成熟期直接相关的基因或位点信息。

引用编号：[4], [5]

证据
[1] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥 | p.45
脆’具有苹果炭疽叶枯病抗病性，连续两年的调查结果表 明子代抗病植株167株，感病植株160株，抗病和感病比例为167:160，具体子代表型分 布见附表1。 2

[2] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋 | p.30
性 5min，变性完成后放在冰盒中防止复性，等待上样。3）电泳。预电泳完成后，停止电 泳仪运行。用注射器吸取缓冲液吹洗点样槽中的气泡和尿素结晶。梳齿朝内将梳子插入 点样槽，齿尖插入胶面并留有空间点样即可。从左到右依次迅速上样，每孔加入 9μL 变性产物。上样完成后设置电泳仪以 2000V65W恒功率运行约 1h45min。 （3）固定 电泳结束后，关闭电泳仪，回收上样缓冲液槽中的缓冲液，卸下玻璃板，取出梳子 和密封条，小心撬开短板。将粘附着聚丙烯酰胺凝胶的长板处理面朝上放入盛有 2L10% 冰醋酸的塑料方盆中，然后放置在摇床上，缓慢震荡 20min左右。完成后回收固定液。 （4）染色 将长板取出处理面朝上放入盛有蒸馏水的塑料方盆中，轻轻摇晃 2~3min，至胶面 光洁即可。然后放入盛有 1.5L1g/L硝酸银溶液和 3mL甲醛溶液的塑料方盆中，在摇 床上震荡 30min。 （5）显影 取出预冷的2L29g/L的碳酸钠溶液，加入 400μL0.1g/mL的硫代硫酸钠溶液和 3 mL甲醛溶液配成显影液，平均倒入 2个塑料方盆中。将玻璃板取出放入盛有超纯水的 塑料方盆中，迅速摇晃 3次，洗去胶面上浮游的银离子。然后放入第一个盛有显影液的

[3] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥 | p.24
面包含的是每条 Reads的比对信息，以制 表符分割开来成多列排列，如图2-2所示。

[4] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_004_koaf007_supplementary_data.zip::Supplemental Table 1-7.xlsx; sheet: Supplementary Table S1; row_index: 59; row_text: Supplementary Table S1. Genome-wide association analysis of apple ripening.: exonic 非同义突变; col_2: gene:MD03G1222600; col_3: Chr03; col_4: 30696840; col_5: 1.1914606479999999E-5; col_6: G; col_7: T; col_8: hom; col_9: MD03G1222600='NAC domain containing protein 2',AT3G15510.1='NAC domain containing protein 2 (NAC2); FUNCTIONS IN: sequence-specific DNA binding transcription factor activity; INVOLVED IN: multicellular organismal development, regulation of transcription; LOCATED IN: cellular_component unknown; EXPRESSED IN: 13 plant structures; EXPRESSED DURING: LP.06 six leaves visible, LP.04 four leaves visible, 4 anthesis, petal differentiation and expansion stage; CONTAINS InterPro DOMAIN/s: No apical meristem (NAM) protein (InterPro:IPR003441); BEST Arabidopsis thaliana protein match is: NAC (No Apical Meristem) domain transcriptional regulator superfamily protein (TAIR:AT1G52880.1); Has 3051 Blast hits to 3043 proteins in 76 species: Archae - 0; Bacteria - 0; Metazoa - 0; Fungi - 2; Plants - 3049; Viruses - 0; Other Eukaryotes - 0 (source: NCBI BLink).'

[5] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_004_koaf007_supplementary_data.zip::Supplemental Table 1-7.xlsx; sheet: Supplementary Table S1; row_index: 58; row_text: Supplementary Table S1. Genome-wide association analysis of apple ripening.: exonic 非同义突变; col_2: gene:MD03G1222600; col_3: Chr03; col_4: 30696690; col_5: 2.7762084789999999E-5; col_6: A; col_7: T; col_8: hom; col_9: MD03G1222600='NAC domain containing protein 2',AT3G15510.1='NAC domain containing protein 2 (NAC2); FUNCTIONS IN: sequence-specific DNA binding transcription factor activity; INVOLVED IN: multicellular organismal development, regulation of transcription; LOCATED IN: cellular_component unknown; EXPRESSED IN: 13 plant structures; EXPRESSED DURING: LP.06 six leaves visible, LP.04 four leaves visible, 4 anthesis, petal differentiation and expansion stage; CONTAINS InterPro DOMAIN/s: No apical meristem (NAM) protein (InterPro:IPR003441); BEST Arabidopsis thaliana protein match is: NAC (No Apical Meristem) domain transcriptional regulator superfamily protein (TAIR:AT1G52880.1); Has 3051 Blast hits to 3043 proteins in 76 species: Archae - 0; Bacteria - 0; Metazoa - 0; Fungi - 2; Plants - 3049; Viruses - 0; Other Eukaryotes - 0 (source: NCBI BLink).'

[6] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 202; row_text: Supplementary Table S5. KASP genotyping in SNP-2,002: Xiao Jin Hai Tang; col_2: 29; col_3: C; col_4: 1237.5999999999999; col_5: 248.3; col_6: FAM; col_7: 1; Supplementary Table S5. KASP genotyping in SNP-1,545: Xiao Jin Hai Tang; col_11: 29; col_12: A; col_13: 1270.9000000000001; col_14: 301.10000000000002; col_15: FAM; col_16: 0.99890000000000001




10. 苹果酸度（acidity）相关的核心基因有哪些？  
    回答
根据提供的证据，无法回答关于苹果酸度（acidity）相关核心基因的问题。

提供的证据中：
- 证据[1]、[2]、[3]来自一篇关于苹果褐斑病抗性基因定位的论文，内容涉及致谢和实验方法，与酸度基因无关。
- 证据[4]、[5]、[6]来自一个基因表达数据表格，其中列出了多个基因及其描述（如甲基酯酶1、内切-1,4-β-葡聚糖酶前体、蛋白磷酸酶2C等），但这些描述并未明确提及与苹果酸度直接相关，也未提供上下文说明这些基因是调控苹果酸度的核心基因。

因此，证据不足，无法确定苹果酸度的核心基因。

引用编号：[1], [2], [3], [4], [5], [6]

证据
[1] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋 | p.81
们在学习、科研以及生活中的关心、体谅和帮助！感谢李瑞师姐和王正阳师兄在 QTL分析上的帮助。感谢宋艳艳师姐在褐斑病接种上的帮助。感谢郭甜丽师姐和团队其 他师兄师姐在平时试验中的照顾和帮助。感谢杨宇森、谢晨、张国锋、雷超、赵彤、张 志军等这些我的兄弟朋友们，在生活和科研上给我的支持。感谢本科生苏根、王鹏、贺 利宏、黄帅康、杨超等在试验中提供的帮助。 感谢我的家人，感谢他们的支持，家永远是最温暖的港湾。 最后，尤其感谢韩容同学陪伴我度过这段酸甜苦乐的硕士生活，在这里与你相遇是 我三年间最大的幸福。在我遇到挫折时帮助我振作，在我取得收获时一起开心快乐。你 的支持是我完成硕士科研生活和勇敢面对未来的最大动力。 再次感谢所有关心和帮助过我的人! 刘博洋 2020年 5月

[2] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋 | p.81
致谢 69 致谢 时光匆匆，转眼间三年的硕士研究生生活即将结束，感慨良多。在这段短暂的时间 里，在许多人的帮助下，我收获了进步和成长。在迈出人生的下一步之前，谨向所有帮 助和关心过我的老师、同学和家人致以最诚挚的谢意。 首先，感谢我的导师李翠英副教授。您渊博的学术知识、丰富的实践经验、严谨的 治学态度和兢兢业业的科研精神深刻地影响和改变了我，为我以后的学习和工作树立了 标杆。在此毕业之际，谨向李老师表达我最真挚的感谢之情。其次，要感谢联合指导教 师梁微博士。本文是在李老师和梁老师的精心指导下完成的，从整个论文的选题、试验 设计与开展，再到论文撰写方面都倾注了两位老师大量的心血和精力。 感谢苹果逆境生物学团队带头人马锋旺教授为试验开展提供了便利的平台。感谢李 明军教授在试验思路和学习生活上的热心帮助。感谢邹养军教授在苹果品种采集方面的 帮助。感谢刘晶莹副教授、王南南老师在科研方法上给予的帮助。感谢管清美教授、李 鹏民教授、龚小庆副教授、李超副教授、徐记迪副教授、刘长海副教授、毛柯博士、马 百全博士等在试验技术上的支持和帮助。感谢符轩畅老师和马正伟师傅在试验材料嫁接 管理上的帮助。感谢意大利博洛尼亚大学 StefanoTartarini教授在苹果 20KSNPIllumina Infinium®芯片基因分型数据分析、遗传连锁图谱的构建、GSA分析和褐斑病接种试验等 方面的帮助和指导。感谢植保学院孙广宇教授和冯浩老师在褐斑病试验部分的帮助。感 谢园艺技术研究中心实验师张静老师、张飞老师、袁阳阳老师等的帮助。感谢实验室的 兄弟姐妹们。感谢王磊师兄、董丽娟师姐、朱丽芳师姐、刘轩师姐、王京师姐，同门李 宇星、焦学艺，师弟王洪涛，师妹刘晨露、张秀志、彭彧骁、李云浩、谢元梅、刘禹彤， 感谢你们在学习、科研以及生活中的关心、体谅和帮助！感谢李瑞师姐和王正阳师兄在 QTL分析上的帮助。感谢宋艳艳师姐在褐斑病接种上的帮助。感谢郭甜丽师姐和团队其 他师兄师姐在平时试验中的照顾和帮助。感谢杨宇森、谢晨、张国锋、雷超、赵彤、张 志军等这些我的兄弟朋友们，在生活和科研上给我的支持。感谢本科生苏根、王

[3] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋 | p.42
板置于加热模块上，在 95℃下使样品变性 20min；再在室温下冷却 30min。；80g离心后拆下箔封。 2）取出微珠芯片装入 Hyb杂交盒插件（图 3-3A）。

[4] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S4; row_index: 255; row_text: Supplementary Table S4. Significantly differentially expressed genes (DEGs) identified from RNA-Seq data for up-regulated during ripening.: Solyc02g065240.3; col_2: 11294.928480279699; col_3: 519.44512001087105; col_4: 21.754217631414001; col_5: 4.4432232276207504; col_6: 1.23927751928679E-65; col_7: 2.0496696878604102E-62; col_8: 1; col_9: Methyl esterase 1 (AHRD V3.3 *** A0A2U1LMY0_ARTAN); Supplementary Table S4. Significantly differentially expressed genes (DEGs) identified from RNA-Seq data for down-regulated during ripening.: Solyc06g007240.4; col_18: 10.4323761043579; col_19: 61.722054579361597; col_20: 0.16706354008429; col_21: -2.5815311806320902; col_22: 3.2211968685412899E-6; col_23: 5.0370148269459001E-5; col_24: 1; col_25: BAG family molecular chaperone regulator 2-like (AHRD V3.3 *** A0A2I4GUW4_9ROSI)

[5] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S4; row_index: 180; row_text: Supplementary Table S4. Significantly differentially expressed genes (DEGs) identified from RNA-Seq data for up-regulated during ripening.: Solyc09g010210.3; col_2: 7372.1240639888201; col_3: 1558.8735006816601; col_4: 4.7299289425870601; col_5: 2.2418185102142898; col_6: 1.1051225681991E-13; col_7: 6.4393605254332601E-12; col_8: 1; col_9: endo-1,4-beta-glucanase precursor (Cel2); Supplementary Table S4. Significantly differentially expressed genes (DEGs) identified from RNA-Seq data for down-regulated during ripening.: Solyc05g026240.3; col_18: 34.106826346462199; col_19: 266.70134858744899; col_20: 0.12816692398934301; col_21: -2.96390410089781; col_22: 1.58194674497773E-27; col_23: 3.17882588446412E-25; col_24: 1; col_25: Leucine-rich repeat receptor-like protein kinase family (AHRD V3.3 *** A0A0K9Q1P6_ZOSMR)

[6] gene
source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S4; row_index: 13; row_text: Supplementary Table S4. Significantly differentially expressed genes (DEGs) identified from RNA-Seq data for up-regulated during ripening.: Solyc03g007230.4; col_2: 1128.50661499393; col_3: 534.58711992077701; col_4: 2.1115859848751799; col_5: 1.0783269956247901; col_6: 6.9546233295191601E-13; col_7: 3.6031652098311199E-11; col_8: 1; col_9: Protein phosphatase 2C (AHRD V3.3 *** A0A2U1KYU0_ARTAN); Supplementary Table S4. Significantly differentially expressed genes (DEGs) identified from RNA-Seq data for down-regulated during ripening.: Solyc07g065540.1; col_18: 0; col_19: 16.705246535441699; col_20: 1.1570552613258501E-2; col_21: -6.4333984201116303; col_22: 4.5550101276940397E-6; col_23: 6.9115929961573505E-5; col_24: 1; col_25: Fasciclin-like arabinogalactan protein (AHRD V3.3 *** A0A2R6P548_ACTCH)



11. 苹果糖度/可溶性固形物相关位点和基因有哪些？  
12. 苹果果皮颜色（skin color）相关位点主要在哪些染色体区域？  
13. 哪些证据明确区分了“病害抗性位点”和“果实品质位点”？  
14. 现有证据里是否有“只给表头、没有具体数据行”的情况？请指出。  
15. 哪些论文的补充数据可直接用于位点级检索（SNP/Indel/QTL）？  
16. 关于 `MdERF3` / `MdERF118`，有哪些与硬度保持相关的证据？  
17. 同一位点是否在多篇研究中重复出现？请给出处。  
18. 对“硬度相关基因”这个问题，当前证据是否足够支持因果结论？  
19. 当前数据库中，哪些回答是“证据不足/未检索到相关材料”，原因是什么？  
20. 请给出“硬度、成熟、酸度、糖度、颜色”五类性状的候选基因速览（含引用）。

## 自动评测 Round 2（2026-03-08 15:55:03）

说明：由后端 /api/chat 自动执行 20 题，参数 route=auto, top_k=6。

### 1. 哪些基因或位点与苹果果肉硬度（firmness）保持相关？请列证据。
- route_used: `hybrid`
- evidence_count: `2`
回答
根据提供的证据，与苹果果肉硬度（firmness）保持相关的基因如下：

**Level A (直接证据)**
证据明确指出，在果实采收时果肉硬度的数量性状位点（QTL）区域内，存在两个差异表达基因（DEGs）与硬度相关：
1. 基因 **MD16G1117200**。证据[1]将其列为该QTL区域内的差异表达基因。
2. 基因 **MD16G1096900**。证据[2]同样将其列为该QTL区域内的差异表达基因。

**Level B (间接证据)**
提供的证据中没有提供关于这些基因具体功能、作用机制或与其他已知硬度相关通路关联的间接支持信息。

引用编号：[1], [2]
证据摘要
- [1] gene | 5 | score=0.11818541
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/016_allelic_variation_in_an_expansin_mdexp_001_43897_2024_121_MOESM2_ESM.xls; sheet: TableS6; row_index: 90; trait: firmness; gene: MD16G1117200; pvalue: ...
- [2] gene | 4 | score=0.11569281
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/016_allelic_variation_in_an_expansin_mdexp_001_43897_2024_121_MOESM2_ESM.xls; sheet: TableS6; row_index: 69; trait: firmness; gene: MD16G1096900; pvalue: ...

### 2. 与苹果脆度（crispness）相关的 SNP 或 marker 有哪些？
- route_used: `hybrid`
- evidence_count: `3`
回答
根据提供的证据，与苹果脆度相关的SNP或分子标记信息如下。

**Level A (直接证据)**
证据[1]明确指出，研究开发了用于评估苹果果实脆度的KASP分子标记，其中包含三个关键的SNP标记：SNP_24399345（与机械特性相关）、SNP_8667563（与含水量相关）和SNP_15566229（与细胞面积相关）。这些标记的组合基因型可用于区分苹果的质地，例如CC-CC-TT基因型代表软苹果，而GG-CC/TC-TT基因型代表质地更坚实的苹果。

**Level B (间接证据)**
证据[2]和[3]列出了在果实硬度QTL区域内差异表达的基因（MD16G1117200和MD16G1096900），这些基因可能与硬度（脆度相关性状）有关。然而，这些证据本身并未直接指明具体的SNP或分子标记，而是提供了可能与脆度相关的候选基因信息。

引用编号：[1], [2], [3]
证据摘要
- [1] paper | 039_development_and_application_of_key_allel_001_Development and application of Key Allele-Specific PCR (KASP) molecular markers for assessing apple fruit crispness.pdf | p.16 | score=0.5502099
  title: 039_development_and_application_of_key_allel_001_Development and application of Key Allele-Specific PCR (KASP) molecular markers for assessing apple fruit crispness
  snippet: a large number of unknown genes and various regulatory genes suggests that the key SNPs may be associated with crispness through more complex biological processes (Table S6). In general, the KASP markers developed in this study integrate as...
- [2] gene | 5 | score=0.31079775
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/016_allelic_variation_in_an_expansin_mdexp_001_43897_2024_121_MOESM2_ESM.xls; sheet: TableS6; row_index: 90; trait: firmness; gene: MD16G1117200; pvalue: ...
- [3] gene | 4 | score=0.31062874
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/016_allelic_variation_in_an_expansin_mdexp_001_43897_2024_121_MOESM2_ESM.xls; sheet: TableS6; row_index: 69; trait: firmness; gene: MD16G1096900; pvalue: ...

### 3. MdNAC18.1 与成熟/硬度性状的关联证据有哪些？
- route_used: `papers`
- evidence_count: `0`
回答
未检索到相关材料。
证据摘要
- 无
### 4. MdNAC5 对果实硬度或成熟差异的作用有什么证据？
- route_used: `papers`
- evidence_count: `4`
回答
根据提供的证据，关于MdNAC5对果实硬度或成熟差异的作用，证据不足。

**Level A (直接证据)**
提供的证据中没有直接说明MdNAC5如何影响果实硬度或成熟差异的实验结果或结论。所有证据片段均来自同一篇论文的同一页（图7），且内容完全重复，仅描述了MdNAC5的不同等位基因（MdNAC5A和MdNAC5T）与MdERF3蛋白的相互作用差异，并提及这种差异调控`MdACS1`。然而，证据片段并未展示或陈述这些分子相互作用与果实硬度或成熟表型之间的直接关联。

**Level B (间接证据)**
证据[1]-[4]提供了间接的分子机制线索。这些证据表明，MdNAC5的自然变异（等位基因MdNAC5A和MdNAC5T）导致其与转录因子MdERF3的相互作用存在差异，并可能由此调控乙烯合成关键基因`MdACS1`。由于乙烯是调控果实成熟和软化的核心激素，因此可以间接推断MdNAC5可能通过此途径影响果实成熟过程和硬度。但证据本身并未提供任何关于果实硬度测量、成熟时间差异等表型数据来证实这一推断。

引用编号：[1], [2], [3], [4]
证据摘要
- [1] paper | 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple.pdf | p.11 | score=0.5254243
  title: 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple
  snippet: Liu et al. | 11 Figure 7.MdNAC5A and MdNAC5T differentially interact with MdERF3 to regulateMdACS1.( A) The structure of MdNAC5A and MdNAC5T.( B)D o c k i n g prediction of MdNAC5A and MdNAC5T on MdERF3. (C) Luciferase complementation imagi...
- [2] paper | 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple.pdf | p.11 | score=0.5254243
  title: 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple
  snippet: Liu et al. | 11 Figure 7.MdNAC5A and MdNAC5T differentially interact with MdERF3 to regulateMdACS1.( A) The structure of MdNAC5A and MdNAC5T.( B)D o c k i n g prediction of MdNAC5A and MdNAC5T on MdERF3. (C) Luciferase complementation imagi...
- [3] paper | 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple.pdf | p.11 | score=0.5254243
  title: 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple
  snippet: Liu et al. | 11 Figure 7.MdNAC5A and MdNAC5T differentially interact with MdERF3 to regulateMdACS1.( A) The structure of MdNAC5A and MdNAC5T.( B)D o c k i n g prediction of MdNAC5A and MdNAC5T on MdERF3. (C) Luciferase complementation imagi...
- [4] paper | 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple.pdf | p.11 | score=0.5254243
  title: 013_natural_variation_in_mdnac5_contributes__001_Natural variation in MdNAC5 contributes to fruit firmness and ripening divergence in apple
  snippet: Liu et al. | 11 Figure 7.MdNAC5A and MdNAC5T differentially interact with MdERF3 to regulateMdACS1.( A) The structure of MdNAC5A and MdNAC5T.( B)D o c k i n g prediction of MdNAC5A and MdNAC5T on MdERF3. (C) Luciferase complementation imagi...

### 5. MdPG、MdACS1 是否在文献中被报告与软化或硬度变化相关？
- route_used: `papers`
- evidence_count: `2`
回答
根据提供的证据，无法直接回答MdPG和MdACS1是否在文献中被报告与软化或硬度变化相关。

**Level A (直接证据)**
提供的证据中没有直接报告MdPG或MdACS1与苹果软化或硬度变化相关的陈述。证据[1]和[2]均只描述了MdNAC18.1转录因子与MdPG1和MdACS1基因启动子的结合情况，并未提及这些基因本身的功能或其与果实硬度变化的关系。

**Level B (间接证据)**
证据[1]和[2]表明MdPG1和MdACS1是转录因子MdNAC18.1的靶基因。在植物生物学中，PG（多聚半乳糖醛酸酶）和ACS（ACC合酶）分别是细胞壁降解和乙烯生物合成的关键酶，通常与果实成熟软化过程相关。然而，此间接关联并非基于当前提供的证据，证据本身并未讨论这些基因的功能或表型。

引用编号：[1], [2]
证据摘要
- [1] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18.pdf | p.10 | score=0.48130777
  title: 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18
  snippet: Supplementary Figure S9. MdNAC18.1 directly binds to the promoters of MdPG1 and MdACS1 in apples. A) Diagrams of the promoters of MdPG1. Fragment P1 and P2 contain one TTACGT motif, respectively. B) Diagrams of the promoters of MdACS1. Frag...
- [2] paper | 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18.pdf | p.10 | score=0.48130777
  title: 001_an_indel_variant_in_the_promoter_002_Supplementary Figures 1-18
  snippet: Supplementary Figure S9. MdNAC18.1 directly binds to the promoters of MdPG1 and MdACS1 in apples. A) Diagrams of the promoters of MdPG1. Fragment P1 and P2 contain one TTACGT motif, respectively. B) Diagrams of the promoters of MdACS1. Frag...

### 6. SNP-2,002 和 SNP-1,545 与哪些性状有关？在哪些品种中出现？
- route_used: `hybrid`
- evidence_count: `6`
回答
根据提供的证据，无法回答SNP-2,002和SNP-1,545与哪些性状有关，也无法确定它们在哪些品种中出现。

**Level A (直接证据)**
提供的证据中没有直接说明SNP-2,002和SNP-1,545与任何具体性状（如果实品质、抗病性等）的关联。

**Level B (间接证据)**
证据[4]、[5]、[6]来自一份KASP基因分型数据表（Supplementary Table S5），其中提到了SNP-2,002和SNP-1,545在“Hua Hong”、“Fujiko”和“Chui Si Hai Tang”等品种中的基因型数据。然而，这些证据仅记录了这些品种在特定SNP位点的等位基因和检测信号值，并未说明这些SNP与何种性状相关。其他证据[1]、[2]、[3]讨论了遗传图谱构建和QTL定位的一般方法，但均未提及SNP-2,002或SNP-1,545。

引用编号：[1], [2], [3], [4], [5], [6]
证据摘要
- [1] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.30 | score=0.668153
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: s 565519 541798 使用Python筛选亲本间相对SNPs标记位点，过滤掉亲本中相对位置缺失的位点后 对亲本基因型进行分型，通过Python脚本将筛选出的遗传标记基因型进行转码，最终 获得共获得SNPs标记共1,865,157个，如表2-4所示，其中“hk× hk”类型标记382316个， “lm× ll”类型标记646400个，“nn× np”类型标记661642个，“cc× ab”类型标记589
- [2] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.7 | score=0.666116
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 摘要 II 摘要 正向遗传分析是获得特定性状遗传分子标记、挖掘相关控制基因的有效方法，是 苹果等果树分子辅助育种的基础。苹果的品质、抗旱等性状多为数量性状，由多基因 控制，高质量遗传图谱是进行相关 QTL 区间定位的基础。基于 RAD-Seq 等测序技术 的 SNP 遗传图谱质量与参考基因组质量密切相关。本论文为了获得高质量的‘蜜脆’ ×‘秦冠’ 杂交 群体的 SNP 连锁遗传图谱，基于 组装更完善 的苹果基因组 GDDH13v1.1 为参考基因组对实验室前期基于GDv1.0...
- [3] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.46 | score=0.6093316
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 富二号’遗传连锁图谱。 其中以 lm×ll分离的 SNP标记有 2,924个，nn×np型有 2,823个，ef×eg型有 118个 （表 3-2）。 表 3-2. 作图群体中多态性 SNP的分离类型及标记数目 Table3-2.SegregationtypesandnumbersofpolymorphicSNPmarkersinmappingpopulation 分离类型 Segregationtypes 母本 Female 父本 Male F1代 F1Progeny 分离...
- [4] gene | 6506 | score=0.4072242
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 100; row_text: Supplementary Table S5. KAS...
- [5] gene | 6641 | score=0.3998974
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 235; row_text: Supplementary Table S5. KAS...
- [6] gene | 6588 | score=0.39950597
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 182; row_text: Supplementary Table S5. KAS...

### 7. 哪些研究使用 KASP 标记评估苹果硬度或脆度？
- route_used: `papers`
- evidence_count: `1`
回答
根据提供的证据，无法回答该问题。

**Level A (直接证据)**
没有证据直接提及任何研究使用KASP标记评估苹果硬度或脆度。提供的证据[1]讨论了遗传图谱、QTL定位与苹果果实品质（如果肉硬度）的关联，但未具体说明使用了何种标记技术，特别是没有提及KASP标记。

**Level B (间接证据)**
证据[1]间接表明，已有研究利用遗传图谱和QTL定位方法对苹果果肉硬度等性状进行了遗传定位（例如引用了Chagné et al. 2012; Peng et al. 2020; Kostick et al. 2021; Wu et al. 2021; Wang et al. 2022等研究）。然而，这些引用并未在提供的文本片段中详细描述其使用的标记类型，因此无法确认这些研究是否使用了KASP标记。

引用编号：[1]
证据摘要
- [1] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.14 | score=0.52255005
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 提高。遗传图谱广泛用于 动植物遗传性状的遗传定位，高密度连锁图谱的应用极大地促进了功能基因的发现， 通过QTL定位方法已经定位到多个果实品质、抗性等相关的QTL位点。如2015年Kujur 等人分别将3625和2177个SNP整合到八个desi和kabuli的染色体中构建特异性鹰嘴豆内 遗传连锁图（Kujur et al. 2015），童春发等人使用Populus deltoides和Populus simonii进 行杂交构建F1代杂交群体并使用限制性位点相关 DNA测序数...

### 8. 哪些文献提供了硬度相关 SNP 明细表（不是方法描述）？
- route_used: `hybrid`
- evidence_count: `2`
回答
根据提供的证据，没有文献直接提供硬度相关的SNP明细表。

**Level A (直接证据)**
提供的两份证据均来自同一文献的补充材料，其中列出了与果实硬度QTL区域相关的差异表达基因（DEGs），例如基因MD16G1283000和MD16G1117200。然而，这些证据描述的是基因列表，并未包含任何SNP（单核苷酸多态性）的详细信息，如SNP位点、等位基因或基因型数据。

**Level B (间接证据)**
没有间接证据。

引用编号：[1], [2]
证据摘要
- [1] gene | 7 | score=0.20944585
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/016_allelic_variation_in_an_expansin_mdexp_001_43897_2024_121_MOESM2_ESM.xls; sheet: TableS6; row_index: 110; trait: firmness; gene: MD16G1283000; pos: 10...
- [2] gene | 5 | score=0.20179386
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/016_allelic_variation_in_an_expansin_mdexp_001_43897_2024_121_MOESM2_ESM.xls; sheet: TableS6; row_index: 90; trait: firmness; gene: MD16G1117200; pvalue: ...

### 9. 关于果实成熟期（harvest date），有哪些候选基因或位点？
- route_used: `hybrid`
- evidence_count: `6`
回答
关于苹果果实成熟期（harvest date）的候选基因或位点，根据提供的证据，回答如下：

**Level A (直接证据)**
证据[4]和[5]直接提供了与苹果成熟期全基因组关联分析相关的候选基因信息。这两个证据指向同一个基因 **MD03G1222600**，该基因编码一个NAC结构域蛋白（NAC domain containing protein 2）。证据显示该基因在染色体Chr03上的两个位点（30696840和30696690）发生了非同义突变，并与成熟期性状显著关联（P值分别为1.19E-5和2.78E-5）。因此，**MD03G1222600** 是一个与果实成熟期相关的明确候选基因。

**Level B (间接证据)**
证据[1]、[2]、[3]和[6]均未提供任何与果实成熟期、其候选基因或遗传位点直接相关的信息。证据[1]和[2]分别涉及苹果炭疽叶枯病和褐斑病的抗性研究，证据[3]描述的是测序数据比对的技术细节，证据[6]是某个SNP的KASP基因分型数据，但未说明该SNP与成熟期性状的关联。因此，这些证据无法为果实成熟期的候选基因或位点提供支持。

引用编号：[4], [5]
证据摘要
- [1] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.45 | score=0.5812901
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 脆’具有苹果炭疽叶枯病抗病性，连续两年的调查结果表 明子代抗病植株167株，感病植株160株，抗病和感病比例为167:160，具体子代表型分 布见附表1。 2
- [2] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.30 | score=0.5203428
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 性 5min，变性完成后放在冰盒中防止复性，等待上样。3）电泳。预电泳完成后，停止电 泳仪运行。用注射器吸取缓冲液吹洗点样槽中的气泡和尿素结晶。梳齿朝内将梳子插入 点样槽，齿尖插入胶面并留有空间点样即可。从左到右依次迅速上样，每孔加入 9μL 变性产物。上样完成后设置电泳仪以 2000V65W恒功率运行约 1h45min。 （3）固定 电泳结束后，关闭电泳仪，回收上样缓冲液槽中的缓冲液，卸下玻璃板，取出梳子 和密封条，小心撬开短板。将粘附着聚丙烯酰胺凝胶的长板处理面朝上放入盛...
- [3] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.24 | score=0.5190188
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 面包含的是每条 Reads的比对信息，以制 表符分割开来成多列排列，如图2-2所示。
- [4] gene | 7128 | score=0.1766142
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_004_koaf007_supplementary_data.zip::Supplemental Table 1-7.xlsx; sheet: Supplementary Table S1; row_index: 59; row_te...
- [5] gene | 7127 | score=0.17641753
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_004_koaf007_supplementary_data.zip::Supplemental Table 1-7.xlsx; sheet: Supplementary Table S1; row_index: 58; row_te...
- [6] gene | 6608 | score=0.17606288
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 202; row_text: Supplementary Table S5. KAS...

### 10. 苹果酸度（acidity）相关的核心基因有哪些？
- route_used: `hybrid`
- evidence_count: `6`
回答
根据提供的证据，无法回答关于苹果酸度（acidity）核心基因的问题。

**Level A (直接证据)**
提供的证据中没有任何信息直接涉及苹果酸度的核心基因。证据[4]、[5]、[6]虽然标注为A级，但内容是关于番茄（Solyc基因编号）或其他植物的差异表达基因，与苹果酸度无关。

**Level B (间接证据)**
证据[1]、[2]、[3]均来自一篇关于构建苹果遗传连锁图谱和定位褐斑病抗性基因的论文，其内容为致谢或实验方法描述，完全不涉及苹果酸度或相关基因。

因此，基于当前证据，无法列出任何与苹果酸度相关的核心基因。

引用编号：[1], [2], [3], [4], [5], [6]
证据摘要
- [1] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.81 | score=0.5946704
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 们在学习、科研以及生活中的关心、体谅和帮助！感谢李瑞师姐和王正阳师兄在 QTL分析上的帮助。感谢宋艳艳师姐在褐斑病接种上的帮助。感谢郭甜丽师姐和团队其 他师兄师姐在平时试验中的照顾和帮助。感谢杨宇森、谢晨、张国锋、雷超、赵彤、张 志军等这些我的兄弟朋友们，在生活和科研上给我的支持。感谢本科生苏根、王鹏、贺 利宏、黄帅康、杨超等在试验中提供的帮助。 感谢我的家人，感谢他们的支持，家永远是最温暖的港湾。 最后，尤其感谢韩容同学陪伴我度过这段酸甜苦乐的硕士生活，在这里与你相遇是 我...
- [2] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.81 | score=0.5689846
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 致谢 69 致谢 时光匆匆，转眼间三年的硕士研究生生活即将结束，感慨良多。在这段短暂的时间 里，在许多人的帮助下，我收获了进步和成长。在迈出人生的下一步之前，谨向所有帮 助和关心过我的老师、同学和家人致以最诚挚的谢意。 首先，感谢我的导师李翠英副教授。您渊博的学术知识、丰富的实践经验、严谨的 治学态度和兢兢业业的科研精神深刻地影响和改变了我，为我以后的学习和工作树立了 标杆。在此毕业之际，谨向李老师表达我最真挚的感谢之情。其次，要感谢联合指导教 师梁微博士。本文是在李老师和梁...
- [3] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.42 | score=0.5397752
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 板置于加热模块上，在 95℃下使样品变性 20min；再在室温下冷却 30min。；80g离心后拆下箔封。 2）取出微珠芯片装入 Hyb杂交盒插件（图 3-3A）。
- [4] gene | 5610 | score=0.038817346
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S4; row_index: 255; row_text: Supplementary Table S4. Sig...
- [5] gene | 5535 | score=0.037661623
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S4; row_index: 180; row_text: Supplementary Table S4. Sig...
- [6] gene | 5368 | score=0.037207793
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S4; row_index: 13; row_text: Supplementary Table S4. Sign...

### 11. 苹果糖度/可溶性固形物相关位点和基因有哪些？
- route_used: `hybrid`
- evidence_count: `6`
回答
根据提供的证据，无法回答关于苹果糖度/可溶性固形物相关位点和基因的问题。

**Level A (直接证据):**
提供的证据中没有任何信息直接涉及苹果的糖度或可溶性固形物相关位点和基因。

**Level B (间接证据):**
证据[1]、[2]、[3]讨论的是苹果抗病性（炭疽叶枯病、褐斑病）的遗传图谱构建和基因定位，与糖度性状无关。证据[4]、[5]、[6]来自基因相关文件，但内容仅涉及实验所用的引物序列或基因型检测数据，未提及这些基因或标记与糖度性状的关联。

引用编号：[1], [2], [3], [4], [5], [6]
证据摘要
- [1] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.45 | score=0.6090106
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 脆’具有苹果炭疽叶枯病抗病性，连续两年的调查结果表 明子代抗病植株167株，感病植株160株，抗病和感病比例为167:160，具体子代表型分 布见附表1。 2
- [2] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.17 | score=0.5636117
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 术的普及和新型标记的开发，上万个的标记可以 通过一次测序分析而被开发出来，这当然会使得我们构建遗传图谱的密度增加，但同
- [3] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.11 | score=0.555913
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 与寄主的相互作用研究......................................................................5 1.1.4 苹果褐斑病的防治与抗性育种...............................................................................6 1.2 苹果遗传图谱构建和 QTL定位研究进展......................................
- [4] gene | 7037 | score=0.022273283
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S7; row_index: 69; row_text: Supplementary Table S7. List...
- [5] gene | 7031 | score=0.012508633
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S7; row_index: 63; row_text: Supplementary Table S7. List...
- [6] gene | 6608 | score=0.01577396
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 202; row_text: Supplementary Table S5. KAS...

### 12. 苹果果皮颜色（skin color）相关位点主要在哪些染色体区域？
- route_used: `hybrid`
- evidence_count: `6`
回答
根据提供的证据，无法回答关于苹果果皮颜色相关位点所在染色体区域的问题。

**Level A (直接证据)**
提供的证据中没有直接涉及苹果果皮颜色（skin color）性状的遗传定位或相关位点信息。

**Level B (间接证据)**
证据[1]、[2]、[3]均来自一篇关于苹果褐斑病抗性基因定位的研究论文，其研究内容与果皮颜色无关。证据[4]、[5]、[6]是来自基因分型数据表的片段，仅显示了特定SNP在不同苹果品种中的基因型数据，未提及这些SNP与果皮颜色的关联，也未提供其染色体位置信息。

引用编号：[1], [2], [3], [4], [5], [6]
证据摘要
- [1] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.4 | score=0.5730625
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 本研究得到： 国家自然科学基金青年项目（编号：31601719）和陕西省自然科 学基础研究计划青年项目（编号：2017JQ3034）的资助。
- [2] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.11 | score=0.57124007
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 与寄主的相互作用研究......................................................................5 1.1.4 苹果褐斑病的防治与抗性育种...............................................................................6 1.2 苹果遗传图谱构建和 QTL定位研究进展......................................
- [3] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.13 | score=0.52490616
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 2007；殷 丽华 2013；程守云等 2019）。这种病害会造成苹果树在生长季大量落叶，光合面积大 大降低，从而导致果园的大量减产和果实品质降低。在褐斑病流行的年份，管理较差的 果园落叶率达到80%以上（李保华等 2013）。长期以来，褐斑病主要在东亚和南亚各国 流行，近年来在欧洲和北美的有机果园也开始频繁发生，已经被列入欧洲植物保护组织 （EPPO）的检疫性病害警戒名单中，在世界范围内对苹果产业造成了巨大的损失 (Tamiettietal.2007；Persenetal....
- [4] gene | 6608 | score=0.12925296
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 202; row_text: Supplementary Table S5. KAS...
- [5] gene | 6421 | score=0.12841848
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 15; row_text: Supplementary Table S5. KASP...
- [6] gene | 6480 | score=0.12380929
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 74; row_text: Supplementary Table S5. KASP...

### 13. 哪些证据明确区分了病害抗性位点和果实品质位点？
- route_used: `hybrid`
- evidence_count: `6`
回答
根据提供的证据，没有信息能够明确区分病害抗性位点和果实品质位点。

**Level A (直接证据)**
提供的证据中没有直接描述或比较病害抗性位点与果实品质位点的内容。

**Level B (间接证据)**
证据[1]提到了苹果褐斑病抗性育种和遗传图谱构建，证据[2]提到了苹果炭疽叶枯病抗病性，但这些内容均未涉及果实品质位点，也没有对两类位点进行区分。其他证据[3]、[4]、[5]、[6]涉及技术细节或基因列表，与问题无关。

引用编号：[1], [2], [3], [4], [5], [6]
证据摘要
- [1] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.19 | score=0.59549576
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 010）。Wöhner等（2019）认为目前还不能准确地将症状较轻的基因型归类为抗病基因 型。多项研究表明，‘秦冠’苹果是对褐斑病具有较强抗性（Zhouetal.2012；Sharmaetal. 2012；Lietal.2012；Yinetal.2013a；2013b；Wangetal.2013；Xuetal.2015）。总之， 目前苹果褐斑病抗性育种的难点在于缺乏高抗苹果品种材料，同时对苹果种质资源的褐 斑病抗病评价也缺乏系统研究。 1.2苹果遗传图谱构建和 QTL定位研究...
- [2] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.45 | score=0.58933544
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 脆’具有苹果炭疽叶枯病抗病性，连续两年的调查结果表 明子代抗病植株167株，感病植株160株，抗病和感病比例为167:160，具体子代表型分 布见附表1。 2
- [3] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.24 | score=0.58517253
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 面包含的是每条 Reads的比对信息，以制 表符分割开来成多列排列，如图2-2所示。
- [4] gene | 7037 | score=0.13809659
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S7; row_index: 69; row_text: Supplementary Table S7. List...
- [5] gene | 6694 | score=0.1378977
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S6; row_index: 1; row_text: Supplementary Table S6. 281 h...
- [6] gene | 6608 | score=0.13763139
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 202; row_text: Supplementary Table S5. KAS...

### 14. 现有证据里是否有只给表头、没有具体数据行的情况？请指出。
- route_used: `papers`
- evidence_count: `6`
回答
根据提供的证据，没有直接或间接的证据表明存在“只给表头、没有具体数据行的情况”。

**Level A (直接证据)**
没有证据直接描述或展示表格结构（如表头与数据行的关系），因此无法确认是否存在仅有表头而无数据行的情况。

**Level B (间接证据)**
证据[3]提到“面包含的是每条 Reads的比对信息，以制表符分割开来成多列排列，如图2-2所示”，这暗示了数据是以多列形式排列的，但并未说明这些数据是否包含表头，也未说明是否存在仅有表头而无数据行的情况。其他证据均未涉及表格或数据行的具体描述。

引用编号：[3]
证据摘要
- [1] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.36 | score=0.7357992
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 现出与 1:1理想分离比的显著性差异，但在
- [2] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.17 | score=0.68856275
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 术的普及和新型标记的开发，上万个的标记可以 通过一次测序分析而被开发出来，这当然会使得我们构建遗传图谱的密度增加，但同
- [3] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.24 | score=0.61082673
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 面包含的是每条 Reads的比对信息，以制 表符分割开来成多列排列，如图2-2所示。
- [4] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.64 | score=0.5664984
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 高湿的环
- [5] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.30 | score=0.5447731
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 性 5min，变性完成后放在冰盒中防止复性，等待上样。3）电泳。预电泳完成后，停止电 泳仪运行。用注射器吸取缓冲液吹洗点样槽中的气泡和尿素结晶。梳齿朝内将梳子插入 点样槽，齿尖插入胶面并留有空间点样即可。从左到右依次迅速上样，每孔加入 9μL 变性产物。上样完成后设置电泳仪以 2000V65W恒功率运行约 1h45min。 （3）固定 电泳结束后，关闭电泳仪，回收上样缓冲液槽中的缓冲液，卸下玻璃板，取出梳子 和密封条，小心撬开短板。将粘附着聚丙烯酰胺凝胶的长板处理面朝上放入盛...
- [6] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.42 | score=0.54355454
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 板置于加热模块上，在 95℃下使样品变性 20min；再在室温下冷却 30min。；80g离心后拆下箔封。 2）取出微珠芯片装入 Hyb杂交盒插件（图 3-3A）。

### 15. 哪些论文的补充数据可直接用于位点级检索（SNP/Indel/QTL）？
- route_used: `hybrid`
- evidence_count: `6`
回答
根据提供的证据，无法直接回答哪些论文的补充数据可直接用于位点级检索（SNP/Indel/QTL）。

**Level A (直接证据)**
没有证据直接列出或说明哪些论文的补充数据（如在线表格、数据库条目等）可以直接用于位点级检索（SNP/Indel/QTL）。提供的证据片段主要描述了特定研究中的遗传图谱构建、QTL定位方法和结果，或展示了KASP基因分型数据的具体数值，但均未明确指出其补充数据是否以及如何可供公开检索或下载用于位点级查询。

**Level B (间接证据)**
证据[1]、[2]、[3]来自同一篇论文（杨南祥，关于‘秦冠’和‘蜜脆’遗传图谱再构建及抗病基因定位），其中提到该研究构建了高密度SNP遗传图谱并进行了QTL定位（如果糖含量QTL），暗示该研究可能生成了相关的SNP和QTL数据。证据[4]、[5]、[6]展示了来自某个研究的补充表格（Supplementary Table S5）中的KASP基因分型数据片段，该表格似乎包含了具体的SNP位点（如SNP-2,002, SNP-1,545）及其在不同品种中的基因型数据，这属于位点级（SNP）数据。然而，所有证据均未明确说明这些数据是否作为可公开访问的补充数据发布，也未提供具体的数据库链接或访问方式，因此无法确认其是否“可直接用于”检索。

引用编号：[1], [2], [3], [4], [5], [6]
证据摘要
- [1] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.7 | score=0.66127867
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 摘要 II 摘要 正向遗传分析是获得特定性状遗传分子标记、挖掘相关控制基因的有效方法，是 苹果等果树分子辅助育种的基础。苹果的品质、抗旱等性状多为数量性状，由多基因 控制，高质量遗传图谱是进行相关 QTL 区间定位的基础。基于 RAD-Seq 等测序技术 的 SNP 遗传图谱质量与参考基因组质量密切相关。本论文为了获得高质量的‘蜜脆’ ×‘秦冠’ 杂交 群体的 SNP 连锁遗传图谱，基于 组装更完善 的苹果基因组 GDDH13v1.1 为参考基因组对实验室前期基于GDv1.0...
- [2] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.14 | score=0.59125876
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 提高。遗传图谱广泛用于 动植物遗传性状的遗传定位，高密度连锁图谱的应用极大地促进了功能基因的发现， 通过QTL定位方法已经定位到多个果实品质、抗性等相关的QTL位点。如2015年Kujur 等人分别将3625和2177个SNP整合到八个desi和kabuli的染色体中构建特异性鹰嘴豆内 遗传连锁图（Kujur et al. 2015），童春发等人使用Populus deltoides和Populus simonii进 行杂交构建F1代杂交群体并使用限制性位点相关 DNA测序数...
- [3] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.39 | score=0.56969655
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 度和连锁群标记和物理图谱的一致性是影响遗传图谱 QTL定位精确性和准 确性的重要影响因素，新构建的遗传图谱QCMapv1.1在连锁群标记和物理图谱的一致 性以及标记相对密度上有很大提升，为 验证QCMap1.1在QTL定位实践中是否提高了 定位结果的准确性 ，通过群体2016年成熟期果实的果糖（ Fru）含量数据 分别使用 QCMapv1.1和QCMapv1.0图谱进行进行QTL定位，结果表明通过QCMapv1.1共筛选到 29个LOD值大于3且最大贡献率大于10的果糖相关的...
- [4] gene | 6601 | score=0.42953032
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 195; row_text: Supplementary Table S5. KAS...
- [5] gene | 6469 | score=0.4287116
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 63; row_text: Supplementary Table S5. KASP...
- [6] gene | 6506 | score=0.42691132
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 100; row_text: Supplementary Table S5. KAS...

### 16. 关于 MdERF3 / MdERF118，有哪些与硬度保持相关的证据？
- route_used: `papers`
- evidence_count: `0`
回答
未检索到相关材料。
证据摘要
- 无
### 17. 同一位点是否在多篇研究中重复出现？请给出处。
- route_used: `hybrid`
- evidence_count: `6`
回答
根据提供的证据，无法回答“同一位点是否在多篇研究中重复出现”的问题。

**Level A (直接证据):**
提供的证据中没有直接说明或比较不同研究中是否对同一个位点进行了重复研究。证据[1]和[2]来自不同的论文，但讨论的是遗传图谱构建和标记分离比，未提及具体的、可比较的位点。证据[4]、[5]、[6]虽然提到了SNP-2,002和SNP-1,545等位点，但它们均来自同一份数据文件（Supplemental Table S5），属于同一项研究内部的数据，不涉及多篇研究的比较。

**Level B (间接证据):**
所有证据均未提供任何关于不同研究（即不同论文）之间是否对相同位点进行过分析的信息。证据中既没有列出具体的基因或QTL位点，也没有引用或对比其他研究的结果。因此，没有间接证据可以支持或否定同一位点在多篇研究中重复出现。

引用编号：[1], [2], [3], [4], [5], [6]
证据摘要
- [1] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.17 | score=0.73618513
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 术的普及和新型标记的开发，上万个的标记可以 通过一次测序分析而被开发出来，这当然会使得我们构建遗传图谱的密度增加，但同
- [2] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.36 | score=0.71852493
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 现出与 1:1理想分离比的显著性差异，但在
- [3] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.42 | score=0.5643635
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 板置于加热模块上，在 95℃下使样品变性 20min；再在室温下冷却 30min。；80g离心后拆下箔封。 2）取出微珠芯片装入 Hyb杂交盒插件（图 3-3A）。
- [4] gene | 6427 | score=0.10524641
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 21; row_text: Supplementary Table S5. KASP...
- [5] gene | 6506 | score=0.099876456
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 100; row_text: Supplementary Table S5. KAS...
- [6] gene | 6608 | score=0.09980125
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/001_an_indel_variant_in_the_promoter_001_Supplemental Table 1-7.xlsx; sheet: Supplementary Table S5; row_index: 202; row_text: Supplementary Table S5. KAS...

### 18. 对硬度相关基因这个问题，当前证据是否足够支持因果结论？
- route_used: `hybrid`
- evidence_count: `2`
回答
根据提供的证据，当前证据**不足以**支持关于硬度相关基因的因果结论。

**Level A (直接证据)**
证据[1]和[2]均明确指出，基因MD16G1117200和MD16G1096900是位于果实硬度（flesh firmness）数量性状位点（QTL）区域内的差异表达基因（DEGs）。这提供了这些基因与硬度性状存在关联的直接证据。

**Level B (间接证据)**
然而，所提供的证据仅表明这些基因在硬度QTL区域内且表达有差异。证据中未包含任何功能验证实验（如基因敲除、过表达等）的结果，也未提供这些基因的遗传变异（如等位变异）与硬度表型差异之间的直接统计关联数据（例如，基于群体遗传学的关联分析p值）。因此，现有证据只能说明这些基因是候选基因，但无法确立其与硬度性状之间的因果关系。

引用编号：[1], [2]
证据摘要
- [1] gene | 5 | score=-0.02233755
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/016_allelic_variation_in_an_expansin_mdexp_001_43897_2024_121_MOESM2_ESM.xls; sheet: TableS6; row_index: 90; trait: firmness; gene: MD16G1117200; pvalue: ...
- [2] gene | 4 | score=-0.026977118
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/016_allelic_variation_in_an_expansin_mdexp_001_43897_2024_121_MOESM2_ESM.xls; sheet: TableS6; row_index: 69; trait: firmness; gene: MD16G1096900; pvalue: ...

### 19. 当前数据库中，哪些回答是证据不足/未检索到相关材料，原因是什么？
- route_used: `papers`
- evidence_count: `6`
回答
根据提供的证据，无法回答该问题。

**Level A (直接证据)**
提供的所有证据均是关于苹果遗传图谱构建、抗病性研究或QTL定位的具体研究内容，没有任何一条证据提及“当前数据库”的状态，也没有证据讨论哪些回答是“证据不足/未检索到相关材料”及其原因。因此，没有直接证据可以回答此问题。

**Level B (间接证据)**
所有证据均与问题无关。证据[1]、[3]、[4]、[5]、[6]讨论了苹果遗传图谱构建、抗炭疽叶枯病研究及相关方法学。证据[2]讨论了苹果褐斑病抗性育种。这些内容均未涉及对数据库回答质量或检索情况的评估。

**引用编号**
[1], [2], [3], [4], [5], [6]
证据摘要
- [1] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.8 | score=0.6661792
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 西北农林科技大学硕士学位论文 菌的转录组分析，共筛选出 7 个在苹果炭疽叶枯病病原菌侵染时存在差异的苹果炭疽 叶枯病候抗病相关的候选基因。 关键词：遗传图谱；遗传定位；苹果炭疽叶枯病；抗病
- [2] paper | 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋.pdf | p.19 | score=0.6354573
  title: 031_paper_001_‘秦冠’苹果遗传连锁图谱的构建及褐斑病抗性基因的定位_刘博洋
  snippet: 010）。Wöhner等（2019）认为目前还不能准确地将症状较轻的基因型归类为抗病基因 型。多项研究表明，‘秦冠’苹果是对褐斑病具有较强抗性（Zhouetal.2012；Sharmaetal. 2012；Lietal.2012；Yinetal.2013a；2013b；Wangetal.2013；Xuetal.2015）。总之， 目前苹果褐斑病抗性育种的难点在于缺乏高抗苹果品种材料，同时对苹果种质资源的褐 斑病抗病评价也缺乏系统研究。 1.2苹果遗传图谱构建和 QTL定位研究...
- [3] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.16 | score=0.6120844
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 。高质量的参考基因组不仅有利于转录组定量分析，基因克隆和分子标记开发， 甚至可以直接用于遗传图谱遗传标记的连锁群划分和排图， 2006年Shifman等人使用 高通量测序技术构建小鼠的高密度连锁遗传图谱时，通过使用标记的物理位置直接进 行遗传标记排序，减少了大量的计算过程，同样 ，Muñ oz等人2012年在构建猪的连锁 遗传图谱时采用了相同的策略，使用标记的物理位置直接进行连锁群的划分和排序， 提高了遗传图谱构建速度和QTL定位的准确性（Shifman et al. 200...
- [4] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.45 | score=0.60444
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 脆’具有苹果炭疽叶枯病抗病性，连续两年的调查结果表 明子代抗病植株167株，感病植株160株，抗病和感病比例为167:160，具体子代表型分 布见附表1。 2
- [5] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.18 | score=0.59851813
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 西北农林科技大学硕士学位论文 6 时标记密度提升 带来计算强度的指数增长也对传统的计算方法和 计算工具提出挑战 (van Os et al. 2005; Liu et al. 2014)。人们一直致力于开发高效准确的算法和软件用于构 建遗传图谱，以解决在构建遗传图谱过程中的问题，并根据不同的算法或计算机语言 开发了Joinmap， SMOOTH，RECORD，FsLinkageMap，OneMap等诸多的算法和软 件(van Os et al. 2005; Wu, et al...
- [6] paper | 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥.pdf | p.14 | score=0.588987
  title: 027_paper_001_‘秦冠’和‘蜜脆’遗传图谱的再构建及苹果抗炭疽叶枯病主效基因的定位_杨南祥
  snippet: 提高。遗传图谱广泛用于 动植物遗传性状的遗传定位，高密度连锁图谱的应用极大地促进了功能基因的发现， 通过QTL定位方法已经定位到多个果实品质、抗性等相关的QTL位点。如2015年Kujur 等人分别将3625和2177个SNP整合到八个desi和kabuli的染色体中构建特异性鹰嘴豆内 遗传连锁图（Kujur et al. 2015），童春发等人使用Populus deltoides和Populus simonii进 行杂交构建F1代杂交群体并使用限制性位点相关 DNA测序数...

### 20. 请给出硬度、成熟、酸度、糖度、颜色五类性状的候选基因速览（含引用）。
- route_used: `hybrid`
- evidence_count: `2`
回答
根据提供的证据，无法回答该问题。

**Level A (直接证据)**
- 硬度：候选基因包括 MD16G1117200 和 MD16G1163400，两者均位于果实硬度QTL区域，且是差异表达基因（DEGs）[1, 2]。
- 成熟、酸度、糖度、颜色：提供的证据中未包含与这些性状相关的任何候选基因信息。

**Level B (间接证据)**
- 无。提供的证据仅涉及硬度性状，未提供关于成熟、酸度、糖度或颜色性状的任何直接或间接证据。

引用编号：[1, 2]
证据摘要
- [1] gene | 5 | score=0.030491471
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/016_allelic_variation_in_an_expansin_mdexp_001_43897_2024_121_MOESM2_ESM.xls; sheet: TableS6; row_index: 90; trait: firmness; gene: MD16G1117200; pvalue: ...
- [2] gene | 6 | score=0.025490817
  snippet: source_file: /Users/shuaige/code/apple-breeding-rag/backend/data/genes/raw_candidates/016_allelic_variation_in_an_expansin_mdexp_001_43897_2024_121_MOESM2_ESM.xls; sheet: TableS6; row_index: 104; trait: firmness; gene: MD16G1163400; pvalue:...

