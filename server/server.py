from socket import *

HOST = ''
PORT = 2333
BUFSIZ = 1024
ADDRESS = (HOST, PORT)

# 创建监听socket
import time
tcpServerSocket = socket(AF_INET, SOCK_STREAM)

def rcd(s):
    tmp0=s.split('/')[0] #水温
    tmp1=s.split('/')[1] #气温
    humi=s.split('/')[2] #湿度
    tmp2=s.split('/')[3] #高精度气温
    pres=s.split('/')[4] #气压
    out=''
    with open('data.js','r') as f:
        s=f.read()
    if len(s)==0:
        out='date=["'+time.strftime("%Y-%m-%d %X")+'"]\n'
        out+='tmp0=[["'+time.strftime("%Y-%m-%d %X")+'",'+tmp0+']]\n'
        out+='tmp1=[["'+time.strftime("%Y-%m-%d %X")+'",'+tmp1+']]\n'
        out+='humi=[["'+time.strftime("%Y-%m-%d %X")+'",'+humi+']]\n'
        out+='pres=[["'+time.strftime("%Y-%m-%d %X")+'",'+pres+']]\n'
        out+='tmp2=[["'+time.strftime("%Y-%m-%d %X")+'",'+tmp2+']]\n'
    else:
        with open('data.js','r') as f:
            s=f.readline()
            while s!='':
                if s[:4]=='date':
                    out+=s[:s.find(']')]+',"'+time.strftime("%Y-%m-%d %X")+'"]\n'
                if s[:4]=='tmp0':
                    out+=s[:s.find(']]')]+'],["'+time.strftime("%Y-%m-%d %X")+'",'+tmp0+']]\n'
                if s[:4]=='tmp1':
                    out+=s[:s.find(']]')]+'],["'+time.strftime("%Y-%m-%d %X")+'",'+tmp1+']]\n'
                if s[:4]=='humi':
                    out+=s[:s.find(']]')]+'],["'+time.strftime("%Y-%m-%d %X")+'",'+humi+']]\n'
                if s[:4]=='pres':
                    out+=s[:s.find(']]')]+'],["'+time.strftime("%Y-%m-%d %X")+'",'+pres+']]\n'
                if s[:4]=='tmp2':
                    out+=s[:s.find(']]')]+'],["'+time.strftime("%Y-%m-%d %X")+'",'+tmp2+']]\n'
                s=f.readline()
    with open('data.js','w') as f:
        f.write(out)

# 绑定IP地址和固定端口
tcpServerSocket.bind(ADDRESS)
print("服务器启动，监听端口{}...".format(ADDRESS[1]))

tcpServerSocket.listen(5)

try:
    while True:
        print('服务器正在运行，等待客户端连接...')

        # client_socket是专为这个客户端服务的socket，client_address是包含客户端IP和端口的元组
        client_socket, client_address = tcpServerSocket.accept()
        print('客户端{}已连接！'.format(client_address))

        try:
            while True:
                # 接收客户端发来的数据，阻塞，直到有数据到来
                # 事实上，除非当前客户端关闭后，才会跳转到外层的while循环，即一次只能服务一个客户
                # 如果客户端关闭了连接，data是空字符串
                data = client_socket.recv(2048)
                if data:
                    try:
                        print('接收到消息 {}({} bytes) 来自 {}'.format(data.decode('utf-8'), len(data), client_address))
                    except:
                        print('消息错误')
                    try:
                        rcd(data.decode('utf-8'))
                        print(type(data))
                        client_socket.send("ok".encode('utf-8'))
                    except:
                        print("error")
                        client_socket.send("error".encode('utf-8'))
                    break
        finally:
            # 关闭为这个客户端服务的socket
            client_socket.close()
finally:
    # 关闭监听socket，不再响应其它客户端连接
    tcpServerSocket.close()











































