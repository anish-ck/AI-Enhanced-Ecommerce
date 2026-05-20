import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

import { api } from '../lib/api'
import { formatPrice } from '../lib/format'
import { useAuth } from '../state/AuthContext'
import { useCart } from '../state/CartContext'

function ProductDetail() {
    const { id } = useParams()
    const productId = Number(id)
    const { user, token } = useAuth()
    const cart = useCart()
    const [product, setProduct] = useState(null)
    const [reviews, setReviews] = useState([])
    const [status, setStatus] = useState('idle')
    const [message, setMessage] = useState('')
    const [reviewForm, setReviewForm] = useState({ rating: 5, review_text: '' })

    useEffect(() => {
        let active = true
        setStatus('loading')

        Promise.all([api.getProduct(productId), api.listReviews(productId)])
            .then(([productData, reviewData]) => {
                if (active) {
                    setProduct(productData)
                    setReviews(reviewData)
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
    }, [productId])

    const handleAdd = async () => {
        setMessage('')
        if (!user) {
            setMessage('Log in to add items to your cart.')
            return
        }
        try {
            await cart.add(productId, 1)
            setMessage('Added to cart.')
        } catch (err) {
            setMessage(err.message || 'Unable to add item.')
        }
    }

    const handleReviewChange = (event) => {
        const { name, value } = event.target
        setReviewForm((prev) => ({ ...prev, [name]: value }))
    }

    const submitReview = async (event) => {
        event.preventDefault()
        setMessage('')
        if (!user) {
            setMessage('Log in to leave a review.')
            return
        }

        try {
            await api.createReview(
                {
                    product_id: productId,
                    rating: Number(reviewForm.rating),
                    review_text: reviewForm.review_text,
                },
                token
            )
            const reviewData = await api.listReviews(productId)
            setReviews(reviewData)
            setReviewForm({ rating: 5, review_text: '' })
            setMessage('Review submitted.')
        } catch (err) {
            setMessage(err.message || 'Unable to submit review.')
        }
    }

    if (status === 'loading') {
        return (
            <div className="page">
                <p className="muted">Loading product...</p>
            </div>
        )
    }

    if (status === 'error' || !product) {
        return (
            <div className="page">
                <p className="muted">Product not found.</p>
            </div>
        )
    }

    return (
        <div className="page">
            <div className="detail-grid">
                <div className="card">
                    <p className="pill">Category {product.category_id}</p>
                    <h2>{product.title}</h2>
                    <p className="muted">{product.description}</p>
                    <div className="price-lg">{formatPrice(product.price)}</div>
                    <div className="stack row">
                        <button className="button primary" type="button" onClick={handleAdd}>
                            Add to cart
                        </button>
                        <span className="pill">Stock {product.stock}</span>
                    </div>
                    {message && <p className="notice">{message}</p>}
                </div>

                <div className="card">
                    <h3>Reviews</h3>
                    <div className="list">
                        {reviews.length === 0 && <p className="muted">No reviews yet.</p>}
                        {reviews.map((review) => (
                            <div className="review" key={review.id}>
                                <strong>Rating {review.rating}/5</strong>
                                <p className="muted">{review.review_text}</p>
                            </div>
                        ))}
                    </div>
                    <form className="form" onSubmit={submitReview}>
                        <label>
                            Rating
                            <select
                                name="rating"
                                value={reviewForm.rating}
                                onChange={handleReviewChange}
                            >
                                {[1, 2, 3, 4, 5].map((value) => (
                                    <option key={value} value={value}>
                                        {value}
                                    </option>
                                ))}
                            </select>
                        </label>
                        <label>
                            Review
                            <textarea
                                name="review_text"
                                rows="3"
                                value={reviewForm.review_text}
                                onChange={handleReviewChange}
                                required
                            />
                        </label>
                        <button className="button ghost" type="submit">
                            Submit review
                        </button>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default ProductDetail
