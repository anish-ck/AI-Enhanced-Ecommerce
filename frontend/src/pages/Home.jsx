import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { api } from '../lib/api'
import { formatPrice } from '../lib/format'
import { useAuth } from '../state/AuthContext'
import { useCart } from '../state/CartContext'

function Home() {
    const { user } = useAuth()
    const cart = useCart()
    const [products, setProducts] = useState([])
    const [status, setStatus] = useState('idle')
    const [message, setMessage] = useState('')

    useEffect(() => {
        let active = true
        setStatus('loading')
        api
            .listProducts()
            .then((data) => {
                if (active) {
                    setProducts(data)
                    setStatus('success')
                }
            })
            .catch(() => {
                if (active) {
                    setStatus('error')
                }
            })

        return () => {
            active = false
        }
    }, [])

    const handleAdd = async (productId) => {
        setMessage('')
        if (!user) {
            setMessage('Please log in to add items to your cart.')
            return
        }

        try {
            await cart.add(productId, 1)
            setMessage('Added to cart.')
        } catch (err) {
            setMessage(err.message || 'Unable to add item.')
        }
    }

    return (
        <div className="page">
            <section className="hero">
                <div className="hero-copy">
                    <span className="eyebrow">Phase 1 OLTP</span>
                    <h1>SignalCart Commerce</h1>
                    <p>
                        Transaction-first storefront that keeps inventory, carts, and orders in
                        sync. Built for fast experiments before the event stream arrives.
                    </p>
                    <div className="hero-actions">
                        <a className="button primary" href="#products">
                            Browse inventory
                        </a>
                        <Link className="button ghost" to="/orders">
                            Order history
                        </Link>
                    </div>
                </div>
                <div className="hero-panel">
                    <div className="stat">
                        <span>FastAPI</span>
                        <strong>Live API</strong>
                    </div>
                    <div className="stat">
                        <span>Postgres</span>
                        <strong>OLTP Core</strong>
                    </div>
                    <div className="stat">
                        <span>JWT</span>
                        <strong>Secure Sessions</strong>
                    </div>
                </div>
            </section>

            <section className="section" id="products">
                <div className="section-head">
                    <div>
                        <h2>Products ready to ship</h2>
                        <p>Pull inventory directly from the API and create your cart flow.</p>
                    </div>
                    {message && <span className="notice">{message}</span>}
                </div>

                {status === 'loading' && <p className="muted">Loading products...</p>}
                {status === 'error' && (
                    <p className="muted">Unable to load products. Try again later.</p>
                )}

                <div className="grid">
                    {status === 'success' && products.length === 0 && (
                        <div className="card">
                            <h3>No products yet</h3>
                            <p className="muted">
                                Add products via the API to see them appear here.
                            </p>
                        </div>
                    )}
                    {products.map((product) => (
                        <article className="card product-card" key={product.id}>
                            <div>
                                <p className="pill">Stock {product.stock}</p>
                                <h3>{product.title}</h3>
                                <p className="muted">{product.description}</p>
                            </div>
                            <div className="product-actions">
                                <div className="price">{formatPrice(product.price)}</div>
                                <div className="stack">
                                    <Link className="button ghost" to={`/products/${product.id}`}>
                                        Details
                                    </Link>
                                    <button
                                        className="button primary"
                                        type="button"
                                        onClick={() => handleAdd(product.id)}
                                    >
                                        Add to cart
                                    </button>
                                </div>
                            </div>
                        </article>
                    ))}
                </div>
            </section>
        </div>
    )
}

export default Home
