import os
from typing import Dict, Any

# Optional: Attempt to load groq or google.generativeai if installed
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


def _run_static_analysis(code: str, language: str) -> Dict[str, Any]:
    """Fallback static code review engine."""
    detected_bugs = []
    quality_score = 10.0
    security_score = 10.0
    suggestions = []

    lines = code.splitlines()

    if len(lines) > 200:
        quality_score -= 1.5
        suggestions.append("Consider refactoring large files into smaller, modular functions.")

    lowered_code = code.lower()

    if "password" in lowered_code and ("=" in lowered_code or ":" in lowered_code):
        security_score -= 3.0
        detected_bugs.append("[Security] Hardcoded credential or secret key detected.")
        suggestions.append("Move hardcoded secrets to environment variables (.env).")

    if language.lower() in ["python", "javascript", "typescript"]:
        if "eval(" in lowered_code:
            security_score -= 4.0
            detected_bugs.append("[Security] Critical use of eval() detected, enabling arbitrary code execution.")
            suggestions.append("Avoid using eval(). Use safe parsers like json.loads() or ast.literal_eval().")

    if "select " in lowered_code and "+" in lowered_code:
        security_score -= 3.5
        detected_bugs.append("[Security] Potential SQL Injection vulnerability via string concatenation.")
        suggestions.append("Use parameterized queries or ORM models instead of string concatenation.")

    todo_count = lowered_code.count("todo") + lowered_code.count("fixme")
    if todo_count > 0:
        quality_score -= min(todo_count * 0.5, 2.0)
        detected_bugs.append(f"[Quality] Found {todo_count} unresolved TODO/FIXME comment(s).")

    quality_score = max(0.0, min(10.0, round(quality_score, 1)))
    security_score = max(0.0, min(10.0, round(security_score, 1)))

    if security_score < 6.0:
        summary = "CRITICAL: Security issues detected. Immediate code remediation required."
    elif quality_score < 7.0:
        summary = "WARNING: Code quality issues found. Refactoring recommended."
    else:
        summary = "PASS: Code structure and security posture look healthy."

    return {
        "quality_score": quality_score,
        "security_score": security_score,
        "summary": summary,
        "suggestions": "\n".join(suggestions) if suggestions else "No major issues identified.",
        "detected_bugs": "\n".join(detected_bugs) if detected_bugs else "No critical bugs detected.",
    }


def analyze_code_snippet(code: str, language: str) -> Dict[str, Any]:
    """Performs hybrid AI + static analysis on the provided code snippet."""
    # Run base static analysis rules
    static_res = _run_static_analysis(code, language)

    groq_api_key = os.getenv("GROQ_API_KEY")

    # If Groq client and API key are present, enhance findings via LLM
    if GROQ_AVAILABLE and groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            prompt = f"""
            You are a Senior Security Engineer and Code Reviewer. Analyze the following {language} snippet:

            ```{language}
            {code}
            ```

            Provide a concise output in this format:
            SUMMARY: <1 sentence overall health statement>
            SUGGESTIONS: <2-3 bullet points for improvement>
            BUGS: <Bullet points of bugs or security vulnerabilities found>
            """

            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )

            llm_text = chat_completion.choices[0].message.content
            
            # Combine static analysis scores with AI insights
            return {
                "quality_score": static_res["quality_score"],
                "security_score": static_res["security_score"],
                "summary": f"[AI Assisted] {static_res['summary']}",
                "suggestions": f"Static Rules:\n{static_res['suggestions']}\n\nAI Insights:\n{llm_text}",
                "detected_bugs": static_res["detected_bugs"],
            }
        except Exception as e:
            # Fall back gracefully to static rules on LLM API error
            static_res["summary"] += f" (LLM Bypass: {str(e)})"
            return static_res

    return static_res