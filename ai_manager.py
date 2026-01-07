import os
import google.generativeai as genai
from openai import OpenAI
from abc import ABC, abstractmethod

# 尝试导入 ollama，防止用户没装报错
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

class AIModelInterface(ABC):
    """AI 模型统一接口"""
    @abstractmethod
    def chat(self, prompt, system_prompt=None):
        pass

class GeminiClient(AIModelInterface):
    """Google Gemini 专用客户端"""
    def __init__(self, api_key, model_name="gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.name = "Gemini"

    def chat(self, prompt, system_prompt="You are a helpful assistant."):
        # Gemini 的 system prompt 通常在配置里，但在简单调用中，
        # 我们可以将其合并到 prompt 前面，或者使用最新的 system_instruction (取决于库版本)
        full_prompt = f"System: {system_prompt}\nUser: {prompt}"
        
        try:
            print(f"✨ {self.name}: ", end="", flush=True)
            response = self.model.generate_content(full_prompt, stream=True)
            full_text = ""
            for chunk in response:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_text += chunk.text
            print()
            return full_text
        except Exception as e:
            return f"Gemini Error: {str(e)}"

class OpenAICompatibleClient(AIModelInterface):
    """通用客户端：支持 ChatGPT 和 DeepSeek"""
    def __init__(self, api_key, base_url, model_name, client_name="AI"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name
        self.name = client_name

    def chat(self, prompt, system_prompt="You are a helpful assistant."):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        try:
            print(f"🚀 {self.name}: ", end="", flush=True)
            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=True
            )
            full_text = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_text += content
            print()
            return full_text
        except Exception as e:
            return f"{self.name} Error: {str(e)}"

class LocalOllamaClient(AIModelInterface):
    """本地 Ollama 客户端"""
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
    
    def chat(self, prompt, system_prompt=""):
        if not OLLAMA_AVAILABLE: return "Error: Ollama library not installed."
        try:
            print(f"🦙 Ollama: ", end="", flush=True)
            stream = ollama.chat(model=self.model_name, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt},
            ], stream=True)
            full_text = ""
            for chunk in stream:
                content = chunk['message']['content']
                print(content, end="", flush=True)
                full_text += content
            print()
            return full_text
        except Exception as e:
            return f"Ollama Error: {str(e)}"

class AIHub:
    """统一管理中心"""
    def __init__(self):
        self.clients = {}

    def register_gemini(self, name, api_key, model="gemini-1.5-flash"):
        self.clients[name] = GeminiClient(api_key, model)

    def register_chatgpt(self, name, api_key, model="gpt-4o"):
        # ChatGPT 使用默认的 OpenAI URL
        self.clients[name] = OpenAICompatibleClient(
            api_key, "https://api.openai.com/v1", model, "ChatGPT"
        )

    def register_deepseek(self, name, api_key, model="deepseek-chat"):
        # DeepSeek 使用特定的 URL
        self.clients[name] = OpenAICompatibleClient(
            api_key, "https://api.deepseek.com", model, "DeepSeek"
        )

    def register_ollama(self, name, model="llama3"):
        self.clients[name] = LocalOllamaClient(model)

    def chat(self, client_name, prompt):
        if client_name not in self.clients:
            print(f"Error: 模型 '{client_name}' 未注册。")
            return
        return self.clients[client_name].chat(prompt)

# --- 使用示例 ---
if __name__ == "__main__":
    # 建议使用环境变量加载 Key，这里为了演示方便留空，请填入你的真实 Key
    GEMINI_KEY = "你的_GEMINI_API_KEY"
    OPENAI_KEY = "你的_OPENAI_API_KEY"
    DEEPSEEK_KEY = "你的_DEEPSEEK_API_KEY"

    hub = AIHub()

    # 1. 注册 DeepSeek (性价比高，常用)
    # DeepSeek 官方 API 地址通常是 https://api.deepseek.com
    if DEEPSEEK_KEY != "你的_DEEPSEEK_API_KEY":
        hub.register_deepseek("ds", DEEPSEEK_KEY, "deepseek-chat")

    # 2. 注册 Gemini (速度快，免费额度大)
    if GEMINI_KEY != "你的_GEMINI_API_KEY":
        hub.register_gemini("gemini", GEMINI_KEY)

    # 3. 注册 ChatGPT
    if OPENAI_KEY != "你的_OPENAI_API_KEY":
        hub.register_chatgpt("gpt", OPENAI_KEY)
    
    # 4. 注册本地 Ollama (无需 Key)
    hub.register_ollama("local", "llama3")

    print("=== 全能 AI 助手 (DeepSeek / Gemini / ChatGPT / Ollama) ===")
    print("可用模型代码: ds, gemini, gpt, local")
    
    while True:
        model_choice = input("\n请选择模型 (输入 q 退出): ").strip()
        if model_choice == 'q': break
        
        prompt = input("请输入问题: ")
        hub.chat(model_choice, prompt)