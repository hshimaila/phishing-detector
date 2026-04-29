import { useState } from 'react'
import styles from './ScanInput.module.css'

export default function ScanInput({ onScan, loading }) {
  const [mode, setMode] = useState('email')
  const [value, setValue] = useState('')

  const placeholder = mode === 'email'
    ? 'Paste email content here...\n\nExample: "URGENT! Your account has been suspended. Click here to verify NOW!"'
    : 'Enter URL to scan...\n\nExample: http://paypa1.verify-login.tk/secure/account'

  function handleSubmit(e) {
    e.preventDefault()
    if (!value.trim() || loading) return
    onScan(mode, value.trim())
  }

  return (
    <form className={styles.wrapper} onSubmit={handleSubmit}>
      <div className={styles.modeBar}>
        <button
          type="button"
          className={mode === 'email' ? `${styles.modeBtn} ${styles.modeBtnActive}` : styles.modeBtn}
          onClick={() => { setMode('email'); setValue('') }}
        >
          <span className={styles.modeBtnIcon}>✉</span> EMAIL SCAN
        </button>
        <button
          type="button"
          className={mode === 'url' ? `${styles.modeBtn} ${styles.modeBtnActive}` : styles.modeBtn}
          onClick={() => { setMode('url'); setValue('') }}
        >
          <span className={styles.modeBtnIcon}>⬡</span> URL SCAN
        </button>
        <div className={styles.modeBarRight}>
          <span className={styles.modeHint}>
            {mode === 'email' ? 'NLP + ML analysis' : 'Structural + threat intel analysis'}
          </span>
        </div>
      </div>

      <div className={styles.inputWrap}>
        {mode === 'email' ? (
          <textarea
            className={styles.textarea}
            value={value}
            onChange={e => setValue(e.target.value)}
            placeholder={placeholder}
            rows={7}
            disabled={loading}
          />
        ) : (
          <input
            className={styles.urlinput}
            type="text"
            value={value}
            onChange={e => setValue(e.target.value)}
            placeholder={placeholder}
            disabled={loading}
          />
        )}

        <div className={styles.inputFooter}>
          <span className={styles.charCount}>
            {value.length > 0 ? `${value.length} chars` : ''}
          </span>
          <button
            type="submit"
            className={styles.scanBtn}
            disabled={!value.trim() || loading}
          >
            {loading
              ? <><span className={styles.spinner} /> ANALYZING...</>
              : <>RUN SCAN ▶</>
            }
          </button>
        </div>
      </div>
    </form>
  )
}