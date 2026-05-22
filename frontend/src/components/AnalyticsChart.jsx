import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

const COLORS = ['#38bdf8', '#818cf8', '#f472b6', '#f97316', '#22c55e']

function inferKeys(data, chart) {
  const keys = data.length ? Object.keys(data[0]) : []
  const numericKeys = data.length
    ? keys.filter((key) => typeof data[0][key] === 'number')
    : []
  const xKey = chart?.x_axis || keys[0] || ''
  const yKey = chart?.y_axis || numericKeys[0] || keys[1] || keys[0] || ''
  return { xKey, yKey }
}

function ChartEmptyState() {
  return (
    <div className="analytics-empty">
      Ask a question to generate a chart.
    </div>
  )
}

function AnalyticsChart({ chartType, chart, data }) {
  if (!data || data.length === 0) {
    return <ChartEmptyState />
  }

  const { xKey, yKey } = inferKeys(data, chart)
  if (!xKey || !yKey) {
    return <ChartEmptyState />
  }

  const type = (chartType || 'bar').toLowerCase()

  return (
    <div className="analytics-chart">
      <ResponsiveContainer width="100%" height="100%">
        {type === 'line' ? (
          <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(15, 20, 24, 0.12)" />
            <XAxis dataKey={xKey} stroke="#5d6570" />
            <YAxis stroke="#5d6570" />
            <Tooltip contentStyle={{ background: '#ffffff', borderColor: '#e6ddd3' }} />
            <Legend />
            <Line type="monotone" dataKey={yKey} stroke="#0f8a7b" strokeWidth={2} />
          </LineChart>
        ) : type === 'pie' ? (
          <PieChart>
            <Tooltip contentStyle={{ background: '#ffffff', borderColor: '#e6ddd3' }} />
            <Legend />
            <Pie dataKey={yKey} data={data} nameKey={xKey} outerRadius={110}>
              {data.map((entry, index) => (
                <Cell key={`${entry[xKey]}-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
          </PieChart>
        ) : (
          <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(15, 20, 24, 0.12)" />
            <XAxis dataKey={xKey} stroke="#5d6570" />
            <YAxis stroke="#5d6570" />
            <Tooltip contentStyle={{ background: '#ffffff', borderColor: '#e6ddd3' }} />
            <Legend />
            <Bar dataKey={yKey} fill="#0f8a7b" radius={[8, 8, 0, 0]} />
          </BarChart>
        )}
      </ResponsiveContainer>
    </div>
  )
}

export default AnalyticsChart
