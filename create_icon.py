from PIL import Image, ImageDraw


def create_icon():
    # 创建一个 256x256 的高分辨率图标画布
    img = Image.new('RGBA', (256, 256), color=(30, 34, 43, 255))  # 深暗背景
    draw = ImageDraw.Draw(img)

    # 1. 画左侧的 M3U8 切片线条（青色渐变感）
    draw.line([(40, 80), (100, 80)], fill=(0, 242, 254, 255), width=8)
    draw.line([(30, 128), (90, 128)], fill=(0, 242, 254, 200), width=8)
    draw.line([(40, 176), (100, 176)], fill=(0, 242, 254, 150), width=8)

    # 2. 画中间的转换闪电箭头
    draw.polygon([(110, 140), (140, 70), (130, 120), (160, 110), (130, 180), (140, 130)], fill=(255, 255, 255, 255))

    # 3. 画右侧的完整 MP4 播放按钮（橙红渐变感）
    # 播放三角形坐标
    triangle_points = [(160, 80), (220, 128), (160, 176)]
    draw.polygon(triangle_points, fill=(255, 81, 47, 255))

    # 保存为ico格式供PyInstaller使用
    img.save('images/app.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])


# 执行一次即可生成你的专属 app.ico
create_icon()