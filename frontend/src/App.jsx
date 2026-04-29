import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import History from './pages/History'
import styles from './App.module.css'

function NavBar() {
  return (
    <nav className={styles.nav}>
      <div className={styles.navBrand}>
        <span className={styles.navLogo}>⬡</span>
        <span className={styles.navTitle}>PhishGuard</span>
        <span className={styles.navTag}>AI v1.0</span>
      </div>
      <div className={styles.navLinks}>
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            isActive ? `${styles.navLink} ${styles.navLinkActive}` : styles.navLink
          }
        >
          SCAN
        </NavLink>
        <NavLink
          to="/history"
          className={({ isActive }) =>
            isActive ? `${styles.navLink} ${styles.navLinkActive}` : styles.navLink
          }
        >
          HISTORY
        </NavLink>
      </div>
      <div className={styles.navStatus}>
        <span className={styles.statusDot} />
        SYSTEM ONLINE
      </div>
    </nav>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <div className={styles.shell}>
        <NavBar />
        <main className={styles.main}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/history" element={<History />} />
          </Routes>
        </main>
        <footer className={styles.footer}>
          <span>PHISHGUARD // AI-POWERED THREAT DETECTION</span>
          <span>ALL SCANS LOGGED LOCALLY</span>
        </footer>
      </div>
    </BrowserRouter>
  )
}