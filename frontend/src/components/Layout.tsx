import { ReactNode } from "react";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";

export default function Layout({ children }: { children: ReactNode }) {
  const { setToken } = useAuth();
  const navigate = useNavigate();

  const logout = () => {
    setToken(null);
    navigate("/login");
  };

  return (
    <div className="min-h-screen flex bg-slate-100">
      <aside className="w-64 bg-slate-900 text-slate-50 p-4 flex flex-col">
        <h1 className="text-xl font-bold mb-4">Team Task Manager</h1>
        <button
          className="mt-auto py-2 px-3 rounded bg-slate-700 hover:bg-slate-600 text-sm"
          onClick={logout}
        >
          Logout
        </button>
      </aside>
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
