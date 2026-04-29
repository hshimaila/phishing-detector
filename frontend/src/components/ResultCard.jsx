import styles from './ResultCard.module.css'

const VERDICT_CONFIG = {
  phishing: {
    label: 'PHISHING DETECTED',
    color: 'var(--accent-red)',
    bg: 'rgba(255,71,87,0.08)',
    border: 'rgba(255,71,87,0.3)',
    icon: '⚠',
  },
  suspicious: {
    label: 'SUSPICIOUS',
    color: 'var(--accent-amber)',
    bg: 'rgba(255,184,48,0.08)',
    border: 'rgba(255,184,48,0.3)',
    icon: '?',
  },
  safe: {
    label: 'SAFE',
    color: 'var(--accent-green)',
    bg: 'rgba(0,255,136,0.08)',
    border: 'rgba(0,255,136,0.3)',
    icon: '✓',
  },
}

function RiskMeter({ score }) {
  const pct = Math.round(score * 100)
  const color = pct >= 60
    ? 'var(--accent-red)'
    : pct >= 30
    ? 'var(--accent-amber)'
    : 'var(--accent-green)'

  return (
    <div className={styles.meterWrap}>
      <div className={styles.meterHeader}>
        <span className={styles.meterLabel}>RISK SCORE</span>
        <span className={styles.meterValue} style={{ color }}>{pct}%</span>
      </div>
      <div className={styles.meterTrack}>
        <div
          className={styles.meterFill}
          style={{ width: `${pct}%`, background: color }}
        />
        <div className={styles.meterMark} style={{ left: '30%' }} />
        <div className={styles.meterMark} style={{ left: '60%' }} />
      </div>
      <div className={styles.meterZones}>
        <span style={{ color: 'var(--accent-green)' }}>SAFE</span>
        <span style={{ color: 'var(--accent-amber)' }}>SUSPICIOUS</span>
        <span style={{ color: 'var(--accent-red)' }}>PHISHING</span>
      </div>
    </div>
  )
}

function ScoreBreakdown({ breakdown }) {
  if (!breakdown) return null
  const items = [
    { label: 'ML MODEL',    value: breakdown.ml_contribution,           color: 'var(--accent-cyan)' },
    { label: 'THREAT INTEL', value: breakdown.threat_intel_contribution, color: 'var(--accent-purple)' },
    { label: 'RULE-BASED',  value: breakdown.rules_contribution,         color: 'var(--accent-amber)' },
  ]
  return (
    <div className={styles.breakdown}>
      <p className={styles.breakdownTitle}>SCORE BREAKDOWN</p>
      {items.map(item => (
        <div key={item.label} className={styles.breakdownRow}>
          <span className={styles.breakdownLabel}>{item.label}</span>
          <div className={styles.breakdownTrack}>
            <div
              className={styles.breakdownFill}
              style={{ width: `${Math.round(item.value * 100)}%`, background: item.color }}
            />
          </div>
          <span className={styles.breakdownPct} style={{ color: item.color }}>
            {Math.round(item.value * 100)}%
          </span>
        </div>
      ))}
    </div>
  )
}

export default function ResultCard({ result }) {
  if (!result) return null
  const cfg = VERDICT_CONFIG[result.verdict] || VERDICT_CONFIG.safe
  const signals = result.signals || []

  return (
    <div
      className={`${styles.card} animate-fade-up`}
      style={{ borderColor: cfg.border, background: `linear-gradient(135deg, ${cfg.bg} 0%, var(--bg-surface) 60%)` }}
    >
      <div className={styles.header}>
        <div className={styles.verdictBadge} style={{ color: cfg.color, borderColor: cfg.border }}>
          <span className={styles.verdictIcon}>{cfg.icon}</span>
          <span className={styles.verdictLabel}>{cfg.label}</span>
        </div>
        <div className={styles.metaChips}>
          <span className={styles.chip}>{result.scan_type?.toUpperCase()} #{result.scan_id}</span>
          <span className={styles.chip} style={{ color: 'var(--accent-purple)' }}>
            CONFIDENCE: {result.confidence?.toUpperCase()}
          </span>
          {result.threat_intel_flagged && (
            <span className={styles.chip} style={{ color: 'var(--accent-red)', borderColor: 'rgba(255,71,87,0.3)' }}>
              THREAT DB HIT
            </span>
          )}
        </div>
      </div>

      <p className={styles.explanation}>{result.explanation}</p>
      <RiskMeter score={result.risk_score} />
      <ScoreBreakdown breakdown={result.score_breakdown} />

      {signals.length > 0 && (
        <div className={styles.signals}>
          <p className={styles.signalsTitle}>DETECTED SIGNALS ({signals.length})</p>
          <ul className={styles.signalList}>
            {signals.map((s, i) => (
              <li key={i} className={styles.signalItem}>
                <span className={styles.signalBullet} style={{ color: cfg.color }}>▸</span>
                {s}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className={styles.footer}>
        <span className={styles.footerItem}>ML_SCORE: <code>{(result.ml_score * 100).toFixed(1)}%</code></span>
        <span className={styles.footerItem}>RISK: <code>{(result.risk_score * 100).toFixed(1)}%</code></span>
        <span className={styles.footerItem}>SCAN_ID: <code>#{result.scan_id}</code></span>
      </div>
    </div>
  )
}