#!/usr/bin/env python
# coding=utf-8
import json
from sts.sts import Sts


def get_credential_demo():
    config = {
        'url': 'https://sts.tencentcloudapi.com/',
        # 域名，非必须，默认为 sts.tencentcloudapi.com
        'domain': 'sts.tencentcloudapi.com',
        # 临时密钥有效时长，单位是秒
        'duration_seconds': 1800,
        'secret_id': 'secret_id',
        # 固定密钥
        'secret_key': 'secret_key',
        # 设置网络代理
        # 'proxy': {
        #     'http': 'xx',
        #     'https': 'xx'
        # },
        # 换成你的 bucket
        'bucket': '15885464645-20220420110217-saas-1310871600',
        # 换成 bucket 所在地区
        'region': 'ap-chengdu',
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            "*"
        ],
    }

    try:
        sts = Sts(config)
        response = sts.get_credential()
        print('get data : ' + json.dumps(dict(response), indent=4))
    except Exception as e:
        print(e)


get_credential_demo()
