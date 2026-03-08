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

    setError(""); // clear previous error

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
        <div className="min-h-screen flex items-center justify-center bg-gray-500">
            <div className="bg-white p-8 rounded-xl shadow-md w-96">

                <h2 className="text-2xl font-bold mb-6 text-center">
                    Login
                </h2>

                {error && (
                    <p className="text-red-500 text-sm mb-4">{error}</p>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">

                    <input
                        type="email"
                        placeholder="email"
                        className="w-full border p-3 rounded"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        className="w-full border p-3 rounded"
                        value={password}
                        onChange={(e) => setpassword(e.target.value)}
                    />

                    <button
                        className="w-full bg-indigo-600 text-white p-3 rounded hover:bg-indigo-700"
                    >
                        Login
                    </button>

                </form>

                <p className="mt-4 text-center text-sm">
                    No account?{" "}
                    <Link to="/signup" className="text-indigo-600">
                        Sign up
                    </Link>
                </p>

            </div>
        </div>
    );
}

export default LoginPage;