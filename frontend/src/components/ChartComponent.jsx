import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

function ChartComponent({ title, data, type = "line" }) {

  if (!data || data.length === 0) {
    return (
      <div className="bg-white border border-stone-200 rounded-xl p-6 shadow-sm">
        <h3 className="font-semibold mb-4">{title}</h3>
        <p className="text-stone-500">No data available</p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-stone-200 rounded-xl p-6 shadow-sm">

      <h3 className="font-semibold mb-4 text-stone-800">
        {title}
      </h3>

      <ResponsiveContainer width="100%" height={300}>

        {type === "bar" ? (

          <BarChart data={data}>

            <CartesianGrid strokeDasharray="3 3" stroke="#e7e5e4" />

            <XAxis
              dataKey="index"
              tick={{ fill: "#57534e", fontSize: 12 }}
            />

            <YAxis
              domain={['auto','auto']}
              tick={{ fill: "#57534e", fontSize: 12 }}
            />

            <Tooltip
              contentStyle={{
                backgroundColor: "#fafaf9",
                border: "1px solid #e7e5e4",
                borderRadius: "8px"
              }}
            />

            <Bar
              dataKey="value"
              fill="#d97706"
              radius={[6,6,0,0]}
            />

          </BarChart>

        ) : (

          <LineChart data={data}>

            <CartesianGrid strokeDasharray="3 3" stroke="#e7e5e4" />

            <XAxis
              dataKey="index"
              tick={{ fill: "#57534e", fontSize: 12 }}
            />

            <YAxis
              domain={['auto','auto']}
              tick={{ fill: "#57534e", fontSize: 12 }}
            />

            <Tooltip
              contentStyle={{
                backgroundColor: "#fafaf9",
                border: "1px solid #e7e5e4",
                borderRadius: "8px"
              }}
            />

            <Line
              type="monotone"
              dataKey="value"
              stroke="#d97706"
              strokeWidth={2}
              dot={false}
            />

          </LineChart>

        )}

      </ResponsiveContainer>

    </div>
  );
}

export default ChartComponent;