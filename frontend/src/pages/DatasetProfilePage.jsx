import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import axios from "../api/axios"
import Navbar from "../components/Navbar"
import Sidebar from "../components/Sidebar"
import CorrelationHeatmap from "../components/CorrelationHeatmap" 
import Breadcrumbs from "../components/Breadcrumbs"

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts"

export default function DatasetProfilePage() {

  const { dataset_id } = useParams()

  const [profile, setProfile] = useState(null)

  useEffect(() => {

    if (!dataset_id) return

    fetchProfile()

  }, [dataset_id])

  const fetchProfile = async () => {
    try {
      const res = await axios.get(`/analytics/${dataset_id}/profile`)
      setProfile(res.data)
    } catch (err) {
      console.error("Failed to load profile", err)
    }
  }

  if (!profile) return <div className="p-10">Loading profile...</div>

  const missingValues = profile?.missing_values || {}
  const numericSummaryData = profile?.numeric_summary || {}
  const columnTypes = profile?.column_types || {}

  const missingData = Object.entries(missingValues).map(
    ([key, value]) => ({
      column: key,
      missing: value
    })
  )

  const numericSummary = Object.entries(numericSummaryData).map(
    ([col, stats]) => ({
      column: col,
      mean: stats?.mean ?? 0
    })
  )

  return (
    <div className="flex min-h-screen text-stone-800 bg-linear-to-br
      from-stone-100
      via-stone-50
      to-stone-200">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-8 max-w-7xl mx-auto space-y-10">

          <Breadcrumbs />

          <h1 className="text-3xl font-bold">
            Dataset Profile
          </h1>

          {/* BASIC INFO */}

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">

            <div className="bg-white border border-stone-200 p-6 rounded-xl shadow-sm">
              <p className="text-gray-500">Rows</p>
              <p className="text-2xl font-bold">{profile?.rows ?? 0}</p>
            </div>

            <div className="bg-white border border-stone-200 p-6 rounded-xl shadow-sm">
              <p className="text-gray-500">Columns</p>
              <p className="text-2xl font-bold">{profile?.columns ?? 0}</p>
            </div>

          </div>

          {/* COLUMN TYPES */}

          <div className="bg-white border border-stone-200 p-6 rounded-xl shadow-sm">

            <h2 className="text-xl font-semibold mb-4">
              Column Types
            </h2>

            <table className="w-full">

              <thead>
                <tr className="text-left border-b">
                  <th className="py-2">Column</th>
                  <th>Type</th>
                </tr>
              </thead>

              <tbody>
                {Object.entries(columnTypes).map(([col, type]) => (
                  <tr key={col} className="border-b">
                    <td className="py-2">{col}</td>
                    <td>{type}</td>
                  </tr>
                ))}
              </tbody>

            </table>

          </div>

          {/* MISSING VALUES */}

          <div className="bg-white border border-stone-200 p-6 rounded-xl shadow-sm">

            <h2 className="text-xl font-semibold mb-4">
              Missing Values
            </h2>

            <ResponsiveContainer width="100%" height={300}>

              <BarChart data={missingData}>

                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="column" />

                <YAxis />

                <Tooltip />

                <Bar dataKey="missing" />

              </BarChart>

            </ResponsiveContainer>

          </div>

          {/* NUMERIC SUMMARY */}

          <div className="bg-white border border-stone-200 p-6 rounded-xl shadow-sm">

            <h2 className="text-xl font-semibold mb-4">
              Numeric Column Means
            </h2>

            <ResponsiveContainer width="100%" height={300}>

              <BarChart data={numericSummary}>

                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="column" />

                <YAxis />

                <Tooltip />

                <Bar dataKey="mean" />

              </BarChart>

            </ResponsiveContainer> 

          </div>
             
          {/* CORRELATION HEATMAP */}

          <div>

            {profile?.correlation && Object.keys(profile.correlation).length > 0 && (

              <div className="bg-white border border-stone-200 p-6 rounded-xl shadow-sm">

                <h2 className="text-xl font-semibold mb-4">
                  Correlation Matrix
                </h2>

                <CorrelationHeatmap correlation={profile.correlation} />

              </div>

            )}

          </div>

        </div>

      </div>

    </div>
  )
}