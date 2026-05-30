'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import styles from './page.module.css'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000'
const INITIAL_CHAT = mkChat()
const LLM_STORAGE_KEY = 'apple-breeding-rag-llm-config'
const CHATS_STORAGE_KEY = 'apple-breeding-rag-chats'
const GENE_TARGETS = [
  { value: 'genes', label: '通用 genes' },
  { value: 'genes_firmness', label: '硬度 genes_firmness' },
  { value: 'genes_color', label: '颜色 genes_color' },
  { value: 'genes_acidity', label: '酸度 genes_acidity' },
  { value: 'genes_harvest', label: '采收期 genes_harvest' },
  { value: 'genes_sugar', label: '糖度 genes_sugar' }
]
const QUICK_PROMPTS = [
  'Ma1基因位点对苹果果实酸度有何影响？',
  'MdMYB10启动子中的R6重复序列对苹果花青素积累有何影响？',
  'MdNAC18基因启动子区域的InDel变体如何影响苹果果肉硬度和成熟时间？',
  '苹果育种中GWAS与QTL作图相比有什么优势？'
]
function mkChat() {
  return {
    id: String(Date.now() + Math.random()),
    title: '新对话',
    messages: [],
    createdAt: new Date().toISOString()
  }
}

function trimTitle(text) {
  const t = (text || '').trim()
  if (!t) return '新对话'
  return t.length > 24 ? `${t.slice(0, 24)}...` : t
}

function geneTargetDisplay(value) {
  const target = GENE_TARGETS.find((item) => item.value === value)
  const label = target?.label?.split(' ')[0] || '通用'
  return `${label}基因库`
}

const SOURCE_LABELS = {
  literature_curated: '人工整理文献库'
}

const SHEET_LABELS = {
  firmness_texture_genes: '硬度与质地基因表',
  color_genes: '果皮颜色基因表',
  acidity_genes: '酸度基因表',
  sugar_genes: '糖度基因表',
  harvest_genes: '采收期基因表'
}

const TRAIT_LABELS = {
  firmness: '硬度',
  color: '颜色',
  acidity: '酸度',
  sugar: '糖度',
  harvest: '采收期',
  texture: '质地',
  ripening: '成熟',
  softening: '软化',
  crispness: '脆度'
}

const EVIDENCE_REPLACEMENTS = [
  // ===== 长语义短语（最长优先） =====
  ['core apple firmness, ripening, and harvest-date regulator', '苹果硬度、成熟和采收期调控的核心候选基因'],
  ['ripening-time GWAS/QTL evidence', '成熟期 GWAS/QTL 证据'],
  ['Honeycrisp-like delayed softening interpretation', 'Honeycrisp 式延迟软化解释'],
  ['Apple ripening and texture GWAS', '苹果成熟与质地 GWAS'],
  ['GWAS/QTL evidence', 'GWAS/QTL 证据'],

  // ===== 复合"生物学+动词"短语（必须先于通用连接词，否则会被通用规则吃掉） =====
  ['Expansin proteins contribute to', 'Expansin 蛋白参与'],
  ['expansin proteins contribute to', 'expansin 蛋白参与'],
  ['expansin gene contributing to', 'expansin 基因参与'],
  ['transcription factors activate or modulate', '转录因子激活或调控'],
  ['transcription factors contribute to variation in', '转录因子参与影响'],
  ['transcription factors contribute to', '转录因子参与'],
  ['gene contributing to', '基因参与'],
  ['gene supports', '基因支持'],

  // ===== 结构/连接词组（先于短词） =====
  ['is used as a normalized gene-family label for', '作为以下范围的归一化基因家族标签：'],
  ['a normalized gene-family label for', '归一化基因家族标签，用于'],
  ['normalized gene-family label', '归一化基因家族标签'],
  ['curated synonym/normalization entry', '人工整理的同义词/归一化条目'],
  ['curated synonym', '人工整理的同义词'],
  ['normalization entry', '归一化条目'],
  ['when the question asks for', '；适用于问题询问'],
  ['when the question asks about', '；适用于问题询问'],
  ['-style questions that ask about', '式相关问题，涉及'],
  ['-style questions', '式相关问题'],
  ['questions that ask about', '相关问题，涉及'],
  ['questions that ask', '相关问题'],
  ['the question asks for', '问题询问'],
  ['the question asks about', '问题询问'],
  ['asks about', '询问'],
  ['asks for', '询问'],
  ['ask about', '关于'],
  ['rather than the specific', '而非特定的'],
  ['rather than', '而非'],
  ['such as', '如'],
  ['through activation of', '通过激活'],
  ['indirectly reducing', '间接降低'],
  ['can affect', '可影响'],
  ['can modulate', '可调控'],
  ['activate or modulate', '激活或调控'],
  ['contributes to variation in', '参与影响'],
  ['contributing to', '参与'],
  ['contributes to', '参与'],
  ['contribute to', '参与'],
  ['is associated with', '与之相关：'],
  ['associated with', '，关联'],
  ['is linked with', '与之相关联：'],
  ['linked with', '相关联'],
  ['during fruit softening', '在果实软化过程中'],
  ['during fruit', '在果实'],
  ['during', '在'],
  ['in apple fruit', '于苹果果实'],
  ['in apple', '于苹果'],
  ['at harvest', '（采收时）'],
  ['a key rate-limiting enzyme for', '关键限速酶，参与'],
  ['rate-limiting enzyme for', '限速酶，参与'],
  ['key rate-limiting enzyme', '关键限速酶'],
  ['-style', '式'],

  // ===== 生物学短语 =====
  ['ACC synthase', 'ACC 合成酶'],
  ['rate-limiting enzyme', '限速酶'],
  ['climacteric ethylene', '跃变型乙烯'],
  ['climacteric', '跃变型'],
  ['harvest maturity', '采收成熟度'],
  ['polygalacturonase', '多聚半乳糖醛酸酶'],
  ['NAC transcription factor', 'NAC 转录因子'],
  ['ethylene-response factor', '乙烯响应因子'],
  ['ethylene response factor', '乙烯响应因子'],
  ['ethylene-response', '乙烯响应'],
  ['ethylene response', '乙烯响应'],
  ['ethylene-pathway gene', '乙烯通路基因'],
  ['ethylene pathway gene', '乙烯通路基因'],
  ['ethylene-pathway', '乙烯通路'],
  ['ethylene pathway', '乙烯通路'],
  ['response factor', '响应因子'],
  ['transcription-factor', '转录因子'],
  ['transcription factors', '转录因子'],
  ['transcription factor', '转录因子'],
  ['candidate transcription factor', '候选转录因子'],
  ['Expansin proteins contribute to', 'Expansin 蛋白参与'],
  ['expansin proteins', 'expansin 蛋白'],
  ['expansin gene', 'expansin 基因'],
  ['fruit softening', '果实软化'],
  ['fruit ripening', '果实成熟'],
  ['fruit texture', '果实质地'],
  ['ripening differences', '成熟差异'],
  ['softening differences', '软化差异'],
  ['firmness differences', '硬度差异'],
  ['texture differences', '质地差异'],
  ['ripening divergence', '成熟差异'],
  ['ripening mechanism', '成熟机制'],
  ['ripening onset', '成熟启动'],
  ['softening interpretation', '软化解释'],
  ['firmness retention', '硬度保持'],
  ['texture retention', '质地保持'],
  ['retainability', '保持性'],

  // ===== 已有的多词术语 =====
  ['apple fruit firmness', '苹果果实硬度'],
  ['apple flesh firmness', '苹果果肉硬度'],
  ['flesh firmness', '果肉硬度'],
  ['fruit firmness', '果实硬度'],
  ['firmness after storage', '贮藏后硬度'],
  ['postharvest softening', '采后软化'],
  ['postharvest firmness', '采后硬度'],
  ['postharvest', '采后'],
  ['delayed softening', '延迟软化'],
  ['ripening-time', '成熟期'],
  ['harvest-date', '采收期'],
  ['harvest date', '采收期'],
  ['cell-wall softening programs', '细胞壁软化过程'],
  ['cell-wall degradation pathways', '细胞壁降解通路'],
  ['cell-wall degradation genes', '细胞壁降解基因'],
  ['cell-wall degradation gene', '细胞壁降解基因'],
  ['cell-wall degradation', '细胞壁降解'],
  ['cell-wall disassembly gene', '细胞壁解体相关基因'],
  ['cell-wall loosening', '细胞壁松弛'],
  ['cell-wall', '细胞壁'],
  ['cell wall', '细胞壁'],
  ['ethylene biosynthesis', '乙烯生物合成'],
  ['ethylene production', '乙烯生成'],
  ['ethylene biology', '乙烯生物学'],
  ['anthocyanin biosynthesis', '花青素生物合成'],
  ['anthocyanin accumulation', '花青素积累'],
  ['red skin coloration', '果皮红色着色'],
  ['red skin color', '红色果皮'],
  ['skin color', '果皮颜色'],
  ['malic acid content', '苹果酸含量'],
  ['titratable acidity', '可滴定酸'],
  ['vacuolar acidification', '液泡酸化'],
  ['malate accumulation', '苹果酸积累'],
  ['candidate-gene support', '候选基因支持'],
  ['candidate gene support', '候选基因支持'],
  ['allelic-variation support', '等位变异支持'],
  ['allelic variation support', '等位变异支持'],
  ['QTL/candidate-gene', 'QTL/候选基因'],
  ['QTL/candidate gene', 'QTL/候选基因'],
  ['candidate-gene', '候选基因'],
  ['candidate gene', '候选基因'],
  ['allelic variation', '等位变异'],
  ['allelic-variation', '等位变异'],
  ['natural-variation', '自然变异'],
  ['natural variation', '自然变异'],
  ['genomics-assisted prediction', '基因组学辅助预测'],
  ['genomics-assisted', '基因组学辅助'],
  ['functional characterization', '功能验证'],
  ['functional analysis', '功能分析'],
  ['expression analysis', '表达分析'],
  ['association analysis', '关联分析'],
  ['promoter analysis', '启动子分析'],
  ['QTL mapping', 'QTL 作图'],
  ['QTL-supported', 'QTL 支持的'],
  ['GWAS/QTL-supported', 'GWAS/QTL 支持的'],
  ['literature-curated', '文献整理的'],
  ['texture variation', '质地差异'],
  ['Multiple apple cultivars', '多个苹果品种'],
  ['Multiple cultivars', '多个品种'],

  // ===== 单字（启用 \b 词边界，避免误伤复合词） =====
  ['encodes', '编码'],
  ['affects', '影响'],
  ['affect', '影响'],
  ['activate', '激活'],
  ['modulate', '调控'],
  ['reducing', '降低'],
  ['supporting', '支持'],
  ['supports', '支持'],
  ['support', '支持'],
  ['onset', '启动'],
  ['production', '生成'],
  ['differences', '差异'],
  ['variations', '变异'],
  ['variation', '变异'],
  ['regulators', '调控因子'],
  ['mechanisms', '机制'],
  ['pathways', '通路'],
  ['enzymes', '酶'],
  ['interpretations', '解释'],
  ['cultivars', '品种'],
  ['cultivar', '品种'],
  ['proteins', '蛋白'],
  ['protein', '蛋白'],
  ['enzyme', '酶'],
  ['symbol', '符号'],
  ['relevant', '相关的'],
  ['key', '关键'],
  ['gene-family', '基因家族'],
  ['genes', '基因'],
  ['gene', '基因'],
  ['fruit', '果实'],
  ['flesh', '果肉'],
  ['interpretation', '解释'],
  ['evidence', '证据'],
  ['apple', '苹果'],
  ['firmness', '硬度'],
  ['texture', '质地'],
  ['ripening', '成熟'],
  ['softening', '软化'],
  ['crispness', '脆度'],
  ['candidate', '候选'],
  ['mechanism', '机制'],
  ['pathway', '通路'],
  ['regulator', '调控因子'],
  ['locus', '位点'],
  ['when', '当'],
  ['in', '于']
]

