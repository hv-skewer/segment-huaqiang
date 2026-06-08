#!/usr/bin/env python3
"""
华强买瓜视频分割项目 - YOLO版本主程序
使用YOLO模型进行视频物体检测和分割
"""

import os
import sys
import logging
import argparse
from pathlib import Path

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from yolo_processor import YOLOVideoProcessor
from config import VIDEO_CONFIG

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/yolo_processor.log'),
            logging.StreamHandler()
        ]
    )

def check_requirements():
    """检查依赖"""
    try:
        import ultralytics
        print("✅ YOLO (ultralytics) 已安装")
        return True
    except ImportError:
        print("❌ YOLO (ultralytics) 未安装")
        print("请运行: pip install ultralytics")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='华强买瓜视频分割 - YOLO版本')
    parser.add_argument('--input', '-i', default=VIDEO_CONFIG['input_video'], 
                       help='输入视频文件路径')
    parser.add_argument('--output', '-o', default=VIDEO_CONFIG['output_video'], 
                       help='输出视频文件路径')
    parser.add_argument('--model', '-m', default='yolov8n-seg', 
                       choices=['yolov8n', 'yolov8s', 'yolov8m', 'yolov8l', 'yolov8x', 
                               'yolov8n-seg', 'yolov8s-seg', 'yolov8m-seg', 'yolov8l-seg', 'yolov8x-seg'],
                       help='YOLO模型类型')
    parser.add_argument('--confidence', '-c', type=float, default=0.5, 
                       help='置信度阈值 (0-1)')
    parser.add_argument('--device', '-d', default='auto', 
                       choices=['auto', 'cpu', 'cuda'], 
                       help='计算设备')
    parser.add_argument('--test', action='store_true', 
                       help='测试模式')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='详细输出')
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # 检查依赖
    if not check_requirements():
        return 1
    
    # 创建必要的目录
    os.makedirs('logs', exist_ok=True)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # 检查输入文件
    if not os.path.exists(args.input):
        logger.error(f"输入文件不存在: {args.input}")
        return 1
    
    # 创建处理器
    logger.info(f"使用YOLO模型: {args.model}")
    logger.info(f"置信度阈值: {args.confidence}")
    logger.info(f"计算设备: {args.device}")
    
    processor = YOLOVideoProcessor(
        model_type=args.model,
        device=args.device,
        confidence_threshold=args.confidence
    )
    
    if args.test:
        # 测试模式
        logger.info("运行测试模式...")
        try:
            from yolo_processor import test_yolo_model
            test_yolo_model()
            logger.info("测试完成")
            return 0
        except Exception as e:
            logger.error(f"测试失败: {str(e)}")
            return 1
    
    # 处理视频
    try:
        logger.info(f"开始处理视频: {args.input}")
        logger.info(f"输出路径: {args.output}")
        
        success = processor.process_full_video(args.input, args.output)
        
        if success:
            logger.info("视频处理完成！")
            logger.info(f"输出文件: {args.output}")
            return 0
        else:
            logger.error("视频处理失败")
            return 1
            
    except Exception as e:
        logger.error(f"处理过程中发生错误: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())