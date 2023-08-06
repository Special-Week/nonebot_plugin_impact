"""一个工具类, 将文本转换为图片, 根据文本长度自动换行"""
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


class TxtToImg:
    def __init__(self) -> None:
        self.LINE_CHAR_COUNT = 30 * 2
        self.CHAR_SIZE = 30
        self.TABLE_WIDTH = 4
        self.module_path: Path = Path(__file__).parent
        self.font = str(self.module_path / "fonts" / "SIMYOU.TTF")

    async def line_break(self, line: str) -> str:
        """将一行文本按照指定宽度进行换行"""
        ret = ""
        width = 0
        for c in line:
            if len(c.encode("utf8")) == 3:  # 中文
                if self.LINE_CHAR_COUNT == width + 1:  # 剩余位置不够一个汉字
                    width = 2
                    ret += "\n" + c
                else:  # 中文宽度加2，注意换行边界
                    width += 2
                    ret += c
            elif c == "\n":
                width = 0
                ret += c
            elif c == "\t":
                space_c = (
                    self.TABLE_WIDTH - width % self.TABLE_WIDTH
                )  # 已有长度对TABLE_WIDTH取余
                ret += " " * space_c
                width += space_c
            else:
                width += 1
                ret += c
            if width >= self.LINE_CHAR_COUNT:
                ret += "\n"
                width = 0
        return ret if ret.endswith("\n") else ret + "\n"

    async def txt_to_img(self, text: str, font_size: int = 30) -> bytes:
        """将文本转换为图片"""
        text = await self.line_break(text)
        d_font = ImageFont.truetype(self.font, font_size)
        lines = text.count("\n")
        image = Image.new(
            "L",
            (self.LINE_CHAR_COUNT * font_size // 2 + 50, font_size * lines + 50),
            "white",
        )
        draw_table = ImageDraw.Draw(im=image)
        draw_table.text(xy=(25, 25), text=text, fill="#000000", font=d_font, spacing=4)
        new_img = image.convert("RGB")
        img_byte = BytesIO()
        new_img.save(img_byte, format="PNG")
        return img_byte.getvalue()


# 创建一个实例
txt_to_img = TxtToImg()
