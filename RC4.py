cipher1=""
def get_message():
    fo = open("data.txt","r")
    s = fo.read()
    s=str(s)
    fo.close()
    return s
def get_message1():
    return cipher1
def get_key():
    print("���������Կ��")
    key = input()
    if key == '':
        key = 'none_public_key'
    return key
def init_box(key):
    """
    S�� 
    """
    s_box = list(range(256)) #����û����ԿС��256�������С��256Ӧ�ò����ظ���伴��
    j = 0
    for i in range(256):
        j = (j + s_box[i] + ord(key[i % len(key)])) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box
def ex_encrypt(plain,box,mode):
    """
    ����PRGA������Կ�����������ֽ���򣬼ӽ���ͬһ���㷨
    """
    if mode == '2':
        plain = plain
    res = []
    i = j =0
    for s in plain:
        i = (i + 1) %256
        j = (j + box[i]) %256
        box[i], box[j] = box[j], box[i]
        t = (box[i] + box[j])% 256
        k = box[t]
        res.append(chr(ord(s)^k))
    cipher = "".join(res)
    if  mode == '1':
        fo=open("cipher.txt","wb+")
        # ���ɿ����ַ���Ҫ����
        print("���ܺ�����:")
        print(cipher)
        #print(type(cipher))
        global cipher1
        cipher1 = cipher
        cipher = cipher.encode()
        fo.seek(0)
        fo.write(cipher)
        fo.seek(0)
        listsss=[fo.read(1) for i in range(100)]
        fo.close()
    if mode == '2':
        # ���ɿ����ַ���Ҫ����
        print("���ܺ�����:")
        print(cipher)
def get_mode():
    print("��ѡ����ܻ��߽���")
    print("1. Encrypt")
    print("2. Decode")
    mode = input()
    if mode == '1':
        message = get_message()
        key = get_key()
        box = init_box(key)
        ex_encrypt(message,box,mode)
    elif mode == '2':
        message = get_message1()
        key = get_key()
        box = init_box(key)
        ex_encrypt(message, box, mode)
    else:
        print("��������")
if __name__ == '__main__':
    while True:
        get_mode()
