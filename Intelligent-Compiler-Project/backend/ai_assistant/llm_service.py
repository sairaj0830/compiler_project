import os

# Uses the new unified Google Gen AI SDK ("google-genai" on PyPI):
#   pip install google-genai --break-system-packages
# The old "google-generativeai" package is deprecated by Google.
from google import genai

MODEL_NAME = "gemini-3.6-flash"


def _get_api_key() -> str | None:
    """
    Reads the Gemini API key from the environment.
    NEVER hardcode a real key here as a default value -- if this file is
    ever shared, committed, or uploaded, that key is compromised.
    """
    return os.environ.get("GEMINI_API_KEY")


def explain_error(code: str, error_message: str) -> str:
    """
    Calls the LLM API to explain a compiler error.
    If no API key is provided, returns a mock response.
    """
    api_key = _get_api_key()
    if not api_key:
        return (
            f"[Mock AI] It looks like you have a '{error_message}'. "
            f"Check your syntax around that line. "
            f"(Set GEMINI_API_KEY for real AI suggestions)."
        )

    try:
        client = genai.Client(api_key=api_key)
        prompt = (
            "Explain this compiler error to a student in simple terms and "
            "suggest a fix. Do not write the whole program, just the fix.\n\n"
            f"Code:\n{code}\n\nError: {error_message}"
        )
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"[AI Error] Could not connect to AI service: {str(e)}"


def explain_optimization(unoptimized_tac: list, optimized_tac: list) -> str:
    """
    Calls the LLM API to explain why the optimized TAC is better.
    If no API key is provided, returns a mock response.
    """
    api_key = _get_api_key()
    if not api_key:
        return (
            "[Mock AI] The optimizer simplified your code by pre-calculating "
            "constants (Constant Folding) and removing unused variables "
            "(Dead Code Elimination)."
        )

    try:
        client = genai.Client(api_key=api_key)
        unopt_str = "\n".join(str(i) for i in unoptimized_tac)
        opt_str = "\n".join(str(i) for i in optimized_tac)
        prompt = (
            "Explain the optimizations applied between the unoptimized TAC "
            f"and optimized TAC.\n\nUnoptimized:\n{unopt_str}\n\n"
            f"Optimized:\n{opt_str}"
        )
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"[AI Error] Could not connect to AI service: {str(e)}"
