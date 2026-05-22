function DataTable({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="analytics-card analytics-empty-table">
        Raw data will appear here once a query completes.
      </div>
    )
  }

  const columns = Object.keys(data[0])

  return (
    <div className="analytics-card">
      <h3>Raw Data</h3>
      <div className="analytics-table">
        <table>
          <thead>
            <tr>
              {columns.map((column) => (
                <th key={column}>
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, rowIndex) => (
              <tr key={`${rowIndex}-${columns[0]}`}>
                {columns.map((column) => (
                  <td key={`${rowIndex}-${column}`}>
                    {String(row[column])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default DataTable
