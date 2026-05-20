import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { useAuth } from '../state/AuthContext'

function Login() {
    const navigate = useNavigate()
    const { login, error, setError } = useAuth()
    const [form, setForm] = useState({ email: '', password: '' })
    const [status, setStatus] = useState('idle')

    const handleChange = (event) => {
        if (error) {
            setError(null)
        }
        setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }))
    }

    const handleSubmit = async (event) => {
        event.preventDefault()
        setStatus('loading')
        try {
            await login(form.email, form.password)
            setStatus('success')
            navigate('/')
        } catch (err) {
            setError(err.message || 'Login failed.')
            setStatus('error')
        }
    }

    return (
        <div className="page narrow">
            <div className="card form-card">
                <h2>Welcome back</h2>
                <p className="muted">Log in to keep your cart and orders in sync.</p>
                <form className="form" onSubmit={handleSubmit}>
                    <label>
                        Email
                        <input
                            name="email"
                            type="email"
                            value={form.email}
                            onChange={handleChange}
                            required
                        />
                    </label>
                    <label>
                        Password
                        <input
                            name="password"
                            type="password"
                            value={form.password}
                            onChange={handleChange}
                            required
                        />
                    </label>
                    {error && <p className="notice error">{error}</p>}
                    <button className="button primary" type="submit" disabled={status === 'loading'}>
                        {status === 'loading' ? 'Signing in...' : 'Log in'}
                    </button>
                </form>
            </div>
        </div>
    )
}

export default Login
