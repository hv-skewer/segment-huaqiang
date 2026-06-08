# 华强买瓜视频分割项目 - 使用说明

## 项目简介
这是一个使用YOLO模型进行视频物体检测和分割的项目，可以自动识别视频中的物体并添加分割效果。

## 修复的问题
1. **字符串格式化错误**：修复了"Unknown format code 'd' for object of type 'float'"错误
2. **视频块重复问题**：修复了分割后的视频块内容重复的问题
3. **相对导入问题**：修复了模块导入时的相对路径问题

## 使用方法

### 方法一：使用简化版本（推荐）
```bash
cd "C:\Users\MarbleVessel\3D Objects\huaqiang-segment"
python simple_yolo_main.py
```

### 方法二：使用完整版本
```bash
cd "C:\Users\MarbleVessel\3D Objects\huaqiang-segment"
python yolo_main.py
```

### 自定义参数
```bash
# 指定输入和输出文件
python simple_yolo_main.py --input input/your_video.mp4 --output output/processed_video.mp4

# 使用不同的YOLO模型
python simple_yolo_main.py --model yolov8s-seg

# 调整置信度阈值
python simple_yolo_main.py --confidence 0.7

# 指定计算设备
python simple_yolo_main.py --device cuda

# 测试模式
python simple_yolo_main.py --test
```

## 支持的YOLO模型
- `yolov8n` - 最小模型，速度最快
- `yolov8s` - 小模型，平衡速度和精度
- `yolov8m` - 中等模型
- `yolov8l` - 大模型
- `yolov8x` - 最大模型，精度最高
- `yolov8n-seg` - 最小分割模型
- `yolov8s-seg` - 小分割模型
- `yolov8m-seg` - 中等分割模型
- `yolov8l-seg` - 大分割模型
- `yolov8x-seg` - 最大分割模型

## 输入要求
- 输入视频文件格式：MP4
- 推荐分辨率：1280x720 或更低
- 推荐时长：2分钟以内（处理时间较长）
- 文件大小：建议不超过500MB

## 输出说明
- 输出文件格式：MP4
- 输出路径：`output/huaqiang_segmented.mp4`
- 处理后的视频会添加YOLO检测结果和分割效果

## 性能优化
- 使用`--device cuda`参数启用GPU加速（如果可用）
- 使用较小的模型（如`yolov8n-seg`）以提高处理速度
- 处理时间大约为视频时长的3-5倍

## 故障排除
1. **如果出现"YOLO未安装"错误**：
   ```bash
   pip install ultralytics
   ```

2. **如果出现CUDA错误**：
   - 确保已安装CUDA
   - 使用`--device cpu`参数强制使用CPU

3. **如果内存不足**：
   - 使用较小的视频文件
   - 分段处理视频

## 文件结构
```
huaqiang-segment/
├── input/              # 输入视频目录
├── output/             # 输出视频目录
├── chunks/             # 临时视频块目录
├── logs/               # 日志文件目录
├── models/             # 模型文件目录
├── config.py          # 配置文件
├── simple_yolo_main.py # 简化版主程序
├── simple_yolo_processor.py # 简化版处理器
├── yolo_main.py       # 完整版主程序
└── yolo_processor.py   # 完整版处理器
```

## 注意事项
- 处理大文件可能需要较长时间
- 确保有足够的磁盘空间（输出文件通常比输入文件大）
- 首次运行会自动下载YOLO模型
- 建议在处理前备份重要文件