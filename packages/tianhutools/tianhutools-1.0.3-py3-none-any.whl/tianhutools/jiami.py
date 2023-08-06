from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import rsa
import base64
import os
def __bytes_to_b64(bytes_var : bytes) -> str:
    return base64.b64decode(bytes_var)
def __b64_to_bytes(b64str : str) -> bytes:
    return base64.b64encode(b64str)
class KaiSa:
    def jiami(self,plaintext, shift):
        """
        凯撒加密算法
        plaintext: 明文
        shift: 偏移量
        """
        ciphertext = ''
        for char in plaintext:
            if char.isalpha():  # 只加密字母
                # 将字母转换成数字，A为65，a为97，因此需要减去相应的值
                num = ord(char)
                if char.isupper():  # 大写字母
                    num = (num - 65 + shift) % 26 + 65
                else:  # 小写字母
                    num = (num - 97 + shift) % 26 + 97
                # 将数字转换回字母
                char = chr(num)
            ciphertext += char
        return ciphertext
    def jiemi(self,ciphertext, shift):
        """
        凯撒解密算法
        ciphertext: 密文
        shift: 偏移量(加密时的偏移量)
        """
        plaintext = ''
        for char in ciphertext:
            if char.isalpha():  # 只解密字母
                num = ord(char)
                if char.isupper():  # 大写字母
                    num = (num - 65 - shift) % 26 + 65
                else:  # 小写字母
                    num = (num - 97 - shift) % 26 + 97
                char = chr(num)
            plaintext += char
        return plaintext
import base64
import rsa

class RSA:
    def newkeys(self, length: int = 1024):
        """
        生成一个rsa密钥对，默认为1024位
        :param length : int,长度，默认为1024
        :return 公钥,私钥
        """
        (gongyao, siyao) = rsa.newkeys(length)
        gongyao_save = gongyao.save_pkcs1().decode()
        siyao_save = siyao.save_pkcs1().decode()
        return gongyao_save, siyao_save

    def jiami(self, gongyao, text) -> str:
        """
        使用rsa算法进行加密
        Args:
            gongyao : rsa 公钥pem格式
            text : 欲加密文本
        Return:
            返回密文(base64)
        """
        message = text.encode()
        gongyao_obj = rsa.PublicKey.load_pkcs1(gongyao.encode())
        miwen = base64.b64encode(rsa.encrypt(message, gongyao_obj)).decode()
        return miwen

    def jiemi(self, siyao, miwen: str):
        """
        使用rsa算法进行解密
        Args:
            siyao : rsa私钥,pem格式
            miwen : 密文（base64）
        Return:
            明文
        """
        siyao_obj = rsa.PrivateKey.load_pkcs1(siyao)
        plaintext = rsa.decrypt(base64.b64decode(miwen), siyao_obj).decode()
        return plaintext

    def sign(self, siyao, text):
        """
        使用rsa算法进行数字签名
        :param siyao:rsa私钥,pem格式
        :param text:欲签名文本
        :return 返回签名文本
        """
        siyao_obj = rsa.PrivateKey.load_pkcs1(siyao)
        qianminwenben = base64.b64encode(rsa.sign(text.encode(), siyao_obj, 'SHA-1')).decode()
        return qianminwenben

    def qmyz(self, text, qmwb, gongyao):
        """
        签名验证
        :param text:被验证的文本
        :param qmwb:签名文本，sign()函数的返回值
        :param gongyao:rsa公钥,pem格式
        :return 成功返回True，失败返回False
        """
        res = rsa.verify(text.encode(), base64.b64decode(qmwb), rsa.PublicKey.load_pkcs1(gongyao))
        if res:
            return True
        else:
            return False


class AES:
    def newkey(self):
        """
        自动生成32位（256位）AES秘钥
        :return: key，base64编码的key
        """
        key = os.urandom(32)
        return base64.b64encode(key).decode()

    def jiami(self, plaintext, key):
        """
        AES加密算法
        plaintext: 明文
        key: 秘钥, base64编码的字符串
        Returns:
            密文, 随机数，验证标签，均为str类型的base64编码
        """
        key_bytes = base64.b64decode(key)
        iv = os.urandom(12)  # 生成12字节的随机向量
        cipher = Cipher(algorithms.AES(key_bytes), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return base64.b64encode(ciphertext).decode(), base64.b64encode(iv).decode(), base64.b64encode(
            encryptor.tag).decode()

    def jiemi(self, ciphertext, key, iv, tag):
        """
        AES解密算法
        ciphertext: 密文
        key: 秘钥
        iv: 加密时生成的随机向量
        tag: 加密时生成的验证标签
        """
        key_bytes = base64.b64decode(key)
        iv_bytes = base64.b64decode(iv)
        tag_bytes = base64.b64decode(tag)

        cipher = Cipher(algorithms.AES(key_bytes), modes.GCM(iv_bytes, tag_bytes), backend=default_backend())
        decryptor = cipher.decryptor()

        try:
            padded_data = decryptor.update(base64.b64decode(ciphertext)) + decryptor.finalize()

            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            plaintext = unpadder.update(padded_data) + unpadder.finalize()

            return plaintext.decode('utf-8')
        except:
            return None
class Weijiniya:
    def jiami(self,plaintext, key):
        """
        使用维吉尼亚密码加密明文字符串

        参数:
            plaintext (str): 明文字符串
            key (str): 加密秘钥，只能包含小写字母

        返回:
            str: 密文字符串
        """
        ciphertext = ""
        key_index = 0
        for c in plaintext:
            if c.isalpha():
                # 计算每个字符的移位量
                shift = ord(key[key_index % len(key)]) - ord('a')
                # 对字符进行移位并加入密文字符串中
                shifted_char = chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
                ciphertext += shifted_char
                key_index += 1
            else:
                # 非字母字符直接加入密文字符串中
                ciphertext += c
        return ciphertext

    def jiemi(self,ciphertext, key):
        """
        使用维吉尼亚密码解密密文字符串

        参数:
            ciphertext (str): 密文字符串
            key (str): 解密秘钥，只能包含小写字母

        返回:
            str: 明文字符串
        """
        plaintext = ""
        key_index = 0
        for c in ciphertext:
            if c.isalpha():
                # 计算每个字符的移位量
                shift = ord(key[key_index % len(key)]) - ord('a')
                # 对字符进行反向移位并加入明文字符串中
                shifted_char = chr((ord(c) - ord('a') - shift + 26) % 26 + ord('a'))
                plaintext += shifted_char
                key_index += 1
            else:
                # 非字母字符直接加入明文字符串中
                plaintext += c
        return plaintext