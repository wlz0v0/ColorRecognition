import cv2


class Color:
    b = 0
    g = 0
    r = 0


class OneSideOfCube:
    block0 = ""  # 二阶魔方某个单面的左上角
    block1 = ""  # 二阶魔方某个单面的右上角
    block2 = ""  # 二阶魔方某个单面的右下角
    block3 = ""  # 二阶魔方某个单面的左下角


Side = [OneSideOfCube.block0, OneSideOfCube.block1, OneSideOfCube.block2, OneSideOfCube.block3]

white = "0"
yellow = "0"
green = "0"
blue = "0"
orange = "0"
red = "0"


def color_set(block_color, model):  # 设置颜色对应的面（白黄绿蓝橙红）
    global white
    global yellow
    global green
    global blue
    global orange
    global red
    if model == 0:
        forward3 = block_color
        if forward3 == "white":
            white = "F"
            yellow = "B"
        elif forward3 == "yellow":
            white = "B"
            yellow = "F"
        elif forward3 == "green":
            green = "F"
            blue = "B"
        elif forward3 == "blue":
            green = "B"
            blue = "F"
        elif forward3 == "orange":
            orange = "F"
            red = "B"
        elif forward3 == "red":
            orange = "B"
            red = "F"
    elif model == 1:
        left2 = block_color
        if left2 == "white":
            white = "L"
            yellow = "R"
        elif left2 == "yellow":
            white = "R"
            yellow = "L"
        elif left2 == "green":
            green = "L"
            blue = "R"
        elif left2 == "blue":
            green = "R"
            blue = "L"
        elif left2 == "orange":
            orange = "L"
            red = "R"
        elif left2 == "red":
            orange = "R"
            red = "L"
    elif model == 2:
        down0 = block_color
        if down0 == "white":
            white = "D"
            yellow = "U"
        elif down0 == "yellow":
            white = "U"
            yellow = "D"
        elif down0 == "green":
            green = "D"
            blue = "U"
        elif down0 == "blue":
            green = "U"
            blue = "D"
        elif down0 == "orange":
            orange = "D"
            red = "U"
        elif down0 == "red":
            orange = "U"
            red = "D"


def color_recognition(b, g, r, flag=0):  # flag为1时是用于识别颜色并输出字符串，为0时是用于判断forward3的颜色以确定正面的颜色
    # rgb转hsv
    # 基础量计算
    B = b / 255
    G = g / 255
    R = r / 255
    C_max = max(B, G, R)
    C_min = min(B, G, R)
    delta = C_max - C_min
    # 计算h大小
    if delta == 0:
        h = 0
    else:
        if C_max == R:
            h = 60 * (G - B) / delta
        elif C_max == G:
            h = 60 * (B - R) / delta + 120
        elif C_max == B:
            h = 60 * (R - G) / delta + 240
    h = abs(h)  # 红色有时是负数，所以取个绝对值
    # 计算s大小
    if C_max == 0:
        s = 0
    else:
        s = delta / C_max
    # 计算v大小
    v = C_max
    # 根据hsv进行比较判断
    if flag == 1:
        if 0 <= h <= 360 and 0 <= s <= 30 / 255 and 120 / 255 <= v <= 1:  # white
            return white
        elif 0 <= h <= 10 and 43 / 255 <= s <= 1 and 46 / 255 <= v <= 1:  # red
            return red
        elif 10 < h <= 40 and 43 / 255 <= s <= 1 and 46 / 255 <= v <= 1:  # orange
            return orange
        elif 40 < h <= 80 and 43 / 255 <= s <= 1 and 46 / 255 <= v <= 1:  # yellow
            return yellow
        elif 100 <= h <= 160 and 43 / 255 <= s <= 1 and 46 / 255 <= v <= 1:  # green
            return green
        elif 160 <= h <= 240 and 43 / 255 <= s <= 1 and 46 / 255 <= v <= 1:  # blue
            return blue
    elif flag == 0:
        if 0 <= h <= 360 and 0 <= s <= 30 / 255 and 120 / 255 <= v <= 1:  # white
            return "white"
        elif 0 <= h <= 10 and 43 / 255 <= s <= 1 and 46 / 255 <= v <= 1:  # red
            return "red"
        elif 10 < h <= 40 and 43 / 255 <= s <= 1 and 46 / 255 <= v <= 1:  # orange
            return "orange"
        elif 40 < h <= 80 and 43 / 255 <= s <= 1 and 46 / 255 <= v <= 1:  # yellow
            return "yellow"
        elif 100 <= h <= 160 and 43 / 255 <= s <= 1 and 46 / 255 <= v <= 1:  # green
            return "green"
        elif 160 <= h <= 240 and 43 / 255 <= s <= 1 and 46 / 255 <= v <= 1:  # blue
            return "blue"
    else:
        return "Flag parameter must be 0 or 1!"


def color_extraction(side, flag=0):
    init_img = cv2.imread(side + ".jpg")                # 获得初始图片
    resize_img = cv2.resize(init_img, (576, 768))      # 缩放初始图片
    final_img = resize_img[0:600, 0:576]                # 图片适当裁剪
    for block in range(2):
        Color.b = final_img[150, 288 * block + 144, 0]
        Color.g = final_img[150, 288 * block + 144, 1]
        Color.r = final_img[150, 288 * block + 144, 2]
        Side[block] = color_recognition(Color.b, Color.g, Color.r, flag)
        if flag == 1:
            print(Side[block], end="")
    Color.b = final_img[450, 432, 0]
    Color.g = final_img[450, 432, 1]
    Color.r = final_img[450, 432, 2]
    Side[2] = color_recognition(Color.b, Color.g, Color.r, flag)
    if flag == 1:
        print(Side[2], end="")
    Color.b = final_img[450, 144, 0]
    Color.g = final_img[450, 144, 1]
    Color.r = final_img[450, 144, 2]
    Side[3] = color_recognition(Color.b, Color.g, Color.r, flag)
    if flag == 1:
        print(Side[3], end="")

        
# **********************************************************************************************************************
color_extraction("forward", 0)  # 识别forward3的颜色
color_set(Side[3], 0)
color_extraction("left", 0)  # 识别left2的颜色
color_set(Side[2], 1)
color_extraction("down", 0)  # 识别down0的颜色
color_set(Side[0], 2)
cube_side = ["back", "down", "forward", "left", "right", "up"]
for single_side in cube_side:  # 识别所有面的颜色
    color_extraction(single_side, 1)
