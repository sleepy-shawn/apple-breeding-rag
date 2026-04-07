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
  { value: 'genes_acidity', label: '酸度 genes_acidity' }
]
const QUICK_PROMPTS = [
  'Ma1基因位点对苹果果实酸度有何影响？',
  'MdMYB10启动子中的R6重复序列对苹果花青素积累有何影响？',
  'MdNAC18基因启动子区域的InDel变体如何影响苹果果肉硬度和成熟时间？',
  '苹果育种中GWAS与QTL作图相比有什么优势？'
]
const PROJECT_STATUS = [
  { label: 'Pipeline', value: 'Online', tone: 'good' },
  { label: 'Workspace', value: 'Default', tone: 'warm' },
  { label: 'Mode', value: 'Trait-aware', tone: 'good' }
]
const DATA_STATUS = [
  { label: 'Papers', value: 'PDF ingest ready' },
  { label: 'Genes', value: 'General + trait collections' },
  { label: 'LLM', value: 'Browser local override supported' }
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

export default function HomePage() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [opMsg, setOpMsg] = useState('')
  const [opLoading, setOpLoading] = useState('')
  const [settingsOpen, setSettingsOpen] = useState(false)
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

  const activeChat = useMemo(() => chats.find((c) => c.id === activeChatId) || chats[0], [chats, activeChatId])

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
    try {
      window.localStorage.setItem(LLM_STORAGE_KEY, JSON.stringify(llmConfig))
    } catch {}
  }, [llmConfig])

  function chatsOrNew(list) {
    return list.length ? list : [mkChat()]
  }

  function setActiveUpdater(updater) {
    setChats((prev) => {
      const next = updater(prev)
      return chatsOrNew(next)
    })
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
    if (!res.ok) {
      const detail = data?.detail || `HTTP ${res.status}`
      throw new Error(detail)
    }
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
          ? {
              ...chat,
              title: chat.messages.length ? chat.title : trimTitle(q),
              messages: [...chat.messages, { role: 'user', text: q }]
            }
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
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: 'assistant',
                    text: data.answer || '',
                    routeUsed: data.route_used,
                    sources: data.sources || []
                  }
                ]
              }
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
    setOpLoading('papers-reindex')
    setError('')
    setOpMsg('')
    try {
      const res = await fetch(`${API_BASE}/api/ingest/papers`, { method: 'POST' })
      const data = await readJsonOrThrow(res)
      setOpMsg(`论文重建完成：${data.inserted} 条 -> ${data.collection}`)
    } catch (e) {
      setError(e.message)
    } finally {
      setOpLoading('')
    }
  }

  async function rebuildGenes() {
    setOpLoading('genes-reindex')
    setError('')
    setOpMsg('')
    try {
      const pathByCollection = {
        genes: '/api/ingest/genes',
        genes_firmness: '/api/ingest/genes_firmness',
        genes_color: '/api/ingest/genes_color',
        genes_acidity: '/api/ingest/genes_acidity'
      }
      const res = await fetch(`${API_BASE}${pathByCollection[geneTarget] || '/api/ingest/genes'}`, { method: 'POST' })
      const data = await readJsonOrThrow(res)
      setOpMsg(`基因重建完成：${data.inserted} 条 -> ${data.collection}`)
    } catch (e) {
      setError(e.message)
    } finally {
      setOpLoading('')
    }
  }

  async function uploadPapers(e) {
    const files = Array.from(e.target.files || [])
    if (!files.length) return
    setOpLoading('papers-upload')
    setError('')
    setOpMsg('')
    try {
      const form = new FormData()
      files.forEach((file) => form.append('files', file))
      const res = await fetch(`${API_BASE}/api/upload/papers?ingest=true`, {
        method: 'POST',
        body: form
      })
      const data = await readJsonOrThrow(res)
      setOpMsg(`已上传 ${data.saved_count} 份论文，已导入 ${data.inserted} 条`)
    } catch (err) {
      setError(err.message)
    } finally {
      e.target.value = ''
      setOpLoading('')
    }
  }

  async function uploadGenes(e) {
    const file = e.target.files?.[0]
    if (!file) return
    setOpLoading('genes-upload')
    setError('')
    setOpMsg('')
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await fetch(`${API_BASE}/api/upload/genes?ingest=true&collection=${encodeURIComponent(geneTarget)}`, {
        method: 'POST',
        body: form
      })
      const data = await readJsonOrThrow(res)
      setOpMsg(`已上传 ${data.saved_file}，已导入 ${data.inserted} 条 -> ${data.collection}`)
    } catch (err) {
      setError(err.message)
    } finally {
      e.target.value = ''
      setOpLoading('')
    }
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

          <section className={styles.sidePanel}>
            <div className={styles.sidePanelTitle}>项目状态</div>
            <div className={styles.statusGrid}>
              {PROJECT_STATUS.map((item) => (
                <div key={item.label} className={styles.statusCard}>
                  <div className={styles.statusLabel}>{item.label}</div>
                  <div className={`${styles.statusValue} ${item.tone === 'good' ? styles.statusValueGood : styles.statusValueWarm}`}>
                    {item.value}
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className={styles.sidePanel}>
            <div className={styles.sidePanelTitle}>数据源状态</div>
            <div className={styles.dataList}>
              {DATA_STATUS.map((item) => (
                <div key={item.label} className={styles.dataRow}>
                  <span className={styles.dataDot} />
                  <div>
                    <div className={styles.dataLabel}>{item.label}</div>
                    <div className={styles.dataValue}>{item.value}</div>
                  </div>
                </div>
              ))}
            </div>
          </section>

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
          <input
            ref={paperInputRef}
            type="file"
            accept=".pdf"
            multiple
            hidden
            onChange={uploadPapers}
          />
          <input
            ref={geneInputRef}
            type="file"
            accept=".csv,.tsv,text/csv,text/tab-separated-values"
            hidden
            onChange={uploadGenes}
          />

          <header className={styles.topBar}>
            <div className={styles.heroOrnamentA} />
            <div className={styles.heroOrnamentB} />
            <div className={styles.heroLeaf} />
            <div className={styles.topTitleBlock}>
              <div className={styles.eyebrow}>Apple Quality Knowledge Studio</div>
              <h1 className={styles.heroTitle}>
                {activeChat?.messages.length ? activeChat?.title || 'Research Session' : 'What should we discover in apples today?'}
              </h1>
              <p className={styles.heroLead}>
                面向苹果育种毕业设计的论文、基因与性状证据工作台。
              </p>
            </div>
            <div className={styles.toolbar}>
              <button className={styles.primaryBtn} onClick={() => paperInputRef.current?.click()}>
                上传论文 PDF
              </button>
              <button className={styles.primaryBtn} onClick={() => geneInputRef.current?.click()}>
                上传基因 CSV/TSV
              </button>
              <select
                className={styles.select}
                value={geneTarget}
                onChange={(e) => setGeneTarget(e.target.value)}
              >
                {GENE_TARGETS.map((item) => (
                  <option key={item.value} value={item.value}>
                    {item.label}
                  </option>
                ))}
              </select>
              <button className={styles.ghostBtn} onClick={rebuildPapers} disabled={opLoading === 'papers-reindex'}>
                {opLoading === 'papers-reindex' ? '重建中...' : '重建论文索引'}
              </button>
              <button className={styles.ghostBtn} onClick={rebuildGenes} disabled={opLoading === 'genes-reindex'}>
                {opLoading === 'genes-reindex' ? '重建中...' : '重建基因索引'}
              </button>
              <button className={styles.ghostBtn} onClick={() => setSettingsOpen((v) => !v)}>
                {settingsOpen ? '收起 LLM 设置' : '配置 LLM Key'}
              </button>
            </div>
          </header>

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
                当前配置只保存在这个浏览器的本地存储中；提问时会随请求发送给后端，不会写回仓库或 `.env`。
              </p>
            </section>
          )}

          <div className={styles.thread}>
            {activeChat?.messages.length ? (
              activeChat.messages.map((m, i) => (
                <article key={i} className={`${styles.msg} ${m.role === 'user' ? styles.msgUser : styles.msgAssistant}`}>
                  <div className={styles.msgHeader}>
                    <div className={styles.msgRole}>{m.role === 'user' ? '你' : '助手'}</div>
                    {m.role === 'assistant' && <div className={styles.msgBadge}>Research Response</div>}
                  </div>
                  <div className={styles.msgText}>{m.text}</div>
                  {m.role === 'assistant' && (
                    <>
                      <div className={styles.route}>route: {m.routeUsed || 'auto'}</div>
                      {Array.isArray(m.sources) && m.sources.length > 0 && (
                        <details className={styles.evidenceBox}>
                          <summary>查看引用与证据卡片（{m.sources.length}）</summary>
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
              ))
            ) : (
              <div className={styles.emptyState}>
                <div className={styles.emptyBadge}>Apple Breeding Assistant</div>
                <div className={styles.emptyTitle}>从文献、基因和性状里，快速拼出一条可验证的育种证据链。</div>
                <div className={styles.emptyBody}>
                  你可以直接提问，也可以先上传新的 PDF 和基因表。当前界面支持即时上传后检索，并可为本地浏览器单独配置 LLM。
                </div>
                <div className={styles.quickRow}>
                  {QUICK_PROMPTS.map((prompt) => (
                    <button
                      key={prompt}
                      className={styles.quickChip}
                      onClick={() => setQuestion(prompt)}
                    >
                      {prompt}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {opMsg && <div className={styles.statusBar}>{opMsg}</div>}

          <footer className={styles.composerShell}>
            <div className={styles.inputBar}>
              <textarea
                className={styles.textarea}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="例如：哪些基因位点与苹果果肉硬度保持有关？"
              />
              <div className={styles.composerFooter}>
                <div className={styles.composerMeta}>
                  <span className={styles.metaPill}>Route auto</span>
                  <span className={styles.metaPill}>{geneTarget}</span>
                  <span className={styles.metaPill}>{llmConfig.apiKey ? 'LLM on' : 'LLM fallback'}</span>
                </div>
                <button className={styles.askBtn} onClick={ask} disabled={loading}>
                  {loading ? '检索中...' : '发送'}
                </button>
              </div>
            </div>
          </footer>

          {error && <p className={styles.error}>错误：{error}</p>}
        </section>
      </div>
    </main>
  )
}
