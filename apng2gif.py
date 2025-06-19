import argparse
import os
import subprocess

from PIL import Image, ImageSequence

input_dir = "input"
output_dir = "output"
temp_dir = "__temp_frames"

os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(temp_dir, exist_ok=True)


def remove_low_alpha_pixels(image: Image.Image, alpha_threshold: int) -> Image.Image:
    """将所有 alpha < 1 的像素变为 alpha = 0（纯透明）"""
    image = image.convert("RGBA")
    pixels = image.getdata()
    new_pixels = []
    for r, g, b, a in pixels:
        if a < alpha_threshold:
            new_pixels.append((0, 0, 0, 0))
        else:
            new_pixels.append((r, g, b, 255))
    image.putdata(new_pixels)
    return image


def convert_apng_to_gif(filepath: str, output_path: str, alpha_threshold: int):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    frame_pattern = os.path.join(temp_dir, f"{filename}_%03d.png")

    # 打开 APNG 并处理每帧
    im = Image.open(filepath)
    frames = []
    for i, frame in enumerate(ImageSequence.Iterator(im)):
        cleaned = remove_low_alpha_pixels(frame.copy(), alpha_threshold)
        cleaned.save(os.path.join(temp_dir, f"{filename}_{i:03d}.png"))
        frames.append(cleaned)

    # 调用 ffmpeg 生成调色板
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "10",
        "-i", frame_pattern,
        "-vf", "palettegen", f"{temp_dir}/{filename}_palette.png"
    ], check=True)

    # 调用 ffmpeg 合成 gif
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "10",
        "-i", frame_pattern,
        "-i", f"{temp_dir}/{filename}_palette.png",
        "-lavfi", "paletteuse", output_path
    ], check=True)

    # 清理临时帧
    for f in os.listdir(temp_dir):
        if f.startswith(filename):
            os.remove(os.path.join(temp_dir, f))

    print(f"✅ 生成：{output_path}")


def batch_convert_apng_to_gif(alpha_threshold=128):
    for file in os.listdir(input_dir):
        if file.lower().endswith(".png"):
            in_path = os.path.join(input_dir, file)
            out_path = os.path.join(output_dir, os.path.splitext(file)[0] + ".gif")
            try:
                convert_apng_to_gif(in_path, out_path, alpha_threshold)
            except Exception as e:
                print(f"❌ 处理失败: {file}, 错误: {e}")


if __name__ == "__main__":
    # 创建命令行解析器
    parser = argparse.ArgumentParser(description='将APNG转换为GIF')
    parser.add_argument('-t', type=int, default=128,
                        help='Alpha透明度阈值(0-255)，低于此值的像素将变为完全透明')
    args = parser.parse_args()

    # 使用命令行参数进行批量转换t
    batch_convert_apng_to_gif(args.t)
