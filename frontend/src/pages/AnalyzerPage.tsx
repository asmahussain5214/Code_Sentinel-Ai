import React, { useState } from 'react';
import api from '../services/api';
import { ShieldCheck, Bug, Lightbulb, Sparkles } from 'lucide-react';

export const AnalyzerPage: React.FC = () => {
  const [title, setTitle] = useState('');
  const [language, setLanguage] = useState('python');
  const [codeContent, setCodeContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      // 1. Save code snippet
      const snippetRes = await api.post('/snippets/', {
        title: title || 'Untitled Snippet',
        language,
        code_content: codeContent,
      });

      // 2. Run analysis
      const analysisRes = await api.post('/analysis/analyze', {
        snippet_id: snippetRes.data.id,
      });

      setResult(analysisRes.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Analysis request failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* Code Input Form */}
      <div className="bg-slate-800 border border-slate-700 p-6 rounded-xl">
        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-sky-400" />
          Code Security Analysis
        </h2>

        {error && <div className="bg-rose-500/10 border border-rose-500 text-rose-400 p-3 rounded mb-4 text-sm">{error}</div>}

        <form onSubmit={handleAnalyze} className="space-y-4">
          <div>
            <label className="block text-sm text-slate-300 mb-1">Snippet Title</label>
            <input
              type="text"
              placeholder="e.g. Auth Controller"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-white"
            />
          </div>

          <div>
            <label className="block text-sm text-slate-300 mb-1">Language</label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-white"
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
              <option value="typescript">TypeScript</option>
              <option value="sql">SQL</option>
            </select>
          </div>

          <div>
            <label className="block text-sm text-slate-300 mb-1">Source Code</label>
            <textarea
              rows={12}
              required
              placeholder="Paste code snippet here..."
              value={codeContent}
              onChange={(e) => setCodeContent(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded p-3 font-mono text-sm text-emerald-400 focus:outline-none focus:border-sky-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-sky-600 hover:bg-sky-500 disabled:opacity-50 text-white font-medium py-2.5 rounded transition"
          >
            {loading ? 'Analyzing Code...' : 'Run Security & Quality Scan'}
          </button>
        </form>
      </div>

      {/* Analysis Output Dashboard */}
      <div className="bg-slate-800 border border-slate-700 p-6 rounded-xl">
        <h2 className="text-xl font-bold text-white mb-4">Scan Results</h2>

        {!result && !loading && (
          <div className="h-64 flex items-center justify-center text-slate-500 text-sm">
            Submit code on the left to see instant quality & vulnerability scores.
          </div>
        )}

        {loading && (
          <div className="h-64 flex items-center justify-center text-sky-400 text-sm animate-pulse">
            Executing hybrid AI static analysis rules...
          </div>
        )}

        {result && (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-900 p-4 rounded-lg border border-slate-700">
                <span className="text-xs text-slate-400 block mb-1">Quality Score</span>
                <span className="text-2xl font-bold text-sky-400">{result.quality_score} / 10</span>
              </div>
              <div className="bg-slate-900 p-4 rounded-lg border border-slate-700">
                <span className="text-xs text-slate-400 block mb-1">Security Score</span>
                <span className="text-2xl font-bold text-emerald-400">{result.security_score} / 10</span>
              </div>
            </div>

            <div className="bg-slate-900/60 p-3 rounded border border-slate-700 text-sm text-slate-200">
              <strong>Summary:</strong> {result.summary}
            </div>

            <div>
              <h3 className="text-sm font-semibold text-rose-400 flex items-center gap-1.5 mb-2">
                <Bug className="w-4 h-4" /> Detected Vulnerabilities / Bugs
              </h3>
              <div className="bg-slate-900 p-3 rounded border border-slate-700 text-xs font-mono text-rose-300 whitespace-pre-wrap">
                {result.detected_bugs}
              </div>
            </div>

            <div>
              <h3 className="text-sm font-semibold text-amber-400 flex items-center gap-1.5 mb-2">
                <Lightbulb className="w-4 h-4" /> Recommendations & AI Feedback
              </h3>
              <div className="bg-slate-900 p-3 rounded border border-slate-700 text-xs font-mono text-slate-300 whitespace-pre-wrap">
                {result.suggestions}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};