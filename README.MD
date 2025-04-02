# RemoteExplorer 远程文件管理器

Powered by NmEV

[TOC]

## ·Simplified-Chinese 简体中文

### ·介绍

用于Windows Server，Linux等纯命令行环境下，使用更小体积的工具更方便完成文件迁移等操作

### ·Client客户端

Client客户端的窗口界面依赖于PyQt6，直接运行Release中`client.exe`或Source code的`client.py`即可运行

### ·Server服务端

#### ·服务端配置文件

Server服务器端的配置文件读取基于官方库`configparser`，所以无法在同一行使用注释，具体讲解如下：

```ini
[general]
port = 5000
#服务端口
max_connections = 100
#最大连接数，当前版本没有作用
reg_user = Admin,User1,User2
#注册用户
plugins = 
#注册插件，插件部分下文详讲

[Admin]
#设置用户详细信息，括号中内容需与reg_user内的相同，区分大小写
username = Admin
#用户名
password = 123456
#密码
chmod = rw
#权限，rw:允许读写

[User1]
username = User1
password = 123456
chmod = r
#r:仅允许读

[User2]
username = User2
password = 123456
chmod = w
#w:仅允许写
```

#### ·服务端插件开发

Server服务器端已经支持插件开发，Release与Source code中已经附带了示例插件。RemoteExplorer Server的插件支持新增或重写已有的指令，使用`pickle`封装，以下是详细的插件开发教程（使用Python 3.13.2）：

1. 在同一目录下新建文件`make.py`，`plg_def.py`

2. 在plg_def.py中写入插件主体内容，如：

   ```python
   #为防止误操作，保护关键目录下的文件不被删除
   def protect_del(action_data): #命令被执行时的动作
       import os
       protected_path = "C:/User"
       if action_data.startswith(protected_path):
           return f"禁止删除 {protected_path} 目录下的文件: {action_data}"
       try:
           os.remove(action_data)
           return f"文件已删除: {action_data}"
       except FileNotFoundError:
           return f"文件未找到: {action_data}"
       except Exception as e:
           return f"删除文件时出错: {e}"
   
   # 注册插件中的命令
   plugin = {
       "del": protect_del
   }
   ```

   

3. 在make.py中写入以下内容

   ```python
   import pickle
   from plg_def import plugin
   
   with open('protect.pkl', 'wb') as f:
       pickle.dump(plugin, f)
   ```

4. 运行`make.py`，在同目录下生成 `protect.pkl`

5. 修改服务器目录下`setting.ini`，导入插件

   ```ini
   [general]
   port = 5000
   max_connections = 100
   reg_user = Admin,User1,User2
   plugins = protect
   #注册插件
   
   [Admin]
   username = Admin
   password = 123456
   chmod = rw
   
   [User1]
   username = User1
   password = 123456
   chmod = r
   
   [User2]
   username = User2
   password = 123456
   chmod = w
   
   [protect]
   name = ProtectPlugin
   #插件名称
   path = ./protect.pkl
   #生成插件文件的相对路径或绝对路径
   author = Author1
   #作者，在当前版本暂时没有作用
   ```

   

6.运行服务端，检查控制台输出，应有

```shell
Plugins load:
        ProtectPlugin: ./protect.pkl
插件 ./protect.pkl 加载成功: ['del']
```



未来计划：

  1.为客户端添加插件功能，允许修改界面

  2.添加插件RSA签名验证功能

  3.启用服务端最大连接数限制



## ·English

### ·Introduction

A lightweight tool for file migration operations in pure command-line environments (Windows Server, Linux, etc.).

### ·Client

The Client GUI relies on `PyQt6`. Simply run `client.exe` from Release or `client.py` from Source code.

### ·Server

#### ·Server setting

Server-side configuration file parsing uses the official configparser library. Note: Comments cannot be used inline. Configuration details:

```ini
[general]
port = 5000
# Service port
max_connections = 100
# Maximum connections (not functional in current version)
reg_user = Admin,User1,User2
# Registered users
plugins = 
# Registered plugins (see plugin section below)

[Admin]
# User details (section name must match reg_user entries, case-sensitive)
username = Admin
# Username
password = 123456
# Password
chmod = rw
# Permissions: rw (read-write allowed)

[User1]
username = User1
password = 123456
chmod = r
# r: read-only

[User2]
username = User2
password = 123456
chmod = w
# w: write-only
```

#### ·Server Plugins Develop

Server-side supports plugin development. Example plugins are included in Release/Source code. Plugins can add/override commands using pickle serialization. Plugin development guide (Python 3.13.2):

1. Create make.py and `plg_def.py` in the same directory

2. Write plugin logic in `plg_def.py`:

   ```python
   # To prevent accidental operations, protect files in critical directories
   def protect_del(action_data): # Action when command executes
       import os
       protected_path = "C:/User"
       if action_data.startswith(protected_path):
           return f"禁止删除 {protected_path} 目录下的文件: {action_data}"
       try:
           os.remove(action_data)
           return f"文件已删除: {action_data}"
       except FileNotFoundError:
           return f"文件未找到: {action_data}"
       except Exception as e:
           return f"删除文件时出错: {e}"
   
   # Register commands
   plugin = {
       "del": protect_del
   }
   ```

3. Write in `make.py`:

   ```python
   import pickle
   from plg_def import plugin
   
   with open('protect.pkl', 'wb') as f:
       pickle.dump(plugin, f)
   ```

4. Run `make.py` to generate protect.pkl

5. Modify `setting.ini` to load plugin:

   ```ini
   [general]
   port = 5000
   max_connections = 100
   reg_user = Admin,User1,User2
   plugins = protect
   # Load plugins
   
   [Admin]
   username = Admin
   password = 123456
   chmod = rw
   
   [User1]
   username = User1
   password = 123456
   chmod = r
   
   [User2]
   username = User2
   password = 123456
   chmod = w
   
   [protect]
   name = ProtectPlugin
   # Plugin name
   path = ./protect.pkl
   # Relative/Absolute path to plugin
   author = Author1
   # Author (currently unused)
   ```

6. Start server. Console should show:

   ```shell
   Plugins load:
           ProtectPlugin: ./protect.pkl
   插件 ./protect.pkl 加载成功: ['del']
   ```


Future plans:

1. Add client-side plugin support for UI customization
2. Implement RSA signature verification for plugins
3. Enable server-side max connections limit