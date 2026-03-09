function InsightsPanel({ insights }) {

  if (!insights || insights.length === 0) {
    return (
      <div className="bg-white shadow rounded p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">
          Insights
        </h2>

        <p className="text-gray-500">
          No insights available
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow rounded p-6 mb-8">

      <h2 className="text-xl font-semibold mb-4">
        Insights
      </h2>

      <ul className="space-y-3">

        {insights.map((item, index) => (
          <li
            key={index}
            className="bg-gray-50 p-3 rounded border text-sm"
          >
            {item}
          </li>
        ))}

      </ul>

    </div>
  );
}

export default InsightsPanel;