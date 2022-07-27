# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
from sts.sts import Sts
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


# 判断桶是否存在
def cos_bucket_exists(bucket):
    client = initCos()
    tf = client.bucket_exists(
        Bucket=bucket,
    )
    return tf


# 判断桶中的文件是否存在
def cos_object_exists(bucket, key):
    client = initCos()
    tf = client.object_exists(
        Bucket=bucket,
        Key=key
    )
    return tf


# 创建公有读私有写的桶
def cos_create_bucket(bucket, acl='public-read'):
    client = initCos()
    response = client.create_bucket(
        Bucket=bucket,
        ACL=acl,
    )

    # 跨域API配置
    cors_config = {
        'CORSRule': [
            {
                'AllowedOrigin': '*',
                'AllowedMethod': ['GET', 'PUT', 'HEAD', 'POST', 'DELETE'],
                'AllowedHeader': "*",
                'ExposeHeader': "*",
                'MaxAgeSeconds': 500
            }
        ]
    }

    client.put_bucket_cors(
        Bucket=bucket,
        CORSConfiguration=cors_config,
    )


# wiki上传文件（对象上传自动转化）
def wiki_upload(bucket, body, key, region='ap-chengdu'):  # 文件对象间接上传
    client = initCos()
    # 上传对象方法，自动转为文件存入
    image_url = client.upload_file_from_buffer(
        Bucket=bucket,
        Body=body,  # post方式上传文件，后台post接收到的对象（request.FILES.get("键") 比如markdown上传的为：editormd-image-file），可以后台查看，再获取
        Key=key,  # 上传完成之后的文件名
    )
    # 上传之后返回一个url--格式：https://dsa-1310871600.cos.ap-nanjing.myqcloud.com/%E5%A4%B4%E5%83%8Fx.png
    return "https://{}.cos.{}.myqcloud.com/{}".format(bucket, region, key)


# 删除单个文件
def cos_delete_object(bucket, key):
    client = initCos()
    client.delete_object(
        Bucket=bucket,
        Key=key
    )


# 删除多个文件
def cos_delete_objects(bucket, key_list):
    client = initCos()
    client.delete_objects(
        Bucket=bucket,
        Delete={'Quiet': 'true', 'Object': key_list}
    )

    # response = client.delete_objects(
    #     Bucket='examplebucket-1250000000',
    #     Delete={
    #         'Object': [
    #             {
    #                 'Key': 'exampleobject1'
    #             },
    #             {
    #                 'Key': 'exampleobject2'
    #             }
    #         ]
    #     }
    # )

    # 查询文件列表


# list_objects返回的对象的数据结构
# {'Name': '15885464645-20220416232209-saas-1310871600',
# 'EncodingType': 'url',
# 'Prefix': None,
# 'Marker': None,
# 'MaxKeys': '1000',
# 'IsTruncated': 'false',
# 'Contents': [
# {'Key': '17ab878b3dd8564e161259e876639237.png', 'LastModified': '2022-04-17T02:22:57.000Z', 'ETag': '"2446715fd8277388b6235f37c779100d"', 'Size': '169216', 'Owner': {'ID': '1310871600', 'DisplayName': '1310871600'}, 'StorageClass': 'STANDARD'},
# {'Key': '22e52799a76819a260d1b0d5751d6f41.jpg', 'LastModified': '2022-04-16T15:26:19.000Z', 'ETag': '"a4f535e46cf6e82a5c6be81b3dff5379"', 'Size': '827348', 'Owner': {'ID': '1310871600', 'DisplayName': '1310871600'}, 'StorageClass': 'STANDARD'},
# {'Key': '25cb2a365314ef4abe455570c9563195.jpg', 'LastModified': '2022-04-17T02:23:04.000Z', 'ETag': '"47d63b9819321b01ec19ff28ce465b51"', 'Size': '108294', 'Owner': {'ID': '1310871600', 'DisplayName': '1310871600'}, 'StorageClass': 'STANDARD'},
# {'Key': '39b05fea356be9584418d1f9e40f210e.jpg', 'LastModified': '2022-04-17T02:22:53.000Z', 'ETag': '"47d63b9819321b01ec19ff28ce465b51"', 'Size': '108294', 'Owner': {'ID': '1310871600', 'DisplayName': '1310871600'}, 'StorageClass': 'STANDARD'},
# ]}

# 前端获取cos临时凭证上传文件
def upload_credential(bucket, region, secret_id=settings.COS_SECRET_ID, secret_key=settings.COS_SECRET_KEY):
    config = {
        'url': 'https://sts.tencentcloudapi.com/',
        # 域名，非必须，默认为 sts.tencentcloudapi.com
        'domain': 'sts.tencentcloudapi.com',
        # 临时密钥有效时长，单位是秒
        'duration_seconds': 5,
        'secret_id': secret_id,
        # 固定密钥
        'secret_key': secret_key,
        # 设置网络代理
        # 'proxy': {
        #     'http': 'xx',
        #     'https': 'xx'
        # },
        # 换成你的 bucket
        'bucket': bucket,
        # 换成 bucket 所在地区
        'region': region,
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            "*",
            # # 简单上传
            # 'name/cos:PutObject',
            # 'name/cos:PostObject',
            # # 分片上传
            # 'name/cos:InitiateMultipartUpload',
            # 'name/cos:ListMultipartUploads',
            # 'name/cos:ListParts',
            # 'name/cos:UploadPart',
            # 'name/cos:CompleteMultipartUpload'
        ],
    }

    try:
        sts = Sts(config)
        result_dict = sts.get_credential()  # 字典类型数据
        return result_dict
    except Exception as e:
        print("获取临时凭证异常：\n" + e)


# 上传文件校验：查询对象元数据
def cos_head_object(bucket, key):
    client = initCos()
    result_dict = client.head_object(
        Bucket=bucket,
        Key=key
    )
    return result_dict


# 列出桶中文件
def cos_list_objects(bucket):
    client = initCos()
    response = client.list_objects(
        Bucket=bucket
    )
    # 这种方式获取最多只能获取1000个文件对象
    result_lst = []
    if 'Contents' in response:  # Contents表示存储文件的字典，桶中没有文件该键值对不存在
        for content in response['Contents']:
            result_lst.append(content['Key'])

    return result_lst


# 实现删除桶
def cos_delete_bucket(bucket):
    client = initCos()

    if not cos_bucket_exists(bucket):
        return False

    else:
        # 删除正常上传的对象
        while True:
            # 每次最多只能取1000个对象
            part_objects = client.list_objects(Bucket=bucket)

            # 删除Contents的多个对象

            if "Contents" not in part_objects.keys():  # 桶中无文件
                break

            client.delete_objects(
                Bucket=bucket,
                Delete={
                    'Quiet': 'true',
                    'Object': [{"Key": iterm["Key"]} for iterm in part_objects["Contents"]]  # 构造数据格式
                }
            )

            # 判断取到的是否截断（不满1000个对象）
            if part_objects['IsTruncated'] == "false":
                break

        # 删除正在分块上传未完成产生的碎片
        while True:
            # 获取Bucket中正在进行的分块上传的碎片，每次最多只能取1000个
            part_uploads = client.list_multipart_uploads(bucket)

            if 'Upload' not in part_uploads.keys():
                break

            for item in part_uploads['Upload']:
                client.abort_multipart_upload(bucket, item['Key'], item['UploadId'])

            if part_uploads['IsTruncated'] == "false":
                break

        # 完成删除文件与碎片后删除桶
        client.delete_bucket(
            Bucket=bucket
        )

        return True
