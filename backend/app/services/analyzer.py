from typing import Dict, Any


def analyze_code_snippet(code: str, language: str) -> Dict[str, Any]:
    """Performs static code review, quality scoring, and vulnerability detection."""
    detected_bugs = []
    quality_score = 10.0
    security_score = 10.0
    suggestions = []

    lines = code.splitlines()

    # Rule 1: Check snippet length
    if len(lines) > 200:
        quality_score -= 1.5
        suggestions.append("Consider refactoring large files into smaller, modular functions.")

    # Rule 2: Basic security checks per language
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

    # Rule 3: Code style & quality checks
    todo_count = lowered_code.count("todo") + lowered_code.count("fixme")
    if todo_count > 0:
        quality_score -= min(todo_count * 0.5, 2.0)
        detected_bugs.append(f"[Quality] Found {todo_count} unresolved TODO/FIXME comment(s).")

    # Clamp scores between 0.0 and 10.0
    quality_score = max(0.0, min(10.0, round(quality_score, 1)))
    security_score = max(0.0, min(10.0, round(security_score, 1)))

    # Generate summary statement
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