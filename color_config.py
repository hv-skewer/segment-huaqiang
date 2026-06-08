#!/usr/bin/env python3
"""
华强买瓜视频分割项目 - 高级配置工具
让您轻松选择不同的颜色方案和分割范围
"""

import os
import sys
import json

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import EFFECT_CONFIG, COLOR_SCHEMES

def show_color_schemes():
    """显示所有可用的颜色方案"""
    print("🎨 可用的颜色方案:")
    print("=" * 50)
    
    for scheme_name, colors in COLOR_SCHEMES.items():
        print(f"\n🌈 {scheme_name.upper()}:")
        for i, color in enumerate(colors):
            # 将BGR转换为RGB用于显示
            rgb_color = color[::-1]  # BGR -> RGB
            print(f"  {i+1}. RGB{rgb_color} (BGR{color})")
    
    print(f"\n🎯 当前配置: {EFFECT_CONFIG.get('color_scheme', 'rainbow')}")

def change_color_scheme(new_scheme):
    """更改颜色方案"""
    if new_scheme not in COLOR_SCHEMES:
        print(f"❌ 错误: 不支持的颜色方案 '{new_scheme}'")
        print("支持的颜色方案: " + ", ".join(COLOR_SCHEMES.keys()))
        return False
    
    # 更新配置
    EFFECT_CONFIG["color_scheme"] = new_scheme
    
    # 保存配置
    try:
        with open("config.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 更新配置字符串
        old_pattern = '    "color_scheme": "' + EFFECT_CONFIG["color_scheme"] + '"'
        new_pattern = '    "color_scheme": "' + new_scheme + '"'
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
        else:
            # 如果找不到，添加新的配置项
            config_line = '    "color_scheme": "' + new_scheme + '",'
            if '"color_scheme":' not in content:
                # 在第一个配置项前插入
                insert_pos = content.find('"neon_enabled":')
                content = content[:insert_pos] + config_line + "\n" + content[insert_pos:]
        
        with open("config.py", "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ 颜色方案已更改为: {new_scheme}")
        return True
        
    except Exception as e:
        print(f"❌ 配置更新失败: {str(e)}")
        return False

def set_custom_colors():
    """设置自定义颜色"""
    print("\n🎨 自定义颜色设置")
    print("请输入颜色列表（BGR格式，如: [[255,0,0], [0,255,0]]）")
    print("或输入 'cancel' 取消")
    
    custom_input = input("自定义颜色列表: ").strip()
    
    if custom_input.lower() == 'cancel':
        return False
    
    try:
        # 尝试解析JSON
        custom_colors = json.loads(custom_input)
        
        # 验证颜色格式
        for color in custom_colors:
            if len(color) != 3 or any(not isinstance(c, int) for c in color):
                raise ValueError("每个颜色必须是包含3个整数的列表")
            if any(c < 0 or c > 255 for c in color):
                raise ValueError("颜色值必须在0-255范围内")
        
        # 更新配置
        EFFECT_CONFIG["color_scheme"] = "custom"
        EFFECT_CONFIG["custom_colors"] = custom_colors
        
        # 保存配置
        try:
            with open("config.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # 更新自定义颜色
            custom_colors_str = json.dumps(custom_colors, ensure_ascii=False)
            
            # 查找并更新自定义颜色配置
            old_custom = '"custom_colors": None'
            if old_custom in content:
                content = content.replace(old_custom, f'"custom_colors": {custom_colors_str}')
            else:
                # 添加自定义颜色配置
                custom_line = f'    "custom_colors": {custom_colors_str},'
                if '"custom_colors":' not in content:
                    insert_pos = content.find('"color_scheme":')
                    content = content[:insert_pos] + custom_line + "\n" + content[insert_pos:]
            
            with open("config.py", "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"✅ 自定义颜色已设置")
            return True
            
        except Exception as e:
            print(f"❌ 配置保存失败: {str(e)}")
            return False
            
    except json.JSONDecodeError:
        print("❌ 错误: 请输入有效的JSON格式")
        return False
    except ValueError as e:
        print(f"❌ 错误: {str(e)}")
        return False

def show_split_settings():
    """显示分割设置"""
    print("\n🎯 分割范围设置:")
    print("=" * 50)
    print(f"当前模式: {'仅中心区域' if EFFECT_CONFIG.get('use_center_only', True) else '全屏区域'}")
    print(f"中心区域比例: {EFFECT_CONFIG.get('center_region_ratio', 0.5):.1%}")
    print(f"透明度: {EFFECT_CONFIG.get('mask_transparency', 0.3):.1f}")
    print(f"边缘厚度: {EFFECT_CONFIG.get('edge_thickness', 2)}")

def set_split_mode():
    """设置分割模式"""
    print("\n🎯 分割模式选择:")
    print("1. 仅中心区域（推荐）- 只识别中心区域的物体")
    print("2. 全屏区域 - 识别全屏的所有物体")
    print("3. 返回")
    
    choice = input("请选择模式 (1-3): ").strip()
    
    if choice == "1":
        EFFECT_CONFIG["use_center_only"] = True
        update_config("use_center_only", True)
        print("✅ 已设置为仅中心区域模式")
    elif choice == "2":
        EFFECT_CONFIG["use_center_only"] = False
        update_config("use_center_only", False)
        print("✅ 已设置为全屏区域模式")
    elif choice == "3":
        return
    else:
        print("❌ 无效选择")

def set_center_ratio():
    """设置中心区域比例"""
    print(f"\n🎯 当前中心区域比例: {EFFECT_CONFIG.get('center_region_ratio', 0.5):.1%}")
    print("请输入新的比例 (0.1-1.0，如 0.3 表示30%的区域)")
    print("或输入 'cancel' 取消")
    
    ratio_input = input("新的中心区域比例: ").strip()
    
    if ratio_input.lower() == 'cancel':
        return
    
    try:
        ratio = float(ratio_input)
        if ratio < 0.1 or ratio > 1.0:
            print("❌ 错误: 比例必须在0.1-1.0之间")
            return
        
        EFFECT_CONFIG["center_region_ratio"] = ratio
        update_config("center_region_ratio", ratio)
        print(f"✅ 中心区域比例已设置为: {ratio:.1%}")
        
    except ValueError:
        print("❌ 错误: 请输入有效的数字")

def update_config(key, value):
    """更新配置文件"""
    try:
        with open("config.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 更新配置值
        if isinstance(value, str):
            pattern = f'"{key}": {repr(value)}'
            new_pattern = f'"{key}": {repr(value)}'
        elif isinstance(value, bool):
            pattern = f'"{key}": {str(value).lower()}'
            new_pattern = f'"{key}": {str(value).lower()}'
        elif isinstance(value, (int, float)):
            pattern = f'"{key}": {value}'
            new_pattern = f'"{key}": {value}'
        
        # 尝试替换现有配置
        if pattern in content:
            content = content.replace(pattern, new_pattern)
        else:
            # 如果找不到，添加新的配置项
            if isinstance(value, str):
                config_line = f'    "{key}": {repr(value)},'
            else:
                config_line = f'    "{key}": {value},'
            
            if f'"{key}":' not in content:
                insert_pos = content.find('"neon_enabled":')
                content = content[:insert_pos] + config_line + "\n" + content[insert_pos:]
        
        with open("config.py", "w", encoding="utf-8") as f:
            f.write(content)
            
    except Exception as e:
        print(f"❌ 配置更新失败: {str(e)}")

def main():
    """主函数"""
    print("🎬 华强买瓜视频分割项目 - 高级配置工具")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 查看颜色方案")
        print("2. 选择颜色方案")
        print("3. 设置自定义颜色")
        print("4. 查看分割设置")
        print("5. 设置分割模式")
        print("6. 调整中心区域大小")
        print("7. 退出")
        
        choice = input("\n请输入选择 (1-7): ").strip()
        
        if choice == "1":
            show_color_schemes()
        elif choice == "2":
            print("\n可用颜色方案:")
            for i, scheme in enumerate(COLOR_SCHEMES.keys(), 1):
                print(f"{i}. {scheme}")
            
            scheme_choice = input("\n请输入颜色方案名称: ").strip()
            change_color_scheme(scheme_choice)
        elif choice == "3":
            set_custom_colors()
        elif choice == "4":
            show_split_settings()
        elif choice == "5":
            set_split_mode()
        elif choice == "6":
            set_center_ratio()
        elif choice == "7":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()