function AnalyticsInput({ value, onChange, onSubmit, disabled }) {
  return (
    <form
      onSubmit={onSubmit}
      className="analytics-input"
    >
      <input
        type="text"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Ask a business question..."
        className="analytics-input-field"
      />
      <button
        type="submit"
        disabled={disabled}
        className="button primary analytics-button"
      >
        Generate
      </button>
    </form>
  )
}

export default AnalyticsInput