function sourceTypeDisplay(value) {
  return value === 'gene' ? '基因' : value === 'paper' ? '文献' : value || '来源'
}

function localizeValue(key, value) {
  if (!value) return ''
  if (key === 'source_file') return SOURCE_LABELS[value] || value
  if (key === 'sheet') return SHEET_LABELS[value] || value
  if (key === 'trait') return TRAIT_LABELS[value] || value
  if (key === 'variety') return translateEvidencePhrase(value)
  return value
}

function translateEvidencePhrase(text) {
  let output = text || ''
  EVIDENCE_REPLACEMENTS.forEach(([from, to]) => {
    // 单词级短语加 \b 词边界（gene 不匹配 genetic）；多词短语以字母结尾且非 s 时允许尾部 s（处理复数）
    const isWordLike = /^[A-Za-z][A-Za-z-]*[A-Za-z]?$/.test(from)
    const isMultiWord = /\s/.test(from)
    const endsInLetterNonS = /[A-Za-rt-z]$/.test(from)
    const escaped = escapeRegExp(from)
    let pattern
    if (isWordLike) {
      pattern = `\\b${escaped}\\b`
    } else if (isMultiWord && endsInLetterNonS) {
      pattern = `${escaped}s?\\b`
    } else {
      pattern = escaped
    }
    output = output.replace(new RegExp(pattern, 'gi'), to)
  })
  return cleanupEvidencePhrase(output)
}

function cleanupEvidencePhrase(text) {
  return (text || '')
    .replace(/,\s*and\s+/gi, '和')
    .replace(/\s+and\s+/gi, '和')
    .replace(/,\s*/g, '、')
    .replace(/\s+/g, ' ')
    .replace(/([\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])/g, '$1')
    .replace(/([\u4e00-\u9fff])\s+(?=[，。；、])/g, '$1')
    .replace(/（\s+/g, '（')
    .replace(/\s+）/g, '）')
    .replace(/([一-鿿])\s+(?=[（）「」])/g, '$1')
    .replace(/把\s+/g, '把')
    .replace(/\s+与\s+/g, '与')
    .replace(/\s+联系/g, '联系')
    .replace(/和(?=[A-Za-z])/g, '和 ')
    .trim()
}

