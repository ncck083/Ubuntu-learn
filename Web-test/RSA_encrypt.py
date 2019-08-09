# -*- coding: UTF-8 -*-
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from urllib import parse

def create_rsa_key(password="123456"):
    """
    创建RSA密钥
    步骤说明：
    1、从 Crypto.PublicKey 包中导入 RSA，创建一个密码
    2、生成 1024/2048 位的 RSA 密钥
    3、调用 RSA 密钥实例的 exportKey 方法，传入密码、使用的 PKCS 标准以及加密方案这三个参数。
    4、将私钥写入磁盘的文件。
    5、使用方法链调用 publickey 和 exportKey 方法生成公钥，写入磁盘上的文件。
    """

    key = RSA.generate(1024)
    encrypted_key = key.exportKey(passphrase=password, pkcs=8,
                                  protection="scryptAndAES128-CBC")
    with open("my_private_rsa_key.bin", "wb") as f:
        f.write(encrypted_key)
    with open("my_rsa_public.pem", "wb") as f:
        f.write(key.publickey().exportKey())


def encrypt_and_decrypt_test(password="123456"):
    # 加载公钥
    recipient_key = RSA.import_key(
        open("my_rsa_public.pem").read()
    )
    cipher_rsa = PKCS1_v1_5.new(recipient_key)

    en_data = cipher_rsa.encrypt(b"123456")
    print(len(en_data), en_data)

    # 读取密钥
    private_key = RSA.import_key(
        open("my_private_rsa_key.bin").read(),
        passphrase=password
    )
    cipher_rsa = PKCS1_v1_5.new(private_key)
    data = cipher_rsa.decrypt(en_data, None)

    print(data)


# def decrypt_data(inputdata, code="123456"):
    # # URLDecode
    # data = parse.unquote(inputdata)

    # # base64decode
    # data = base64.b64decode(data)

    # private_key = RSA.import_key(
    #     open(curr_dir + "/my_private_rsa_key.bin").read(),
    #     passphrase=code
    # )
    # # 使用 PKCS1_v1_5，不要用 PKCS1_OAEP
    # # 使用 PKCS1_OAEP 的话，前端 jsencrypt.js 加密的数据解密不了
    # cipher_rsa = PKCS1_v1_5.new(private_key)

    # # 当解密失败，会返回 sentinel
    # sentinel = None
    # ret = cipher_rsa.decrypt(data, sentinel)

    # return ret
def decrypt_data(password):
    #password = request.values.get('password')
    with open('my_private_rsa_key.bin') as f:
        key = f.read()
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    password = cipher.decrypt(base64.b64decode(password), RANDOM_GENERATOR)
    #如果返回的password类型不是str，说明秘钥公钥不一致，或者程序错误
    if str(type(password))!="<type 'str'>":
        return 'fail'
    #结果应该为I_LOVE_YAYA

    
if __name__ == '__main__':
    #create_rsa_key()
    encrypt_and_decrypt_test()
