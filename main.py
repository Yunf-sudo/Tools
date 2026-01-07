import os
import sys
import time
from colorama import Fore, Style, init

# 导入配置文件
import config
# 导入功能模块
from image_processor import ImageToolbox
from ai_manager import AIHub

# 初始化颜色输出
init(autoreset=True)

def clean_path(path_str):
    """辅助函数：清理路径中的引号和空格"""
    return path_str.strip().strip('"').strip("'")

def print_header(text):
    print(f"\n{Fore.CYAN}{'='*10} {text} {'='*10}{Style.RESET_ALL}")

def run_image_tools():
    tool = ImageToolbox()
    
    while True:
        print_header("图片处理工具箱")
        print("1. 单张图片处理 (增强/格式转换)")
        print("2. 文件夹批量处理")
        print("0. 返回主菜单")
        
        choice = input(f"\n{Fore.YELLOW}请选择功能序号: {Style.RESET_ALL}").strip()
        
        if choice == '0':
            break
            
        elif choice == '1':
            src = input("请输入源图片路径: ")
            dst = input("请输入输出路径 (包含文件名): ")
            enhance = input("是否开启画质增强? (y/n, 默认y): ").lower() != 'n'
            
            src = clean_path(src)
            dst = clean_path(dst)
            
            print(f"{Fore.BLUE}正在处理...")
            success, msg = tool.process_single(src, dst, enhance)
            if success:
                print(f"{Fore.GREEN}✔ 成功: {msg}")
            else:
                print(f"{Fore.RED}✘ 失败: {msg}")
                
        elif choice == '2':
            src_dir = input("请输入输入文件夹路径: ")
            dst_dir = input("请输入输出文件夹路径: ")
            enhance = input("是否开启画质增强? (y/n, 默认y): ").lower() != 'n'
            
            src_dir = clean_path(src_dir)
            dst_dir = clean_path(dst_dir)
            
            print(f"{Fore.BLUE}正在开始批量任务...")
            tool.process_batch(src_dir, dst_dir, enhance)
            
        else:
            print(f"{Fore.RED}输入无效，请重试。")
        
        input(f"\n按 {Fore.GREEN}Enter{Style.RESET_ALL} 键继续...")

def run_ai_tools():
    # 初始化 AI Hub 并从 config 加载配置
    hub = AIHub()
    
    # 注册模型 (仅当 Key 不为空时注册)
    if "你的" not in config.GEMINI_API_KEY:
        hub.register_gemini("gemini", config.GEMINI_API_KEY, config.MODELS['gemini'])
    
    if "你的" not in config.DEEPSEEK_API_KEY:
        hub.register_deepseek("deepseek", config.DEEPSEEK_API_KEY, config.MODELS['deepseek'])
        
    if "你的" not in config.OPENAI_API_KEY:
        hub.register_chatgpt("gpt", config.OPENAI_API_KEY, config.MODELS['chatgpt'])
        
    # 本地模型总是注册
    hub.register_ollama("local", config.MODELS['local'])

    while True:
        print_header("AI 模型实验室")
        print(f"可用模型: {', '.join(hub.clients.keys())}")
        print("-------------------")
        print("1. 进入对话模式")
        print("0. 返回主菜单")
        
        choice = input(f"\n{Fore.YELLOW}请选择: {Style.RESET_ALL}").strip()
        
        if choice == '0':
            break
            
        if choice == '1':
            model_key = input(f"请输入要使用的模型代号 (如 local, deepseek): ").strip()
            
            if model_key not in hub.clients:
                print(f"{Fore.RED}错误: 模型 '{model_key}' 未注册或未配置Key。")
                continue
                
            print(f"\n{Fore.GREEN}已连接到 {model_key}。输入 'exit' 退出对话。{Style.RESET_ALL}")
            while True:
                user_input = input(f"\n{Fore.WHITE}You: {Style.RESET_ALL}")
                if user_input.lower() in ['exit', 'quit']:
                    break
                if not user_input.strip():
                    continue
                    
                # 调用 AI
                hub.chat(model_key, user_input)

def main():
    while True:
        # 清屏 (Windows用cls, Mac/Linux用clear)
        # os.system('cls' if os.name == 'nt' else 'clear') 
        
        print(f"\n{Fore.MAGENTA}╔══════════════════════════════════╗")
        print(f"║     My Super ToolBox v1.0        ║")
        print(f"╚══════════════════════════════════╝{Style.RESET_ALL}")
        
        print("1. 🖼️  图片处理 (Image Processing)")
        print("2. 🤖  AI 模型调用 (AI Models)")
        print("0. 🚪  退出程序 (Exit)")
        
        option = input(f"\n{Fore.YELLOW}请输入功能序号并回车: {Style.RESET_ALL}").strip()
        
        if option == '1':
            run_image_tools()
        elif option == '2':
            run_ai_tools()
        elif option == '0':
            print(f"{Fore.CYAN}再见! Have a nice day.")
            sys.exit()
        else:
            print(f"{Fore.RED}无效选项，请重新输入。")

if __name__ == "__main__":
    main()