function escapeRegExp(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function translateEvidenceText(text) {
  if (!text) return ''
  return text
    .split(/(?<=\.)\s+/)
    .map((sentence) => translateEvidenceSentence(sentence.trim()))
    .filter(Boolean)
    .join('')
}

// 中文前缀拼接：content 以中文开头则不加空格，否则加一个空格
function joinCJ(prefix, content) {
  const c = content || ''
  if (!c) return prefix
  return /^[一-鿿]/.test(c) ? `${prefix}${c}` : `${prefix} ${c}`
}

function translateEvidenceSentence(sentence) {
  if (!sentence) return ''

  const evidenceType = sentence.match(/^Evidence type:\s*(.+)\.?$/i)
  if (evidenceType) return `证据类型：${translateEvidencePhrase(evidenceType[1]).replace(/\.$/, '')}。`

  const trait = sentence.match(/^Trait:\s*(.+)\.?$/i)
  if (trait) return `关联性状：${translateEvidencePhrase(trait[1]).replace(/\.$/, '')}。`

  const curated = sentence.match(/^(.+?) is curated as (?:an?|the)?\s*(.+)\.?$/i)
  if (curated) return `${joinCJ(`${curated[1]} 被整理为`, translateEvidencePhrase(curated[2]).replace(/\.$/, ''))}。`

  const located = sentence.match(/^Located on (chromosome|Chr)(.+),\s*(.+)\.?$/i)
  if (located) return `位于 Chr${located[2].trim().replace(/^Chr/i, '')}，${translateEvidencePhrase(located[3]).replace(/\.$/, '')}。`

  const regionLinks = sentence.match(/^The (.+?) region links (.+?) with (.+)\.?$/i)
  if (regionLinks) {
    return `${regionLinks[1]} 区域把 ${translateEvidencePhrase(regionLinks[2])} 与 ${translateEvidencePhrase(regionLinks[3]).replace(/\.$/, '')} 联系起来。`
  }

  const supports = sentence.match(/^It supports answers where (.+)\.?$/i)
  if (supports) return `该证据可支持以下问题场景：${translateEvidencePhrase(supports[1]).replace(/\.$/, '')}。`

  const supportsQuestions = sentence.match(/^It supports (.+)\.?$/i)
  if (supportsQuestions) return `该证据支持：${translateEvidencePhrase(supportsQuestions[1]).replace(/\.$/, '')}。`

  const association = sentence.match(/^(.+?) is associated with (.+)\.?$/i)
  if (association) return `${association[1]} 与 ${translateEvidencePhrase(association[2]).replace(/\.$/, '')} 相关。`

  // X encodes Y, a Z（同位语结构：X 编码 Y，即 Z）
  const encodesAppos = sentence.match(/^(.+?)\s+encodes\s+(.+?),\s+(?:an?|the)\s+(.+)\.?$/i)
  if (encodesAppos) {
    return `${encodesAppos[1]} 编码 ${translateEvidencePhrase(encodesAppos[2])}，即${translateEvidencePhrase(encodesAppos[3]).replace(/\.$/, '')}。`
  }

  // X encodes Y
  const encodes = sentence.match(/^(.+?)\s+encodes\s+(.+)\.?$/i)
  if (encodes) return `${encodes[1]} 编码 ${translateEvidencePhrase(encodes[2]).replace(/\.$/, '')}。`

  // X affects Y
  const affects = sentence.match(/^(.+?)\s+affects\s+(.+)\.?$/i)
  if (affects) return `${affects[1]} 影响 ${translateEvidencePhrase(affects[2]).replace(/\.$/, '')}。`

  // X is linked with Y
  const linked = sentence.match(/^(.+?)\s+is linked with\s+(.+)\.?$/i)
  if (linked) return `${translateEvidencePhrase(linked[1])} 与 ${translateEvidencePhrase(linked[2]).replace(/\.$/, '')} 相关联。`

  // X contributes to Y（X 也走翻译，处理"Expansin proteins"这类需要翻译的主语）
  const contributes = sentence.match(/^(.+?)\s+contributes? to\s+(.+)\.?$/i)
  if (contributes) return `${translateEvidencePhrase(contributes[1])} 参与 ${translateEvidencePhrase(contributes[2]).replace(/\.$/, '')}。`

  return `${translateEvidencePhrase(sentence).replace(/\.$/, '')}。`
}

function parseEvidenceFields(text) {
  const fields = {}
  ;(text || '').split(/;\s+(?=[A-Za-z_]+:)/).forEach((part) => {
    const match = part.match(/^([^:]+):\s*(.*)$/)
    if (match) fields[match[1].trim()] = match[2].trim()
  })
  return fields
}

function EvidenceCardBody({ source }) {
  const fields = parseEvidenceFields(source.chunk_text)
  if (!fields.evidence_text) return <p>{source.chunk_text}</p>

  const provenance = [
    fields.source_file && `来源：${localizeValue('source_file', fields.source_file)}`,
    fields.sheet && `表格：${localizeValue('sheet', fields.sheet)}`,
    fields.row_index && `行号：${fields.row_index}`
  ].filter(Boolean)

  const facts = [
    fields.trait && `性状：${localizeValue('trait', fields.trait)}`,
    fields.gene && `基因：${fields.gene}`,
    fields.snp && `SNP/位点：${fields.snp}`,
    fields.chr && `染色体：${fields.chr}`,
    fields.pos && `位置：${fields.pos}`,
    fields.pvalue && `P 值：${fields.pvalue}`,
    fields.variety && `材料/群体：${localizeValue('variety', fields.variety)}`
  ].filter(Boolean)

  return (
    <div className={styles.evidenceBody}>
      {provenance.length > 0 && <p className={styles.evidenceLine}>{provenance.join('；')}</p>}
      {facts.length > 0 && <p className={styles.evidenceLine}>{facts.join('；')}</p>}
      <p className={styles.evidenceLine}>证据说明：{translateEvidenceText(fields.evidence_text)}</p>
    </div>
  )
}

// ── Markdown renderer ──────────────────────────────────────────────────────
const GENE_PATTERN = /\b(Md[A-Z][A-Za-z0-9-]*|Ma\d+|MdMYB\d+|MdNAC\d+|MdEXP[-A-Z0-9]*|MdALMT\d+|MdPG\d*|MdACS\d*|MdACO\d*)\b/
const CHR_PATTERN = /\bChr\s?\d+[A-Za-z]?\b/

function jumpToCitation(ctx, n) {
  if (!ctx) return
  const { articleId, sourceCount } = ctx
  if (!articleId || !n || n < 1 || (sourceCount && n > sourceCount)) return
  const details = document.getElementById(`${articleId}-details`)
  if (details && !details.open) details.open = true
  // 等下一帧 details 展开
  requestAnimationFrame(() => {
    const target = document.getElementById(`${articleId}-src-${n - 1}`)
    if (!target) return
    target.scrollIntoView({ behavior: 'smooth', block: 'center' })
    target.classList.add(styles.evidenceItemFlash)
    setTimeout(() => target.classList.remove(styles.evidenceItemFlash), 1600)
  })
}

function parseInline(text, prefix = '', ctx = null) {
  const out = []
  let rem = text
  let k = 0

  while (rem.length) {
    const candidates = [
      matchAndWrap(rem, /\*\*(.+?)\*\*/, 'b'),
      matchAndWrap(rem, /(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/, 'i'),
      matchAndWrap(rem, /`([^`]+)`/, 'c'),
      ctx && matchAndWrap(rem, /\[(\d+)\]/, 'cite'),
      matchAndWrap(rem, GENE_PATTERN, 'gene'),
      matchAndWrap(rem, CHR_PATTERN, 'chr')
    ].filter(Boolean).sort((a, b) => a.m.index - b.m.index)

    if (!candidates.length) { out.push(rem); break }
    const { type, m } = candidates[0]
    if (m.index > 0) out.push(rem.slice(0, m.index))

    if (type === 'b') out.push(<strong key={`${prefix}b${k++}`}>{m[1]}</strong>)
    else if (type === 'i') out.push(<em key={`${prefix}i${k++}`}>{m[1]}</em>)
    else if (type === 'c') out.push(<code key={`${prefix}c${k++}`} className={styles.mdCode}>{m[1]}</code>)
    else if (type === 'cite') {
      const n = parseInt(m[1], 10)
      out.push(
        <button
          key={`${prefix}cite${k++}`}
          type="button"
          className={styles.citationChip}
          onClick={() => jumpToCitation(ctx, n)}
          title={`查看第 ${n} 条证据`}
        >
          {n}
        </button>
      )
    } else if (type === 'gene') {
      out.push(<span key={`${prefix}g${k++}`} className={styles.geneChip}>{m[0]}</span>)
    } else if (type === 'chr') {
      out.push(<span key={`${prefix}chr${k++}`} className={styles.chrChip}>{m[0]}</span>)
    }
    rem = rem.slice(m.index + m[0].length)
  }
  return out
}

function matchAndWrap(rem, regex, type) {
  const m = rem.match(regex)
  return m ? { type, m } : null
}

// 抽出答案最开头的 "**结论：**…" 作为 TL;DR
function extractTldr(text) {
  if (!text) return { tldr: null, body: text || '' }
  const m = text.match(/^\s*\*\*结论[:：]\*\*\s*([^\n]+?)(?:\n|$)/)
  if (!m) return { tldr: null, body: text }
  return { tldr: m[1].trim().replace(/[。.\s]+$/, ''), body: text.slice(m[0].length).replace(/^\s+/, '') }
}

function MarkdownBlock({ text, ctx = null }) {
  const lines = (text || '').split('\n')
  const els = []
  let i = 0
  let k = 0

  while (i < lines.length) {
    const line = lines[i]

    // fenced code block
    if (line.startsWith('```')) {
      const codeLines = []
      i++
      while (i < lines.length && !lines[i].startsWith('```')) {
        codeLines.push(lines[i])
        i++
      }
      els.push(<pre key={k++} className={styles.mdPre}><code>{codeLines.join('\n')}</code></pre>)
      i++
      continue
    }

    // headings
    const hm = line.match(/^(#{1,4})\s+(.+)$/)
    if (hm) {
      const lvl = hm[1].length
      const Tag = ['h2', 'h3', 'h4', 'h5'][lvl - 1] || 'h5'
      els.push(<Tag key={k++} className={styles[`mdH${lvl}`]}>{parseInline(hm[2], `h${k}`, ctx)}</Tag>)
      i++
      continue
    }

    // horizontal rule
    if (/^[-*_]{3,}$/.test(line.trim())) {
      els.push(<hr key={k++} className={styles.mdHr} />)
      i++
      continue
    }

    // blockquote
    if (line.startsWith('>')) {
      const ql = []
      while (i < lines.length && lines[i].startsWith('>')) {
        ql.push(lines[i].replace(/^>\s?/, ''))
        i++
      }
      els.push(
        <blockquote key={k++} className={styles.mdBlockquote}>
          {ql.map((l, j) => <p key={j}>{parseInline(l, `bq${j}`, ctx)}</p>)}
        </blockquote>
      )
      continue
    }

    // unordered list
    if (/^[-*+]\s/.test(line)) {
      const items = []
      while (i < lines.length && /^[-*+]\s/.test(lines[i])) {
        items.push(<li key={i}>{parseInline(lines[i].replace(/^[-*+]\s+/, ''), `ul${i}`, ctx)}</li>)
        i++
      }
      els.push(<ul key={k++} className={styles.mdUl}>{items}</ul>)
      continue
    }

    // ordered list
    if (/^\d+\.\s/.test(line)) {
      const items = []
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) {
        items.push(<li key={i}>{parseInline(lines[i].replace(/^\d+\.\s+/, ''), `ol${i}`, ctx)}</li>)
        i++
      }
      els.push(<ol key={k++} className={styles.mdOl}>{items}</ol>)
      continue
    }

    // empty line → skip (margin between paragraphs handles spacing)
    if (!line.trim()) { i++; continue }

    // paragraph
    els.push(<p key={k++} className={styles.mdP}>{parseInline(line, `p${k}`, ctx)}</p>)
    i++
  }

  return <div className={styles.markdownContent}>{els}</div>
}
// ──────────────────────────────────────────────────────────────────────────

// ── Pipeline loader (presentation-friendly RAG visualization) ─────────────
const PIPELINE_STEPS = [
  { key: 'parse', label: '解析问题', sub: '路由判定 · 关键词提取' },
  { key: 'retrieve', label: '向量检索', sub: 'Milvus · top-K 召回' },
  { key: 'rerank', label: '汇总证据', sub: '论文片段 + 候选基因' },
  { key: 'generate', label: 'LLM 生成', sub: '带引用的回答' }
]

function PipelineLoader() {
  const [stage, setStage] = useState(0)
  useEffect(() => {
    const timers = [
      setTimeout(() => setStage(1), 450),
      setTimeout(() => setStage(2), 1100),
      setTimeout(() => setStage(3), 2000)
    ]
    return () => timers.forEach(clearTimeout)
  }, [])
  return (
    <div className={styles.pipeline}>
      {PIPELINE_STEPS.map((s, i) => {
        const done = i < stage
        const current = i === stage
        const cls = [
          styles.pipelineStep,
          done && styles.pipelineStepDone,
          current && styles.pipelineStepCurrent
        ].filter(Boolean).join(' ')
        return (
          <div key={s.key} className={cls}>
            <div className={styles.pipelineDot}>
              {done ? '✓' : i + 1}
            </div>
            <div className={styles.pipelineText}>
              <div className={styles.pipelineLabel}>{s.label}</div>
              <div className={styles.pipelineSub}>{s.sub}</div>
            </div>
            {i < PIPELINE_STEPS.length - 1 && <div className={styles.pipelineRail} />}
          </div>
        )
      })}
    </div>
  )
}

// ── Empty state hero (project highlights + arch diagram + stats) ──────────
const STAT_PILLS = [
  { value: '75', label: '篇论文' },
  { value: '18', label: '份基因表' },
  { value: '6', label: '个性状' },
  { value: 'DeepSeek', label: '可换任意 OpenAI 兼容模型' }
]

// 内联 SVG 线稿（替换 emoji，统一线宽与色彩）
const ICON_DOC = (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round">
    <path d="M6 3h8l4 4v14H6z" /><path d="M14 3v4h4" /><path d="M9 12h6M9 16h6M9 8h2" />
  </svg>
)
const ICON_VEC = (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="6" cy="6" r="1.6" /><circle cx="18" cy="6" r="1.6" /><circle cx="6" cy="18" r="1.6" /><circle cx="18" cy="18" r="1.6" /><circle cx="12" cy="12" r="1.6" />
    <path d="M7 7l4 4M17 7l-4 4M7 17l4-4M17 17l-4-4" opacity="0.55" />
  </svg>
)
const ICON_ROUTE = (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 6h6l4 12h6" /><path d="M4 18h6l4-12h6" opacity="0.55" />
  </svg>
)
const ICON_STAR = (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 3v18M3 12h18" /><path d="M5 5l14 14M19 5L5 19" opacity="0.45" />
  </svg>
)

const ARCH_NODES = [
  { icon: ICON_DOC, label: '论文 PDF\n基因表 CSV' },
  { icon: ICON_VEC, label: '嵌入向量\nMilvus 索引' },
  { icon: ICON_ROUTE, label: '智能路由\n分库检索' },
  { icon: ICON_STAR, label: '大模型生成\n带引用回答' }
]

// 苹果植物专论线稿：一颗完整苹果（带枝叶）+ 旁边一个半剖（露出果心五瓣 + 种子）
// 暗合「育种 / 基因 / 候选位点」主题
const APPLE_BOTANICAL = (
  <svg className={styles.heroOrnamentSvg} viewBox="0 0 240 320" fill="none" aria-hidden="true">
    <g stroke="currentColor" strokeWidth="1.35" strokeLinecap="round" strokeLinejoin="round" fill="none">
      {/* ── 主苹果（完整） ───────────────────────────────────────── */}
      {/* 果体 — 双肩 + 圆底的苹果轮廓 */}
      <path d="M 118 118
               C 108 102, 70 100, 56 124
               C 40 154, 40 198, 58 230
               C 76 260, 104 278, 118 274
               C 132 278, 160 260, 178 230
               C 196 198, 196 154, 180 124
               C 166 100, 128 102, 118 118 Z" />
      {/* 顶部小凹陷 */}
      <path d="M 110 116 Q 118 110, 126 116" opacity="0.7" />
      {/* 果柄 */}
      <path d="M 118 114 C 120 100, 126 86, 134 76" />
      {/* 叶片（不对称椭圆，尖端） */}
      <path d="M 134 76
               C 152 66, 174 64, 188 48
               C 176 68, 158 84, 140 92 Z" />
      {/* 叶脉 */}
      <path d="M 142 86 C 154 78, 168 68, 182 54" opacity="0.55" />
      <path d="M 150 90 C 156 84, 162 78, 168 72" opacity="0.4" />
      {/* 果体内侧轻微体积线（植物图鉴惯例） */}
      <path d="M 80 142 C 72 175, 72 215, 84 248" opacity="0.32" />

      {/* ── 半剖苹果（科研图鉴感，露出五瓣果心 + 种子） ───────────── */}
      {/* 半剖外轮廓，缩在主图右上角 */}
      <g transform="translate(160, 12)" opacity="0.7">
        <path d="M 0 18
                 C 0 8, 12 0, 22 4
                 C 26 -4, 38 -2, 40 16
                 C 42 32, 30 44, 22 44
                 C 14 44, 0 32, 0 18 Z" />
        {/* 顶端凹 + 小果柄 */}
        <path d="M 18 4 Q 22 1, 26 4" />
        <path d="M 22 2 C 24 -4, 28 -8, 32 -10" />
        {/* 五瓣果心（star pattern）*/}
        <path d="M 22 22
                 L 14 18 L 17 27 L 22 30
                 L 27 27 L 30 18 Z" opacity="0.55" />
        {/* 两枚种子 */}
        <path d="M 16 26 C 14 28, 14 32, 17 33 C 19 31, 19 28, 16 26 Z" opacity="0.6" />
        <path d="M 28 26 C 30 28, 30 32, 27 33 C 25 31, 25 28, 28 26 Z" opacity="0.6" />
      </g>
    </g>
  </svg>
)

function EmptyHero({ onPickPrompt }) {
  return (
    <div className={styles.emptyState}>
      <div className={styles.emptyOrnament}>{APPLE_BOTANICAL}</div>
      <div className={styles.emptyBadge}>本科毕业设计 · 园艺专业</div>
      <div className={styles.emptyTitle}>把论文和基因表里散落的证据，连成可以追溯的回答</div>
      <div className={styles.emptyBody}>
        围绕硬度、颜色、酸度、糖度、采收期这几个果实品质性状，把已发表论文和人工整理的基因表打通成一个能直接问答的库。回答的每条引用都能点开看原文。
      </div>

      <div className={styles.statPills}>
        {STAT_PILLS.map((s, i) => (
          <span key={s.label} className={styles.statPill}>
            <span className={styles.statPillValue}>{s.value}</span>
            <span className={styles.statPillLabel}>{s.label}</span>
            {i < STAT_PILLS.length - 1 && <span className={styles.statPillDot}>◆</span>}
          </span>
        ))}
      </div>

      <div className={styles.archStrip}>
        {ARCH_NODES.map((n, i) => (
          <div key={n.label} className={styles.archGroup}>
            <div className={styles.archNode}>
              <div className={styles.archIcon}>{n.icon}</div>
              <div className={styles.archLabel}>{n.label}</div>
            </div>
            {i < ARCH_NODES.length - 1 && <div className={styles.archArrow}>→</div>}
          </div>
        ))}
      </div>

      <div className={styles.quickRowLabel}>从这些问题开始</div>
      <div className={styles.quickRow}>
        {QUICK_PROMPTS.map((prompt) => (
          <button key={prompt} className={styles.quickChip} onClick={() => onPickPrompt(prompt)}>
            {prompt}
          </button>
        ))}
      </div>
    </div>
  )
}

// ── About modal ───────────────────────────────────────────────────────────
function AboutModal({ open, onClose }) {
  const [shareUrl, setShareUrl] = useState('')
  useEffect(() => {
    if (typeof window !== 'undefined') setShareUrl(window.location.origin)
  }, [open])

  if (!open) return null
  const isLocalhost = /^(http:\/\/)?(localhost|127\.0\.0\.1|0\.0\.0\.0)/.test(shareUrl)
  const qrSrc = shareUrl
    ? `https://api.qrserver.com/v1/create-qr-code/?size=320x320&margin=14&qzone=2&color=1F2410&bgcolor=FAF4E4&data=${encodeURIComponent(shareUrl)}`
    : ''

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalCard} onClick={(e) => e.stopPropagation()}>
        <button className={styles.modalClose} onClick={onClose} aria-label="关闭">×</button>
        <div className={styles.modalEyebrow}>About</div>
        <h2 className={styles.modalTitle}>Apple Breeding RAG</h2>
        <p className={styles.modalLead}>
          本科毕业设计。把苹果育种相关的论文和人工整理的基因表合到一个能直接问答的库里，回答都附出处，方便核对。
        </p>

        {/* ── 扫码访问 ─ 放在最显眼的位置，方便答辩现场让听众扫码 ──── */}
        <div className={styles.qrBlock}>
          <div className={styles.qrFrame}>
            {qrSrc && <img src={qrSrc} className={styles.qrImage} alt={`扫码访问 ${shareUrl}`} />}
          </div>
          <div className={styles.qrSide}>
            <div className={styles.qrLabel}>扫码访问</div>
            <div className={styles.qrUrl}>{shareUrl || '…'}</div>
            <p className={styles.qrHint}>
              {isLocalhost
                ? '当前是本机地址，扫出来只能在这台电脑上打开。要让别人扫，请通过公网链接打开本页面，二维码会自动更新。'
                : '手机扫一下即可在你自己设备上打开同一个演示。'}
            </p>
          </div>
        </div>

        <div className={styles.modalSection}>
          <div className={styles.modalSectionTitle}>用到的东西</div>
          <div className={styles.modalChips}>
            <span className={styles.modalChip}>Next.js 14</span>
            <span className={styles.modalChip}>FastAPI</span>
            <span className={styles.modalChip}>Milvus 向量库</span>
            <span className={styles.modalChip}>BGE Embeddings</span>
            <span className={styles.modalChip}>DeepSeek / OpenAI 兼容</span>
            <span className={styles.modalChip}>Docker Compose</span>
          </div>
        </div>

        <div className={styles.modalSection}>
          <div className={styles.modalSectionTitle}>库里有什么</div>
          <ul className={styles.modalList}>
            <li>苹果育种相关论文 75 篇，覆盖 GWAS、QTL 和候选基因功能验证</li>
            <li>6 个性状的候选基因表：硬度、颜色、酸度、糖度、采收期，外加一个通用</li>
            <li>每条基因记录都标了性状、SNP、染色体位置和 P 值，方便核对</li>
          </ul>
        </div>

        <div className={styles.modalSection}>
          <div className={styles.modalSectionTitle}>能做什么</div>
          <ul className={styles.modalList}>
            <li>根据问题自动决定走论文、基因表，还是两边都查</li>
            <li>答案里 [1] [2] 可以点开，直接跳到对应的原文或基因记录</li>
            <li>支持上传新论文和基因表，可重建索引</li>
          </ul>
        </div>

        <div className={styles.modalFoot}>本科毕业设计 · 仅供学术与教学使用</div>
      </div>
    </div>
  )
}

