'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import styles from './page.module.css'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'
const INITIAL_CHAT = mkChat()
const LLM_STORAGE_KEY = 'apple-breeding-rag-llm-config'
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

// ── Markdown renderer ──────────────────────────────────────────────────────
function parseInline(text, prefix = '') {
  const out = []
  let rem = text
  let k = 0

  while (rem.length) {
    // bold **...**
    const b = rem.match(/\*\*(.+?)\*\*/)
    // italic *...*
    const it = rem.match(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/)
    // inline code `...`
    const ic = rem.match(/`([^`]+)`/)

    const candidates = [
      b && { type: 'b', m: b },
      it && { type: 'i', m: it },
      ic && { type: 'c', m: ic }
    ].filter(Boolean).sort((a, b2) => a.m.index - b2.m.index)

    if (!candidates.length) { out.push(rem); break }

    const { type, m } = candidates[0]
    if (m.index > 0) out.push(rem.slice(0, m.index))
    if (type === 'b') out.push(<strong key={`${prefix}b${k++}`}>{m[1]}</strong>)
    else if (type === 'i') out.push(<em key={`${prefix}i${k++}`}>{m[1]}</em>)
    else out.push(<code key={`${prefix}c${k++}`} className={styles.mdCode}>{m[1]}</code>)
    rem = rem.slice(m.index + m[0].length)
  }
  return out
}

function MarkdownBlock({ text }) {
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
      els.push(<Tag key={k++} className={styles[`mdH${lvl}`]}>{parseInline(hm[2], `h${k}`)}</Tag>)
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
          {ql.map((l, j) => <p key={j}>{parseInline(l, `bq${j}`)}</p>)}
        </blockquote>
      )
      continue
    }

    // unordered list
    if (/^[-*+]\s/.test(line)) {
      const items = []
      while (i < lines.length && /^[-*+]\s/.test(lines[i])) {
        items.push(<li key={i}>{parseInline(lines[i].replace(/^[-*+]\s+/, ''), `ul${i}`)}</li>)
        i++
      }
      els.push(<ul key={k++} className={styles.mdUl}>{items}</ul>)
      continue
    }

    // ordered list
    if (/^\d+\.\s/.test(line)) {
      const items = []
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) {
        items.push(<li key={i}>{parseInline(lines[i].replace(/^\d+\.\s+/, ''), `ol${i}`)}</li>)
        i++
      }
      els.push(<ol key={k++} className={styles.mdOl}>{items}</ol>)
      continue
    }

    // empty line → skip (margin between paragraphs handles spacing)
    if (!line.trim()) { i++; continue }

    // paragraph
    els.push(<p key={k++} className={styles.mdP}>{parseInline(line, `p${k}`)}</p>)
    i++
  }

  return <div className={styles.markdownContent}>{els}</div>
}
// ──────────────────────────────────────────────────────────────────────────

export default function HomePage() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [opMsg, setOpMsg] = useState('')
  const [opLoading, setOpLoading] = useState('')
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [dataToolsOpen, setDataToolsOpen] = useState(false)
  const [geneTarget, setGeneTarget] = useState('genes')
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
  }, [])

  useEffect(() => {
    try { window.localStorage.setItem(LLM_STORAGE_KEY, JSON.stringify(llmConfig)) } catch {}
  }, [llmConfig])

  useEffect(() => {
    if (!threadRef.current) return
    const node = threadRef.current
    node.scrollTo({ top: node.scrollHeight, behavior: 'smooth' })
  }, [activeChatId, activeChat?.messages.length, loading])

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

  async function readJsonOrThrow(res) {
    const data = await res.json().catch(() => ({}))
    if (!res.ok) { const detail = data?.detail || `HTTP ${res.status}`; throw new Error(detail) }
    return data
  }

  async function ask() {
    if (!question.trim() || !activeChat) return
    const q = question.trim()
    setQuestion('')
    setLoading(true)
    setError('')

    setActiveUpdater((prev) =>
      prev.map((chat) =>
        chat.id === activeChat.id
          ? { ...chat, title: chat.messages.length ? chat.title : trimTitle(q), messages: [...chat.messages, { role: 'user', text: q }] }
          : chat
      )
    )

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: q,
          top_k: 6,
          route: 'auto',
          llm_api_key: llmConfig.apiKey.trim() || undefined,
          llm_base_url: llmConfig.baseUrl.trim() || undefined,
          llm_model: llmConfig.model.trim() || undefined
        })
      })
      const data = await readJsonOrThrow(res)
      setActiveUpdater((prev) =>
        prev.map((chat) =>
          chat.id === activeChat.id
            ? { ...chat, messages: [...chat.messages, { role: 'assistant', text: data.answer || '', routeUsed: data.route_used, sources: data.sources || [] }] }
            : chat
        )
      )
    } catch (e) {
      setError(e.message)
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
      <div className={styles.app}>
        <aside className={styles.sidebar}>
          <div className={styles.sideTop}>
            <div className={styles.brandWrap}>
              <div className={styles.brandMark}>AP</div>
              <div>
                <div className={styles.brand}>Apple Breeding RAG</div>
                <div className={styles.brandSub}>Yellow-green research workspace</div>
              </div>
            </div>
            <button className={styles.newChatBtn} onClick={newChat}>+ 新建对话</button>
          </div>

          <div className={styles.sideSectionTitle}>Recent Threads</div>
          <ul className={styles.chatList}>
            {chats.map((chat) => (
              <li key={chat.id}>
                <button
                  className={`${styles.chatItem} ${chat.id === activeChat?.id ? styles.chatItemActive : ''}`}
                  onClick={() => setActiveChatId(chat.id)}
                >
                  {chat.title}
                </button>
              </li>
            ))}
          </ul>
        </aside>

        <section className={styles.mainPane}>
          <input ref={paperInputRef} type="file" accept=".pdf" multiple hidden onChange={uploadPapers} />
          <input ref={geneInputRef} type="file" accept=".csv,.tsv,text/csv,text/tab-separated-values" hidden onChange={uploadGenes} />

          <header className={`${styles.topBar} ${threadHasMessages ? styles.topBarCompact : ''}`}>
            <div className={styles.heroOrnamentA} />
            <div className={styles.heroOrnamentB} />
            <div className={styles.heroLeaf} />
            <div className={styles.topTitleBlock}>
              <div className={styles.eyebrow}>Apple Quality Knowledge Studio</div>
              <h1 className={`${styles.heroTitle} ${threadHasMessages ? styles.heroTitleCompact : ''}`}>
                {threadHasMessages ? activeChat?.title || 'Research Session' : 'What should we discover in apples today?'}
              </h1>
              <p className={`${styles.heroLead} ${threadHasMessages ? styles.heroLeadCompact : ''}`}>
                {threadHasMessages
                  ? '继续围绕这条研究线索，补充论文证据、候选基因和 trait-specific 检索结果。'
                  : '面向苹果育种毕业设计的论文、基因与性状证据工作台。'}
              </p>
            </div>
            <div className={styles.toolbar}>
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
                设计上把“上传追加”和“全量重建”分开，是因为它们对应两种完全不同的后端行为：前者是增量加入，后者是替换整个 collection。
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
                  {activeChat.messages.map((m, i) => (
                    <article key={i} className={`${styles.msg} ${m.role === 'user' ? styles.msgUser : styles.msgAssistant}`}>
                      <div className={styles.msgHeader}>
                        <div className={styles.msgRole}>{m.role === 'user' ? '你' : '助手'}</div>
                        {m.role === 'assistant' && <div className={styles.msgBadge}>Research Response</div>}
                      </div>
                      {m.role === 'assistant' ? (
                        <MarkdownBlock text={m.text} />
                      ) : (
                        <div className={styles.msgTextUser}>{m.text}</div>
                      )}
                      {m.role === 'assistant' && (
                        <>
                          <div className={styles.msgMetaRow}>
                            <span className={`${styles.metaPill} ${styles.routePill}`}>route · {m.routeUsed || 'auto'}</span>
                            <span className={`${styles.metaPill} ${styles.routePillAccent}`}>
                              {(Array.isArray(m.sources) ? m.sources.length : 0)} source cards
                            </span>
                          </div>
                          {Array.isArray(m.sources) && m.sources.length > 0 && (
                            <details className={styles.evidenceBox}>
                              <summary className={styles.evidenceSummary}>
                                <span>查看引用与证据卡片</span>
                                <span className={styles.evidenceSummaryCount}>{m.sources.length}</span>
                              </summary>
                              <ul className={styles.evidenceList}>
                                {m.sources.map((s, idx) => (
                                  <li key={idx} className={styles.evidenceItem}>
                                    <div className={styles.evidenceHead}>
                                      <span className={styles.evidenceIndex}>[{idx + 1}]</span>
                                      <span className={styles.evidenceType}>{s.source_type}</span>
                                      {s.page ? <span className={styles.evidenceMeta}>p.{s.page}</span> : null}
                                    </div>
                                    {s.title ? <div className={styles.evidenceTitle}>{s.title}</div> : null}
                                    <p>{s.chunk_text}</p>
                                  </li>
                                ))}
                              </ul>
                            </details>
                          )}
                        </>
                      )}
                    </article>
                  ))}
                  {loading && (
                    <article className={`${styles.msg} ${styles.msgAssistant}`}>
                      <div className={styles.msgRole}>助手</div>
                      <div className={styles.loadingDots}>
                        <span /><span /><span />
                      </div>
                    </article>
                  )}
                </>
              ) : (
                <div className={styles.emptyState}>
                  <div className={styles.emptyBadge}>Apple Breeding Assistant</div>
                  <div className={styles.emptyTitle}>从文献、基因和性状里，快速拼出一条可验证的育种证据链。</div>
                  <div className={styles.emptyBody}>
                    你可以直接提问，也可以先上传新的 PDF 和基因表。当前界面支持即时上传后检索，并可为本地浏览器单独配置 LLM。
                  </div>
                  <div className={styles.quickRow}>
                    {QUICK_PROMPTS.map((prompt) => (
                      <button key={prompt} className={styles.quickChip} onClick={() => setQuestion(prompt)}>
                        {prompt}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {opMsg && <div className={`${styles.statusBar} ${styles.statusBarSuccess}`}>{opMsg}</div>}
          {error && <p className={`${styles.statusBar} ${styles.statusBarError}`}>错误：{error}</p>}

          <footer className={styles.composerShell}>
            <div className={styles.composerQuickRow}>
              {QUICK_PROMPTS.slice(0, threadHasMessages ? 3 : QUICK_PROMPTS.length).map((prompt) => (
                <button key={prompt} className={styles.composerQuickChip} onClick={() => setQuestion(prompt)}>
                  {prompt}
                </button>
              ))}
            </div>
            <div className={styles.inputBar}>
              <textarea
                className={styles.textarea}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={handleComposerKeyDown}
                placeholder="例如：哪些基因位点与苹果果肉硬度保持有关？"
                rows={3}
              />
              <div className={styles.composerFooter}>
                <div className={styles.composerMeta}>
                  <span className={styles.metaPill}>Route auto</span>
                  <span className={styles.metaPill}>{geneTarget}</span>
                  <span className={styles.metaPill}>{llmConfig.apiKey ? 'LLM on' : 'LLM fallback'}</span>
                </div>
                <div className={styles.composerHint}>Enter 发送 · Shift+Enter 换行</div>
                <button className={styles.askBtn} onClick={ask} disabled={loading || !question.trim()}>
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
