import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { api } from '../lib/api'
import { formatPrice } from '../lib/format'
import { useAuth } from '../state/AuthContext'
import { useCart } from '../state/CartContext'

function Checkout() {
    const { user } = useAuth()
    const cart = useCart()
    const navigate = useNavigate()
    const [productMap, setProductMap] = useState({})
    const [status, setStatus] = useState('idle')
    const [message, setMessage] = useState('')

    useEffect(() => {
        if (cart.items.length === 0) {
            setProductMap({})
            return
        }

        const ids = [...new Set(cart.items.map((item) => item.product_id))]

        Promise.all(ids.map((id) => api.getProduct(id)))
            .then((products) => {
                const nextMap = products.reduce((acc, product) => {
                    acc[product.id] = product
                    return acc
                }, {})
                setProductMap(nextMap)
            })
            .catch(() => {
                setMessage('Unable to load product details.')
            })
    }, [cart.items])

    const total = useMemo(() => {
        return cart.items.reduce((sum, item) => {
            const product = productMap[item.product_id]
            const price = product ? Number(product.price) : 0
            return sum + price * item.quantity
        }, 0)
    }, [cart.items, productMap])

    const handleCheckout = async () => {
        setStatus('loading')
        setMessage('')
        try {
            await cart.checkout()
            setStatus('success')
            navigate('/orders')
        } catch (err) {
            setMessage(err.message || 'Checkout failed.')
            setStatus('error')
        }
    }

    if (!user) {
        return (
            <div className="page">
                <div className="card">
                    <h2>Log in to check out</h2>
                    <p className="muted">Your order needs an authenticated account.</p>
                </div>
            </div>
        )
    }

    if (cart.items.length === 0) {
        return (
            <div className="page">
                <div className="card">
                    <h2>Your cart is empty</h2>
                    <p className="muted">Add products before checking out.</p>
                </div>
            </div>
        )
    }

    return (
        <div className="page narrow">
            <div className="card">
                <h2>Checkout</h2>
                <p className="muted">Review totals and place your order.</p>
                <div className="list">
                    {cart.items.map((item) => {
                        const product = productMap[item.product_id]
                        return (
                            <div className="line-item" key={item.id}>
                                <span>{product ? product.title : `Product ${item.product_id}`}</span>
                                <span>
                                    {item.quantity} x {formatPrice(product?.price)}
                                </span>
                            </div>
                        )
                    })}
                </div>
                <div className="price-lg">Total {formatPrice(total)}</div>
                {message && <p className="notice error">{message}</p>}
                <button
                    className="button primary"
                    type="button"
                    disabled={status === 'loading'}
                    onClick={handleCheckout}
                >
                    {status === 'loading' ? 'Placing order...' : 'Place order'}
                </button>
            </div>
        </div>
    )
}

export default Checkout
