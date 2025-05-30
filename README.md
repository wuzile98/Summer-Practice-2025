# Summer-Practice-2025
同济大学2025年暑期实践指南

---

## 目录
1. [教程：Insta360 全景→8 个方向图片](#教程insta360-全景→8-个方向图片)  
   - [前置准备](#前置准备)  
   - [步骤 1：导出 360° 视频](#步骤-1导出-360°-视频)  
   - [步骤 2：使用 FFmpeg 提取全景照片](#步骤-2使用-ffmpeg-提取全景照片)  
   - [步骤 3：使用 AliceVision 生成 8 个方向图片](#步骤-3使用-alicevision-生成-8-个方向图片)  
2. [暑期实践分工任务](#暑期实践分工任务)  
   - [区域概述](#区域概述)  
   - [团队分工](#团队分工)  

---

## 教程：Insta360 全景→8 个方向图片

### 前置准备
- Insta360 One X（或 One R）相机  
- Insta360 Studio（用于 MP4 导出）  
- 已安装并添加到系统 `PATH` 的 FFmpeg（版本 ≥ 4.0）  
- AliceVision 可执行文件或预编译二进制  

---

### 步骤 1：导出 360° 视频

1. 将 Insta360 相机通过 USB 连接到电脑。  
2. 打开 **Insta360 Studio**，导入你的拍摄视频。  
3. 在导出预设中选择 **360° MP4**，点击 **导出**。  
4. ![Insta360 Studio 导出界面](docs/screenshots/insta360_export.png)  

---

### 步骤 2：使用 FFmpeg 提取全景照片

在终端中运行以下命令，将 360° MP4 拆分为 JPG 帧：

```bash
ffmpeg -i input_360.mp4 -vf fps=1 panorama_%04d.jpg
```

fps=1：每秒提取一帧；可根据需要调整。

输出文件将命名为 panorama_0001.jpg, panorama_0002.jpg 等。

### 步骤 3：使用 AliceVision 生成 8 个方向图片
使用 AliceVision 的工具将每张全景图拆分成 8 个视角：

```bash
Copy
Edit
aliceVisionConvertViews \
  --input panorama_%04d.jpg \
  --outputFolder views_output \
  --views 8
```
注意：  

把 panorama_%04d.jpg 替换为你的实际文件模式。  

views_output/ 目录下会生成 view_00…view_07 文件夹，内含对应方向的 JPG。  

## 暑期实践分工任务
### 区域概述
我们已将采集区域按道路拓扑聚类划分为 16 个子区域，确保各团队能在区域内连贯行驶并均衡采集。

| 区域范围  | 团队成员      | 主要任务                              |
| ----- | --------- | --------------------------------- |
| 1–5   | 成员 A、成员 B | • Insta360 视频采集<br>• 初步数据检查       |
| 6–10  | 成员 C、成员 D | • FFmpeg 全景帧提取<br>• 图片命名与格式校验     |
| 11–15 | 成员 E、成员 F | • AliceVision 生成 8 视角<br>• 输出文件整理 |
| 16–20 | 成员 G、成员 H | • 质量检查（清晰度/曝光）<br>• GPS 元数据校对与日志  |


### 说明：

1. 采集：使用 Insta360 Studio 导出 MP4。

2. 提取：用 FFmpeg 拆分全景视频为 JPG 帧。

3. 分割：用 AliceVision 生成 8 个方向视图。

4. 质检：人工检查图片质量，并填写位置/时间戳日志。