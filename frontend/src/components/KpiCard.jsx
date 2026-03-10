function KpiCard({ title, value }) {

  const formatValue = (val) => {
    if (typeof val === "number") {
      return val.toLocaleString();
    }
    return val;
  };

  return (
    <div className="bg-white/80 backdrop-blur border border-stone-200 rounded-xl p-6 shadow-sm hover:shadow-lg transition">

      <h3 className="text-stone-500 text-sm mb-2">
        {title}
      </h3>

      <p className="text-2xl font-bold text-amber-600">
        {formatValue(value)}
      </p>

    </div>
  );
}

export default KpiCard;