from socket import *
import threading
import time
import json

HOST = ''
PORT = 2333
ADDRESS = (HOST, PORT)

# 12.3/23/66/23.4/80800

def record(s):
    tmp0=s.split('/')[0] #水温
    tmp1=s.split('/')[1] #气温
    humi=s.split('/')[2] #湿度
    tmp2=s.split('/')[3] #高精度气温
    pres=s.split('/')[4] #气压
    out=''
    tmp0=float(tmp0) # 过滤非法信息
    tmp1=float(tmp1)
    humi=float(humi)
    tmp2=float(tmp2)
    pres=float(pres)
    with open('data.js','r') as f:
        s=f.read()
    if len(s)==0:
        dic={'date':[],'tmp0':[],'tmp1':[],'tmp2':[],'humi':[],'pres':[]}
    else:
        dic=json.loads(s)
    t=time.strftime("%Y-%m-%d %X")
    dic['date'].append(t)
    dic['tmp0'].append([t,tmp0])
    dic['tmp1'].append([t,tmp1])
    dic['tmp2'].append([t,tmp2])
    dic['humi'].append([t,humi])
    dic['pres'].append([t,pres])
    with open('data.js','w') as f:
        f.write(json.dumps(dic))
    dic={'date':t,'tmp0':tmp0,'tmp1':tmp1,'tmp2':tmp2,'humi':humi,'pres':pres}
    with open('now.js','w') as f:
        f.write(json.dumps(dic))

def client_server(client,addr):
    try:
        client.settimeout(60)
        data = client.recv(2048)
        if data:
            try:
                print('接收到消息 {}({} bytes) 来自 {}'.format(data.decode('utf-8'), len(data), addr))
            except:
                print('消息错误')
            try:
                record(data.decode('utf-8'))
                print(type(data))
                client.send("ok".encode('utf-8'))
            except:
                print("error")
                client.send("error".encode('utf-8'))
    finally:
        print("已关闭来自{}的连接".format(addr))
        client.close()

# 绑定IP地址和固定端口
sock=socket(AF_INET, SOCK_STREAM)
sock.bind(ADDRESS)
print("服务器启动，监听端口{}...".format(ADDRESS[1]))

sock.listen(5)

while True:
    print('服务器正在运行，等待客户端连接...')
    client,addr = sock.accept()
    print('客户端{}已连接！'.format(addr))
    threading.Thread(target=client_server,args=(client,addr)).start()
