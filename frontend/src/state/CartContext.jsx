import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'

import { api } from '../lib/api'
import { useAuth } from './AuthContext'

const CartContext = createContext(null)

export function CartProvider({ children }) {
    const { token } = useAuth()
    const [items, setItems] = useState([])
    const [loading, setLoading] = useState(false)

    const refresh = useCallback(async () => {
        if (!token) {
            setItems([])
            return
        }

        setLoading(true)
        try {
            const data = await api.listCart(token)
            setItems(data)
        } finally {
            setLoading(false)
        }
    }, [token])

    useEffect(() => {
        refresh()
    }, [refresh])

    const add = async (productId, quantity) => {
        if (!token) {
            throw new Error('Login required')
        }
        await api.addToCart({ product_id: productId, quantity }, token)
        await refresh()
    }

    const update = async (productId, quantity) => {
        if (!token) {
            throw new Error('Login required')
        }
        await api.updateCart({ product_id: productId, quantity }, token)
        await refresh()
    }

    const remove = async (productId) => {
        if (!token) {
            throw new Error('Login required')
        }
        await api.removeFromCart(productId, token)
        await refresh()
    }

    const checkout = async () => {
        if (!token) {
            throw new Error('Login required')
        }
        const order = await api.createOrder(token)
        await refresh()
        return order
    }

    const count = items.reduce((sum, item) => sum + item.quantity, 0)

    const value = useMemo(
        () => ({
            items,
            loading,
            count,
            refresh,
            add,
            update,
            remove,
            checkout,
        }),
        [items, loading, count, refresh]
    )

    return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}

export function useCart() {
    const context = useContext(CartContext)
    if (!context) {
        throw new Error('useCart must be used within CartProvider')
    }
    return context
}
