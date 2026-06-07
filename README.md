# 华强买瓜视频分割项目
## Segment Anything 视频处理工具

### 项目简介
本项目基于Segment Anything Model (SAM) 2，对经典视频"华强买瓜"进行实时图像分割，生成新的艺术化视频效果。

### 硬件要求
- 最低配置：CPU模式，8GB内存
- 推荐配置：GPU加速，16GB内存，RTX 3060及以上

### 项目结构
```
huaqiang-segment/
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖库列表
├── config.py              # 配置文件
├── processor/
│   ├── __init__.py
│   ├── chunked_processor.py  # 分块处理器
│   ├── optimized_processor.py # 优化处理器
│   └── utils.py            # 工具函数
├── models/                # 模型文件目录
├── input/                 # 输入视频目录
├── output/                # 输出视频目录
├── temp/                  # 临时文件目录
└── README.md              # 项目说明
```

### 安装步骤
1. 安装Python 3.8+
2. 安装依赖：`pip install -r requirements.txt`
3. 下载SAM模型到models目录
4. 准备输入视频到input目录
5. 运行：`python main.py`

### 使用方法
```bash
# 基本处理
python main.py

# 自定义配置
python main.py --method chunked --fps 15 --device cpu

# 查看帮助
python main.py --help
```

### 技术特性
- 分块处理：支持长视频分割
- 懒分割：时间换空间策略
- 多种艺术效果：霓虹灯、卡通化、像素艺术
- 性能监控：实时显示处理进度
- 低配置优化：CPU模式支持