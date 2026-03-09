function AnomalyTable({ anomalies }) {

  if (!anomalies || anomalies.length === 0) {
    return <p>No anomalies detected.</p>;
  }

  const columns = Object.keys(anomalies[0].values);

  return (
    <div className="bg-white shadow rounded p-4 mt-4 overflow-auto">

      <table className="min-w-full text-sm">

        <thead>
          <tr className="border-b">

            <th className="p-2 text-left">Row</th>

            {columns.map(col => (
              <th key={col} className="p-2 text-left">{col}</th>
            ))}

          </tr>
        </thead>

        <tbody>

          {anomalies.map((row, i) => (
            <tr key={i} className="border-b">

              <td className="p-2 font-medium">
                {row.row_index}
              </td>

              {columns.map(col => (
                <td key={col} className="p-2">
                  {String(row.values[col])}
                </td>
              ))}

            </tr>
          ))}

        </tbody>

      </table>

    </div>
  );
}

export default AnomalyTable;