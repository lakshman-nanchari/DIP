function InsightsPanel({ insights }) {

  if (!insights) {
    return (
      <div className="bg-white shadow rounded p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Insights</h2>
        <p className="text-gray-500">No insights available</p>
      </div>
    );
  }

  const statistical = insights.statistical_insights || [];
  const business = insights.business_insights || [];

  return (
    <div className="bg-white shadow rounded p-6 mb-8">

      <h2 className="text-xl font-semibold mb-6">
        Insights
      </h2>

      {statistical.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-3 text-blue-600">
            Statistical Insights
          </h3>

          <ul className="space-y-3">
            {statistical.map((item, index) => (
              <li
                key={index}
                className="bg-gray-50 p-3 rounded border text-sm"
              >
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}

      {business.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold mb-3 text-green-600">
            Business Insights
          </h3>

          <ul className="space-y-3">
            {business.map((item, index) => (
              <li
                key={index}
                className="bg-green-50 p-3 rounded border text-sm"
              >
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}

    </div>
  );
}

export default InsightsPanel;