# pip install ddddocr -i https://mirrors.aliyun.com/pypi/simple/
# 安装 ddddocr 库，用于识别验证码

import requests
import ddddocr

def get_ocr(img):
    """获取验证码识别结果"""
    # 初始化 ddddocr 对象
    ocr = ddddocr.DdddOcr()
    with open(img, 'rb') as f:
        # 读取验证码图片
        image = f.read()
    # 使用 ddddocr 对象识别验证码
    res = ocr.classification(image)
    print(res)
    # 返回识别结果
    return res