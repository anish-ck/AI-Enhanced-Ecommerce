function SQLPreview({ sql }) {
    return (
        <div className="analytics-card">
            <h3>Generated SQL</h3>
            <pre className="analytics-sql">
                {sql || 'Run a query to see the generated SQL.'}
            </pre>
        </div>
    )
}

export default SQLPreview
