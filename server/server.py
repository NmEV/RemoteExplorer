#格式：command:Username,Password,action,action_data
#例如：command:admin,123456,ls,/home
import socket,os,shutil,pickle
import configparser as cp

ini = cp.ConfigParser()
ini.read('setting.ini')
port = ini.getint('general','port')
user_list = ini.get('general','reg_user').split(',')
user = {}
plugins = {}
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

def load_plugins():
    plugin_name = ini.get('general', 'plugins').split(',')
    plugin_paths = []
    for i in plugin_name:
        try:
            plugin_paths.append(ini.get(i,'path'))
        except :
            pass
    print('Plugins load:')
    for i in plugin_name:
        try:
            print(f'\t{ini.get(i,"name")}: {ini.get(i,"path")}')
        except:
            pass
    for path in plugin_paths:
        try:
            with open(path, 'rb') as f:
                plugin = pickle.load(f)
                if isinstance(plugin, dict):
                    plugins.update(plugin)
                    print(f"插件 {path} 加载成功: {list(plugin.keys())}")
                else:
                    print(f"插件 {path} 格式错误，必须是字典")
        except FileNotFoundError:
            print(f"插件文件 {path} 未找到")
        except Exception as e:
            print(f"加载插件 {path} 时出错: {e}")
def send_huge_data(data,client_socket):
    try:
        for i in range(0, len(data), 4096):
            client_socket.sendall(data[i:i+4096])
    except ConnectionAbortedError as e:
        print(f"Connection aborted: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
def execute_plugin_command(action, username, password, action_data, client_socket,cm):
    """执行插件命令"""
    if action in plugins:
        if User(username, password, '').authentication() and cm == 'rw':
            try:
                response = plugins[action](action_data)
                client_socket.send(f"message:{response}".encode('utf-8'))
            except Exception as e:
                client_socket.send(f"000warn:插件执行失败: {e}".encode('utf-8'))
        elif cm != 'rw':
            client_socket.send("000warn:无权限\n插件命令必须拥有全部权限".encode('utf-8'))
        else:
            client_socket.send("Authentication failed".encode('utf-8'))
        return True
    return False
def start_server():
    load_plugins()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)
    print("Server is listening on port {}...".format(port))
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established!")
    
        data = b""
        while True:
            packet = client_socket.recv(1024)
            if not packet:
                break
            data += packet

        data = data.decode('utf-8')
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
                elif execute_plugin_command(action, username, password, action_data, client_socket,cm):
                    continue
                
                elif action == 'ls':
                    if User(username,password,'').authentication() and 'r' in cm:
                        if action_data == '':
                            action_data = '.'
                        try:
                            file_list = os.listdir(action_data)
                            for i in range(len(file_list)):
                                if os.path.isdir(action_data+'/'+file_list[i]):
                                    file_list[i] = 'DIR:'+file_list[i]
                                else:
                                    file_list[i] = 'FILE:'+file_list[i]
                            client_socket.send(str(file_list).encode('utf-8'))
                        except FileNotFoundError:
                            client_socket.send("000warn:File not found".encode('utf-8'))
                    elif 'r' not in cm:
                        client_socket.send("000warn:无权限".encode('utf-8'))
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                
                elif action == 'del':
                    if User(username,password,'').authentication() and 'w' in cm:
                        try:
                            os.remove(action_data)
                            client_socket.send("messgae:File deleted".encode('utf-8'))
                        except FileNotFoundError:
                            client_socket.send("000warn:File not found".encode('utf-8'))
                    elif 'w' not in cm:
                        client_socket.send("000warn:无权限".encode('utf-8'))
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                
                elif action == 'mkdir':
                    if User(username,password,'').authentication() and 'w' in cm:
                        try:
                            os.mkdir(action_data)
                            client_socket.send("messgae:Directory created".encode('utf-8'))
                        except FileExistsError:
                            client_socket.send("000warn:Directory already exists".encode('utf-8'))
                    elif 'w' not in cm:
                        client_socket.send("000warn:无权限".encode('utf-8'))
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                
                elif action == 'cp':
                    if User(username,password,'').authentication() and 'w' in cm:
                        try:
                            with open(action_data.split(';')[0],'rb') as f:
                                data = f.read()
                            with open(action_data.split(';')[1],'wb') as f:
                                f.write(data)
                            client_socket.send("messgae:File copied".encode('utf-8'))
                        except FileNotFoundError:
                            client_socket.send("000warn:File not found".encode('utf-8'))
                    elif 'w' not in cm:
                        client_socket.send("000warn:无权限".encode('utf-8'))
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                
                elif action == 'rename':
                    if User(username,password,'').authentication() and 'w' in cm:
                        try:
                            os.rename(action_data.split(';')[0],action_data.split(';')[1])
                            client_socket.send("messgae:File renamed".encode('utf-8'))
                        except FileNotFoundError:
                            client_socket.send("000warn:File not found".encode('utf-8'))
                    elif 'w' not in cm:
                        client_socket.send("000warn:无权限".encode('utf-8'))
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                
                elif action == 'upload': #传输给客户端
                    if User(username,password,'').authentication() and 'r' in cm:
                        try:
                            with open(action_data,'rb') as f:
                                data = f.read()
                            send_huge_data(data,client_socket)
                        except FileNotFoundError:
                            client_socket.send("000warn:File not found".encode('utf-8'))
                    elif 'r' not in cm:
                        client_socket.send("000warn:无权限".encode('utf-8'))
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                    pass
                
                elif action == 'download': #从客户端接收
                    if User(username,password,'').authentication() and 'w' in cm:
                        file = action_data.split('::')[0]
                        print(file)
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
                    elif 'w' not in cm:
                        client_socket.send("000warn:无权限".encode('utf-8'))
                    else:
                        client_socket.send("Authentication failed".encode('utf-8'))
                    pass
                
                elif action == 'cpdir': #复制文件夹
                    if User(username,password,'').authentication() and 'w' in cm:
                        try:
                            shutil.copytree(action_data.split(';')[0],action_data.split(';')[1])
                            client_socket.send("message:Directory copied".encode('utf-8'))
                        except FileNotFoundError:
                            client_socket.send("message:Directory not found".encode('utf-8'))
                    elif 'w' not in cm:
                        client_socket.send("000warn:无权限".encode('utf-8'))
                    else:
                        client_socket.send("message:Authentication failed".encode('utf-8'))
                    pass
                
                elif action == 'deldir': #删除文件夹

                    if User(username,password,'').authentication() and 'w' in cm:
                        try:
                            shutil.rmtree(action_data)
                            client_socket.send("message:Directory deleted".encode('utf-8'))
                        except FileNotFoundError:
                            client_socket.send("message:Directory not found".encode('utf-8'))
                    elif 'w' not in cm:
                        client_socket.send("000warn:无权限".encode('utf-8'))
                    else:
                        client_socket.send("message:Authentication failed".encode('utf-8'))
                    pass
                
                
        except Exception as e:
            print('00error:Error')
            print(e)
            client_socket.send(f'message:Error{e}'.encode('utf-8'))
        else:
            client_socket.close()

if __name__ == '__main__':
    start_server()