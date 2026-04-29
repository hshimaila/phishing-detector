import { useState } from 'react'
import ScanInput from '../components/ScanInput'
import ResultCard from '../components/ResultCard'
import AlertBanner from '../components/AlertBanner'
import { scanEmail, scanUrl } from '../services/api'
import styles from './Dashboard.module.css'

const STAT_TIPS = [
  'Phishing attacks account for 90% of data breaches.',
  '1.5 million new phishing sites are created every month.',
  'AI-based detection reduces false positives by up to 60%.',
  'The average phishing email is opened within 16 minutes.',
]

export default function Dashboard() {
  const [loading, setLoading] = useState(false)
  const [result, setResult]   = useState(null)
  const [error, setError]     = useState(null)
  const [tip]                 = useState(() => STAT_TIPS[Math.floor(Math.random() * STAT_TIPS.length)])

  async function handleScan(mode, value) {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = mode === 'email' ? await scanEmail(value) : await scanUrl(value)
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to reach the backend. Is Flask running on port 5000?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>THREAT SCANNER</h1>
          <p className={styles.subtitle}>
            Paste an email or URL below — the AI will analyze it for phishing indicators in real time.
          </p>
        </div>
        <div className={styles.tip}>
          <span className={styles.tipLabel}>DID YOU KNOW</span>
          <p className={styles.tipText}>{tip}</p>
        </div>
      </div>

      {error && <AlertBanner type="error" message={error} onClose={() => setError(null)} />}

      <ScanInput onScan={handleScan} loading={loading} />

      {loading && (
        <div className={styles.analyzing}>
          <div className={styles.analyzingDots}>
            <span /><span /><span />
          </div>
          <p>ANALYZING CONTENT — AI MODEL RUNNING...</p>
        </div>
      )}

      <ResultCard result={result} />

      {!result && !loading && (
        <div className={styles.howItWorks}>
          <p className={styles.howTitle}>HOW IT WORKS</p>
          <div className={styles.steps}>
            {[
              { n: '01', label: 'NLP ANALYSIS',  desc: 'SpaCy cleans and tokenizes text. TF-IDF extracts word importance scores.' },
              { n: '02', label: 'ML INFERENCE',   desc: 'Random Forest model predicts phishing probability from 500+ features.' },
              { n: '03', label: 'THREAT INTEL',   desc: 'URL cross-checked against Google Safe Browsing and PhishTank databases.' },
              { n: '04', label: 'RISK SCORE',     desc: 'Weighted score from ML (50%), threat intel (35%), and rules (15%).' },
            ].map(s => (
              <div key={s.n} className={styles.step}>
                <span className={styles.stepNum}>{s.n}</span>
                <p className={styles.stepLabel}>{s.label}</p>
                <p className={styles.stepDesc}>{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}