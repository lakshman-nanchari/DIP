import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api/axios";

function SignupPage() {

  const navigate = useNavigate();

  const [form,setForm] = useState({
    full_name:"",
    email:"",
    password:"",
    organization:"",
    role:"analyst"
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSignup = async (e) => {

    e.preventDefault();

    setError("");
    setLoading(true);

    try {

      await API.post("/users", form);

      navigate("/");

    } catch (err) {

      if (err.response?.status === 400) {
        setError("Invalid input or user already exists");
      } else {
        setError("Signup failed. Please try again.");
      }

    } finally {
      setLoading(false);
    }

  };

  return (

    <div className="flex min-h-screen bg-linear-to-br from-stone-100 via-stone-50 to-stone-200">

      {/* LEFT SIDE BRAND */}

      <div className="hidden md:flex w-1/2 bg-stone-900 text-white flex flex-col justify-center items-center p-12">

        <h1 className="text-4xl font-bold mb-6">
          Data Intelligence
        </h1>

        <p className="text-stone-300 text-lg text-center max-w-md">
          Build dashboards, generate insights, forecast trends and detect
          anomalies from your datasets automatically.
        </p>

      </div>


      {/* RIGHT SIDE FORM */}

      <div className="flex w-full md:w-1/2 items-center justify-center">

        <form
          onSubmit={handleSignup}
          className="bg-white/90 backdrop-blur border border-stone-200 p-10 rounded-xl shadow-md w-96"
        >

          <h2 className="text-2xl font-bold mb-6 text-stone-800">
            Create Account
          </h2>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 text-sm p-3 rounded mb-4">
              {error}
            </div>
          )}

          <input
            name="full_name"
            placeholder="Full Name"
            onChange={handleChange}
            className="w-full mb-4 p-3 border border-stone-300 rounded focus:ring-2 focus:ring-amber-500 outline-none"
          />

          <input
            name="email"
            placeholder="Email"
            onChange={handleChange}
            className="w-full mb-4 p-3 border border-stone-300 rounded focus:ring-2 focus:ring-amber-500 outline-none"
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            onChange={handleChange}
            className="w-full mb-4 p-3 border border-stone-300 rounded focus:ring-2 focus:ring-amber-500 outline-none"
          />

          <input
            name="organization"
            placeholder="Organization"
            onChange={handleChange}
            className="w-full mb-4 p-3 border border-stone-300 rounded focus:ring-2 focus:ring-amber-500 outline-none"
          />

          <button
            disabled={loading}
            className="w-full bg-amber-600 hover:bg-amber-700 text-white py-3 rounded transition disabled:opacity-50"
          >
            {loading ? "Creating account..." : "Sign Up"}
          </button>

          <p className="text-sm text-center mt-4 text-stone-600">
            Already have an account?{" "}
            <Link to="/" className="text-amber-600 hover:underline">
              Login
            </Link>
          </p>

        </form>

      </div>

    </div>

  );
}

export default SignupPage;