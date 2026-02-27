'use client'

import { useState } from 'react'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'

export default function HomePage() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  async function ask() {
    if (!question.trim()) return
    setLoading(true)
    setError('')
    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, top_k: 6, route: 'auto' })
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  async function ingestPapers() {
    await fetch(`${API_BASE}/api/ingest/papers`, { method: 'POST' })
  }

  async function ingestGenes() {
    await fetch(`${API_BASE}/api/ingest/genes`, { method: 'POST' })
  }

  return (
    <main style={styles.main}>
      <section style={styles.panel}>
        <h1 style={styles.title}>Apple Breeding RAG</h1>
        <p style={styles.sub}>先导入数据，再提问。回答会附带证据片段。</p>

        <div style={styles.actions}>
          <button style={styles.btn} onClick={ingestPapers}>导入论文 PDF</button>
          <button style={styles.btn} onClick={ingestGenes}>导入基因 CSV</button>
        </div>

        <textarea
          style={styles.textarea}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="例如：哪些基因位点与苹果果肉硬度保持有关？"
        />
        <button style={styles.askBtn} onClick={ask} disabled={loading}>
          {loading ? '查询中...' : '提问'}
        </button>

        {error && <p style={styles.error}>错误: {error}</p>}

        {result && (
          <div style={styles.result}>
            <h3>回答</h3>
            <p style={styles.answer}>{result.answer}</p>
            <h3>证据</h3>
            <ul style={styles.list}>
              {result.sources?.map((s, i) => (
                <li key={i} style={styles.item}>
                  <strong>[{i + 1}] {s.source_type}</strong> {s.title ? `| ${s.title}` : ''} {s.page ? `| p.${s.page}` : ''}
                  <p>{s.chunk_text}</p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>
    </main>
  )
}

const styles = {
  main: {
    minHeight: '100vh',
    padding: '32px',
    background: 'linear-gradient(130deg, #f3f8ec 0%, #fff8ec 100%)',
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif'
  },
  panel: {
    maxWidth: 900,
    margin: '0 auto',
    background: '#fff',
    borderRadius: 16,
    padding: 24,
    boxShadow: '0 10px 30px rgba(0,0,0,0.08)'
  },
  title: { margin: 0, fontSize: 32, color: '#234f1e' },
  sub: { color: '#555' },
  actions: { display: 'flex', gap: 10, marginBottom: 12, flexWrap: 'wrap' },
  btn: { border: '1px solid #234f1e', background: '#fff', padding: '8px 12px', borderRadius: 10, cursor: 'pointer' },
  askBtn: { marginTop: 10, border: 'none', background: '#234f1e', color: '#fff', padding: '10px 16px', borderRadius: 10, cursor: 'pointer' },
  textarea: { width: '100%', minHeight: 120, borderRadius: 10, border: '1px solid #ddd', padding: 12, fontSize: 16 },
  error: { color: '#ab1f1f' },
  result: { marginTop: 20 },
  answer: { whiteSpace: 'pre-wrap' },
  list: { paddingLeft: 20 },
  item: { marginBottom: 10 }
}
