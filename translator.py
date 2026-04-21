"""
Translate Japanese text to Simplified Chinese using local Ollama.
"""
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

SYSTEM_PROMPT = (
    "你是一个专业翻译。将用户输入的日语文本翻译成简体中文。"
    "只输出翻译结果，不要解释，不要加任何前缀。"
)


def translate(japanese_text: str) -> str:
    payload = {
        "model": MODEL,
        "system": SYSTEM_PROMPT,
        "prompt": japanese_text,
        "stream": False,
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "").strip()
    except requests.exceptions.ConnectionError:
        return "[错误：Ollama 未运行，请先执行 `ollama serve`]"
    except Exception as e:
        return f"[翻译错误: {e}]"
