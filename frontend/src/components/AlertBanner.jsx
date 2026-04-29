import styles from './AlertBanner.module.css'

export default function AlertBanner({ message, type = 'error', onClose }) {
  const colors = {
    error:   { color: 'var(--accent-red)',   bg: 'rgba(255,71,87,0.1)',  border: 'rgba(255,71,87,0.25)',  icon: '✕' },
    warning: { color: 'var(--accent-amber)', bg: 'rgba(255,184,48,0.1)', border: 'rgba(255,184,48,0.25)', icon: '!' },
    info:    { color: 'var(--accent-cyan)',   bg: 'rgba(0,229,255,0.08)', border: 'rgba(0,229,255,0.2)',  icon: 'i' },
  }
  const c = colors[type] || colors.error

  return (
    <div className={styles.banner} style={{ background: c.bg, borderColor: c.border }}>
      <span className={styles.icon} style={{ color: c.color }}>{c.icon}</span>
      <span className={styles.message} style={{ color: c.color }}>{message}</span>
      {onClose && (
        <button className={styles.close} style={{ color: c.color }} onClick={onClose}>✕</button>
      )}
    </div>
  )
}