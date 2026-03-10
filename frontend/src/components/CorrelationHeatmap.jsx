export default function CorrelationHeatmap({ correlation }) {

  const columns = Object.keys(correlation)

  return (
    <div className="overflow-x-auto">

      <table className="table-auto border">

        <thead>
          <tr>
            <th></th>
            {columns.map(col => (
              <th key={col} className="p-2">{col}</th>
            ))}
          </tr>
        </thead>

        <tbody>

          {columns.map(row => (
            <tr key={row}>

              <td className="font-semibold p-2">{row}</td>

              {columns.map(col => {

                const value = correlation[row][col]

                const color =
                  value > 0.7
                    ? "bg-red-300"
                    : value > 0.4
                    ? "bg-yellow-200"
                    : "bg-green-200"

                return (
                  <td key={col} className={`p-2 text-center ${color}`}>
                    {value.toFixed(2)}
                  </td>
                )
              })}

            </tr>
          ))}

        </tbody>

      </table>

    </div>
  )
}