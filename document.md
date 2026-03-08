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