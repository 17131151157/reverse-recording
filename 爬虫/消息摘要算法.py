#  pip install pycryptodome -i https://mirrors.aliyun.com/pypi/simple/

from Crypto.Hash import MD5, SHA1, SHA256, SHA512, SHA3_256, SHA3_512, BLAKE2b, BLAKE2s



# MD5
md5 = MD5.new()
md5.update(b'hello world')
print(md5.hexdigest())

# SHA1
sha1 = SHA1.new()
sha1.update(b'hello world')
print('sha1算法的加密值：{}'.format(sha1.hexdigest()))

# SHA256
sha256 = SHA256.new()
sha256.update(b'hello world')
print('SHA256算法的加密值：{}'.format(sha256.hexdigest()))


# SHA3_256
sha3_256 = SHA3_256.new()
sha3_256.update(b'hello world')
print('SHA3_256算法的加密值：{}'.format(sha3_256.hexdigest()))