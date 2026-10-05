import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';

export const Register: React.FC = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleRegister = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    setError('');
    setLoading(true);

    try {
      await api.post('/auth/register', {
        username: username.trim(),
        email: email.trim(),
        password,
      });

      navigate('/login');

    } catch (err: any) {
      const detail = err.response?.data?.detail;

      if (Array.isArray(detail)) {
        setError(
          detail
            .map(
              (item: any) =>
                `${item.loc?.[item.loc.length - 1] ?? 'input'}: ${item.msg}`
            )
            .join(' | ')
        );
      } else if (typeof detail === 'string') {
        setError(detail);
      } else if (err.code === 'ERR_NETWORK') {
        setError(
          'Cannot reach the backend. Make sure FastAPI is running on port 8000.'
        );
      } else {
        setError(
          'Registration failed. Check the backend terminal for the exact error.'
        );
      }

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center">
      <div className="bg-slate-800 border border-slate-700 p-8 rounded-xl w-full max-w-md shadow-2xl">

        <h2 className="text-2xl font-bold text-white mb-6 text-center">
          Create Sentinel Account
        </h2>

        {error && (
          <div className="bg-rose-500/10 border border-rose-500 text-rose-400 p-3 rounded mb-4 text-sm">
            {error}
          </div>
        )}

        <form
          onSubmit={handleRegister}
          className="space-y-4"
        >
          <div>
            <label className="block text-sm text-slate-300 mb-1">
              Username
            </label>

            <input
              type="text"
              required
              minLength={3}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded p-2.5 text-white focus:outline-none focus:border-sky-500"
            />
          </div>

          <div>
            <label className="block text-sm text-slate-300 mb-1">
              Email
            </label>

            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded p-2.5 text-white focus:outline-none focus:border-sky-500"
            />
          </div>

          <div>
            <label className="block text-sm text-slate-300 mb-1">
              Password
            </label>

            <input
              type="password"
              required
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded p-2.5 text-white focus:outline-none focus:border-sky-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-sky-600 hover:bg-sky-500 disabled:opacity-50 text-white font-medium py-2.5 rounded transition"
          >
            {loading
              ? 'Creating Account...'
              : 'Register'}
          </button>
        </form>

        <p className="text-sm text-slate-400 text-center mt-4">
          Already registered?{' '}
          <Link
            to="/login"
            className="text-sky-400 hover:underline"
          >
            Login
          </Link>
        </p>

      </div>
    </div>
  );
};