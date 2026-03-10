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

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSignup = async (e) => {

    e.preventDefault();

    try {

      await API.post("/users", form);

      alert("Account created");

      navigate("/");

    } catch {
      alert("Signup failed");
    }

  };

  return (

    <div className="flex min-h-screen">

      {/* LEFT SIDE BRAND */}

      <div className="w-1/2 bg-stone-900 text-white flex flex-col justify-center items-center p-12">

        <h1 className="text-4xl font-bold mb-6">
          Data Intelligence
        </h1>

        <p className="text-stone-300 text-lg text-center max-w-md">
          Build dashboards, generate insights, forecast trends and detect
          anomalies from your datasets automatically.
        </p>

      </div>


      {/* RIGHT SIDE FORM */}

      <div className="w-1/2 flex items-center justify-center bg-stone-100">

        <form
          onSubmit={handleSignup}
          className="bg-white border border-stone-200 p-10 rounded-xl shadow-md w-96"
        >

          <h2 className="text-2xl font-bold mb-6 text-stone-800">
            Create Account
          </h2>

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

          <select
            name="role"
            onChange={handleChange}
            className="w-full mb-6 p-3 border border-stone-300 rounded focus:ring-2 focus:ring-amber-500 outline-none"
          >
            <option value="analyst">Analyst</option>
            <option value="admin">Admin</option>
          </select>

          <button
            className="w-full bg-amber-600 hover:bg-amber-700 text-white py-3 rounded transition"
          >
            Sign Up
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