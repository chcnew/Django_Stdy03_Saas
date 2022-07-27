# -*- coding:utf-8 -*-
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# font_file路径必须为绝对路径
def check_code(width=105, height=30, char_length=4, font_file=r"F:\My_Study\1.Python_learning\8.Django_Learning\saas\utils\monaco.ttf", font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """
        生成随机字母
        :return:
        """
        # return chr(random.randint(65, 90)) # 固定取大写字母
        # 数字0~9对应的ASCII码（十进制）袭为“48”~“57”
        # 大写字母A~Z对应的ASCII码（十进制）为“65”~“90”
        # 小写字母a~z对应的百ASCII码（十进制）为"97"~“122”
        # 取数字占1/4；取字母占3/4
        lst = [True, True, True, False]
        if random.choice(lst):
            seq = [chr(random.randint(65, 90)), chr(random.randint(97, 122))]
        else:
            seq = [chr(random.randint(48, 57))]
        return random.choice(seq)

    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return random.randint(0, 255), random.randint(10, 255), random.randint(64, 255)

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)  # 返回图片及文字

# if __name__ == '__main__':
# # 1. 直接打开
# img, code = check_code()
# img.show()

# # 2. 写入文件
# img, code = check_code()
# with open('CheckCode.png', 'wb') as f:
#     img.save(f, format='png')

# 3. 写入内存(Python3)
# from io import BytesIO
# stream = BytesIO()
# img.save(stream, 'png')
# stream.getvalue()

# 4. 写入内存（Python2）
# import StringIO
# stream = StringIO.StringIO()
# img.save(stream, 'png')
# stream.getvalue()
