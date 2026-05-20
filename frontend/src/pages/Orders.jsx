import { useEffect, useState } from 'react'

import { api } from '../lib/api'
import { formatPrice } from '../lib/format'
import { useAuth } from '../state/AuthContext'

function Orders() {
    const { user, token } = useAuth()
    const [orders, setOrders] = useState([])
    const [status, setStatus] = useState('idle')

    useEffect(() => {
        if (!token) {
            return
        }

        let active = true
        setStatus('loading')
        api
            .listOrders(token)
            .then((data) => {
                if (active) {
                    setOrders(data)
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
    }, [token])

    if (!user) {
        return (
            <div className="page">
                <div className="card">
                    <h2>Log in to see orders</h2>
                    <p className="muted">Order history appears after checkout.</p>
                </div>
            </div>
        )
    }

    return (
        <div className="page">
            <div className="section-head">
                <div>
                    <h2>Order history</h2>
                    <p className="muted">Track every checkout from your account.</p>
                </div>
            </div>

            {status === 'loading' && <p className="muted">Loading orders...</p>}
            {status === 'error' && <p className="muted">Unable to load orders.</p>}

            <div className="stack">
                {orders.length === 0 && status === 'success' && (
                    <div className="card">
                        <p className="muted">No orders yet.</p>
                    </div>
                )}
                {orders.map((order) => (
                    <div className="card order-card" key={order.id}>
                        <div className="order-head">
                            <div>
                                <h3>Order #{order.id}</h3>
                                <p className="muted">Status: {order.status}</p>
                            </div>
                            <div className="price">{formatPrice(order.total_amount)}</div>
                        </div>
                        <div className="list">
                            {(order.items || []).map((item) => (
                                <div className="line-item" key={item.id}>
                                    <span>Product {item.product_id}</span>
                                    <span>
                                        {item.quantity} x {formatPrice(item.price)}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Orders
