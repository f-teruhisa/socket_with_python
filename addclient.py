#!/usr/bin/env python

import socket
import struct

def send_msg(sock, msg):
    # 送信できたバイト数
    total_sent_len = 0
    # 送信したいバイト数
    total_msg_len = len(msg)
    # 未送信のデータが無いかを判定する
    while total_sent_len < total_msg_len:
        # ソケットにバイト列を書き込み、書き込んだバイト数を得る
        sent_len = sock.send(msg[total_sent_len:])
        # 書き込めない場合は、ソケットの接続が終了している
        if sent_len == 0:
            raise RuntimeError('socket connection broken')
        total_sent_len += sent_len


def recv_msg(sock, total_msg_size):
    """
    ソケットからの特定のバイト数を読み込む関数
    """
    # これまで受信できたバイト数
    total_recv_size = 0
    while total_recv_size < total_msg_size:
        # ソケットから指定したバイト列を読みこむ
        received_chunk = sock.recv(total_msg_size - total_recv_size)
        # 1バイトも読めなかったときは接続が終了している
        if len(received_chunk) == 0:
            raise RuntimeError('socket connection broken')
        # 受信したバイト数を返す
        yield received_chunk
        # インクリメント
        total_recv_size += len(received_chunk)
        
def main():
    # IPv4 / TCPで通信するソケットを用意する
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # クライアントから接続を待ち受けるIPアドレスとポートを指定
    client_socket.connect(('127.0.0.1', 54321))
    
    # 送信する値を用意
    operand1, operand2 = 1000, 2000
    print(f'operand1: {operand1}, operand2: {operand2}')
    
    # ネットワークバイトオーダーのバイト列に変換する
    request_msg = struct.pack('!ii', operand1, operand2)
    # ソケットにバイト列を書き込み
    send_msg(client_socket, request_msg)
    print(f'sent: {request_msg}')
    
    # ソケットからバイト列を読み込む
    recieved_msg = b''.join(recv_msg(client_socket, total_msg_size=8))
    print(f'received: {recieved_msg}')
    
    # 64ビットの整数として解釈する
    (added_value, ) = struct.unpack('!q', recieved_msg)
    print(f'result: {added_value}')
    
    # ソケットを閉じる
    client_socket.close()
    
if __name__ == '__main__':
    main()
    
    