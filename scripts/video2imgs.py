import subprocess
import gpxpy
import piexif
from datetime import datetime
from fractions import Fraction
from pathlib import Path

# === 参数配置 ===
GPX_FILE = r"F:\03-Temp_Data\wuzile\06-sitp数据实验\01-datalake\01-insta同济大学测试数据\VID_20250814_173131_00_006.gpx"
VIDEO_FILE = r"F:\03-Temp_Data\wuzile\06-sitp数据实验\01-datalake\01-insta同济大学测试数据\VID_20250814_173131_00_006.mp4"
OUTPUT_DIR = Path(r"F:\03-Temp_Data\wuzile\06-sitp数据实验\01-datalake\03-同济大学导出结果\文远楼周边")
OUTPUT_DIR.mkdir(exist_ok=True)

BASE_ALTITUDE  =  15.0    # 从地图/DEM 查询到的地面海拔（米）
CAMERA_HEIGHT  =   1.5    # 相机距地面的高度（米）
MANUAL_ALTITUDE = BASE_ALTITUDE + CAMERA_HEIGHT

# === 工具函数：将十进制度分秒转为 EXIF 分数格式 ===
def deg_to_dms_frac(deg: float):
    """返回 [(deg_num,deg_den),(min_num,min_den),(sec_num,sec_den)]"""
    d = int(deg)
    m_float = (deg - d) * 60
    m = int(m_float)
    s = (m_float - m) * 60
    return [
        (d, 1),
        (m, 1),
        (Fraction(s).limit_denominator(1000000).numerator,
         Fraction(s).limit_denominator(1000000).denominator)
    ]

# === 1. 解析 GPX ===
with open(GPX_FILE, 'r', encoding='utf-8') as f:
    gpx = gpxpy.parse(f)

# 汇总所有 trackpoints
points = []
for track in gpx.tracks:
    for seg in track.segments:
        for pt in seg.points:
            points.append({
                "time": pt.time.replace(tzinfo=None),  # datetime
                "lat": pt.latitude,
                "lon": pt.longitude,
                "ele": pt.elevation
            })

if not points:
    raise RuntimeError("在 GPX 中未找到任何轨迹点！")

# === 2. 计算相对偏移 ===
t0 = points[0]["time"]
for idx, pt in enumerate(points):
    delta = pt["time"] - t0
    pt["offset_s"] = delta.total_seconds()

# === 3. 提取帧并写入 EXIF ===
for idx, pt in enumerate(points):
    sec = pt["offset_s"]
    out_jpeg = OUTPUT_DIR / f"frame_{idx:04d}.jpg"
    
    # ffmpeg 提取单帧
    cmd = [
        "ffmpeg",
        "-hide_banner", "-loglevel", "error",
        "-ss", str(sec),
        "-i", VIDEO_FILE,
        "-frames:v", "1",
        "-q:v", "2",  # 画质
        str(out_jpeg)
    ]
    subprocess.run(cmd, check=True)
    
    # 准备 GPS EXIF 数据
    lat, lon = pt["lat"], pt["lon"]
    ele = MANUAL_ALTITUDE

    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: b'N' if lat >= 0 else b'S',
        piexif.GPSIFD.GPSLatitude: deg_to_dms_frac(abs(lat)),
        piexif.GPSIFD.GPSLongitudeRef: b'E' if lon >= 0 else b'W',
        piexif.GPSIFD.GPSLongitude: deg_to_dms_frac(abs(lon)),
        piexif.GPSIFD.GPSAltitudeRef: 0,
        piexif.GPSIFD.GPSAltitude: (int(ele * 100), 100)
    }
    exif_dict = {"GPS": gps_ifd}
    exif_bytes = piexif.dump(exif_dict)
    
    # 插入 EXIF
    piexif.insert(exif_bytes, str(out_jpeg))

    print(f"✔ 已生成 {out_jpeg.name} @ {sec:.1f}s, GPS=({lat:.6f},{lon:.6f},{ele:.1f}m)")

print("全部完成！")