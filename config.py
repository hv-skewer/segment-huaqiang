# 项目配置文件

# 视频处理配置
VIDEO_CONFIG = {
    "input_video": "input/huaqiang-maigua.mp4",
    "output_video": "output/huaqiang_segmented.mp4",
    "temp_dir": "temp",
    "chunk_duration": 30,        # 每块时长（秒）
    "chunk_overlap": 2,         # 块重叠时间（秒）
    "target_fps": 30,           # 目标帧率
    "sample_interval": 1,        # 懒分割间隔帧数
    "max_workers": 1,           # 最大工作线程数
}

# SAM模型配置
SAM_CONFIG = {
    "model_type": "vit_b",       # 模型类型: sam (Segment Everything), vit_b, vit_l, vit_h
    "model_path": "models/sam_vit_b_01ec64.pth",
    "device": "auto",           # auto, cpu, cuda
    "checkpoint": None,         # 模型检查点路径
}

# 分割效果配置
EFFECT_CONFIG = {
    "neon_enabled": True,       # 霓虹灯效果
    "cartoon_enabled": True,    # 卡通化效果
    "pixel_enabled": True,     # 像素艺术效果
    "edge_detection": True,     # 边缘检测
    "mask_transparency": 0.3,   # 掩码透明度
    "edge_thickness": 2,        # 边缘厚度
    "color_scheme": "rainbow",  # 颜色方案: rainbow, warm, cool, monochrome, custom
    "custom_colors": None,      # 自定义颜色列表 (BGR格式)
    "center_region_ratio": 0.5,  # 中心区域比例 (0.1-1.0)，值越小中心区域越小
    "use_center_only": True,    # 是否仅使用中心区域进行分割
}

# 颜色方案预设
COLOR_SCHEMES = {
    "rainbow": [
        [255, 0, 0],      # 红色
        [0, 255, 0],      # 绿色
        [0, 0, 255],      # 蓝色
        [255, 255, 0],    # 黄色
        [255, 0, 255],    # 紫色
        [0, 255, 255],    # 青色
    ],
    "warm": [
        [255, 0, 0],      # 红色
        [255, 128, 0],    # 橙色
        [255, 255, 0],    # 黄色
        [255, 0, 128],    # 粉色
        [255, 64, 0],     # 深橙色
        [255, 192, 128],  # 浅橙色
    ],
    "cool": [
        [0, 0, 255],      # 蓝色
        [0, 255, 255],    # 青色
        [128, 0, 255],    # 紫色
        [0, 128, 255],    # 天蓝色
        [128, 255, 255],  # 浅青色
        [64, 0, 255],     # 深蓝色
    ],
    "monochrome": [
        [128, 128, 128],  # 灰色
        [64, 64, 64],     # 深灰色
        [192, 192, 192],  # 浅灰色
        [32, 32, 32],     # 很深的灰色
        [224, 224, 224],  # 很浅的灰色
        [160, 160, 160],  # 中等灰色
    ],
}

# 性能配置
PERFORMANCE_CONFIG = {
    "use_gpu": True,           # 是否使用GPU
    "memory_limit": "8GB",     # 内存限制
    "batch_size": 1,           # 批处理大小
    "cache_enabled": True,     # 是否启用缓存
    "cache_size": 100,         # 缓存大小
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",           # DEBUG, INFO, WARNING, ERROR
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/processor.log",
    "console": True,
}

# 路径配置
PATHS = {
    "models_dir": "models",
    "input_dir": "input",
    "output_dir": "output",
    "temp_dir": "temp",
    "logs_dir": "logs",
}

# 低配置优化开关
LOW_CONFIG_MODE = {
    "enabled": True,           # 启用低配置模式
    "force_cpu": True,         # 强制使用CPU
    "reduce_fps": False,       # 降低帧率（False保持原始帧率）
    "chunk_processing": True,  # 启用分块处理
    "lazy_segmentation": True, # 启用懒分割
    "reduce_resolution": False, # 降低分辨率
}

# 监控配置
MONITOR_CONFIG = {
    "show_progress": True,     # 显示进度条
    "show_resources": True,    # 显示资源使用情况
    "update_interval": 1,      # 更新间隔（秒）
    "eta_calculation": True,   # 计算预计剩余时间
}