from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def txt_to_img(text: str, font_size=30, font_path="simsun.ttc") -> bytes:
    text = line_break(text)
    d_font = ImageFont.truetype(font_path, font_size)
    lines = text.count('\n')  # 计算行数
    image = Image.new("L", (LINE_CHAR_COUNT*font_size //
                      2 + 50, font_size*lines+50), "white")
    draw_table = ImageDraw.Draw(im=image)
    draw_table.text(xy=(25, 25), text=text, fill='#000000',
                    font=d_font, spacing=4)  # spacing调节机制不清楚如何计算
    new_img = image.convert("RGB")
    img_byte = BytesIO()
    new_img.save(img_byte, format='PNG')
    binary_content = img_byte.getvalue()
    return binary_content


LINE_CHAR_COUNT = 30*2  # 每行字符数：30个中文字符(=60英文字符)
CHAR_SIZE = 30
TABLE_WIDTH = 4


def line_break(line: str) -> str:
    ret = ''
    width = 0
    for c in line:
        if len(c.encode('utf8')) == 3:  # 中文
            if LINE_CHAR_COUNT == width + 1:  # 剩余位置不够一个汉字
                width = 2
                ret += '\n' + c
            else:  # 中文宽度加2，注意换行边界
                width += 2
                ret += c
        else:
            if c == '\t':
                space_c = TABLE_WIDTH - width % TABLE_WIDTH  # 已有长度对TABLE_WIDTH取余
                ret += ' ' * space_c
                width += space_c
            elif c == '\n':
                width = 0
                ret += c
            else:
                width += 1
                ret += c
        if width >= LINE_CHAR_COUNT:
            ret += '\n'
            width = 0
    if ret.endswith('\n'):
        return ret
    return ret + '\n'
