import base64

from Crypto.Cipher import AES  # 导入AES加密模块
from Crypto.Util.Padding import pad, unpad  # 导入填充模块，用于数据对齐
from base64 import b64encode, b64decode  # 导入base64编码和解码模块，用于编码加密后的数据以便传输和存储
from Crypto.Random import get_random_bytes  # 导入随机数生成模块，用于生成随机密钥

key = get_random_bytes(16)  # AES密钥，必须是16, 24或32字节长，这里生成一个16字节的随机密钥

nonce = get_random_bytes(8)  # 用于ctr模式，ECB模式不需要，这里生成一个8字节


# 定义ECB模式的加密函数
def encrypt_ecb(data):
    aes = AES.new(key, AES.MODE_ECB)  # 创建AES加密对象，使用ECB模式
    res = aes.encrypt(pad(data, AES.block_size))  # 对数据进行填充后加密，AES.block_size为块大小，对于AES来说是16字节
    encrypted_data_base64 = base64.b64encode(res).decode()  # 将加密后的数据进行base64编码以便于显示和传输
    print(encrypted_data_base64)  # 打印加密后的数据
    return encrypted_data_base64  # 返回加密后的数据

# 定义ECB模式的解密函数
def decrypt_ecb(data):
    aes = AES.new(key, AES.MODE_ECB)  # 创建AES解密对象，使用ECB模式
    encrypted_data_bytes = base64.b64decode(data.encode())  # 将base64编码的加密数据解码为字节
    decrypted_data_padded = aes.decrypt(encrypted_data_bytes)  # 解密数据
    decrypted_data = unpad(decrypted_data_padded, AES.block_size)  # 使用unpad函数去除填充，返回明文
    print(decrypted_data.decode())  # 打印明文
    return decrypted_data  # 返回明文



iv = get_random_bytes(16)

# 定义CBC模式的加密函数
def encrypt_cbc(data):
    aes = AES.new(key, AES.MODE_CBC,iv=iv)  # 创建AES加密对象，使用CBC模式
    res = aes.encrypt(pad(data, AES.block_size))  # 对数据进行填充后加密，AES.block_size为块大小，对于AES来说是16字节
    encrypted_data_base64 = base64.b64encode(res).decode()  # 将加密后的数据进行base64编码以便于显示和传输
    print(encrypted_data_base64)  # 打印加密后的数据
    return encrypted_data_base64  # 返回加密后的数据

# 定义CBC模式的解密函数
def decrypt_CBC(data):
    aes = AES.new(key, AES.MODE_CBC,iv=iv)  # 创建AES解密对象，使用CBC模式
    encrypted_data_bytes = base64.b64decode(data.encode())  # 将base64编码的加密数据解码为字节
    decrypted_data_padded = aes.decrypt(encrypted_data_bytes)  # 解密数据
    decrypted_data = unpad(decrypted_data_padded, AES.block_size)  # 使用unpad函数去除填充，返回明文
    print(decrypted_data.decode())  # 打印明文
    return decrypted_data  # 返回明文




# 定义OFB模式的加密函数
def encrypt_ofb(data):
    aes = AES.new(key, AES.MODE_OFB,iv=iv)  # 创建AES加密对象，使用OFB模式
    res = aes.encrypt(pad(data, AES.block_size))  # 对数据进行填充后加密，AES.block_size为块大小，对于AES来说是16字节
    encrypted_data_base64 = base64.b64encode(res).decode()  # 将加密后的数据进行base64编码以便于显示和传输
    print(encrypted_data_base64)  # 打印加密后的数据
    return encrypted_data_base64  # 返回加密后的数据

# 定义OFB模式的解密函数
def decrypt_ofb(data):
    aes = AES.new(key, AES.MODE_OFB,iv=iv)  # 创建AES解密对象，使用OFB模式
    encrypted_data_bytes = base64.b64decode(data.encode())  # 将base64编码的加密数据解码为字节
    decrypted_data_padded = aes.decrypt(encrypted_data_bytes)  # 解密数据
    decrypted_data = unpad(decrypted_data_padded, AES.block_size)  # 使用unpad函数去除填充，返回明文
    print(decrypted_data.decode())  # 打印明文
    return decrypted_data  # 返回明文



