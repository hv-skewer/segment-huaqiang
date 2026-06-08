#!/usr/bin/env python3
"""
华强买瓜视频分割项目 - YOLO版本
使用YOLO模型进行物体检测和分割，相比SAM更适合视频处理
"""

import os
import cv2
import numpy as np
import torch
import time
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from tqdm import tqdm

# 导入YOLO
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    logging.warning("YOLO未安装，将使用pip install ultralytics安装")

class YOLOVideoProcessor:
    """YOLO视频处理器 - 使用YOLO模型进行物体检测和分割"""
    
    def __init__(self, model_type="yolov8n-seg", device="auto", confidence_threshold=0.5):
        """
        初始化YOLO处理器
        
        Args:
            model_type: YOLO模型类型
            device: 计算设备
            confidence_threshold: 置信度阈值
        """
        self.model_type = model_type
        self.confidence_threshold = confidence_threshold
        self.device = self._get_device(device)
        self.logger = logging.getLogger(__name__)
        
        # 初始化YOLO模型
        if YOLO_AVAILABLE:
            self._init_yolo_model()
        
        # 处理配置
        self.chunk_duration = 30
        self.chunk_overlap = 2
        
    def _get_device(self, device):
        """获取计算设备"""
        if device == "auto":
            return torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return torch.device(device)
    
    def _init_yolo_model(self):
        """初始化YOLO模型"""
        try:
            # 下载并加载YOLO模型
            self.model = YOLO(self.model_type)
            self.logger.info(f"YOLO模型加载成功: {self.model_type}")
            
            # 如果是分割模型，确认支持分割功能
            if 'seg' in self.model_type:
                self.logger.info("使用YOLO分割模型，支持实例分割")
            else:
                self.logger.info("使用YOLO检测模型，仅支持边界框检测")
                
        except Exception as e:
            self.logger.error(f"YOLO模型加载失败: {str(e)}")
            self.model = None
    
    def split_video_into_chunks(self, video_path: str, output_dir: str = "chunks") -> List[Dict]:
        """
        将视频分割成小块
        
        Args:
            video_path: 视频文件路径
            output_dir: 输出目录
            
        Returns:
            分块信息列表
        """
        os.makedirs(output_dir, exist_ok=True)
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        chunks = []
        
        for start_time in range(0, int(duration), self.chunk_duration):
            end_time = min(start_time + self.chunk_duration, duration)
            
            # 计算帧范围
            start_frame = int(start_time * fps)
            end_frame = int(end_time * fps)
            
            chunk_info = {
                'start_time': start_time,
                'end_time': end_time,
                'start_frame': start_frame,
                'end_frame': end_frame,
                'output_path': os.path.join(output_dir, f"chunk_{int(start_time):04d}-{int(end_time):04d}.mp4")
            }
            chunks.append(chunk_info)
        
        cap.release()
        self.logger.info(f"视频已分割为 {len(chunks)} 个块")
        return chunks
    
    def process_single_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        处理单帧图像
        
        Args:
            frame: 输入帧
            
        Returns:
            处理后的帧
        """
        if self.model is None:
            # 如果没有YOLO模型，使用基础分割
            return self._basic_segmentation(frame)
        
        try:
            # 使用YOLO进行推理
            results = self.model(frame, conf=self.confidence_threshold, verbose=False)
            
            # 获取第一帧的结果
            result = results[0]
            
            # 创建处理后的帧
            processed_frame = frame.copy()
            
            # 如果有检测结果
            if len(result.boxes) > 0:
                # 绘制检测结果
                processed_frame = result.plot()
                
                # 如果支持分割，添加分割效果
                if hasattr(result, 'masks') and result.masks is not None:
                    processed_frame = self._apply_segmentation_masks(processed_frame, result)
            
            return processed_frame
            
        except Exception as e:
            import traceback
            print(f"错误详情: {str(e)}")
            print(f"错误类型: {type(e)}")
            print(f"错误位置: {traceback.format_exc()}")
            self.logger.warning(f"帧处理失败: {str(e)}")
            return frame
    
    def _apply_segmentation_masks(self, frame: np.ndarray, result) -> np.ndarray:
        """
        应用分割掩码
        
        Args:
            frame: 原始帧
            result: YOLO结果
            
        Returns:
            处理后的帧
        """
        # 导入配置
        try:
            from config import EFFECT_CONFIG, COLOR_SCHEMES
        except ImportError:
            # 如果相对导入失败，尝试绝对导入
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from config import EFFECT_CONFIG, COLOR_SCHEMES
        
        # 获取颜色方案
        color_scheme = EFFECT_CONFIG.get("color_scheme", "rainbow")
        custom_colors = EFFECT_CONFIG.get("custom_colors", None)
        
        if custom_colors and color_scheme == "custom":
            colors = custom_colors
        else:
            colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["rainbow"])
        
        # 获取掩码数据
        masks = result.masks.data
        if masks is None or len(masks) == 0:
            return frame
        
        # 创建处理后的帧
        result_frame = frame.copy()
        
        # 处理每个掩码
        for i, mask in enumerate(masks):
            if i >= len(colors):  # 限制颜色数量
                break
                
            # 获取颜色
            color = colors[i % len(colors)]
            
            # 创建掩码可视化
            mask_uint8 = (mask.cpu().numpy() * 255).astype(np.uint8)
            
            # 调整掩码尺寸以匹配原始帧
            if mask_uint8.shape[:2] != frame.shape[:2]:
                mask_uint8 = cv2.resize(mask_uint8, (frame.shape[1], frame.shape[0]))
            
            mask_color = np.zeros_like(result_frame)
            mask_color[mask_uint8 > 0] = color
            
            # 应用半透明效果
            transparency = EFFECT_CONFIG.get("mask_transparency", 0.3)
            result_frame = cv2.addWeighted(result_frame, 1 - transparency, mask_color, transparency, 0)
            
            # 添加边框
            edge_thickness = EFFECT_CONFIG.get("edge_thickness", 2)
            contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) > 0:
                # 更亮的边框颜色
                edge_color = [min(255, c + 100) for c in color]
                cv2.drawContours(result_frame, contours, -1, edge_color, edge_thickness)
        
        return result_frame
    
    def _basic_segmentation(self, frame: np.ndarray) -> np.ndarray:
        """基础分割功能（用于无YOLO模型的情况）"""
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 边缘检测
        edges = cv2.Canny(gray, 50, 150)
        
        # 形态学操作
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        # 转换回彩色
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        # 混合原图和边缘
        result = cv2.addWeighted(frame, 0.7, edges_colored, 0.3, 0)
        
        return result
    
    def process_chunk(self, chunk_info: Dict) -> str:
        """
        处理单个视频块
        
        Args:
            chunk_info: 分块信息
            
        Returns:
            处理后的文件路径
        """
        video_path = chunk_info['video_path']
        output_path = chunk_info['output_path']
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # 创建输出视频
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # 设置视频读取位置到块的开始帧
        start_frame = chunk_info['start_frame']
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        frame_count = 0
        total_chunk_frames = chunk_info['end_frame'] - chunk_info['start_frame']
        
        # 处理进度条
        pbar = tqdm(total=total_chunk_frames, 
                   desc=f"处理块 {chunk_info['start_time']}-{chunk_info['end_time']}",
                   unit="frames")
        
        while cap.isOpened() and frame_count < total_chunk_frames:
            ret, frame = cap.read()
            if not ret:
                break
                
            # 处理当前帧
            result_frame = self.process_single_frame(frame)
            out.write(result_frame)
            
            frame_count += 1
            pbar.update(1)
        
        pbar.close()
        cap.release()
        out.release()
        
        self.logger.info(f"块处理完成: {output_path}")
        return output_path
    
    def process_full_video(self, video_path: str, output_path: str) -> bool:
        """
        完整的YOLO处理流程
        
        Args:
            video_path: 输入视频路径
            output_path: 输出视频路径
            
        Returns:
            处理是否成功
        """
        try:
            self.logger.info("开始YOLO处理...")
            
            # 1. 分割视频
            chunks = self.split_video_into_chunks(video_path)
            
            # 2. 处理每个块
            processed_chunks = []
            for chunk in chunks:
                chunk['video_path'] = video_path
                chunk_path = self.process_chunk(chunk)
                processed_chunks.append(chunk_path)
            
            # 3. 合并所有块
            self._merge_chunks(processed_chunks, output_path)
            
            # 4. 清理临时文件
            for chunk_path in processed_chunks:
                try:
                    os.remove(chunk_path)
                except:
                    pass
            
            self.logger.info("YOLO处理完成！")
            return True
            
        except Exception as e:
            self.logger.error(f"YOLO处理失败: {str(e)}")
            return False
    
    def _merge_chunks(self, chunk_paths: List[str], output_path: str):
        """
        合并所有处理后的块
        
        Args:
            chunk_paths: 块文件路径列表
            output_path: 输出文件路径
        """
        if not chunk_paths:
            raise ValueError("没有可合并的块文件")
        
        # 读取第一个块获取视频参数
        cap = cv2.VideoCapture(chunk_paths[0])
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        
        # 创建输出视频
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # 合并所有块
        for chunk_path in chunk_paths:
            cap = cv2.VideoCapture(chunk_path)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
            cap.release()
        
        out.release()
        
        self.logger.info(f"块合并完成: {output_path}")

def test_yolo_model():
    """测试YOLO模型"""
    print("🧪 测试YOLO模型...")
    
    # 创建处理器
    processor = YOLOVideoProcessor(model_type="yolov8n-seg", confidence_threshold=0.5)
    
    # 测试单帧处理
    test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    result = processor.process_single_frame(test_frame)
    
    print(f"✅ YOLO模型测试成功")
    print(f"   输入形状: {test_frame.shape}")
    print(f"   输出形状: {result.shape}")
    
    return True

def install_yolo():
    """安装YOLO"""
    print("📦 安装YOLO...")
    
    try:
        import subprocess
        subprocess.check_call(["pip", "install", "ultralytics"])
        print("✅ YOLO安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ YOLO安装失败")
        return False

if __name__ == "__main__":
    # 测试YOLO
    if not YOLO_AVAILABLE:
        print("YOLO未安装，正在安装...")
        if not install_yolo():
            print("请手动安装: pip install ultralytics")
            exit(1)
    
    # 重新导入
    try:
        from ultralytics import YOLO
        YOLO_AVAILABLE = True
    except ImportError:
        print("YOLO安装失败")
        exit(1)
    
    # 运行测试
    test_yolo_model()