# !/usr/bin/python
#improt socket module

from socket import *
serverSocket = socket(AF_INET,SOCK_STREAM)
#Prepare a server socket
serverSocket.bind(('127.0.0.1',6789)) # 将TCP欢迎套接字绑定到指定端口
serverSocket.listen(1) # 最大连接数为1
while True:
    #Establish the connection
    print ('Ready to serve...')
    connectionSocket,addr = serverSocket.accept() # 接受到客户连接请求后,建立新的TCP连接套接字
    try:
        message = connectionSocket.recv(1024) # 获取客户发送哦内的报文
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read();
        # Send one HTTP header line into socket
        # 发送一个HTTP Message 头部到 Socket
        header = ' HTTP/1.1 200 OK\n Connection:close\nContent-Type: text/html\nContent-Length: %d\n\n ' %(len(outputdata))
        connectionSocket.send(header.encode())

        # Send the content of the requested file to the client
        # 发送请求的文件的内容给 客户端
        for i in range(0,len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        # 处理 访问非法的情况
        header = 'HTTP/1.1 404 not Found'
        connectionSocket.send(header.encode())

        # close client socket
        connectionSocket.close()
serverSocket.close()
