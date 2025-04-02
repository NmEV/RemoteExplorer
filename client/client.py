import socket,os
import pickle as pk
def send_data(data, addr, file=False):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((addr,int(ui.port.text())))

    data = data.encode('utf-8')

    try:
        for i in range(0, len(data), 4096):
            client_socket.sendall(data[i:i+4096])

        client_socket.shutdown(socket.SHUT_WR)  # 发送完数据后关闭写端

        if not file:
            response = client_socket.recv(1024).decode('utf-8')
        else:
            response = b""
            while True:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                response += packet

        print(f"Response from server: {response}\n")
        if response[:8] == 'message:':
            ui.show_info(response[8:])
        elif response[:8] == '000warn:':
            ui.show_warn(response[8:])
        elif response[:8] == '00error:':
            ui.show_error(response[8:])
        else:
            client_socket.close()
            return response
    except ConnectionAbortedError as e:
        print(f"Connection aborted: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(QtWidgets.QWidget):
    def show_warn(self,message):
        QtWidgets.QMessageBox.warning(self.centralwidget, '错误', message)
    
    def show_info(self,message):
        # QtWidgets.QMessageBox.warning(self.centralwidget, '错误', message)
        QtWidgets.QMessageBox.information(self.centralwidget,'消息',message)
        
    def show_error(self,message):
        
        QtWidgets.QMessageBox.critical(self.centralwidget,'警告',message)

    def setupUi(self, MainWindow):
        self.now_check = ''
        self.cp_list_index = 0
        self.copyls=QtCore.QStringListModel()
        self.quickls=QtCore.QStringListModel()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 508)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.connect = QtWidgets.QPushButton(parent=self.centralwidget)
        self.connect.setGeometry(QtCore.QRect(380, 40, 93, 28))
        self.connect.setObjectName("connect")
        self.connect.clicked.connect(self.confirm_connect)
        self.username = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.username.setGeometry(QtCore.QRect(70, 40, 113, 21))
        self.username.setObjectName("username")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 40, 72, 15))
        self.label_2.setObjectName("label_2")
        self.password = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.password.setGeometry(QtCore.QRect(250, 40, 113, 21))
        self.password.setText("")
        self.password.setObjectName("password")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 72, 15))
        self.label_3.setObjectName("label_3")
        self.copy = QtWidgets.QPushButton(parent=self.centralwidget)
        self.copy.setEnabled(False)
        self.copy.setGeometry(QtCore.QRect(260, 130, 93, 28))
        self.copy.setObjectName("copy")
        self.copy.clicked.connect(self.cp)
        self.paste = QtWidgets.QPushButton(parent=self.centralwidget)
        self.paste.setEnabled(False)
        self.paste.setGeometry(QtCore.QRect(260, 170, 93, 28))
        self.paste.setObjectName("paste")
        self.paste.clicked.connect(self.pas)
        self.cut = QtWidgets.QPushButton(parent=self.centralwidget)
        self.cut.setEnabled(False)
        self.cut.setGeometry(QtCore.QRect(260, 210, 93, 28))
        self.cut.setObjectName("cut")
        self.cut.clicked.connect(self.ct)
        self.dele = QtWidgets.QPushButton(parent=self.centralwidget)
        self.dele.setEnabled(False)
        self.dele.setGeometry(QtCore.QRect(260, 250, 93, 28))
        self.dele.setObjectName("dele")
        self.dele.clicked.connect(self.delete)
        self.copylist = QtWidgets.QListView(parent=self.centralwidget)
        self.copylist.setEnabled(False)
        self.copylist.setGeometry(QtCore.QRect(380, 130, 241, 131))
        self.copylist.setObjectName("copylist")
        self.copylist.setModel(self.copyls)
        self.copylist.clicked.connect(self.update_cp_list_index)
        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(380, 110, 101, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 70, 72, 15))
        self.label_5.setObjectName("label_5")
        self.address = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.address.setEnabled(False)
        self.address.setGeometry(QtCore.QRect(90, 70, 271, 21))
        self.address.setObjectName("address")
        self.go = QtWidgets.QPushButton(parent=self.centralwidget)
        self.go.setEnabled(False)
        self.go.setGeometry(QtCore.QRect(380, 70, 93, 28))
        self.go.setObjectName("go")
        self.go.clicked.connect(self.ls)
        self.rename = QtWidgets.QPushButton(parent=self.centralwidget)
        self.rename.setEnabled(False)
        self.rename.setGeometry(QtCore.QRect(260, 290, 93, 28))
        self.rename.setObjectName("rename")
        self.dir = QtWidgets.QListView(parent=self.centralwidget)
        self.dir.setEnabled(False)
        self.dir.setGeometry(QtCore.QRect(20, 130, 221, 361))
        self.dir.setObjectName("dir")
        self.dir.clicked.connect(self.update_now_check)
        self.dir.doubleClicked.connect(self.enter_dir)
        self.label_6 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 10, 81, 16))
        self.label_6.setObjectName("label_6")
        self.server_addr = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.server_addr.setGeometry(QtCore.QRect(110, 10, 211, 21))
        self.server_addr.setObjectName("server_addr")
        self.label_7 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(330, 10, 81, 16))
        self.label_7.setObjectName("label_7")
        self.port = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.port.setGeometry(QtCore.QRect(370, 10, 61, 21))
        self.port.setText("")
        self.port.setObjectName("port")
        self.upload = QtWidgets.QPushButton(parent=self.centralwidget)
        self.upload.setEnabled(False)
        self.upload.setGeometry(QtCore.QRect(260, 330, 93, 28))
        self.upload.setObjectName("upload")
        self.upload.clicked.connect(self.upl)
        self.rename.clicked.connect(self.rename_)
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.dir.setGridSize(QtCore.QSize(60,20))
        self.label_8 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(380, 280, 101, 16))
        self.label_8.setObjectName("label_8")
        self.quick_list = QtWidgets.QListView(parent=self.centralwidget)
        self.quick_list.setEnabled(False)
        self.quick_list.setGeometry(QtCore.QRect(380, 300, 241, 131))
        self.quick_list.setObjectName("quick_list")
        self.add_quick_list = QtWidgets.QPushButton(parent=self.centralwidget)
        self.add_quick_list.setEnabled(False)
        self.add_quick_list.setGeometry(QtCore.QRect(380, 440, 131, 28))
        self.add_quick_list.setObjectName("add_quick_list")
        self.add_quick_list.clicked.connect(self.add_quick)
        self.rm_quick_list = QtWidgets.QPushButton(parent=self.centralwidget)
        self.rm_quick_list.setEnabled(False)
        self.rm_quick_list.setGeometry(QtCore.QRect(380, 470, 131, 28))
        self.rm_quick_list.setObjectName("rm_quick_list")
        self.quick_list.clicked.connect(self.update_quick_check_index)
        self.quick_list.doubleClicked.connect(self.goto_quick)
        self.quick_list.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        MainWindow.setCentralWidget(self.centralwidget)
        self.rm_quick_list.clicked.connect(self.rm_quick)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.listModel=QtCore.QStringListModel()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RemoteExplorerClient"))
        self.quick_select_index = 0
        self.connect.setText(_translate("MainWindow", "连接"))
        self.label.setText(_translate("MainWindow", "用户名"))
        self.label_2.setText(_translate("MainWindow", "操作码"))
        self.label_3.setText(_translate("MainWindow", "文件夹"))
        self.copy.setText(_translate("MainWindow", "复制"))
        self.paste.setText(_translate("MainWindow", "黏贴"))
        self.cut.setText(_translate("MainWindow", "剪切"))
        self.dele.setText(_translate("MainWindow", "删除"))
        self.label_4.setText(_translate("MainWindow", "剪贴板历史"))
        self.label_5.setText(_translate("MainWindow", "当前目录"))
        self.go.setText(_translate("MainWindow", "快速跳转"))
        self.rename.setText(_translate("MainWindow", "重命名"))
        self.label_6.setText(_translate("MainWindow", "服务器地址"))
        self.server_addr.setText(_translate("MainWindow", "127.0.0.1"))
        self.password.setText("123456")
        self.username.setText("Admin")
        self.port.setText('5000')
        self.label_7.setText(_translate("MainWindow", "端口"))
        self.upload.setText(_translate("MainWindow", "上传"))
        self.label_8.setText(_translate("MainWindow", "快捷访问"))
        self.add_quick_list.setText(_translate("MainWindow", "固定到快捷访问"))
        self.rm_quick_list.setText(_translate("MainWindow", "从快捷访问移除"))
        self.read_pickle()
        self.quick_list.setModel(self.quickls)
        
    
    def update_now_check(self):
        self.now_check = self.dir.currentIndex().data()

    def enter_dir(self):
        if self.now_check[-1] == '/':
            self.address.setText(self.address.text() + self.now_check.split(':')[-1])
            if self.now_check.split(':')[0] == 'FILE':
                self.download()
            else:
                self.ls()
        else:
            self.address.setText(self.address.text() + self.now_check.split(':')[-1] + '/')
            if self.now_check.split(':')[0] == 'FILE':
                self.download()
            else:
                self.ls()

    def confirm_connect(self):
        try:
            data = f"command:{self.username.text()},{self.password.text()},confirm,"
            res = send_data(data,self.server_addr.text())
            print(res)
            if 'Authentication success' in res:
                self.copy.setEnabled(True)
                self.upload.setEnabled(True)
                self.dele.setEnabled(True)
                self.copylist.setEnabled(True)
                self.address.setEnabled(True)
                self.go.setEnabled(True)
                self.rename.setEnabled(True)
                self.dir.setEnabled(True)
                self.server_addr.setEnabled(False)
                self.username.setEnabled(False)
                self.password.setEnabled(False)
                self.connect.setEnabled(False)
                self.address.setText('C:/')
                self.port.setEnabled(False)
                self.add_quick_list.setEnabled(True)
                self.rm_quick_list.setEnabled(True)
                self.quick_list.setEnabled(True)
                self.quick_list.setModel(self.quickls)
                self.ls()
                if 'w' not in res.split(':')[-1]:
                    self.dele.setEnabled(False)
                    self.copy.setEnabled(0)
                    self.upload.setEnabled(0)
                    self.rename.setEnabled(0)

            else:
                QtWidgets.QMessageBox.warning(self.centralwidget, '错误', '用户名或密码错误')
        except:
            QtWidgets.QMessageBox.warning(self.centralwidget, '错误', '连接失败')
    
    def ls(self):
        try:
            
            data = f"command:{self.username.text()},{self.password.text()},ls,{self.address.text()}"
            di = send_data(data,self.server_addr.text())[1:-1].split(',')
            for i in range(len(di)):
                di[i] = di[i][1:].strip("'")
            di = ['/..'] + di
            self.listModel.setStringList(di)
            self.listModel.sort(0)
            self.dir.setModel(self.listModel)
            self.dir.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
            if self.address.text()[-4:] == '/../':
                self.address.setText('/'.join(self.address.text()[:-4].split('/')[:-2])+'/')
                print('/'.join(self.address.text()[:-4].split('/')[:-2])+'/')
        except:
            QtWidgets.QMessageBox.warning(self.centralwidget, '错误', '连接失败')
            self.address.setText('/'.join(self.address.text()[:-4].split('/')[:-1])+'/')
    
    def download(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self.centralwidget, 'Save File', '', 'All Files (*)')
        if path:
            with open(path, 'wb') as f:
                f.write(send_data(f"command:{self.username.text()},{self.password.text()},upload,{self.address.text().strip('/')}",self.server_addr.text(),file=True))
                self.address.setText('/'.join(self.address.text()[:-4].split('/')[:-1])+'/')
        else:
            self.address.setText('/'.join(self.address.text()[:-4].split('/')[:-1])+'/')
    
    def cp(self):
        self.copyls.setStringList([self.now_check.split(':')[0] + ':'+self.address.text() + self.now_check.split(':')[-1]]+self.copyls.stringList())
        self.paste.setEnabled(True)
        self.cut.setEnabled(True) 
    def pas(self): #黏贴
        ori = self.copyls.stringList()[self.cp_list_index]
        filename = ori.split('/')[-1]
        type_ = ori.split(':')[0]
        aim = self.address.text() + filename
        if type_ == 'FILE':
            send_data(f"command:{self.username.text()},{self.password.text()},cp,{ori.strip('FILE:/').strip('DIR:/')};{aim}",self.server_addr.text())
        elif type_ == 'DIR':
            send_data(f"command:{self.username.text()},{self.password.text()},cpdir,{ori.strip('FILE:/').strip('DIR:/')};{aim}",self.server_addr.text())
        self.ls()
    def ct(self): #剪切
        ori = self.copyls.stringList()[self.cp_list_index]
        filename = ori.split('/')[-1]
        aim = self.address.text() + filename
        send_data(f"command:{self.username.text()},{self.password.text()},cp,{ori.strip('FILE:/').strip('DIR:/')};{aim}",self.server_addr.text())
        send_data(f"command:{self.username.text()},{self.password.text()},del,{ori.strip('FILE:/').strip('DIR:/')}",self.server_addr.text())
        pass
    def delete(self): #删除
        ori = self.now_check.split(':')[0]+':'+self.address.text() + '/' + self.now_check.split(':')[-1]
        # print(ori)
        filename = ori.split('/')[-1]
        type_ = ori.split(':')[0]
        aim = self.address.text() + filename
        if type_ == 'FILE':
            send_data(f"command:{self.username.text()},{self.password.text()},del,{self.address.text().strip('/') + '/'+self.now_check.split(':')[-1]}",self.server_addr.text())
        elif type_ == 'DIR':
            send_data(f"command:{self.username.text()},{self.password.text()},deldir,{ori.strip('FILE:/').strip('DIR:/')}",self.server_addr.text())
        self.ls()
    def update_cp_list_index(self):
        self.cp_list_index = self.copylist.currentIndex().row()
    
    def upl(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, 'Open File', '', 'All Files (*)')
        if path:
            try:
                with open(path, 'rb') as f:
                    data = f.read()
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((self.server_addr.text(), int(self.port.text())))
                command = f"command:{self.username.text()},{self.password.text()},download,{self.address.text().strip('/') + '/' + os.path.basename(path) + '::'}"
                client_socket.sendall(command.encode('utf-8'))
                client_socket.sendall(data)
                client_socket.shutdown(socket.SHUT_WR)
                response = client_socket.recv(1024).decode('utf-8')
                client_socket.close()
                if 'message:File uploaded' in response:
                    self.show_info('文件上传成功')
                else:
                    self.show_warn('文件上传失败')
            except Exception as e:
                self.show_error(f'上传文件时出错: {e}')
        else:
            self.show_warn('未选择文件')
        self.ls()
    def rename_ (self):
        text,_ = QtWidgets.QInputDialog.getText(self.centralwidget,'重命名','请输入新的文件名')
        if text:
            try:
                send_data(f"command:{self.username.text()},{self.password.text()},rename,{self.address.text().strip('/') + '/' + self.now_check.split(':')[-1]};{self.address.text().strip('/') + '/'+text}",self.server_addr.text())
            except Exception as e:
                self.show_error(f'修改文件名文件时出错: {e}')
            self.ls()
        else:
            self.show_warn('未输入文件名')
    
    def add_quick(self):
        self.quickls.setStringList([self.address.text()]+self.quickls.stringList())
        self.save_pickle()
    def update_quick_check_index (self):
        self.quick_select_index = self.quick_list.currentIndex().data()
        pass
    def rm_quick(self):
        self.quickls.setStringList([x for x in self.quickls.stringList() if x != self.quick_select_index])
        self.save_pickle()
        pass
    def goto_quick(self):
        self.address.setText(self.quick_select_index)
        self.ls()
    def save_pickle (self):
        try :
            for i in range(len(self.quickls.stringList())):
                self.quickls.setStringList([x for x in self.quickls.stringList() if x != ''])
            with open('quick.pkl','wb') as f:
                pk.dump(self.quickls.stringList(),f)
        except:
            pass
    def read_pickle (self):
        try:
            with open('quick.pkl','rb') as f:
                self.quickls.setStringList(pk.load(f))
        except:
            pass
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
