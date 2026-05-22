import { useMemo, useState } from 'react'
import axios from 'axios'

import AnalyticsInput from '../components/AnalyticsInput'
import AnalyticsChart from '../components/AnalyticsChart'
import SQLPreview from '../components/SQLPreview'
import DataTable from '../components/DataTable'
import LoadingSpinner from '../components/LoadingSpinner'

const API_URL =
    import.meta.env.VITE_ANALYTICS_API_URL || 'http://localhost:8002/analytics/query'

const sampleQuestions = [
    'Which product sold most?',
    'Show monthly revenue trend',
    'Top customers by spending',
    'Which category generated highest revenue?',
]

function AnalyticsPage() {
    const [question, setQuestion] = useState('')
    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const canSubmit = question.trim().length > 0 && !loading

    const handleSubmit = async (value) => {
        const prompt = value.trim()
        if (!prompt) {
            return
        }

        setLoading(true)
        setError('')
        try {
            const response = await axios.post(API_URL, { question: prompt })
            setResult(response.data)
        } catch (err) {
            const message = err?.response?.data?.detail || 'Failed to generate analytics'
            setError(message)
        } finally {
            setLoading(false)
        }
    }

    const handleFormSubmit = (event) => {
        event.preventDefault()
        handleSubmit(question)
    }

    const chartPayload = useMemo(() => {
        if (!result) {
            return null
        }
        return {
            chartType: result.chart_type,
            chart: result.chart,
            data: result.data || [],
        }
    }, [result])

    return (
        <section className="page analytics-page">
            <div className="analytics-shell">
                <header className="analytics-header">
                    <span className="eyebrow">AI Analytics</span>
                    <h1>AI Analytics Dashboard</h1>
                    <p className="muted">
                        Ask a business question and get Databricks insights with generated SQL,
                        interactive charts, and raw data.
                    </p>
                </header>

                <AnalyticsInput
                    value={question}
                    onChange={setQuestion}
                    onSubmit={handleFormSubmit}
                    disabled={!canSubmit}
                />

                <div className="analytics-samples">
                    {sampleQuestions.map((item) => (
                        <button
                            key={item}
                            type="button"
                            onClick={() => {
                                setQuestion(item)
                                handleSubmit(item)
                            }}
                            className="analytics-chip"
                        >
                            {item}
                        </button>
                    ))}
                </div>

                {loading && (
                    <div className="analytics-status">
                        <LoadingSpinner />
                        <span>Generating analytics...</span>
                    </div>
                )}

                {error && <div className="notice error">{error}</div>}

                <div className="analytics-grid">
                    <div className="analytics-card analytics-chart-card">
                        <h3>Chart Visualization</h3>
                        <AnalyticsChart
                            chartType={chartPayload?.chartType}
                            chart={chartPayload?.chart}
                            data={chartPayload?.data || []}
                        />
                    </div>
                    <SQLPreview sql={result?.sql} />
                </div>

                <DataTable data={result?.data || []} />
            </div>
        </section>
    )
}

export default AnalyticsPage
