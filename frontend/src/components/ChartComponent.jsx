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
      <div className="bg-white shadow rounded p-6">
        <h3 className="font-semibold mb-4">{title}</h3>
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow rounded p-6">

      <h3 className="font-semibold mb-4">{title}</h3>

      <ResponsiveContainer width="100%" height={300}>

        {type === "bar" ? (

          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="index" />
            <YAxis domain={['auto','auto']} />
            <Tooltip />
            <Bar
              dataKey="value"
              fill="#6366f1"
            />
          </BarChart>

        ) : (

          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="index" />
            <YAxis domain={['auto','auto']} />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="value"
              stroke="#6366f1"
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