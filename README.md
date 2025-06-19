# apng2gif

一个将 APNG 文件批量高质量转换为 GIF 的小工具，尽可能还原图像细节。
可用于将 Line 动态表情转换为 GIF 格式。

## 使用方法

1. 将待转换的 APNG 文件放入 `input` 目录(支持多文件批量处理，若目录不存在可以先运行一下程序来自动创建)。
2. 运行 `apng2gif.exe` 。
3. 转换后的 GIF 文件会输出到 `output` 目录。

可在运行时使用 `-t` 调整透明度阈值。默认值为 128。
GIF 格式不支持半透明，只能不透明或完全透明。因此透明度低于该值的像素将被转换为全透明。

```bash
./apng2gif.exe -t 200
```

## 从源码运行或打包

### 安装依赖

本项目使用 [uv](https://github.com/astral-sh/uv) 包管理器：

```bash
uv sync
```

此外还依赖于 [FFmpeg](https://ffmpeg.org/) 工具。

### 运行脚本

```bash
uv run apng2gif.py
```

### 打包为可执行文件

```bash
pyinstaller --onefile apng2gif.py
```

---
