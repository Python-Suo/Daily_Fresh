from hashlib import sha1


def get_hash(str, salt=None):  # 盐　加佐料让明文变得更复杂
    '''取一个字符串的散列值'''
    # 提高字符串的复杂度
    str = '!@#$%' + str + '^&*()'
    if salt:
    # 若salt不为空　则拼接使明文更复杂
        str = str + salt

    # 取字符串的散列值
    sh = sha1()
    sh.update(str.encode('utf-8'))  # encode编码格式默认是utf-8
    return sh.hexdigest()