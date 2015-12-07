#!/usr/bin/python2.6

from socket import *
import time
import thread

HOST = ''
PORT = 8887
BUFSIZ = 1024*1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#tcpSerSock.setsockopt(SOL_SOCKET, SO_LINGER, 0)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

CMD_CREADY = 'CReady'
CMD_GOTC = 'GotC'

CMD_MREADY = 'MReady'
CMD_GOTM = 'GotM'

READY_TO_RELY = 'RReady'

server_sock=None
jpeg_data_list = []

def conn_handler(tcpCliSock, addr):
    print 'handler start'
    jpeg_data = ''
    #while read data
    while True:
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            print 'no data, will break'
            break
        elif data == CMD_CREADY:
            print 'get cmd CReady'
            if len(jpeg_data_list)< 10:
                tcpCliSock.send(READY_TO_RELY)
            else:
                tcpCliSock.send(CMD_GOTC)
            break
        elif data == CMD_MREADY:
            print 'get cmd MReady'
            print 'jpeg data list len: ', len(jpeg_data_list)
            if len(jpeg_data_list)<=0:
                tcpCliSock.send(CMD_GOTM)
            else:
                tcpCliSock.send(jpeg_data_list[0])
                del jpeg_data_list[0]
                print 'delete one jpeg'
            break
        else:
            print 'camera data coming'
            jpeg_data += data

    if jpeg_data:
        print 'append one jpeg'
        jpeg_data_list.append(jpeg_data)
        jpeg_data = ''
    tcpCliSock.close()

    print 'handler end'
    
def main():
    while True:
        print 'waiting for connection...'
        tcpCliSock, addr = tcpSerSock.accept()
        print '...connected from:', addr
        #thread.start_new_thread(conn_handler,(tcpCliSock, addr))
        conn_handler(tcpCliSock, addr)
        print 'a new thread created'
        

        #time.sleep(2)

    tcpSerSock.close()

if __name__ == '__main__':
    main()
