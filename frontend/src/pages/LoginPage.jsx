import { useContext, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api/axios";
import { AuthContext } from "../context/AuthContext";

function LoginPage() {
    const { login } = useContext(AuthContext);
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setpassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        setError("");

        try {

            const formData = new URLSearchParams();
            formData.append("username", email);
            formData.append("password", password);

            const res = await API.post("/users/login", formData, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            });

            login(res.data.access_token);

            navigate("/dashboard");

        } catch (err) {
            setError("Invalid credentials");
        }
    };

    return (

        <div className="flex min-h-screen bg-linear-to-br from-stone-100 via-stone-50 to-stone-200">

            {/* LEFT SIDE BRAND PANEL */}

            <div className="hidden md:flex w-1/2 bg-stone-900 text-white flex-col justify-center items-center p-12">

                <h1 className="text-4xl font-bold mb-6">
                    Data Intelligence
                </h1>

                <p className="text-stone-300 text-lg text-center max-w-md">
                    Upload datasets, analyze trends, detect anomalies, and generate powerful insights
                    from your data in seconds.
                </p>

            </div>


            {/* LOGIN FORM */}

            <div className="flex w-full md:w-1/2 items-center justify-center">

                <div className="bg-white/90 backdrop-blur border border-stone-200 p-8 rounded-xl shadow-lg w-96">

                    <h2 className="text-2xl font-bold mb-6 text-center text-stone-800">
                        Login
                    </h2>

                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-600 text-sm p-3 rounded mb-4">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-4">

                        <input
                            type="email"
                            placeholder="Email"
                            className="w-full border border-stone-300 p-3 rounded focus:outline-none focus:ring-2 focus:ring-amber-500 transition"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />

                        <input
                            type="password"
                            placeholder="Password"
                            className="w-full border border-stone-300 p-3 rounded focus:outline-none focus:ring-2 focus:ring-amber-500 transition"
                            value={password}
                            onChange={(e) => setpassword(e.target.value)}
                        />

                        <button
                            className="w-full bg-amber-600 text-white p-3 rounded hover:bg-amber-700 transition font-medium"
                        >
                            Login
                        </button>

                    </form>

                    <p className="mt-6 text-center text-sm text-stone-600">
                        No account?{" "}
                        <Link
                            to="/signup"
                            className="text-amber-600 font-medium hover:underline"
                        >
                            Sign up
                        </Link>
                    </p>

                </div>

            </div>

        </div>

    );
}

export default LoginPage;
