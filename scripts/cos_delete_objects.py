# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
# import base
from django.conf import settings


# 初始化client
def initCos(region='ap-chengdu'):
    # 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在CosConfig中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
    secret_id = settings.COS_SECRET_ID  # 替换为用户的 SecretId，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
    secret_key = settings.COS_SECRET_KEY  # 替换为用户的 SecretKey，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
    region = region  # 替换为用户的 region，已创建桶归属的region可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
    token = None  # 如果使用永久密钥不需要填入token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见https://cloud.tencent.com/document/product/436/14048
    scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
    client = CosS3Client(config)
    return client


key_list = [
    {'Key': '1650592066112_03_gettyimages-895174530_res.jpg'},  # Key首字母大写
    {'Key': '1650592066110_02_gettyimages-892790542_res.jpg'},  # Key首字母大写
    {'Key': '1650592066106_01_adobestock_100657102_resi.jpg'},  # Key首字母大写
    {'Key': '1650592066113_06_gettyimages-86292695_resi.jpg'},  # Key首字母大写
    {'Key': '1650592106379_09_shutterstock_212336365_re.jpg'}   # Key首字母大写
]

client = initCos()
client.delete_objects(
    Bucket='15885464645-20220422005237-saas-1310871600',
    Delete={'Quiet': 'true', 'Object': key_list}
)