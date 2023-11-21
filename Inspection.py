# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/25 10:24
@Auth ： xyz
@File ：Inspection.py
@IDE ：PyCharm
"""
import cv2
import tkinter
from tkinter import filedialog
import numpy as np
import subprocess
import pyautogui
import pygetwindow as gw
import time

def open_application(applicatin_path):
    subprocess.Popen(applicatin_path)

    time.sleep(1)
    window = gw.getWindowsWithTitle("Uniscan M2130 Wizard")[0]
    window.activate()
    window_x = window.left
    window_y = window.top

    # 点击scan
    time.sleep(1)
    dropdown_x = window_x + 184
    dropdown_y = window_y + 136
    pyautogui.click(dropdown_x, dropdown_y)

    # 点击按键选择
    time.sleep(1)
    dropdown_x = window_x + 170
    dropdown_y = window_y + 200
    pyautogui.click(dropdown_x, dropdown_y)

    # 选中按键选择
    time.sleep(1)
    dropdown_x = window_x + 250
    dropdown_y = window_y + 250
    pyautogui.click(dropdown_x, dropdown_y)

    # 选中按键选择
    time.sleep(1)
    dropdown_x = window_x + 40
    dropdown_y = window_y + 540
    pyautogui.click(dropdown_x, dropdown_y)

    # 选中按键选择
    time.sleep(5)
    dropdown_x = window_x + 437
    dropdown_y = window_y + 14
    pyautogui.click(dropdown_x, dropdown_y)

def select_file():
    global root
    root = tkinter.Tk()
    root.title('路径选择')
    max_w, max_h = root.maxsize()
    root.geometry(f'500x300+{int((max_w - 500) / 2)}+{int((max_h - 300) / 2)}')  # 居中显示
    root.resizable(width=False, height=False)

    # 标签组件
    label = tkinter.Label(root, text='选择模版：', font=('华文彩云', 15))
    label.place(x=50, y=80)

    # 标签组件
    label2 = tkinter.Label(root, text='选择扫描：', font=('华文彩云', 15))
    label2.place(x=50, y=155)

    # 输入框控件
    global entry_text
    entry_text = tkinter.StringVar()
    entry = tkinter.Entry(root, textvariable=entry_text, font=('FangSong', 10), width=30, state='readonly')
    entry.place(x=150, y=85)

    # 输入框控件
    global entry_text2
    entry_text2 = tkinter.StringVar()
    entry2 = tkinter.Entry(root, textvariable=entry_text2, font=('FangSong', 10), width=30, state='readonly')
    entry2.place(x=150, y=155)

    # 按钮控件
    global a
    a = []

def get_path():
    # 返回一个字符串，可以获取到任意文件的路径。
    path1 = filedialog.askopenfilename(title='请选择文件')
    a.append(path1)
    entry_text.set(path1)
    return path1

def get_path2():
    global a
    path2 = filedialog.askopenfilename(title='请选择文件')
    a.append(path2)
    entry_text2.set(path2)
    return path2

def f1():
    button = tkinter.Button(root, text='选择路径', command=get_path)
    button.place(x=400, y=75)

def f2():
    button2 = tkinter.Button(root, text='选择路径', command=get_path2)
    button2.place(x=400, y=155)
    root.mainloop()

def get_file_list():
    return a

def calculate_black_pixel_count(image):
    # 统计像素值为0的黑色像素数量
    white_pixels = np.sum(image == 255)
    return white_pixels

def calculate_similarity(sub_design, sub_printout):
    white_pixels1 = calculate_black_pixel_count(sub_design)
    white_pixels2 = calculate_black_pixel_count(sub_printout)

    difference = abs(white_pixels1 - white_pixels2)
    b = max(white_pixels1, white_pixels2) - difference
    similarity = (b + 100) / (max(white_pixels1, white_pixels2) + 100)

    return similarity

def compare_and_resize_images(image1, image2):
    # 加载图片
    # image1 = cv2.imread(image1_path)
    # image2 = cv2.imread(image2_path)

    # 获取图片尺寸
    height1, width1  = image1.shape
    height2, width2 = image2.shape

    # 比较图片尺寸
    if height1 * width1 > height2 * width2:
        # 图片1尺寸较大，将其缩小成和图片2一样大
        image1 = cv2.resize(image1, (width2, height2))
    elif height1 * width1 < height2 * width2:
        # 图片2尺寸较大，将其缩小成和图片1一样大
        image2 = cv2.resize(image2, (width1, height1))

    return image1, image2

def process_image(ori_image):
    # 定义黑色字体的颜色范围（在灰度图像中）
    lower_black = 0
    upper_black = 50

    # 获取图像的宽度和高度
    height, width = ori_image.shape


    # # 裁剪图像
    # image = image[1:height - 1, 1:width - 1]
    left = 5
    top = 5
    right = width - 5
    bottom = height - 5
    image = ori_image[top:bottom, left:right]

    height, width = image.shape

    # 初始化四个坐标点
    top = None
    bottom = None
    left = None
    right = None

    # 从顶部边缘向下查找黑色字体
    for y in range(height):
        if top is not None:
            break
        for x in range(width):
            pixel_value = image[y, x]
            if lower_black <= pixel_value <= upper_black:
                top = (x, y)
                break

    # 从底部边缘向上查找黑色字体
    for y in range(height - 1, -1, -1):
        if bottom is not None:
            break
        for x in range(width):
            pixel_value = image[y, x]
            if lower_black <= pixel_value <= upper_black:
                bottom = (x, y)
                break

    # 从左侧边缘向右查找黑色字体
    for x in range(width):
        if left is not None:
            break
        for y in range(height):
            pixel_value = image[y, x]
            if lower_black <= pixel_value <= upper_black:
                left = (x, y)
                break

    # 从右侧边缘向左查找黑色字体
    for x in range(width - 1, -1, -1):
        if right is not None:
            break
        for y in range(height):
            pixel_value = image[y, x]
            if lower_black <= pixel_value <= upper_black:
                right = (x, y)
                break

    # 计算最大矩形的坐标
    if top is not None and bottom is not None and left is not None and right is not None:
        # 计算最大矩形的坐标
        x1 = min(top[0], bottom[0], left[0], right[0])
        y1 = min(top[1], bottom[1], left[1], right[1])
        x2 = max(top[0], bottom[0], left[0], right[0])
        y2 = max(top[1], bottom[1], left[1], right[1])

        # # 扩展矩形边界
        # x1 -= int(0.005 * width)
        # y1 -= int(0.005 * height)
        # x2 += int(0.005 * width)
        # y2 += int(0.005 * height)
        #
        # # 确保边界不超出图像范围
        # x1 = max(x1, 0)
        # y1 = max(y1, 0)
        # x2 = min(x2, width - 1)
        # y2 = min(y2, height - 1)

        # 创建一个彩色图像副本，用于绘制边界框
        colored_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        # # 绘制最大矩形框
        # cv2.rectangle(colored_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 裁剪图像
        cropped_image = image[y1:y2, x1:x2]

        return colored_image, cropped_image
    else:
        print("未找到黑色字体")
        return None, None

def pixel_comparison(design, printout):
    # 灰度处理
    gray_design = cv2.cvtColor(design, cv2.COLOR_BGR2GRAY)
    gray_printout = cv2.cvtColor(printout, cv2.COLOR_BGR2GRAY)

    # 二值化
    _, thresh_design = cv2.threshold(gray_design, 127, 255, cv2.THRESH_BINARY_INV)
    _, thresh_printout = cv2.threshold(gray_printout, 127, 255, cv2.THRESH_BINARY_INV)


    # 划定轮廓
    contours_design, _ = cv2.findContours(thresh_design, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_printout, _ = cv2.findContours(thresh_printout, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # print(len(contours_design))
    # 对每个子区域进行匹配比对和阈值检测
    for i in range(len(contours_design)):
        # 获取设计原件和打印稿中的当前子区域
        x_d, y_d, w_d, h_d = cv2.boundingRect(contours_design[i])
        sub_design = thresh_design[y_d:y_d + h_d, x_d:x_d + w_d]

        # 在设计原件上画框
        # cv2.rectangle(design, (x_d, y_d), (x_d + w_d, y_d + h_d), (0, 0, 255), 2)

        # 映射子区域到打印稿中的对应位置
        x_p, y_p, w_p, h_p = x_d, y_d, w_d, h_d
        sub_printout = thresh_printout[y_p:y_p + h_p, x_p:x_p + w_p]

        similarity = calculate_similarity(sub_design, sub_printout)

        # # 如果黑色像素个数不同，则在打印稿上框选缺陷区域
        # if similarity < 0.7:
        #     cv2.rectangle(printout, (x_p, y_p), (x_p + w_p, y_p + h_p), (0, 0, 255), 2)

        cv2.rectangle(printout, (x_p, y_p), (x_p + w_p, y_p + h_p), (0, 0, 255), 2)

    for i in range(len(contours_printout)):
        # 获取设计原件和打印稿中的当前子区域
        x_d, y_d, w_d, h_d = cv2.boundingRect(contours_printout[i])
        sub_printout = thresh_printout[y_d:y_d + h_d, x_d:x_d + w_d]

        # 在设计原件上画框
        # cv2.rectangle(design, (x_d, y_d), (x_d + w_d, y_d + h_d), (0, 0, 255), 2)

        # 映射子区域到打印稿中的对应位置
        x_p, y_p, w_p, h_p = x_d, y_d, w_d, h_d
        sub_design = thresh_design[y_p:y_p + h_p, x_p:x_p + w_p]

        similarity = calculate_similarity(sub_design, sub_printout)

        # # 如果黑色像素个数不同，则在打印稿上框选缺陷区域
        # if similarity < 0.7:
        #     cv2.rectangle(printout, (x_p, y_p), (x_p + w_p, y_p + h_p), (0, 0, 255), 2)

        cv2.rectangle(printout, (x_p, y_p), (x_p + w_p, y_p + h_p), (0, 0, 255), 2)

    combined_image = np.hstack((cv2.resize(design, None, fx=0.5, fy=0.5), cv2.resize(printout, None, fx=0.5, fy=0.5)))

    return combined_image

if __name__ == "__main__":
    # application_path = r"C:\Program Files (x86)\UNIS\Uniscan M2130_1.2.5\Userinfo\Uniscan Wizard Button.exe"
    # open_application(application_path)

    select_file()
    f1()
    f2()
    a = get_file_list()
    # 记录程序开始时间
    start_time = time.time()
    # 读取模版图像并灰度化
    image_tempalte = cv2.imread(a[0], cv2.IMREAD_GRAYSCALE)
    # 读取扫描图像并灰度化
    image_scan = cv2.imread(a[1], cv2.IMREAD_GRAYSCALE)
    height, width =image_tempalte.shape
    # 处理图像
    colored_image, cropped_image = process_image(image_tempalte)
    colored_scanImg, cropped_scanImg = process_image(image_scan)
    # 裁剪图像
    originalImage, scanImage = compare_and_resize_images(cropped_image, cropped_scanImg)
    # 转为3通道
    originalImage = cv2.cvtColor(originalImage, cv2.COLOR_GRAY2BGR)
    scanImage = cv2.cvtColor(scanImage, cv2.COLOR_GRAY2BGR)
    # 进行像素对比
    combined_image = pixel_comparison(originalImage, scanImage)

    # 记录程序结束时间
    end_time = time.time()
    # 计算整个程序的运行时间
    total_duration = end_time - start_time
    # 输出整个程序的运行时间
    print(f"整个程序的运行时间：{total_duration}秒")

    cv2.imshow('Result', combined_image)
    cv2.waitKey(0)
