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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # クライアントから接続を待ち受けるIPアドレスとポートを指定
    server_socket.bind(('127.0.0.1', 54321))
    # 接続の待ち受けを開始
    server_socket.listen()
    print('starting server...')
    # 接続を処理する
    client_socket, (client_address, client_port) = server_socket.accept()
    # 接続したクライアントの情報を表示する
    print(f'accepted from {client_address}:{client_port}')
    # バイト列を受信する
    recieved_msg = b''.join(recv_msg(client_socket, total_msg_size=8))
    # 受信したバイト列を表示する
    print(f'received: {recieved_msg}')
    # バイト列をふたつの32ビットの整数として解釈
    (operand1, operand2) = struct.unpack('!ii', recieved_msg)
    print(f'operand1: {operand1}, operand2: {operand2}')
    
    # 計算する
    result = operand1 + operand2
    print(f'result: {result}')
    
    # 計算した値を64ビットの整数としてネットワークバイトオーダーのバイト列に変換する
    result_msg = struct.pack('!q', result)
    # ソケットにバイト列を書き込み
    send_msg(client_socket, result_msg)
    print(f'sent: {result_msg}')
    
    # ソケットの接続を終了
    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    main()
