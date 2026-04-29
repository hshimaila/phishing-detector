import { useState, useEffect } from 'react'
import ScanHistory from '../components/ScanHistory'
import AlertBanner from '../components/AlertBanner'
import { getHistory, deleteScan } from '../services/api'
import styles from './History.module.css'

export default function History() {
  const [scans, setScans]     = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter]   = useState('all')
  const [error, setError]     = useState(null)

  async function load() {
    setLoading(true)
    try {
      const params = filter !== 'all' ? { type: filter } : {}
      const data = await getHistory(params)
      setScans(data.scans || [])
    } catch {
      setError('Could not load scan history. Is Flask running?')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [filter])

  async function handleDelete(id) {
    try {
      await deleteScan(id)
      setScans(prev => prev.filter(s => s.id !== id))
    } catch {
      setError('Failed to delete scan.')
    }
  }

  const total      = scans.length
  const phishing   = scans.filter(s => s.verdict === 'phishing').length
  const safe       = scans.filter(s => s.verdict === 'safe').length
  const suspicious = scans.filter(s => s.verdict === 'suspicious').length
  const detectRate = total > 0 ? Math.round((phishing / total) * 100) : 0

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>SCAN HISTORY</h1>
          <p className={styles.subtitle}>All scans are stored locally in your SQLite database.</p>
        </div>
        <button className={styles.refreshBtn} onClick={load}>↺ REFRESH</button>
      </div>

      <div className={styles.stats}>
        {[
          { label: 'TOTAL SCANS',    value: total,       color: 'var(--text-primary)' },
          { label: 'PHISHING',       value: phishing,    color: 'var(--accent-red)' },
          { label: 'SUSPICIOUS',     value: suspicious,  color: 'var(--accent-amber)' },
          { label: 'SAFE',           value: safe,        color: 'var(--accent-green)' },
          { label: 'DETECTION RATE', value: `${detectRate}%`, color: 'var(--accent-cyan)' },
        ].map(s => (
          <div key={s.label} className={styles.statCard}>
            <span className={styles.statLabel}>{s.label}</span>
            <span className={styles.statValue} style={{ color: s.color }}>{s.value}</span>
          </div>
        ))}
      </div>

      {error && <AlertBanner type="error" message={error} onClose={() => setError(null)} />}

      <div className={styles.filterBar}>
        {['all', 'email', 'url'].map(f => (
          <button
            key={f}
            className={filter === f ? `${styles.filterBtn} ${styles.filterBtnActive}` : styles.filterBtn}
            onClick={() => setFilter(f)}
          >
            {f.toUpperCase()}
          </button>
        ))}
        <span className={styles.filterCount}>{scans.length} RESULTS</span>
      </div>

      {loading ? (
        <div className={styles.loading}>
          <span className={styles.loadingDot} />
          LOADING SCAN HISTORY...
        </div>
      ) : (
        <ScanHistory scans={scans} onDelete={handleDelete} />
      )}
    </div>
  )
}