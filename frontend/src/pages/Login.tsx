import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';

export const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await api.post('/auth/login', formData);
      localStorage.setItem('token', response.data.access_token);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid username or password');
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center">
      <div className="bg-slate-800 border border-slate-700 p-8 rounded-xl w-full max-w-md shadow-2xl">
        <h2 className="text-2xl font-bold text-white mb-6 text-center">Login to CodeSentinel</h2>
        {error && <div className="bg-rose-500/10 border border-rose-500 text-rose-400 p-3 rounded mb-4 text-sm">{error}</div>}
        
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm text-slate-300 mb-1">Username</label>
            <input
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded p-2.5 text-white focus:outline-none focus:border-sky-500"
            />
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-1">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded p-2.5 text-white focus:outline-none focus:border-sky-500"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-sky-600 hover:bg-sky-500 text-white font-medium py-2.5 rounded transition"
          >
            Sign In
          </button>
        </form>
        <p className="text-sm text-slate-400 text-center mt-4">
          Don't have an account? <Link to="/register" className="text-sky-400 hover:underline">Register</Link>
        </p>
      </div>
    </div>
  );
};