"""
项目结构验证脚本
检查所有必要文件和目录是否存在
"""

import os
import sys
from pathlib import Path

def check_project_structure():
    """检查项目结构"""
    print("华强买瓜视频分割项目 - 结构验证")
    print("=" * 50)
    
    # 必需文件列表
    required_files = [
        "main.py",
        "demo.py", 
        "setup.py",
        "config.py",
        "requirements.txt",
        "README.md",
        "QUICKSTART.md",
        "processor/__init__.py",
        "processor/chunked_processor.py",
        "processor/optimized_processor.py",
        "processor/utils.py"
    ]
    
    # 必需目录列表
    required_dirs = [
        "models",
        "input",
        "output", 
        "temp",
        "logs",
        "processor"
    ]
    
    # 检查文件
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
            print(f"✓ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"✗ {file_path}")
    
    # 检查目录
    missing_dirs = []
    existing_dirs = []
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            existing_dirs.append(dir_path)
            print(f"✓ {dir_path}/")
        else:
            missing_dirs.append(dir_path)
            print(f"✗ {dir_path}/")
    
    # 检查输入视频
    input_video = "input/huaqiang_maigua.mp4"
    if os.path.exists(input_video):
        print(f"✓ {input_video}")
    else:
        print(f"✗ {input_video} (请将视频文件放在此处)")
    
    # 显示统计信息
    print("\n" + "=" * 50)
    print("统计信息")
    print("=" * 50)
    print(f"必需文件: {len(required_files)}")
    print(f"已存在文件: {len(existing_files)}")
    print(f"缺失文件: {len(missing_files)}")
    print(f"必需目录: {len(required_dirs)}")
    print(f"已存在目录: {len(existing_dirs)}")
    print(f"缺失目录: {len(missing_dirs)}")
    
    # 检查Python环境
    print("\n" + "=" * 50)
    print("Python环境检查")
    print("=" * 50)
    
    try:
        import sys
        print(f"Python版本: {sys.version}")
        
        # 检查关键依赖
        dependencies = [
            ("opencv-python", "cv2"),
            ("numpy", "numpy"),
            ("torch", "torch"),
            ("PIL", "PIL"),
            ("tqdm", "tqdm")
        ]
        
        for package_name, import_name in dependencies:
            try:
                __import__(import_name)
                print(f"✓ {package_name}")
            except ImportError:
                print(f"✗ {package_name}")
                
    except Exception as e:
        print(f"检查Python环境时出现错误: {str(e)}")
    
    # 生成建议
    print("\n" + "=" * 50)
    print("建议操作")
    print("=" * 50)
    
    if missing_files or missing_dirs:
        print("需要完成的操作:")
        for file_path in missing_files:
            print(f"  - 创建文件: {file_path}")
        for dir_path in missing_dirs:
            print(f"  - 创建目录: {dir_path}")
        print("\n运行以下命令完成设置:")
        print("  python setup.py")
    else:
        print("✓ 所有必需文件和目录都已存在")
        print("现在可以开始使用项目:")
        print("  1. 将华强买瓜视频文件放在 input/ 目录下")
        print("  2. 运行: python main.py")
        print("  3. 或运行演示: python demo.py --demo all")
    
    return len(missing_files) == 0 and len(missing_dirs) == 0

def create_missing_structure():
    """创建缺失的项目结构"""
    print("\n尝试创建缺失的目录结构...")
    
    required_dirs = [
        "models",
        "input",
        "output",
        "temp", 
        "logs",
        "processor"
    ]
    
    for dir_path in required_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ 创建目录: {dir_path}/")
    
    print("目录结构创建完成！")

def main():
    """主函数"""
    success = check_project_structure()
    
    if not success:
        create_missing_structure()
        print("\n现在请运行: python setup.py 来安装依赖")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)