# -*- coding: utf-8 -*-
import redis

try:
    # 创建 Redis 连接（根据你的配置修改参数）
    r = redis.Redis(
        host='45.136.15.198',    # 替换为你的服务器 IP
        port=6379,                # 默认端口
        password='121474129Nm',   # 你的密码
        db=0,                     # 默认数据库
        socket_timeout=5,         # 超时时间（秒）
        ssl=False,                # 如果启用 SSL 改为 True
        ssl_cert_reqs='none'      # 忽略 SSL 证书验证（测试用）
    )

    # 测试连接
    r.ping()
    print("连接成功！")

    # 写入测试数据
    r.set('test_key', 'Hello Redis!')
    value = r.get('test_key')
    print(f"读取到的值: {value.decode()}")

except redis.exceptions.ConnectionError as e:
    print(f"连接失败：{e}")
    print("请检查：IP、端口、防火墙/安全组是否开放 6379 端口")

except redis.exceptions.AuthenticationError as e:
    print(f"认证失败：{e}")
    print("请检查密码是否正确（注意特殊字符需要 URL 编码）")

except Exception as e:
    print(f"未知错误：{e}")