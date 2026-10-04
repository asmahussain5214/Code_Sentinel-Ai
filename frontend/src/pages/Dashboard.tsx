import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Code, Shield } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const [snippets, setSnippets] = useState<any[]>([]);

  useEffect(() => {
    api.get('/snippets/')
      .then((res) => setSnippets(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
        <Shield className="w-6 h-6 text-sky-400" />
        Code Sentinel Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {snippets.map((s) => (
          <div key={s.id} className="bg-slate-800 border border-slate-700 p-5 rounded-xl hover:border-sky-500 transition">
            <div className="flex justify-between items-center mb-2">
              <h3 className="font-semibold text-white">{s.title}</h3>
              <span className="text-xs bg-slate-900 text-sky-400 px-2 py-0.5 rounded font-mono uppercase">{s.language}</span>
            </div>
            <pre className="bg-slate-900 p-3 rounded text-xs font-mono text-slate-400 overflow-hidden text-ellipsis h-24 mb-3">
              {s.code_content}
            </pre>
            <span className="text-xs text-slate-500">ID: #{s.id}</span>
          </div>
        ))}

        {snippets.length === 0 && (
          <div className="col-span-full bg-slate-800/50 border border-slate-700 p-8 rounded-xl text-center text-slate-400">
            No code snippets scanned yet. Go to <strong className="text-sky-400">Analyze Code</strong> to scan your first snippet!
          </div>
        )}
      </div>
    </div>
  );
};