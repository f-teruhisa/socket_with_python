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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ループバックアドレスのTCP/80ポートに接続
    client_socket.connect(('127.0.0.1', 80))
    # HTTPサーバからドキュメントを取得するGETリクエスト
    request_text = 'GET / HTTP/1.0\r\n\r\n'
    # 文字列をエンコード
    request_bytes = request_text.encode('ASCII')
    # ソケットにリクエストのバイト列を書き込む
    send_msg(client_socket, request_bytes)
    # ソケットからレスポンスのバイト列を読み込む
    recieved_bytes = b''.join(recv_msg(client_socket))
    # 読み込んだバイト列を文字列にデコード
    recieved_text = recieved_bytes.decode('ASCII')
    # 文字列を表示
    print(recieved_text)
    # 使い終わったソケットを閉じる
    client_socket.close()
    

if __name__ == '__main__':
    main()
