import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { toast } from 'react-toastify'
import api from '../services/api'
import './Login.css'

const Signup = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: ''
  })
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    // Validation
    if (formData.password !== formData.confirmPassword) {
      toast.error('Passwords do not match')
      setLoading(false)
      return
    }

    if (formData.password.length < 6) {
      toast.error('Password must be at least 6 characters long')
      setLoading(false)
      return
    }

    if (formData.username.length < 3) {
      toast.error('Username must be at least 3 characters long')
      setLoading(false)
      return
    }

    try {
      // Add timeout to prevent infinite loading
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 10000) // 10 second timeout
      
      const response = await api.post('/auth/register', {
        username: formData.username,
        password: formData.password,
        role: 'EMPLOYEE' // Default role for public signup
      }, {
        signal: controller.signal,
        timeout: 10000
      })
      
      clearTimeout(timeoutId)

      if (response.status === 201) {
        toast.success('Account created successfully! Please login.')
        setTimeout(() => {
          navigate('/login')
        }, 1000) // Small delay to show success message
      }
    } catch (error) {
      if (error.name === 'AbortError' || error.code === 'ECONNABORTED') {
        toast.error('Request timed out. Please check if the backend server is running.')
        console.error('Request timeout - backend may not be responding')
      } else if (error.response) {
        // Server responded with error
        const errorMessage = error.response?.data?.message || 'Failed to create account'
        console.error('Signup error:', error.response?.data || error)
        toast.error(errorMessage)
      } else if (error.request) {
        // Request made but no response
        toast.error('Cannot connect to server. Please check if the backend is running on port 5000.')
        console.error('No response from server:', error.request)
      } else {
        // Other error
        const errorMessage = error.message || 'Failed to create account'
        console.error('Signup error:', error)
        toast.error(errorMessage)
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>💰 Cash & Carry Mart</h1>
          <p>Create Your Account</p>
        </div>
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              name="username"
              className="input"
              value={formData.username}
              onChange={handleChange}
              required
              placeholder="Choose a username (min 3 characters)"
              minLength={3}
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              className="input"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Enter password (min 6 characters)"
              minLength={6}
            />
          </div>
          <div className="form-group">
            <label>Confirm Password</label>
            <input
              type="password"
              name="confirmPassword"
              className="input"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              placeholder="Confirm your password"
              minLength={6}
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            style={{ width: '100%', marginTop: '24px' }}
          >
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>
        <div className="login-footer">
          <p>
            Already have an account? <Link to="/login" style={{ color: 'var(--primary)', textDecoration: 'none' }}>Login here</Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Signup

