#格式：command:Username,Password,action,action_data
#例如：command:admin,123456,ls,/home
import socket,os,shutil
import configparser as cp

ini = cp.ConfigParser()
ini.read('setting.ini')
port = ini.getint('general','port')
user_list = ini.get('general','reg_user').split(',')
user = {}
for i in user_list:
    user[i] = {'username':ini.get(i,'username'),'password':ini.get(i,'password'),'chmod':ini.get(i,'chmod')}

class User:
    def __init__(self,username,password,chmod):
        self.username = username
        self.password = password
        self.chmod = chmod
    
    def authentication(self):
        if self.username in user:
            if user[self.username]['password'] == self.password:
                return True
            else:
                return False
        else:
            return False
        
def send_huge_data(data,client_socket):
    try:
        for i in range(0, len(data), 4096):
            client_socket.sendall(data[i:i+4096])
    except ConnectionAbortedError as e:
        print(f"Connection aborted: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # client_socket.shutdown(socket.SHUT_WR)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)
    print("Server is listening on port {}...".format(port))

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established!")
        
        # data = client_socket.recv(8192).decode('utf-8')
        data = b""
        while True:
            packet = client_socket.recv(1024)
            if not packet:
                break
            data += packet

        data = data.decode('utf-8')
        # print(f"Received data: {data}")
        print(f"Received data: {data}")
        try:

            if data[:8] == 'command:':
                data = data[8:]
                data = data.split(',')
                username = data[0]
                password = data[1]
                action = data[2]
                action_data = data[3]
                print(f"username: {username}, password: {password}, action: {action}, action_data: {action_data}")
                if action == 'confirm':
                    if User(username,password,'').authentication():
                        cm = user[username]['chmod']
                        client_socket.send(f"Authentication success:{cm}".encode('utf-8'))
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                
                if action == 'ls':
                    if User(username,password,'').authentication() and 'r' in cm:
                        if action_data == '':
                            action_data = '.'
                        try:
                            file_list = os.listdir(action_data)
                            #如果是文件夹，加上'DIR:',如果是文件，加上'FILE:'
                            for i in range(len(file_list)):
                                if os.path.isdir(action_data+'/'+file_list[i]):
                                    file_list[i] = 'DIR:'+file_list[i]
                                else:
                                    file_list[i] = 'FILE:'+file_list[i]
                            client_socket.send(str(file_list).encode('utf-8'))
                        except FileNotFoundError:
                            client_socket.send("000warn:File not found".encode('utf-8'))
                    
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                elif 'w' not in cm:
                    client_socket.send("000warn:无权限".encode('utf-8'))
                if action == 'del':
                    if User(username,password,'').authentication() and 'w' in cm:
                        try:
                            os.remove(action_data)
                            client_socket.send("messgae:File deleted".encode('utf-8'))
                        except FileNotFoundError:
                            client_socket.send("000warn:File not found".encode('utf-8'))
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                elif 'w' not in cm:
                    client_socket.send("000warn:无权限".encode('utf-8'))
                if action == 'mkdir' and 'w' in cm:
                    if User(username,password,'').authentication():
                        try:
                            os.mkdir(action_data)
                            client_socket.send("messgae:Directory created".encode('utf-8'))
                        except FileExistsError:
                            client_socket.send("000warn:Directory already exists".encode('utf-8'))
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                elif 'w' not in cm:
                    client_socket.send("000warn:无权限".encode('utf-8'))
                if action == 'cp' and 'w' in cm:
                    if User(username,password,'').authentication():
                        try:
                            with open(action_data.split(';')[0],'rb') as f:
                                data = f.read()
                            with open(action_data.split(';')[1],'wb') as f:
                                f.write(data)
                            client_socket.send("messgae:File copied".encode('utf-8'))
                        except FileNotFoundError:
                            client_socket.send("000warn:File not found".encode('utf-8'))
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                elif 'w' not in cm:
                    client_socket.send("000warn:无权限".encode('utf-8'))
                if action == 'rename' and 'w' in cm:
                    if User(username,password,'').authentication():
                        try:
                            os.rename(action_data.split(';')[0],action_data.split(';')[1])
                            client_socket.send("messgae:File renamed".encode('utf-8'))
                        except FileNotFoundError:
                            client_socket.send("000warn:File not found".encode('utf-8'))
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                elif 'w' not in cm:
                    client_socket.send("000warn:无权限".encode('utf-8'))
                if action == 'upload' and 'r' in cm: #传输给客户端
                    if User(username,password,'').authentication():
                        try:
                            with open(action_data,'rb') as f:
                                data = f.read()
                            send_huge_data(data,client_socket)
                        except FileNotFoundError:
                            client_socket.send("000warn:File not found".encode('utf-8'))
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                    pass
                elif 'r' not in cm:
                    client_socket.send("000warn:无权限".encode('utf-8'))
                if action == 'download' and 'w' in cm: #从客户端接收
                    file = action_data.split('::')[0]
                    print(file)
                    if User(username,password,'').authentication():
                        try:
                            with open(file,'wb') as f:
                                while True:
                                    packet = client_socket.recv(1024)
                                    if not packet:
                                        break
                                    f.write(packet)
                                f.close()
                            client_socket.send("message:File uploaded".encode('utf-8'))
                        except FileNotFoundError as e:
                            client_socket.send("000warn:File not found".encode('utf-8'))
                            print(e)
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                    pass
                elif 'w' not in cm:
                    client_socket.send("000warn:无权限".encode('utf-8'))
                if action == 'cpdir' and 'w' in cm: #复制文件夹
                    if User(username,password,'').authentication():
                        try:
                            shutil.copytree(action_data.split(';')[0],action_data.split(';')[1])
                            client_socket.send("message:Directory copied".encode('utf-8'))
                        except FileNotFoundError:
                            client_socket.send("message:Directory not found".encode('utf-8'))
                    else:
                        client_socket.send("message:Authentication failed".encode('utf-8'))
                    pass
                elif 'w' not in cm:
                    client_socket.send("000warn:无权限".encode('utf-8'))
                if action == 'deldir' and 'w' in cm: #删除文件夹

                    if User(username,password,'').authentication():
                        try:
                            shutil.rmtree(action_data)
                            client_socket.send("message:Directory deleted".encode('utf-8'))
                        except FileNotFoundError:
                            client_socket.send("message:Directory not found".encode('utf-8'))
                    else:
                        client_socket.send("message:Authentication failed".encode('utf-8'))
                    pass
                elif 'w' not in cm:
                    client_socket.send("000warn:无权限".encode('utf-8'))
                
        except Exception as e:
            print('00error:Error')
            print(e)
            client_socket.send(f'message:Error{e}'.encode('utf-8'))
        else:
            # client_socket.send("Data received".encode('utf-8'))
            client_socket.close()

if __name__ == '__main__':
    start_server()