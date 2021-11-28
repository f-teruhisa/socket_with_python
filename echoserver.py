#!/usr/bin/env python3

import socket

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
        
def recv_msg(sock, chunk_len=1024):
    """
    ソケットから接続完了までバイト列を読み込む関数
    """
    while True:
        # ソケットから指定したバイト列を読みこむ
        received_chunk = sock.recv(chunk_len)
        # まったく読めなかったときは接続が終了している
        if len(received_chunk) == 0:
            break
        yield received_chunk

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
    # ソケットからバイト列を読み込む
    for received_msg in recv_msg(client_socket):
        # 読み込んだ内容をそのままソケットに書き込む = エコーバック
        send_msg(client_socket, received_msg)
        print(f'echo: {received_msg}')
    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    main()
    