import os
import time
from PIL import Image, ImageEnhance, ImageFilter
from tqdm import tqdm
from colorama import Fore, Style, init

# 初始化颜色输出
init(autoreset=True)

class ImageToolbox:
    def __init__(self):
        self.supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

    def enhance_quality(self, img_obj, factor=1.3):
        """
        综合画质增强管道：
        1. 锐化 (Sharpening)
        2. 对比度增强 (Contrast)
        3. 色彩饱和度优化 (Color)
        """
        # 1. 锐化
        enhancer = ImageEnhance.Sharpness(img_obj)
        img_obj = enhancer.enhance(factor * 1.2)  # 稍微加强锐化

        # 2. 对比度
        enhancer = ImageEnhance.Contrast(img_obj)
        img_obj = enhancer.enhance(factor * 1.1)

        # 3. 色彩 (防止过饱和)
        enhancer = ImageEnhance.Color(img_obj)
        img_obj = enhancer.enhance(factor * 1.05)
        
        # 4. 简单的降噪 (可选，此处使用中值滤波去除噪点)
        # img_obj = img_obj.filter(ImageFilter.MedianFilter(size=3))
        
        return img_obj

    def process_single(self, input_path, output_path, enhance=True):
        """处理单张图片"""
        try:
            with Image.open(input_path) as img:
                # 转换颜色模式，防止RGBA保存为JPEG报错
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                if enhance:
                    img = self.enhance_quality(img)
                
                # 确保输出目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                img.save(output_path, quality=95, subsampling=0)
                return True, f"Saved to {output_path}"
        except Exception as e:
            return False, str(e)

    def process_batch(self, input_dir, output_dir, enhance=True):
        """批量处理目录"""
        if not os.path.exists(input_dir):
            print(f"{Fore.RED}错误: 输入目录不存在")
            return

        # 收集所有图片
        tasks = []
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith(self.supported_formats):
                    src_path = os.path.join(root, file)
                    # 保持原有的目录结构
                    rel_path = os.path.relpath(src_path, input_dir)
                    dst_path = os.path.join(output_dir, rel_path)
                    tasks.append((src_path, dst_path))

        print(f"{Fore.CYAN}发现 {len(tasks)} 张图片，开始处理...")

        # 使用 tqdm 显示进度条
        success_count = 0
        for src, dst in tqdm(tasks, desc="Processing", unit="img"):
            status, _ = self.process_single(src, dst, enhance)
            if status:
                success_count += 1
        
        print(f"\n{Fore.GREEN}处理完成! 成功: {success_count}/{len(tasks)}")
        print(f"输出目录: {output_dir}")

# --- 简单测试接口 ---
if __name__ == "__main__":
    tool = ImageToolbox()
    print(f"{Fore.YELLOW}=== 图片处理工具箱 ===")
    mode = input("选择模式 (1: 单张, 2: 目录批量): ").strip()
    
    if mode == "1":
        i_path = input("输入图片路径: ").strip().strip('"') # 去除可能存在的引号
        o_path = input("输出图片路径 (包含文件名): ").strip().strip('"')
        tool.process_single(i_path, o_path)
        print(f"{Fore.GREEN}单张处理完成。")
        
    elif mode == "2":
        i_dir = input("输入文件夹路径: ").strip().strip('"')
        o_dir = input("输出文件夹路径: ").strip().strip('"')
        tool.process_batch(i_dir, o_dir)