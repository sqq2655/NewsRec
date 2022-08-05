import hashlib

def md5_pwd(uid,pwd):
    h = hashlib.md5(uid.encode('utf-8'))
    h.update(pwd.encode('utf-8'))
    return h.hexdigest()

if __name__ == '__main__':
    print(md5_pwd('100004','123456'))