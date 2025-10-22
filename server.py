import socket
import threading
import json

# 設置伺服器地址和端口
server_address = ('0.0.0.0', 8080)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_address)
server.listen(2)

clients = []  # 存儲客戶端連接
players_statement = [{'x': 40, 'y': 40, 'dir': 'down', 'frame': 1, 'bomb': False, 'start':False}, 
                     {'x': 600, 'y': 520, 'dir': 'down', 'frame': 1, 'bomb': False, 'start':False}]  # 初始化玩家位置和動作
lock = threading.Lock()

def handle_client(client_socket, player_id):
    global players_statement
    buffer = ""
    client_socket.send((json.dumps({'player_id': player_id}) + '\n').encode('utf-8'))  # 發送玩家ID給客戶端
    while True:
        try:
            # 接收數據
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print(f"玩家 {player_id} 斷開連接")
                break

            buffer += data
            while '\n' in buffer:
                message, buffer = buffer.split('\n', 1)
                try:
                    received_data = json.loads(message)
                    with lock:
                        if all(k in received_data for k in ('x', 'y', 'dir', 'frame', 'bomb', 'start')):
                            if received_data['dir'] is None:
                                players_statement[player_id]['x'] = received_data['x']
                                players_statement[player_id]['y'] = received_data['y']
                                players_statement[player_id]['frame'] = received_data['frame']
                                players_statement[player_id]['bomb'] = received_data['bomb']
                                players_statement[player_id]['start'] = received_data['start']
                            else:
                                players_statement[player_id]['x'] = received_data['x']
                                players_statement[player_id]['y'] = received_data['y']
                                players_statement[player_id]['dir'] = received_data['dir']
                                players_statement[player_id]['frame'] = received_data['frame']
                                players_statement[player_id]['bomb'] = received_data['bomb']
                                players_statement[player_id]['start'] = received_data['start']
                        else:
                            print(f"玩家 {player_id} 發送了不完整的數據: {received_data}")
                except json.JSONDecodeError:
                    print("Failed to decode JSON")

                # 發送更新後的玩家位置
                response = json.dumps(players_statement) + '\n'
                with lock:
                    for c in clients:
                        if c == client_socket:
                            if players_statement[0]['start'] and players_statement[1]['start']:
                                c.send(response.encode('utf-8'))
                        else:
                            c.send(response.encode('utf-8'))
        except json.JSONDecodeError as e:
            print(f"JSON 解碼錯誤: {e}")
            break
        except ConnectionResetError:
            if player_id == 0:
                players_statement[0]['start'] = False
            else:
                players_statement[1]['start'] = False
            print(f"玩家 {player_id} 斷開連接（連接重置）")
            break
        except Exception as e:
            print(f"處理客戶端 {player_id} 時出錯: {e}")
            break

    with lock:
        clients.remove(client_socket)
    client_socket.close()

def start_server():
    print("伺服器啟動...")
    while True:
        client_socket, addr = server.accept()
        if None in clients:
                player_id = clients.index(None)
                clients[player_id] = client_socket
                threading.Thread(target=handle_client, args=(client_socket, player_id)).start()
        elif len(clients) < 2:
            clients.append(client_socket)
            player_id = len(clients) - 1
            threading.Thread(target=handle_client, args=(client_socket, player_id)).start()
        else:
            print("伺服器已滿，拒絕連接")
            client_socket.close()

start_server()
