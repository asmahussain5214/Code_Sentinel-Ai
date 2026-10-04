import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShieldAlert, Code2, LogOut, LayoutDashboard } from 'lucide-react';

export const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="bg-slate-900 border-b border-slate-800 text-white px-6 py-4 flex justify-between items-center">
      <Link to="/" className="flex items-center gap-2 text-xl font-bold text-sky-400">
        <ShieldAlert className="w-6 h-6 text-sky-400" />
        <span>CodeSentinel AI</span>
      </Link>

      {token ? (
        <div className="flex items-center gap-6">
          <Link to="/dashboard" className="flex items-center gap-1 hover:text-sky-400 transition">
            <LayoutDashboard className="w-4 h-4" />
            <span>Dashboard</span>
          </Link>
          <Link to="/analyze" className="flex items-center gap-1 hover:text-sky-400 transition">
            <Code2 className="w-4 h-4" />
            <span>Analyze Code</span>
          </Link>
          <button
            onClick={handleLogout}
            className="flex items-center gap-1 text-rose-400 hover:text-rose-300 transition"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </button>
        </div>
      ) : (
        <div className="flex gap-4">
          <Link to="/login" className="hover:text-sky-400 transition">Login</Link>
          <Link to="/register" className="bg-sky-600 hover:bg-sky-500 text-white px-4 py-1.5 rounded-md font-medium transition">
            Register
          </Link>
        </div>
      )}
    </nav>
  );
};