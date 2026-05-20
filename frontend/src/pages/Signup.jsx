import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { useAuth } from '../state/AuthContext'

function Signup() {
    const navigate = useNavigate()
    const { signup, error, setError } = useAuth()
    const [form, setForm] = useState({ name: '', email: '', password: '' })
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
            await signup(form.name, form.email, form.password)
            setStatus('success')
            navigate('/')
        } catch (err) {
            setError(err.message || 'Signup failed.')
            setStatus('error')
        }
    }

    return (
        <div className="page narrow">
            <div className="card form-card">
                <h2>Create your account</h2>
                <p className="muted">Start with one login and track every order.</p>
                <form className="form" onSubmit={handleSubmit}>
                    <label>
                        Name
                        <input name="name" value={form.name} onChange={handleChange} required />
                    </label>
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
                        {status === 'loading' ? 'Creating...' : 'Sign up'}
                    </button>
                </form>
            </div>
        </div>
    )
}

export default Signup
