import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "../api/auth";
import { useAuth } from "../hooks/useAuth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { setToken } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const res = await login({ email, password });
      setToken(res.access_token);
      navigate("/");
    } catch {
      setError("Invalid email or password");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <form onSubmit={handleSubmit} className="bg-white rounded shadow p-6 w-full max-w-sm space-y-4">
        <h1 className="text-lg font-semibold text-center">Login</h1>
        {error && <div className="text-xs text-red-600">{error}</div>}
        <div className="space-y-1">
          <label className="text-xs">Email</label>
          <input
            className="border rounded px-2 py-1 w-full text-sm"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="space-y-1">
          <label className="text-xs">Password</label>
          <input
            className="border rounded px-2 py-1 w-full text-sm"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button className="w-full bg-indigo-600 text-white text-sm py-2 rounded hover:bg-indigo-500">
          Login
        </button>
        <div className="text-xs text-center">
          No account? <Link className="text-indigo-600" to="/signup">Sign up</Link>
        </div>
      </form>
    </div>
  );
}
