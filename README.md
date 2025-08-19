# Summer-Practice-2025

基于全景相机的街道风貌采集指南

---

## 写在最前面：

**这个Github repo用于同济大学2025年暑期实践。“基于全景相机的街道风貌采集指南”**
**目前的课程要求分为两个具体的部分，预实验部分和实景风貌采集建模部分**
**预实验部分的数据采集自同济大学校园内，意在帮助同学们熟悉整个建模的流程，所占分值占本次暑期实践的50%，交付成果是如下所示：**
**实操部分的任务要求同学们在衡复风貌区范围内，任选两条相交的街道，按照完整流程，采集相关的街景影像以及最后的三维成果**

## 📖 目录

> ![暑期实验流程图](./images/全流程图说明.png)



1. [全景相机视频采集](#全景相机视频采集)  
2. [全景相机的数据导出](#全景相机的数据导出)  
3. [轨迹匹配&抽帧&EXIF写入](#轨迹匹配&抽帧&EXIF写入)  
4. [三维成果重建](#三维成果重建)  

---

## 软件安装指南：

* Python > 3.10
* insta360 Studio
* FFmpeg
* Agisoft Metashape
* AliceVision(可选)

### Python 安装：
网址链接：

### Insta360 Studio 安装

### FFmpeg安装

### Agisoft Metashape 安装

### AliceVision 安装


---

## 全景相机视频采集

### 前置准备

* Insta360 One X 全景相机（建议型号x2以上，前文已经提到）
* Insta360 Studio 软件（用于 MP4 导出）
* 已安装并添加到系统环境变量 `PATH` 中的 FFmpeg
* Meshroom 2021.1.0

---

### 步骤 1：全景相机视频采集

1. 使用 USB 数据线连接 Insta360 相机与电脑。
2. 启动 **Insta360 Studio**，导入拍摄的原始视频文件。
3. 在导出选项中选择**全景视频**，点击**导出**。

> ![Insta360 视频导出示例](./images/视频转换.png)

---

### 步骤 2：使用 FFmpeg 提取全景照片

1. **下载 FFmpeg**

   前往 [FFmpeg 官网](https://ffmpeg.org/download.html) 下载适合 Windows 系统的版本，推荐使用 **Windows builds by BtbN**。

   ![FFmpeg 下载示例](./images/ffmpeg.png)

2. **配置环境变量**

   在 Windows 搜索栏中搜索 "环境变量"，点击**编辑系统环境变量**，将解压后的 FFmpeg 文件夹路径加入系统 `PATH`。

   ![环境变量配置](./images/添加到PATH.png)

3. **提取帧图片**

   在终端（CMD 或 PowerShell）中执行以下命令，提取 JPG 图片帧：

   ```bash
   ffmpeg -i path/to/360_video.mp4 -vf fps=1 -qscale:v 1 path/to/output_folder/image_%04d.jpg
   ```

   > 参数说明：
   >
   > * `fps=1`：每秒提取一帧（推荐设置）。

> **备注：** 以上步骤也可使用 Python 脚本批量调用。

---

### 步骤 3：使用 AliceVision 拆分成 8 个方向图片

**简介：** AliceVision 是 Meshroom 背后的三维重建引擎，提供了一些实用脚本，例如本指南用到的 `aliceVision_utils_split360Images`，用于将全景图拆分成不同方向的平面图。

1. **下载 Meshroom**

   前往 [Meshroom 下载页面](https://www.fosshub.com/Meshroom-old.html) 下载。

   > **注意：请选择下载 Meshroom 2021.1.0 版本！**

   ![Meshroom 下载示例](./images/meshroom.png)

2. **执行拆分脚本**

   在 PowerShell 中进入 AliceVision 安装目录，执行以下命令：

   ```bash
   aliceVision_utils_split360Images.exe \
   -i path/to/input_360_image_folder \
   -o path/to/output_2D_image_folder \
   --equirectangularNbSplits 8 \
   --equirectangularSplitResolution 1200
   ```

   > **说明：**
   >
   > * 请确保命令行当前目录为 AliceVision 安装根目录。
   > * 输入输出目录需使用绝对路径。

---

## 三维重建：使用 Meshroom 或 Colmap

此部分将在后续更新，敬请关注。

---

📌 如有任何问题或建议，欢迎在 GitHub Issues 中提交反馈！
