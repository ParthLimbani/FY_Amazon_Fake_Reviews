/**
 * Main Application Component
 * ==========================
 * Root component that manages the application state and renders
 * either the search page or results dashboard.
 * 
 * Application Flow:
 * 1. User enters Amazon URL on home page
 * 2. App sends URL to backend for analysis
 * 3. Results are displayed in dashboard
 */

import { useState } from 'react'
import Header from './components/Header'
import Footer from './components/Footer'
import SearchPage from './pages/SearchPage'
import ResultsPage from './pages/ResultsPage'
import LoadingPage from './pages/LoadingPage'

function App() {
  // Application state
  const [currentPage, setCurrentPage] = useState('search') // 'search', 'loading', 'results'
  const [analysisResult, setAnalysisResult] = useState(null)
  const [error, setError] = useState(null)

  /**
   * Handle analysis completion
   * Called when backend returns analysis results
   */
  const handleAnalysisComplete = (result) => {
    setAnalysisResult(result)
    setCurrentPage('results')
    setError(null)
  }

  /**
   * Handle analysis error
   */
  const handleError = (errorMessage) => {
    setError(errorMessage)
    setCurrentPage('search')
  }

  /**
   * Start new analysis
   */
  const handleStartAnalysis = () => {
    setCurrentPage('loading')
    setError(null)
  }

  /**
   * Reset to search page
   */
  const handleReset = () => {
    setCurrentPage('search')
    setAnalysisResult(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header onLogoClick={handleReset} />
      
      <main className="flex-grow">
        {currentPage === 'search' && (
          <SearchPage 
            onStartAnalysis={handleStartAnalysis}
            onComplete={handleAnalysisComplete}
            onError={handleError}
            error={error}
          />
        )}
        
        {currentPage === 'loading' && (
          <LoadingPage />
        )}
        
        {currentPage === 'results' && analysisResult && (
          <ResultsPage 
            result={analysisResult}
            onAnalyzeAnother={handleReset}
          />
        )}
      </main>
      
      <Footer />
    </div>
  )
}

export default App
