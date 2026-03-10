function KpiCard({ title, value }) {

  const formatValue = (val) => {
    if (typeof val === "number") {
      return val.toLocaleString();
    }
    return val;
  };

  return (
    <div className="bg-white shadow rounded p-6">

      <h3 className="text-sm text-gray-500 mb-2">
        {title}
      </h3>

      <p className="text-2xl font-bold text-indigo-600">
        {formatValue(value)}
      </p>

    </div>
  );
}

export default KpiCard;