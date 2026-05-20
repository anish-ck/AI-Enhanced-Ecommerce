import { createContext, useContext, useEffect, useMemo, useState } from 'react'

import { api } from '../lib/api'
import { clearToken, getToken, setToken as storeToken } from '../lib/storage'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
    const [token, setToken] = useState(getToken())
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    useEffect(() => {
        let active = true

        if (!token) {
            setUser(null)
            return undefined
        }

        setLoading(true)
        api
            .me(token)
            .then((data) => {
                if (active) {
                    setUser(data)
                }
            })
            .catch(() => {
                if (active) {
                    clearToken()
                    setToken(null)
                    setUser(null)
                }
            })
            .finally(() => {
                if (active) {
                    setLoading(false)
                }
            })

        return () => {
            active = false
        }
    }, [token])

    const login = async (email, password) => {
        setError(null)
        const data = await api.login({ email, password })
        storeToken(data.access_token)
        setToken(data.access_token)
        const me = await api.me(data.access_token)
        setUser(me)
        return me
    }

    const signup = async (name, email, password) => {
        setError(null)
        await api.signup({ name, email, password })
        return login(email, password)
    }

    const logout = () => {
        clearToken()
        setToken(null)
        setUser(null)
    }

    const value = useMemo(
        () => ({
            token,
            user,
            loading,
            error,
            setError,
            login,
            signup,
            logout,
        }),
        [token, user, loading, error]
    )

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
    const context = useContext(AuthContext)
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider')
    }
    return context
}
