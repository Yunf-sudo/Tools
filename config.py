# config.py

# 请将你的 Key 填入引号中
GEMINI_API_KEY = "你的_GEMINI_KEY"
OPENAI_API_KEY = "你的_OPENAI_KEY"
DEEPSEEK_API_KEY = "sk-fcf313630b854ab6b90dd24ef11ce3c8"

# 你可以在这里修改默认调用的模型版本
MODELS = {
    "gemini": "gemini-1.5-flash",
    "deepseek": "deepseek-reasoner",
    "chatgpt": "gpt-4o",
    "local": "qwen2.5:7b"  # 本地 Ollama 模型名称
}

# 默认增强倍数 (1.0 为原图，>1.0 为增强)
DEFAULT_ENHANCE_FACTOR = 1.3