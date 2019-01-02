
import requests
# img_url = 'http://mp.weixin.qq.com/mp/verifycode?cert=1543817816454.1658'



import base64
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import ssl

def base64_img():
    with open('./wechat_yanzhenma/1.jpg', 'rb') as f:
        base64_img_data = base64.b64encode(f.read())
    return base64_img_data.decode('utf-8')

def get_code():
    img = base64_img()
    # print(img)
    host = 'http://302307.market.alicloudapi.com'
    path = '/ocr/captcha'
    method = 'POST'
    appcode = 'e7772b7b45d14a348fdda76cd0907206'
    querys = ''
    bodys = {}
    url = host + path
    bodys['image'] = '''data:image/jpeg;base64,%s''' % img
    bodys['type'] = '''1001'''
    post_data = urlencode(bodys).encode('utf-8')
    request = Request(url, post_data)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    # 根据API的要求，定义相对应的Content-Type
    request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = False
    response = urlopen(request, context=ctx)
    content = response.read()

    return content if content else ''


# def tessor():
#     import tesserocr
#     print(tesserocr.file_to_text('./wechat_yanzhenma/1.jpg'))
#
#     from PIL import Image
#     image = Image.open('./wechat_yanzhenma/4.jpg')
#
#     image = image.convert('L')
#     threshold = 220
#     table = []
#     for i in range(256):
#         if i < threshold:
#             table.append(0)
#         else:
#             table.append(1)
#
#     image = image.point(table, '1')
#     image.show()
#
#     result = tesserocr.image_to_text(image)
#     print(result)

# if __name__ == '__main__':
#     tessor()