# 定义CFB模式的加密函数
def encrypt_cfb(data):
    aes = AES.new(key, AES.MODE_CFB,iv=iv)  # 创建AES加密对象，使用CFB模式
    res = aes.encrypt(pad(data, AES.block_size))  # 对数据进行填充后加密，AES.block_size为块大小，对于AES来说是16字节
    encrypted_data_base64 = base64.b64encode(res).decode()  # 将加密后的数据进行base64编码以便于显示和传输
    print(encrypted_data_base64)  # 打印加密后的数据
    return encrypted_data_base64  # 返回加密后的数据

# 定义CFB模式的解密函数
def decrypt_cfb(data):
    aes = AES.new(key, AES.MODE_CFB,iv=iv)  # 创建AES解密对象，使用CFB模式
    encrypted_data_bytes = base64.b64decode(data.encode())  # 将base64编码的加密数据解码为字节
    decrypted_data_padded = aes.decrypt(encrypted_data_bytes)  # 解密数据
    decrypted_data = unpad(decrypted_data_padded, AES.block_size)  # 使用unpad函数去除填充，返回明文
    print(decrypted_data.decode())  # 打印明文
    return decrypted_data  # 返回明文



# 定义CTR模式的加密函数
def encrypt_ctr(data):
    aes = AES.new(key, AES.MODE_CTR,nonce=nonce)  # 创建AES加密对象，使用CTR模式
    res = aes.encrypt(pad(data, AES.block_size))  # 对数据进行填充后加密，AES.block_size为块大小，对于AES来说是16字节
    encrypted_data_base64 = base64.b64encode(res).decode()  # 将加密后的数据进行base64编码以便于显示和传输
    print(encrypted_data_base64)  # 打印加密后的数据
    return encrypted_data_base64  # 返回加密后的数据

# 定义CTR模式的解密函数
def decrypt_ctr(data):
    aes = AES.new(key, AES.MODE_CTR,nonce=nonce)  # 创建AES解密对象，使用CTR模式
    encrypted_data_bytes = base64.b64decode(data.encode())  # 将base64编码的加密数据解码为字节
    decrypted_data_padded = aes.decrypt(encrypted_data_bytes)  # 解密数据
    decrypted_data = unpad(decrypted_data_padded, AES.block_size)  # 使用unpad函数去除填充，返回明文
    print(decrypted_data.decode())  # 打印明文
    return decrypted_data  # 返回明文


if __name__ == '__main__':
    print('ECB模式')
    data = 'Hello World!'.encode()  # 待加密数据，将字符串编码为字节
    res = encrypt_ecb(data)  # 调用加密函数
    print(f'加密后的数据为：{res}')  # 打印加密后的数据
    decrypt_ecb(res)  # 调用解密函数，验证加密解密过程
    print('-'*50)
    print('CBC模式')
    res = encrypt_cbc(data)  # 调用加密函数
    print(f'加密后的数据为：{res}')  # 打印加密后的数据
    decrypt_CBC(res)  # 调用解密函数，验证加密解密过程
    print('-'*50)
    print('OFB模式')
    res = encrypt_ofb(data)  # 调用加密函数
    print(f'加密后的数据为：{res}')  # 打印加密后的数据
    decrypt_ofb(res)  # 调用解密函数，验证加密解密过程
    print('-'*50)
    print('CFB模式')
    res = encrypt_cfb(data)  # 调用加密函数
    print(f'加密后的数据为：{res}')  # 打印加密后的数据
    decrypt_cfb(res)  # 调用解密函数，验证加密解密过程
    print('-'*50)
    print('CTR模式')
    res = encrypt_ctr(data)  # 调用加密函数
    print(f'加密后的数据为：{res}')  # 打印加密后的数据
    decrypt_ctr(res)  # 调用解密函数，验证加密解密过程
    print('-'*50)