// ── Files modal — 看 data/papers + data/genes 里实际有哪些文件 ────────────
function formatBytes(n) {
  if (!n && n !== 0) return ''
  if (n < 1024) return `${n} B`
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`
  return `${(n / 1024 / 1024).toFixed(1)} MB`
}

function FilesModal({ open, loading, data, onClose, onRefresh }) {
  if (!open) return null
  const papers = data?.papers || []
  const genes = data?.genes || []
  const err = data?.error
  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={`${styles.modalCard} ${styles.modalCardWide}`} onClick={(e) => e.stopPropagation()}>
        <button className={styles.modalClose} onClick={onClose} aria-label="关闭">×</button>
        <div className={styles.modalEyebrow}>文件夹</div>
        <h2 className={styles.modalTitle}>data 目录里的文件</h2>
        <p className={styles.modalLead}>
          这些是后端 <code className={styles.mdCode}>data/papers</code> 和 <code className={styles.mdCode}>data/genes</code> 里实际存在的文件。重建索引时会从这里读。
        </p>

        <div className={styles.filesActions}>
          <button className={styles.ghostBtn} onClick={onRefresh} disabled={loading}>
            {loading ? '读取中…' : '重新读取'}
          </button>
          {!loading && data && !err && (
            <span className={styles.filesSummary}>
              PDF {data.papers_count} 份 · 基因表 {data.genes_count} 份
            </span>
          )}
        </div>

        {err && <div className={styles.filesError}>读取失败：{err}</div>}

        {!err && (
          <div className={styles.filesGrid}>
            <section className={styles.filesPane}>
              <div className={styles.filesPaneHead}>
                <span>data/papers</span>
                <span className={styles.filesPaneCount}>{papers.length}</span>
              </div>
              {loading && !papers.length ? (
                <div className={styles.filesEmpty}>读取中…</div>
              ) : papers.length ? (
                <ul className={styles.filesList}>
                  {papers.map((f) => (
                    <li key={f.name} className={styles.filesItem}>
                      <span className={styles.filesName} title={f.name}>{f.name}</span>
                      <span className={styles.filesSize}>{formatBytes(f.size)}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <div className={styles.filesEmpty}>没有 PDF 文件</div>
              )}
            </section>

            <section className={styles.filesPane}>
              <div className={styles.filesPaneHead}>
                <span>data/genes</span>
                <span className={styles.filesPaneCount}>{genes.length}</span>
              </div>
              {loading && !genes.length ? (
                <div className={styles.filesEmpty}>读取中…</div>
              ) : genes.length ? (
                <ul className={styles.filesList}>
                  {genes.map((f) => (
                    <li key={f.name} className={styles.filesItem}>
                      <span className={styles.filesName} title={f.name}>{f.name}</span>
                      <span className={styles.filesSize}>{formatBytes(f.size)}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <div className={styles.filesEmpty}>没有基因表文件</div>
              )}
            </section>
          </div>
        )}
      </div>
    </div>
  )
}

export default function HomePage() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [lastQuestion, setLastQuestion] = useState('')
  const [copiedIdx, setCopiedIdx] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [opMsg, setOpMsg] = useState('')
  const [opLoading, setOpLoading] = useState('')
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [dataToolsOpen, setDataToolsOpen] = useState(false)
  const [aboutOpen, setAboutOpen] = useState(false)
  const [filesOpen, setFilesOpen] = useState(false)
  const [filesData, setFilesData] = useState(null)
  const [filesLoading, setFilesLoading] = useState(false)
  const [geneTarget, setGeneTarget] = useState('genes')
  const [llmOnly, setLlmOnly] = useState(false) // 关掉 RAG，让大模型直接答（用于对照）
  const [llmConfig, setLlmConfig] = useState({
    apiKey: '',
    baseUrl: 'https://api.deepseek.com',
    model: 'deepseek-chat'
  })

  const [chats, setChats] = useState([INITIAL_CHAT])
  const [activeChatId, setActiveChatId] = useState(INITIAL_CHAT.id)

  const paperInputRef = useRef(null)
  const geneInputRef = useRef(null)
  const threadRef = useRef(null)
  const textareaRef = useRef(null)

  const activeChat = useMemo(() => chats.find((c) => c.id === activeChatId) || chats[0], [chats, activeChatId])
  const threadHasMessages = Boolean(activeChat?.messages.length)
  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(LLM_STORAGE_KEY)
      if (!saved) return
      const parsed = JSON.parse(saved)
      setLlmConfig((prev) => ({
        ...prev,
        apiKey: parsed.apiKey || '',
        baseUrl: parsed.baseUrl || prev.baseUrl,
        model: parsed.model || prev.model
      }))
    } catch {}
    try {
      const saved = window.localStorage.getItem(CHATS_STORAGE_KEY)
      if (!saved) return
      const parsed = JSON.parse(saved)
      if (Array.isArray(parsed) && parsed.length) {
        setChats(parsed)
        setActiveChatId(parsed[0].id)
      }
    } catch {}
  }, [])

  useEffect(() => {
    try { window.localStorage.setItem(LLM_STORAGE_KEY, JSON.stringify(llmConfig)) } catch {}
  }, [llmConfig])

  useEffect(() => {
    try { window.localStorage.setItem(CHATS_STORAGE_KEY, JSON.stringify(chats)) } catch {}
  }, [chats])

  useEffect(() => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 220) + 'px'
  }, [question])

  // 末条 assistant 文本长度 — 流式时依此触发滚动
  const lastMsg = activeChat?.messages?.[activeChat.messages.length - 1]
  const lastMsgTextLen = lastMsg?.text?.length || 0
  const lastMsgStreaming = !!lastMsg?.streaming
  useEffect(() => {
    if (!threadRef.current) return
    const node = threadRef.current
    // 流式期间用瞬时滚动避免卡顿；切对话/收完回答时用平滑滚动
    node.scrollTo({
      top: node.scrollHeight,
      behavior: lastMsgStreaming ? 'auto' : 'smooth'
    })
  }, [activeChatId, activeChat?.messages.length, loading, lastMsgTextLen, lastMsgStreaming])

  function chatsOrNew(list) { return list.length ? list : [mkChat()] }

  function setActiveUpdater(updater) {
    setChats((prev) => { const next = updater(prev); return chatsOrNew(next) })
  }

  function newChat() {
    const c = mkChat()
    setChats((prev) => [c, ...prev])
    setActiveChatId(c.id)
    setQuestion('')
    setError('')
  }

  function deleteChat(chatId) {
    setChats((prev) => {
      const next = prev.filter((c) => c.id !== chatId)
      if (!next.length) {
        const fresh = mkChat()
        setActiveChatId(fresh.id)
        return [fresh]
      }
      if (chatId === activeChatId) setActiveChatId(next[0].id)
      return next
    })
  }

  function copyToClipboard(text, idx) {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedIdx(idx)
      setTimeout(() => setCopiedIdx(null), 2000)
    }).catch(() => {})
  }

  function clearLocalCache() {
    const ok = window.confirm('确定要清掉本地缓存吗？\n会删掉所有对话记录和 LLM 设置，并刷新页面。')
    if (!ok) return
    try {
      window.localStorage.removeItem(LLM_STORAGE_KEY)
      window.localStorage.removeItem(CHATS_STORAGE_KEY)
    } catch {}
    window.location.reload()
  }

  async function openFilesModal() {
    setFilesOpen(true)
    if (filesData) return
    setFilesLoading(true)
    try {
      const res = await fetch(`${API_BASE}/api/files`)
      const data = await readJsonOrThrow(res)
      setFilesData(data)
    } catch (e) {
      setFilesData({ error: e.message })
    } finally {
      setFilesLoading(false)
    }
  }

  async function refreshFiles() {
    setFilesLoading(true)
    try {
      const res = await fetch(`${API_BASE}/api/files`)
      const data = await readJsonOrThrow(res)
      setFilesData(data)
    } catch (e) {
      setFilesData({ error: e.message })
    } finally {
      setFilesLoading(false)
    }
  }

  function exportAnswerAsMd(msgIdx) {
    if (!activeChat) return
    const msg = activeChat.messages[msgIdx]
    if (!msg || msg.role !== 'assistant') return
    const userPrev = activeChat.messages[msgIdx - 1]
    const lines = []
    lines.push(`# ${activeChat.title || 'Apple Breeding RAG'}`)
    lines.push('')
    lines.push(`> 导出时间：${new Date().toLocaleString('zh-CN')}`)
    lines.push(`> 路由：${msg.routeUsed || 'auto'}`)
    lines.push('')
    if (userPrev?.role === 'user') {
      lines.push('## 提问')
      lines.push('')
      lines.push(userPrev.text)
      lines.push('')
    }
    lines.push('## 回答')
    lines.push('')
    lines.push(msg.text || '')
    lines.push('')
    if (Array.isArray(msg.sources) && msg.sources.length) {
      lines.push('## 引用与证据')
      lines.push('')
      msg.sources.forEach((s, i) => {
        lines.push(`### [${i + 1}] ${sourceTypeDisplay(s.source_type)}${s.title ? ` — ${s.title}` : ''}`)
        if (s.page) lines.push(`- 页码：p.${s.page}`)
        lines.push('')
        lines.push(s.chunk_text || '')
        lines.push('')
      })
    }
    const blob = new Blob([lines.join('\n')], { type: 'text/markdown;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    const safe = (activeChat.title || 'answer').replace(/[\\/:*?"<>|]/g, '_')
    a.download = `${safe}-${msgIdx + 1}.md`
    a.click()
    URL.revokeObjectURL(url)
  }

  async function readJsonOrThrow(res) {
    const data = await res.json().catch(() => ({}))
    if (!res.ok) { const detail = data?.detail || `HTTP ${res.status}`; throw new Error(detail) }
    return data
  }

  // 把 assistant 消息往当前 chat 末尾追加一条（增量更新用）
  function appendAssistantMessage(chatId, initial) {
    setActiveUpdater((prev) =>
      prev.map((chat) =>
        chat.id === chatId
          ? { ...chat, messages: [...chat.messages, { role: 'assistant', ...initial }] }
          : chat
      )
    )
  }

  // 改最后一条 assistant 消息的部分字段（增量 delta 累加用）
  function updateLastAssistantMessage(chatId, patcher) {
    setActiveUpdater((prev) =>
      prev.map((chat) => {
        if (chat.id !== chatId) return chat
        if (!chat.messages.length) return chat
        const last = chat.messages[chat.messages.length - 1]
        if (last.role !== 'assistant') return chat
        const next = patcher(last)
        return { ...chat, messages: [...chat.messages.slice(0, -1), next] }
      })
    )
  }

  async function streamFromSSE(res, { onMeta, onDelta, onAudit }) {
    if (!res.body) throw new Error('该浏览器不支持流式响应')
    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    let buf = ''
    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      buf += decoder.decode(value, { stream: true })
      // 按 SSE 协议双换行分块
      let sep
      while ((sep = buf.indexOf('\n\n')) !== -1) {
        const raw = buf.slice(0, sep)
        buf = buf.slice(sep + 2)
        if (!raw.trim()) continue
        let evt = 'message', dataStr = ''
        for (const line of raw.split('\n')) {
          if (line.startsWith('event:')) evt = line.slice(6).trim()
          else if (line.startsWith('data:')) dataStr += line.slice(5).trim()
        }
        let data = {}
        try { data = dataStr ? JSON.parse(dataStr) : {} } catch {}
        if (evt === 'meta' && onMeta) onMeta(data)
        else if (evt === 'delta' && onDelta) onDelta(data)
        else if (evt === 'audit' && onAudit) onAudit(data)
        else if (evt === 'done') return
      }
    }
  }

  async function ask(retryText) {
    const sourceText = typeof retryText === 'string' ? retryText : question
    const q = sourceText.trim()
    if (!q || !activeChat) return
    const chatId = activeChat.id
    setQuestion('')
    setLastQuestion(q)
    setLoading(true)
    setError('')

    setActiveUpdater((prev) =>
      prev.map((chat) =>
        chat.id === chatId
          ? { ...chat, title: chat.messages.length ? chat.title : trimTitle(q), messages: [...chat.messages, { role: 'user', text: q }] }
          : chat
      )
    )

    // 先占位一条空 assistant，后续 delta 直接累加上去
    appendAssistantMessage(chatId, { text: '', routeUsed: null, sources: [], streaming: true, audit: null })

    try {
      const res = await fetch(`${API_BASE}/api/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
        body: JSON.stringify({
          question: q,
          top_k: 6,
          route: llmOnly ? 'llm_only' : 'auto',
          llm_api_key: llmConfig.apiKey.trim() || undefined,
          llm_base_url: llmConfig.baseUrl.trim() || undefined,
          llm_model: llmConfig.model.trim() || undefined
        })
      })
      if (!res.ok) {
        const detail = await res.text().catch(() => '')
        throw new Error(detail || `HTTP ${res.status}`)
      }

      await streamFromSSE(res, {
        onMeta: ({ route, sources }) => {
          updateLastAssistantMessage(chatId, (m) => ({
            ...m,
            routeUsed: route || m.routeUsed,
            sources: Array.isArray(sources) ? sources : m.sources
          }))
        },
        onDelta: ({ text }) => {
          if (!text) return
          updateLastAssistantMessage(chatId, (m) => ({ ...m, text: (m.text || '') + text }))
        },
        onAudit: (audit) => {
          updateLastAssistantMessage(chatId, (m) => ({ ...m, audit }))
        }
      })

      // 流结束，去掉 streaming 标记
      updateLastAssistantMessage(chatId, (m) => ({ ...m, streaming: false }))
    } catch (e) {
      setError(e.message)
      // 流失败：删掉那条空 assistant 占位（如果还是空且 streaming）
      updateLastAssistantMessage(chatId, (m) =>
        m.streaming && !m.text
          ? { ...m, streaming: false, text: '（请求失败：' + e.message + '）' }
          : { ...m, streaming: false }
      )
    } finally {
      setLoading(false)
    }
  }

  async function rebuildPapers() {
    setOpLoading('papers-reindex'); setError(''); setOpMsg('')
    try {
      const res = await fetch(`${API_BASE}/api/ingest/papers`, { method: 'POST' })
      const data = await readJsonOrThrow(res)
      setOpMsg(`论文重建完成：${data.inserted} 条 -> ${data.collection}`)
    } catch (e) { setError(e.message) }
    finally { setOpLoading('') }
  }

  async function rebuildGenes() {
    setOpLoading('genes-reindex'); setError(''); setOpMsg('')
    try {
      const pathByCollection = {
        genes: '/api/ingest/genes', genes_firmness: '/api/ingest/genes_firmness',
        genes_color: '/api/ingest/genes_color', genes_acidity: '/api/ingest/genes_acidity',
        genes_harvest: '/api/ingest/genes_harvest', genes_sugar: '/api/ingest/genes_sugar'
      }
      const res = await fetch(`${API_BASE}${pathByCollection[geneTarget] || '/api/ingest/genes'}`, { method: 'POST' })
      const data = await readJsonOrThrow(res)
      setOpMsg(`基因重建完成：${data.inserted} 条 -> ${data.collection}`)
    } catch (e) { setError(e.message) }
    finally { setOpLoading('') }
  }

  async function uploadPapers(e) {
    const files = Array.from(e.target.files || [])
    if (!files.length) return
    setOpLoading('papers-upload'); setError(''); setOpMsg('')
    try {
      const form = new FormData()
      files.forEach((file) => form.append('files', file))
      const res = await fetch(`${API_BASE}/api/upload/papers?ingest=true`, { method: 'POST', body: form })
      const data = await readJsonOrThrow(res)
      setOpMsg(`已上传 ${data.saved_count} 份论文，已导入 ${data.inserted} 条`)
    } catch (err) { setError(err.message) }
    finally { e.target.value = ''; setOpLoading('') }
  }

  async function uploadGenes(e) {
    const file = e.target.files?.[0]
    if (!file) return
    setOpLoading('genes-upload'); setError(''); setOpMsg('')
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await fetch(`${API_BASE}/api/upload/genes?ingest=true&collection=${encodeURIComponent(geneTarget)}`, { method: 'POST', body: form })
      const data = await readJsonOrThrow(res)
      setOpMsg(`已上传 ${data.saved_file}，已导入 ${data.inserted} 条 -> ${data.collection}`)
    } catch (err) { setError(err.message) }
    finally { e.target.value = ''; setOpLoading('') }
  }

  function handleComposerKeyDown(e) {
    if (e.key !== 'Enter' || e.shiftKey || e.nativeEvent?.isComposing) return
    e.preventDefault()
    ask()
  }

  return (
    <main className={styles.page}>
      <AboutModal open={aboutOpen} onClose={() => setAboutOpen(false)} />
      <FilesModal
        open={filesOpen}
        loading={filesLoading}
        data={filesData}
        onClose={() => setFilesOpen(false)}
        onRefresh={refreshFiles}
      />
      <div className={styles.app}>
        <aside className={styles.sidebar}>
          <div className={styles.sideTop}>
            <div className={styles.brandWrap}>
              <div className={styles.brandMark}>
                <img className={styles.brandLogo} src="/nwafu-logo.png" alt="西北农林科技大学校徽" />
              </div>
              <div>
                <div className={styles.brand}>Apple Breeding RAG</div>
              </div>
            </div>
            <div className={styles.sideTopActions}>
              <button className={styles.newChatBtn} onClick={newChat}>+ 新建对话</button>
              <button className={styles.sidebarToggle} onClick={() => setSidebarOpen((v) => !v)}>
                {sidebarOpen ? '收起对话列表' : '展开对话列表'}
              </button>
            </div>
          </div>

          <div className={`${styles.sidebarBody} ${sidebarOpen ? styles.sidebarBodyOpen : ''}`}>
            <div className={styles.sideSectionTitle}>对话历史</div>
            <ul className={styles.chatList}>
              {chats.map((chat) => (
                <li
                  key={chat.id}
                  className={`${styles.chatItemWrap} ${chat.id === activeChat?.id ? styles.chatItemWrapActive : ''}`}
                >
                  <button
                    className={styles.chatItem}
                    onClick={() => setActiveChatId(chat.id)}
                    title={chat.title}
                  >
                    <span className={styles.chatItemTitle}>{chat.title}</span>
                  </button>
                  <button
                    className={styles.chatDeleteBtn}
                    onClick={(e) => { e.stopPropagation(); deleteChat(chat.id) }}
                    title="删除对话"
                    aria-label="删除对话"
                  >
                    ×
                  </button>
                </li>
              ))}
            </ul>
          </div>

          <div className={styles.sidebarFoot}>
            <div className={styles.sidebarFootLine}>本科毕业设计</div>
            <div className={styles.sidebarFootDim}>园艺专业 · v1.0</div>
          </div>
        </aside>

        <section className={styles.mainPane}>
          <input ref={paperInputRef} type="file" accept=".pdf" multiple hidden onChange={uploadPapers} />
          <input ref={geneInputRef} type="file" accept=".csv,.tsv,text/csv,text/tab-separated-values" hidden onChange={uploadGenes} />

          <header className={`${styles.topBar} ${threadHasMessages ? styles.topBarCompact : ''}`}>
            <div className={styles.topTitleBlock}>
              <div className={styles.eyebrow}>本科毕业设计 · APPLE BREEDING RAG</div>
              <h1 className={`${styles.heroTitle} ${threadHasMessages ? styles.heroTitleCompact : ''}`}>
                {threadHasMessages ? activeChat?.title || '新的研究问题' : '苹果育种文献与基因问答'}
              </h1>
              <p className={`${styles.heroLead} ${threadHasMessages ? styles.heroLeadCompact : ''}`}>
                {threadHasMessages
                  ? '可以继续追问，或者换个性状、换篇论文再找一次。'
                  : '本科毕业设计。把苹果育种领域的论文和人工整理的基因位点表合并到一个库里，能直接提问，回答全部附出处。'}
              </p>
            </div>
            <div className={styles.toolbar}>
              <button
                className={styles.ghostBtn}
                onClick={openFilesModal}
                title="看看现在库里有哪些 PDF 和基因表"
              >
                文件夹
              </button>
              <button
                className={styles.ghostBtn}
                onClick={clearLocalCache}
                title="清掉浏览器里存的对话和 LLM 配置"
              >
                刷新缓存
              </button>
              <button
                className={styles.ghostBtn}
                onClick={() => setAboutOpen(true)}
                title="关于本项目"
              >
                关于
              </button>
              <button
                className={`${styles.ghostBtn} ${dataToolsOpen ? styles.ghostBtnActive : ''}`}
                onClick={() => { setDataToolsOpen((v) => !v); setSettingsOpen(false) }}
              >
                {dataToolsOpen ? '收起数据与索引' : '数据与索引'}
              </button>
              <button
                className={`${styles.ghostBtn} ${settingsOpen ? styles.ghostBtnActive : ''}`}
                onClick={() => { setSettingsOpen((v) => !v); setDataToolsOpen(false) }}
              >
                {settingsOpen ? '收起 LLM 设置' : '配置 LLM Key'}
              </button>
            </div>
          </header>

          {dataToolsOpen && (
            <section className={styles.settingsCard}>
              <div className={styles.settingsTitle}>数据与索引</div>
              <div className={styles.dataToolsGrid}>
                <div className={styles.toolSection}>
                  <div className={styles.toolSectionHeader}>
                    <div className={styles.toolSectionTitle}>论文 PDF</div>
                    <div className={styles.toolSectionDesc}>
                      上传只会把这次选中的 PDF 追加进当前 `papers` collection；全量重建会重新读取 `backend/data/papers` 并覆盖整个论文索引。
                    </div>
                  </div>
                  <div className={styles.dataToolsBtnRow}>
                    <button className={styles.primaryBtn} onClick={() => paperInputRef.current?.click()} disabled={!!opLoading}>
                      {opLoading === 'papers-upload' ? '上传中...' : '上传 PDF 并立即入库'}
                    </button>
                    <button className={styles.ghostBtn} onClick={rebuildPapers} disabled={opLoading === 'papers-reindex'}>
                      {opLoading === 'papers-reindex' ? '重建中...' : '全量重建论文库'}
                    </button>
                  </div>
                </div>

                <div className={styles.toolSection}>
                  <div className={styles.toolSectionHeader}>
                    <div className={styles.toolSectionTitle}>基因表</div>
                    <div className={styles.toolSectionDesc}>
                      先选择目标 collection，再决定是上传新 CSV 还是用默认文件全量重建该集合。
                    </div>
                  </div>
                  <div className={styles.dataToolsGroup}>
                    <div className={styles.dataToolsGroupLabel}>目标 collection</div>
                    <select
                      className={styles.select}
                      value={geneTarget}
                      onChange={(e) => setGeneTarget(e.target.value)}
                    >
                      {GENE_TARGETS.map((item) => (
                        <option key={item.value} value={item.value}>{item.label}</option>
                      ))}
                    </select>
                  </div>
                  <div className={styles.dataToolsBtnRow}>
                    <button className={styles.primaryBtn} onClick={() => geneInputRef.current?.click()} disabled={!!opLoading}>
                      {opLoading === 'genes-upload' ? '上传中...' : '上传基因 CSV'}
                    </button>
                    <button className={styles.ghostBtn} onClick={rebuildGenes} disabled={opLoading === 'genes-reindex'}>
                      {opLoading === 'genes-reindex' ? '重建中...' : '重建所选基因集合'}
                    </button>
                  </div>
                </div>
              </div>
              <p className={styles.tip}>
                上传是把新文件追加进当前库；全量重建会把对应 collection 整个清掉、按本地文件重新跑一遍。两件事不要搞混。
              </p>
            </section>
          )}

          {settingsOpen && (
            <section className={styles.settingsCard}>
              <div className={styles.settingsTitle}>LLM 设置</div>
              <div className={styles.settingsGrid}>
                <label className={styles.field}>
                  <span>API Key</span>
                  <input
                    className={styles.input}
                    type="password"
                    value={llmConfig.apiKey}
                    onChange={(e) => setLlmConfig((prev) => ({ ...prev, apiKey: e.target.value }))}
                    placeholder="输入你的 API Key"
                  />
                </label>
                <label className={styles.field}>
                  <span>Base URL</span>
                  <input
                    className={styles.input}
                    value={llmConfig.baseUrl}
                    onChange={(e) => setLlmConfig((prev) => ({ ...prev, baseUrl: e.target.value }))}
                    placeholder="https://api.deepseek.com"
                  />
                </label>
                <label className={styles.field}>
                  <span>Model</span>
                  <input
                    className={styles.input}
                    value={llmConfig.model}
                    onChange={(e) => setLlmConfig((prev) => ({ ...prev, model: e.target.value }))}
                    placeholder="deepseek-chat"
                  />
                </label>
              </div>
              <p className={styles.tip}>
                当前配置只保存在这个浏览器的本地存储中；提问时会随请求发送给后端，不会写回仓库或 <code className={styles.mdCode}>.env</code>。
              </p>
            </section>
          )}

          <div className={styles.threadShell}>
            <div className={styles.thread} ref={threadRef}>
              {threadHasMessages ? (
                <>
                  {(() => {
                    const lastAssistantIdx = (() => {
                      for (let j = activeChat.messages.length - 1; j >= 0; j--) {
                        if (activeChat.messages[j].role === 'assistant') return j
                      }
                      return -1
                    })()
                    return activeChat.messages.map((m, i) => (
                      <article key={i} className={`${styles.msg} ${m.role === 'user' ? styles.msgUser : styles.msgAssistant}`}>
                        <div className={styles.msgHeader}>
                          <div className={styles.msgRole}>{m.role === 'user' ? '你' : '助手'}</div>
                          <div className={styles.msgHeaderRight}>
                            {m.role === 'assistant' && (
                              <>
                                <button className={styles.copyBtn} onClick={() => copyToClipboard(m.text, i)} title="复制回答">
                                  {copiedIdx === i ? '已复制' : '复制'}
                                </button>
                                <button className={styles.copyBtn} onClick={() => exportAnswerAsMd(i)} title="导出为 Markdown">
                                  导出 .md
                                </button>
                              </>
                            )}
                            {m.role === 'assistant' && <div className={styles.msgBadge}>Research Response</div>}
                          </div>
                        </div>
                        {m.role === 'assistant' ? (() => {
                          const sourceCount = Array.isArray(m.sources) ? m.sources.length : 0
                          const articleId = `msg-${i}`
                          const ctx = { articleId, sourceCount }
                          const { tldr, body } = extractTldr(m.text)
                          // 流式中且还没出字 → 显示 pipeline；有字了 → 渲染 markdown
                          if (m.streaming && !m.text) {
                            return <PipelineLoader />
                          }
                          return (
                            <>
                              {tldr && (
                                <div className={styles.tldrCallout}>
                                  <span className={styles.tldrTag} aria-label="结论" />
                                  <div className={styles.tldrText}>{parseInline(tldr, `tldr${i}`, ctx)}</div>
                                </div>
                              )}
                              <MarkdownBlock text={body} ctx={ctx} />
                              {m.streaming && <span className={styles.streamingCursor} aria-hidden="true" />}
                            </>
                          )
                        })() : (
                          <div className={styles.msgTextUser}>{m.text}</div>
                        )}
                        {m.role === 'assistant' && (
                          <>
                            <div className={styles.msgMetaRow}>
                              {m.routeUsed === 'llm_only' ? (
                                <span className={`${styles.metaPill} ${styles.routePillBare}`}>纯模型 · 无 RAG</span>
                              ) : (
                                <>
                                  <span className={`${styles.metaPill} ${styles.routePill}`}>route · {m.routeUsed || 'auto'}</span>
                                  <span className={`${styles.metaPill} ${styles.routePillAccent}`}>
                                    {(Array.isArray(m.sources) ? m.sources.length : 0)} 张证据卡片
                                  </span>
                                </>
                              )}
                            </div>
                            {Array.isArray(m.sources) && m.sources.length > 0 && (
                              <details id={`msg-${i}-details`} className={styles.evidenceBox} open={i === lastAssistantIdx}>
                                <summary className={styles.evidenceSummary}>
                                  <span>查看引用与证据卡片</span>
                                  <span className={styles.evidenceSummaryCount}>{m.sources.length}</span>
                                </summary>
                                <ul className={styles.evidenceList}>
                                  {m.sources.map((s, idx) => {
                                    const fields = parseEvidenceFields(s.chunk_text)
                                    return (
                                      <li key={idx} id={`msg-${i}-src-${idx}`} className={styles.evidenceItem}>
                                        <div className={styles.evidenceHead}>
                                          <span className={styles.evidenceIndex}>[{idx + 1}]</span>
                                          <span className={styles.evidenceType}>{sourceTypeDisplay(s.source_type)}</span>
                                          {fields.chr ? <span className={styles.evidenceChr}>Chr {String(fields.chr).replace(/^Chr/i, '')}</span> : null}
                                          {fields.pvalue ? <span className={styles.evidencePvalue}>P {fields.pvalue}</span> : null}
                                          {s.page ? <span className={styles.evidenceMeta}>p.{s.page}</span> : null}
                                        </div>
                                        {s.title ? <div className={styles.evidenceTitle}>{s.title}</div> : null}
                                        <EvidenceCardBody source={s} />
                                      </li>
                                    )
                                  })}
                                </ul>
                              </details>
                            )}
                          </>
                        )}
                      </article>
                    ))
                  })()}
                  {/* 流式期间 pipeline 直接画进 assistant 气泡里，不再单独占一行 */}
                </>
              ) : (
                <EmptyHero onPickPrompt={setQuestion} />
              )}
            </div>
          </div>

          {opMsg && <div className={`${styles.statusBar} ${styles.statusBarSuccess}`}>{opMsg}</div>}
          {error && (
            <div className={`${styles.statusBar} ${styles.statusBarError} ${styles.statusBarWithAction}`}>
              <span>错误：{error}</span>
              {lastQuestion && <button className={styles.retryBtn} onClick={() => ask(lastQuestion)}>重试</button>}
            </div>
          )}

          <footer className={styles.composerShell}>
            {threadHasMessages && (
              <div className={styles.composerQuickRow}>
                {QUICK_PROMPTS.slice(0, 3).map((prompt) => (
                  <button key={prompt} className={styles.composerQuickChip} onClick={() => setQuestion(prompt)}>
                    {prompt}
                  </button>
                ))}
              </div>
            )}
            <div className={styles.inputBar}>
              <textarea
                ref={textareaRef}
                className={styles.textarea}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={handleComposerKeyDown}
                placeholder="例如：哪些基因位点与苹果果肉硬度保持有关？"
              />
              <div className={styles.composerFooter}>
                <div className={styles.composerMeta}>
                  <button
                    type="button"
                    className={`${styles.modePill} ${llmOnly ? styles.modePillBare : styles.modePillRag}`}
                    onClick={() => setLlmOnly((v) => !v)}
                    title={llmOnly
                      ? '当前：仅大模型直答（不查论文与基因表）。点击切回 RAG。'
                      : '当前：RAG 检索 + 大模型生成。点击切到纯模型对照模式。'}
                  >
                    <span className={styles.modePillDot} />
                    {llmOnly ? '纯模型 · 无 RAG' : 'RAG · 自动路由'}
                  </button>
                  <span className={styles.metaPill}>{geneTargetDisplay(geneTarget)}</span>
                  <span className={styles.metaPill}>{llmConfig.apiKey ? '大模型已配置' : '未配置大模型'}</span>
                </div>
                <div className={styles.composerHint}>Enter 发送 · Shift+Enter 换行</div>
                <button className={styles.askBtn} onClick={() => ask()} disabled={loading || !question.trim()}>
                  {loading ? '检索中...' : '发送'}
                </button>
              </div>
            </div>
          </footer>
        </section>
      </div>
    </main>
  )
}
