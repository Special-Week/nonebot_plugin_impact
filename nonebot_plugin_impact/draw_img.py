"""绘画图表模块"""
import random
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont


class DrawBarChart:
    def __init__(self) -> None:
        self.colors: List[Tuple[int, int, int]] = [
            (31, 119, 180),  # 蓝色
            (44, 160, 44),  # 绿色
            (214, 39, 40),  # 红色
            (255, 127, 14),  # 橙色
            (148, 103, 189),  # 紫色
            (23, 190, 207),  # 青色
            (188, 189, 34),  # 黄色
            (227, 119, 194),  # 粉色
            (255, 99, 71),  # 红橙色
            (255, 215, 0),  # 金色
        ]
        self.module_path: Path = Path(__file__).parent
        self.font = str(self.module_path / "fonts" / "SIMYOU.TTF")

    async def draw_bar_chart(self, data: Dict[str, float]) -> bytes:
        values = list(data.values())
        keys = list(data.keys())
        image = Image.new("RGBA", (1920, 1080), (255, 255, 255, 255))
        draw = ImageDraw.Draw(image)

        # ------------------------ 画一个框框 ------------------------

        image_new = Image.new("RGBA", (1920, 1080), (255, 255, 255, 0))
        draw_new = ImageDraw.Draw(image_new)
        draw_new.rectangle((420, 25, 1860, 1060), fill=(255, 255, 255, 220))
        image_new = image_new.filter(ImageFilter.GaussianBlur(radius=0.1))
        image.paste(image_new, (0, 0), image_new)

        # ------------------------ 画一个坐标轴 ------------------------

        draw.line((490, 770, 1800, 770), fill="black", width=2)
        draw.line((500, 50, 500, 1030), fill="black", width=2)
        maxnum_scale = abs(max(values) / 9)
        minnum_scale = abs(min(values) / 3)

        # ------------------------ 画一些虚线 ------------------------

        def draw_dotted_line(y):
            x_start, x_end = 500, 1800
            dash_length = 10
            gap_length = 5
            x = x_start
            while x < x_end:
                x_dash_end = min(x + dash_length, x_end)
                draw.line((x, y, x_dash_end, y), fill="black", width=1)
                x += dash_length + gap_length

        for i in range(10):
            draw_dotted_line(770 - 780 * i / 10)
            draw_dotted_line(770 + 780 * i / 10)
        maxnum_scale = int(maxnum_scale / 50 + 1) * 50
        minnum_scale = int(minnum_scale / 50 + 1) * 50

        if maxnum_scale == 0:
            maxnum_scale = 50
        if minnum_scale == 0:
            minnum_scale = 50
        for i in range(10):
            draw.text(
                (450, 770 - 780 * i / 10 - 10),
                str(maxnum_scale * i),
                fill="black",
                font=ImageFont.truetype(self.font, 20),
            )
        for i in range(1, 4):
            draw.text(
                (450, 770 + 780 * i / 10 - 10),
                f"-{str(minnum_scale * i)}",
                fill="black",
                font=ImageFont.truetype(self.font, 20),
            )

        # ------------------------ 画柱状图 ------------------------

        columns = Image.new("RGBA", (1920, 1080), (255, 255, 255, 0))
        draw = ImageDraw.Draw(columns)
        random.shuffle(self.colors)
        for i, value in enumerate(values):
            color = self.colors[i]
            # 在左边依次画出颜色的方块, 并且写上名字, 间隔20像素, 方块边长为50像素
            draw.rectangle((50, 50 + 70 * i, 100, 100 + 70 * i), fill=color + (250,))
            draw.text(
                (120, 60 + 70 * i),
                keys[i] if len(keys[i]) < 8 else f"{keys[i][:8]}...",
                fill="black",
                font=ImageFont.truetype(self.font, 28),
            )
            if value > 0:
                draw.rectangle(
                    (
                        540 + 120 * i,
                        770 - 78 * (value / maxnum_scale),
                        635 + 120 * i,
                        770,
                    ),
                    fill=color + (200,),
                )
                # 在柱子上方写上值, 居中
                draw.text(
                    (540 + 120 * i, 770 - 78 * (value / maxnum_scale) - 30),
                    str(value),
                    fill="black",
                    font=ImageFont.truetype(self.font, 32),
                )
            else:
                draw.rectangle(
                    (
                        540 + 120 * i,
                        770,
                        635 + 120 * i,
                        770 - 78 * (value / minnum_scale),
                    ),
                    fill=color + (200,),
                )
                # 在柱子下方写上值, 居中
                draw.text(
                    (540 + 120 * i, 770 - 78 * (value / minnum_scale) + 10),
                    str(value),
                    fill="black",
                    font=ImageFont.truetype(self.font, 32),
                )

        # ------------------------ 粘贴上来 ------------------------
        image.paste(columns, (0, 0), columns)
        img_byte = BytesIO()
        image.save(img_byte, format="PNG")
        return img_byte.getvalue()

    async def draw_line_chart(self, data: Dict[str, float]):
        # 画折线图
        values = list(data.values())
        keys = list(data.keys())
        image = Image.new("RGBA", (1920, 1080), (255, 255, 255, 255))
        draw = ImageDraw.Draw(image)

        # ------------------------ 画一个框框 ------------------------

        image_new = Image.new("RGBA", (1920, 1080), (255, 255, 255, 0))
        draw_new = ImageDraw.Draw(image_new)
        draw_new.rectangle((420, 25, 1860, 1060), fill=(255, 255, 255, 220))
        image_new = image_new.filter(ImageFilter.GaussianBlur(radius=0.1))
        image.paste(image_new, (0, 0), image_new)

        # ------------------------ 画一个坐标轴 ------------------------

        draw.line((490, 1000, 1800, 1000), fill="black", width=2)
        draw.line((500, 50, 500, 1030), fill="black", width=2)
        maxnum_scale = max(values) / 9

        # ------------------------ 画一些虚线 ------------------------

        def draw_dotted_line(y):
            x_start, x_end = 500, 1800
            dash_length = 10
            gap_length = 5
            x = x_start
            while x < x_end:
                x_dash_end = min(x + dash_length, x_end)
                draw.line((x, y, x_dash_end, y), fill="black", width=1)
                x += dash_length + gap_length

        for i in range(10):
            draw_dotted_line(1000 - 950 * i / 10)
        maxnum_scale = int((maxnum_scale / 20 + 1) * 20)
        if maxnum_scale == 0:
            maxnum_scale = 20

        for i in range(10):
            draw.text(
                (450, 1000 - 950 * i / 10 - 10),
                str(maxnum_scale * i),
                fill="black",
                font=ImageFont.truetype(self.font, 20),
            )

        # ------------------------ 画折线图 ------------------------

        def draw_line_chart():
            x_start = 540
            x_gap = (1800 - x_start) / (len(values) - 1)
            x = x_start
            y = 1000 - 95 * (values[0] / maxnum_scale)
            draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill="black", width=2)
            draw.text(
                (x - 20, y - 30),
                str(values[0]),
                fill="black",
                font=ImageFont.truetype(self.font, 32),
            )
            for i in range(1, len(values)):
                x_new = x_start + x_gap * i
                y_new = 1000 - 95 * (values[i] / maxnum_scale)
                draw.line((x, y, x_new, y_new), fill="black", width=2)
                x, y = x_new, y_new
                # 给每个点画个圆圈
                draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill="black", width=2)
                # 在每个点上写上值
                draw.text(
                    (x - 20, y - 30),
                    str(values[i]),
                    fill="black",
                    font=ImageFont.truetype(self.font, 32),
                )

        draw_line_chart()
        if len(values) > 18:
            keys = keys[:9] + keys[-9:]
        position = 0
        for i in range(len(values)):
            position += 50
            if i == 9:
                draw.text(
                    (50, position),
                    ".........\n.........",
                    fill="black",
                    font=ImageFont.truetype(self.font, 34),
                )
                position += 100
            draw.text(
                (50, position),
                f"{keys[i]}   {values[i]}ml",
                fill="black",
                font=ImageFont.truetype(self.font, 34),
            )
        bytes_io = BytesIO()
        image.save(bytes_io, format="PNG")
        return bytes_io.getvalue()


draw_bar_chart = DrawBarChart()
