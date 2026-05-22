import { getToken } from './storage'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const request = async (path, options = {}) => {
    const token = options.token === undefined ? getToken() : options.token
    const headers = { ...(options.headers || {}) }

    if (options.body !== undefined && !(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json'
    }

    if (token) {
        headers.Authorization = `Bearer ${token}`
    }

    const response = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers,
    })

    if (response.status === 204) {
        return null
    }

    const contentType = response.headers.get('content-type') || ''
    const isJson = contentType.includes('application/json')
    const data = isJson ? await response.json() : await response.text()

    if (!response.ok) {
        const message = isJson && data && data.detail ? data.detail : response.statusText
        const error = new Error(message)
        error.status = response.status
        error.data = data
        throw error
    }

    return data
}

export const api = {
    signup: (payload) =>
        request('/auth/signup', {
            method: 'POST',
            body: JSON.stringify(payload),
            token: null,
        }),
    login: (payload) =>
        request('/auth/login', {
            method: 'POST',
            body: JSON.stringify(payload),
            token: null,
        }),
    me: (token) => request('/auth/me', { token }),
    listProducts: () => request('/products'),
    getProduct: (productId) => request(`/products/${productId}`),
    createProduct: (payload) =>
        request('/products', {
            method: 'POST',
            body: JSON.stringify(payload),
        }),
    listCategories: () => request('/categories'),
    createCategory: (payload) =>
        request('/categories', {
            method: 'POST',
            body: JSON.stringify(payload),
        }),
    generateProductAI: (imageFile, productId = null) => {
        const formData = new FormData()
        formData.append('image', imageFile)
        if (productId !== null && productId !== undefined) {
            formData.append('product_id', String(productId))
        }
        return request('/products/ai-generate', {
            method: 'POST',
            body: formData,
        })
    },
    listReviews: (productId) => request(`/products/${productId}/reviews`),
    createReview: (payload, token) =>
        request('/reviews', {
            method: 'POST',
            body: JSON.stringify(payload),
            token,
        }),
    listCart: (token) => request('/cart', { token }),
    addToCart: (payload, token) =>
        request('/cart/add', {
            method: 'POST',
            body: JSON.stringify(payload),
            token,
        }),
    updateCart: (payload, token) =>
        request('/cart/update', {
            method: 'PUT',
            body: JSON.stringify(payload),
            token,
        }),
    removeFromCart: (productId, token) =>
        request(`/cart/remove?product_id=${productId}`, {
            method: 'DELETE',
            token,
        }),
    createOrder: (token) =>
        request('/orders/create', {
            method: 'POST',
            token,
        }),
    listOrders: (token) => request('/orders', { token }),
}
