import styles from './ScanHistory.module.css'

const VERDICT_COLOR = {
  phishing:   'var(--accent-red)',
  suspicious: 'var(--accent-amber)',
  safe:       'var(--accent-green)',
}

function formatDate(iso) {
  return new Date(iso).toLocaleString('en-US', {
    month: 'short', day: '2-digit',
    hour: '2-digit', minute: '2-digit', hour12: false
  })
}

function truncate(str, n = 55) {
  return str.length > n ? str.slice(0, n) + '…' : str
}

export default function ScanHistory({ scans, onDelete }) {
  if (!scans || scans.length === 0) {
    return (
      <div className={styles.empty}>
        <span className={styles.emptyIcon}>⬡</span>
        <p>NO SCAN HISTORY YET</p>
        <p className={styles.emptyHint}>Run a scan to see results here</p>
      </div>
    )
  }

  return (
    <div className={styles.tableWrap}>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>ID</th>
            <th>TYPE</th>
            <th>CONTENT</th>
            <th>VERDICT</th>
            <th>RISK</th>
            <th>DATE</th>
            {onDelete && <th></th>}
          </tr>
        </thead>
        <tbody>
          {scans.map(scan => (
            <tr key={scan.id} className={styles.row}>
              <td className={styles.idCell}>#{scan.id}</td>
              <td><span className={styles.typeChip}>{scan.scan_type.toUpperCase()}</span></td>
              <td className={styles.contentCell}>{truncate(scan.input_content)}</td>
              <td>
                <span className={styles.verdictChip} style={{ color: VERDICT_COLOR[scan.verdict] }}>
                  {scan.verdict.toUpperCase()}
                </span>
              </td>
              <td>
                <span className={styles.riskVal} style={{ color: VERDICT_COLOR[scan.verdict] }}>
                  {Math.round(scan.risk_score * 100)}%
                </span>
              </td>
              <td className={styles.dateCell}>{formatDate(scan.created_at)}</td>
              {onDelete && (
                <td>
                  <button className={styles.deleteBtn} onClick={() => onDelete(scan.id)}>✕</button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}