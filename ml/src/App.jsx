import { useState } from 'react'
import './App.css'

function App() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])

  // Use environment variable or fallback to localhost for development
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!text.trim()) {
      setError('Please enter a movie description')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('text', text)

      console.log('Sending request with text:', text)
      console.log('API URL:', API_URL)

      const response = await fetch(`${API_URL}/api/predict`, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json'
        }
      })

      console.log('Response status:', response.status)
      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Failed to get prediction')
      }

      if (data.result) {
        setResult(data.result)
        setHistory([{ text, genre: data.result }, ...history.slice(0, 4)])
        setText('')
      } else {
        setError('No result returned from server')
      }
    } catch (err) {
      console.error('Error:', err)
      setError(err.message || 'Error connecting to prediction service')
    } finally {
      setLoading(false)
    }
  }

  const genreColors = {
    'Romance': '#FF6B9D',
    'Sci-Fi': '#00D4FF',
    'Thriller': '#FF6B35',
    'Comedy': '#FFD93D',
    'Action': '#EE5A52',
    'Horror': '#8B4789'
  }

  return (
    <div className="app-container">
      <div className="animated-bg">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
        <div className="blob blob-3"></div>
      </div>
      
      <div className="content">
        <div className="header">
          <h1>Genre Predictor</h1>
          <p className="subtitle">AI-Powered Movie Classification System</p>
        </div>

        <form onSubmit={handleSubmit} className="form">
          <div className="input-group">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter your movie description here... (e.g., 'A group of friends discover an ancient treasure in a jungle adventure')"
              className="textarea"
              disabled={loading}
            />
            <div className="char-count">{text.length} / 500</div>
          </div>

          <button 
            type="submit" 
            className="submit-btn"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Predicting...
              </>
            ) : (
              "Predict Genre"
            )}
          </button>
        </form>

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {result && (
          <div className="result-box" style={{ borderColor: genreColors[result] }}>
            <div className="result-label">Predicted Genre</div>
            <div className="result-value" style={{ color: genreColors[result] }}>
              {result}
            </div>
          </div>
        )}

        {history.length > 0 && (
          <div className="history-section">
            <h3>Recent Predictions</h3>
            <div className="history-list">
              {history.map((item, idx) => (
                <div key={idx} className="history-item" style={{ borderLeftColor: genreColors[item.genre] }}>
                  <span className="history-text">{item.text.substring(0, 40)}...</span>
                  <span className="history-genre" style={{ backgroundColor: genreColors[item.genre] }}>
                    {item.genre}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

