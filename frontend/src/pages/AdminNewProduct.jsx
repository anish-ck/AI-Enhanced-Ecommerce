import { useEffect, useMemo, useState } from 'react'

import { api } from '../lib/api'

const emptyForm = {
    title: '',
    description: '',
    category_id: '',
    price: '',
    stock: '',
    ai_title: '',
    ai_description: '',
    ai_category: '',
    ai_tags: '',
    ai_generated: false,
}

const normalizeTags = (value) => {
    if (!value) {
        return []
    }
    return value
        .split(',')
        .map((tag) => tag.trim())
        .filter(Boolean)
}

function AdminNewProduct() {
    const [form, setForm] = useState(emptyForm)
    const [categories, setCategories] = useState([])
    const [categoryStatus, setCategoryStatus] = useState('idle')
    const [categoryMessage, setCategoryMessage] = useState('')
    const [categoryTone, setCategoryTone] = useState('info')
    const [status, setStatus] = useState('idle')
    const [message, setMessage] = useState('')
    const [aiStatus, setAiStatus] = useState('idle')
    const [aiMessage, setAiMessage] = useState('')
    const [imageFile, setImageFile] = useState(null)
    const [imagePreview, setImagePreview] = useState('')
    const [newCategory, setNewCategory] = useState('')

    const tagPreview = useMemo(() => normalizeTags(form.ai_tags), [form.ai_tags])

    useEffect(() => {
        let active = true
        setCategoryStatus('loading')
        api
            .listCategories()
            .then((data) => {
                if (!active) {
                    return
                }
                setCategories(data)
                setCategoryStatus('success')
                setCategoryMessage('')
            })
            .catch(() => {
                if (!active) {
                    return
                }
                setCategoryStatus('error')
                setCategoryTone('error')
                setCategoryMessage('Unable to load categories. Add one below.')
            })

        return () => {
            active = false
        }
    }, [])

    useEffect(() => {
        if (!imageFile) {
            setImagePreview('')
            return undefined
        }
        const url = URL.createObjectURL(imageFile)
        setImagePreview(url)
        return () => {
            URL.revokeObjectURL(url)
        }
    }, [imageFile])

    const handleChange = (event) => {
        const { name, value } = event.target
        setMessage('')
        setForm((prev) => ({
            ...prev,
            [name]: value,
        }))
    }

    const handleImageChange = (event) => {
        const file = event.target.files && event.target.files[0]
        setAiMessage('')
        setImageFile(file || null)
    }

    const handleGenerate = async () => {
        setAiMessage('')
        if (!imageFile) {
            setAiMessage('Upload an image before generating AI content.')
            return
        }

        setAiStatus('loading')
        try {
            const result = await api.generateProductAI(imageFile)
            const tagText = Array.isArray(result.ai_tags) ? result.ai_tags.join(', ') : ''
            const matchedCategory = categories.find(
                (category) =>
                    result.ai_category &&
                    category.name.toLowerCase() === result.ai_category.toLowerCase()
            )

            setForm((prev) => ({
                ...prev,
                ai_title: result.ai_title || prev.ai_title,
                ai_description: result.ai_description || prev.ai_description,
                ai_category: result.ai_category || prev.ai_category,
                ai_tags: tagText || prev.ai_tags,
                ai_generated: true,
                category_id: matchedCategory ? String(matchedCategory.id) : prev.category_id,
            }))
            setAiStatus('success')
        } catch (err) {
            setAiStatus('error')
            setAiMessage(err.message || 'AI generation failed.')
        }
    }

    const handleApplyAI = () => {
        setForm((prev) => ({
            ...prev,
            title: prev.ai_title || prev.title,
            description: prev.ai_description || prev.description,
        }))
    }

    const handleCreateCategory = async () => {
        const name = newCategory.trim()
        if (!name) {
            return
        }

        setCategoryStatus('loading')
        setCategoryMessage('')
        try {
            const created = await api.createCategory({ name })
            setCategories((prev) => [...prev, created])
            setForm((prev) => ({ ...prev, category_id: String(created.id) }))
            setNewCategory('')
            setCategoryTone('info')
            setCategoryMessage('Category created.')
            setCategoryStatus('success')
        } catch (err) {
            setCategoryStatus('error')
            setCategoryTone('error')
            setCategoryMessage(err.message || 'Unable to create category.')
        }
    }

    const handleSubmit = async (event) => {
        event.preventDefault()
        setMessage('')

        const payload = {
            title: form.title.trim(),
            description: form.description.trim(),
            category_id: Number(form.category_id),
            price: Number(form.price),
            stock: Number(form.stock),
            ai_title: form.ai_title.trim() || null,
            ai_description: form.ai_description.trim() || null,
            ai_category: form.ai_category.trim() || null,
            ai_tags: normalizeTags(form.ai_tags),
            ai_generated: Boolean(form.ai_generated),
        }

        if (!payload.title || !payload.description || !payload.category_id) {
            setStatus('error')
            setMessage('Fill out title, description, and category before saving.')
            return
        }

        if (!Number.isFinite(payload.price) || !Number.isFinite(payload.stock)) {
            setStatus('error')
            setMessage('Price and stock must be valid numbers.')
            return
        }

        setStatus('loading')
        try {
            const created = await api.createProduct(payload)
            setStatus('success')
            setMessage(`Product ${created.id} created.`)
            setForm(emptyForm)
            setImageFile(null)
        } catch (err) {
            setStatus('error')
            setMessage(err.message || 'Unable to create product.')
        }
    }

    return (
        <div className="page">
            <section className="section">
                <div className="section-head">
                    <div>
                        <span className="eyebrow">Admin</span>
                        <h2>Create product</h2>
                        <p className="muted">
                            Upload an image, generate AI content, then fine-tune before publishing.
                        </p>
                    </div>
                    {message && (
                        <span className={`notice ${status === 'error' ? 'error' : ''}`}>
                            {message}
                        </span>
                    )}
                </div>

                <div className="admin-grid">
                    <div className="card form-card">
                        <h3>Product details</h3>
                        <form className="form" onSubmit={handleSubmit}>
                            <label>
                                Title
                                <input
                                    name="title"
                                    value={form.title}
                                    onChange={handleChange}
                                    required
                                />
                            </label>
                            <label>
                                Description
                                <textarea
                                    name="description"
                                    rows="4"
                                    value={form.description}
                                    onChange={handleChange}
                                    required
                                />
                            </label>
                            <label>
                                Category
                                <select
                                    name="category_id"
                                    value={form.category_id}
                                    onChange={handleChange}
                                    required
                                >
                                    <option value="">Select a category</option>
                                    {categories.map((category) => (
                                        <option key={category.id} value={category.id}>
                                            {category.name}
                                        </option>
                                    ))}
                                </select>
                            </label>
                            <div className="inline-form">
                                <input
                                    name="new_category"
                                    placeholder="New category name"
                                    value={newCategory}
                                    onChange={(event) => setNewCategory(event.target.value)}
                                />
                                <button
                                    className="button ghost"
                                    type="button"
                                    onClick={handleCreateCategory}
                                    disabled={categoryStatus === 'loading'}
                                >
                                    {categoryStatus === 'loading' ? 'Saving...' : 'Add category'}
                                </button>
                            </div>
                            {categoryMessage && (
                                <span
                                    className={`notice ${categoryTone === 'error' ? 'error' : ''
                                        }`}
                                >
                                    {categoryMessage}
                                </span>
                            )}
                            <div className="stack row">
                                <label>
                                    Price
                                    <input
                                        name="price"
                                        type="number"
                                        min="0"
                                        step="0.01"
                                        value={form.price}
                                        onChange={handleChange}
                                        required
                                    />
                                </label>
                                <label>
                                    Stock
                                    <input
                                        name="stock"
                                        type="number"
                                        min="0"
                                        value={form.stock}
                                        onChange={handleChange}
                                        required
                                    />
                                </label>
                            </div>
                            <button
                                className="button primary"
                                type="submit"
                                disabled={status === 'loading'}
                            >
                                {status === 'loading' ? 'Saving...' : 'Save product'}
                            </button>
                        </form>
                    </div>

                    <div className="card ai-panel">
                        <h3>AI content generator</h3>
                        <div className="form">
                            <label>
                                Product image
                                <input
                                    type="file"
                                    accept="image/*"
                                    onChange={handleImageChange}
                                />
                            </label>
                        </div>
                        {imagePreview && (
                            <div className="image-preview">
                                <img src={imagePreview} alt="Product upload preview" />
                            </div>
                        )}
                        <button
                            className="button primary"
                            type="button"
                            onClick={handleGenerate}
                            disabled={aiStatus === 'loading'}
                        >
                            {aiStatus === 'loading' ? 'Generating...' : 'Generate AI content'}
                        </button>
                        {aiMessage && <span className="notice error">{aiMessage}</span>}

                        <div className="form">
                            <label>
                                AI title
                                <input
                                    name="ai_title"
                                    value={form.ai_title}
                                    onChange={handleChange}
                                />
                            </label>
                            <label>
                                AI description
                                <textarea
                                    name="ai_description"
                                    rows="4"
                                    value={form.ai_description}
                                    onChange={handleChange}
                                />
                            </label>
                            <label>
                                AI category
                                <input
                                    name="ai_category"
                                    value={form.ai_category}
                                    onChange={handleChange}
                                />
                            </label>
                            <label>
                                AI tags
                                <input
                                    name="ai_tags"
                                    placeholder="comma, separated, tags"
                                    value={form.ai_tags}
                                    onChange={handleChange}
                                />
                            </label>
                            <button className="button ghost" type="button" onClick={handleApplyAI}>
                                Use AI title + description
                            </button>
                        </div>

                        <div className="ai-preview">
                            <h4>AI preview</h4>
                            {form.ai_title ? <strong>{form.ai_title}</strong> : null}
                            {form.ai_description ? (
                                <p className="muted">{form.ai_description}</p>
                            ) : (
                                <p className="muted">No AI content yet.</p>
                            )}
                            {form.ai_category && (
                                <span className="pill">{form.ai_category}</span>
                            )}
                            <div className="tag-list">
                                {tagPreview.length > 0 ? (
                                    tagPreview.map((tag, index) => (
                                        <span className="tag" key={`${tag}-${index}`}>
                                            {tag}
                                        </span>
                                    ))
                                ) : (
                                    <span className="muted">No tags yet.</span>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    )
}

export default AdminNewProduct
