import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { api } from '../lib/api'
import { formatPrice } from '../lib/format'
import { useAuth } from '../state/AuthContext'
import { useCart } from '../state/CartContext'

function Cart() {
    const { user } = useAuth()
    const cart = useCart()
    const [productMap, setProductMap] = useState({})
    const [qtyMap, setQtyMap] = useState({})
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

    useEffect(() => {
        const nextQty = cart.items.reduce((acc, item) => {
            acc[item.product_id] = item.quantity
            return acc
        }, {})
        setQtyMap(nextQty)
    }, [cart.items])

    const total = useMemo(() => {
        return cart.items.reduce((sum, item) => {
            const product = productMap[item.product_id]
            const price = product ? Number(product.price) : 0
            return sum + price * item.quantity
        }, 0)
    }, [cart.items, productMap])

    const handleUpdate = async (productId) => {
        setMessage('')
        try {
            const quantity = Number(qtyMap[productId]) || 1
            await cart.update(productId, quantity)
        } catch (err) {
            setMessage(err.message || 'Unable to update cart.')
        }
    }

    const handleRemove = async (productId) => {
        setMessage('')
        try {
            await cart.remove(productId)
        } catch (err) {
            setMessage(err.message || 'Unable to remove item.')
        }
    }

    if (!user) {
        return (
            <div className="page">
                <div className="card">
                    <h2>Log in to view your cart</h2>
                    <p className="muted">Your cart syncs with your account.</p>
                    <Link className="button primary" to="/login">
                        Log in
                    </Link>
                </div>
            </div>
        )
    }

    return (
        <div className="page">
            <div className="section-head">
                <div>
                    <h2>Your cart</h2>
                    <p className="muted">Review items before you check out.</p>
                </div>
                {message && <span className="notice">{message}</span>}
            </div>

            {cart.loading && <p className="muted">Syncing cart...</p>}

            {cart.items.length === 0 ? (
                <div className="card">
                    <p className="muted">Your cart is empty.</p>
                    <Link className="button ghost" to="/">
                        Browse products
                    </Link>
                </div>
            ) : (
                <div className="cart-grid">
                    <div className="stack">
                        {cart.items.map((item) => {
                            const product = productMap[item.product_id]
                            return (
                                <div className="card cart-row" key={item.id}>
                                    <div>
                                        <h3>{product ? product.title : `Product ${item.product_id}`}</h3>
                                        <p className="muted">
                                            {product ? product.description : 'Loading description...'}
                                        </p>
                                    </div>
                                    <div className="cart-actions">
                                        <div className="price">{formatPrice(product?.price)}</div>
                                        <div className="qty">
                                            <input
                                                type="number"
                                                min="1"
                                                value={qtyMap[item.product_id] || 1}
                                                onChange={(event) =>
                                                    setQtyMap((prev) => ({
                                                        ...prev,
                                                        [item.product_id]: event.target.value,
                                                    }))
                                                }
                                            />
                                            <button
                                                className="button ghost"
                                                type="button"
                                                onClick={() => handleUpdate(item.product_id)}
                                            >
                                                Update
                                            </button>
                                        </div>
                                        <button
                                            className="button danger"
                                            type="button"
                                            onClick={() => handleRemove(item.product_id)}
                                        >
                                            Remove
                                        </button>
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                    <aside className="card summary">
                        <h3>Order summary</h3>
                        <p className="muted">Subtotal</p>
                        <div className="price-lg">{formatPrice(total)}</div>
                        <Link className="button primary" to="/checkout">
                            Proceed to checkout
                        </Link>
                    </aside>
                </div>
            )}
        </div>
    )
}

export default Cart
