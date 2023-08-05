import base64 as _base64
import hashlib as _hashlib
import json as _json
import os as _os
import string as _string
import subprocess as _subprocess
import threading as _threading
import time as _time
from Crypto.Cipher import AES as _AES
from Crypto.Util.Padding import pad as _pad, unpad as _unpad
import requests as _requests
import platform as _platform


class lab:
    def __init__(self, lab_server_address: str, port: int, key: str):
        """初始化

        Args:
            lab_server_address (str): CMS服务器地址
            port (int): 端口
            key (str): 密钥
        """
        self.lab_server_address = lab_server_address
        self.lab_server_port = port
        self.lab_server = f'{self.lab_server_address}:{port}'
        self.key = key
        # 密钥管理
        self.keys=self._keys()
        self.keys._request=self.request

    def encrypt_data(self,data: str, key: str):
        """加密函数

        Args:
            data (str): 待加密的数据
            key (str): 加密密钥

        Returns:
            str: base64格式的加密数据
        """
        try:
            key = key.encode()
            cryptor = _AES.new(key, _AES.MODE_ECB)
            text = cryptor.encrypt(_pad(data.encode('utf-8'), _AES.block_size))
            return _base64.b64encode(text).decode()
        except:
            return False


    def decrypt_data(self,data: str, key: str):
        """解密函数

        Args:
            data (str): 加密的数据
            key (str): 密钥

        Returns:
            str: 解密的数据
        """
        try:
            key = key.encode()
            data = _base64.b64decode(data)
            cryptor = _AES.new(key, _AES.MODE_ECB)
            text = cryptor.decrypt(data)
            text = _unpad(text, _AES.block_size).decode()
            return text
        except:
            return False
    
    def request(self, path: str, data: tuple={}):
        """向CMS发送数据

        Args:
            path (str): _description_
            data (tuple): _description_

        Returns:
            _type_: _description_
        """
        data = {
            "key_md5": _hashlib.md5(self.key.encode(encoding='utf-8')).hexdigest(),
            "timestamp": _time.time(),
            "data": data
        }
        data = self.encrypt_data(_json.dumps(data, ensure_ascii=False), self.key)
        if path[0] == '/':
            path = path[1:]
        try:
            res = _requests.post(f'{self.lab_server}/{path}',
                            json={'data': data},timeout=5).text
        except:
            raise Exception('failed to connect')
        try:
            res = _json.loads(self.decrypt_data(res, self.key))
        except:
            raise Exception('permission denied')
        if res and int(res['status_code']) == 1:
            return res['data']
        if res['status_code'] == 0:
            raise Exception(res['status'])

    def device(self, device_id):
        """连接到设备/初始化注册设备

        Args:
            device_id (str): 设备id

        Returns:
            object: 设备对象
        """
        d = self._device(device_id)
        d._lab_server = self.lab_server
        d._key = self.key
        d._request = self.request
        try:
            d._map()
        except:
            pass
        return d

    def status(self):
        """查询系统状态

        Returns:
            dict: 状态信息
        """
        return self.request('/status',{})
        
    def list_devices(self):
        """列出所有设备

        Returns:
            dict: 设备信息
        """
        return self.request('/device/list', {})
    
    def list_webdavs(self):
        """列出所有webdav

        Returns:
            dict: webdav信息
        """
        return self.request('/file/webdav/list', {})

    class _device:
        """
        设备类
        """
        def __init__(self, device_id: str):
            """初始化

            Args:
                device_id (str): 设备id
            """
            self._device_id = device_id
            self._mapped = False

        def _status(self):
            """查询设备状态

            Returns:
                dict: 设备状态信息
            """
            res = self._request('/device/status', {'id': self._device_id})
            if not res:
                return False
            return res['data']

        def _map(self):
            """
            映射设备函数
            """
            res = self._status()
            self._functions = res['functions']
            for function in self._functions:
                simple_name = function['name'].replace('.', '_')
                # 建立一个转发器
                exec(
                    f"self._transport_{simple_name}=self._transport(res['id'],function)")
                # 传递request
                exec(
                    f"self._transport_{simple_name}._request=self._request")
                # 传递action_status
                exec(
                    f"self._transport_{simple_name}._action_status=self._action_status")
                # 若存在".",递归建立class
                head = ''
                now = ''
                tail = function['name']
                while len(tail):
                    if tail[0] == '.' and len(tail) > 1:
                        if now not in dir(eval(f"self{head}")):
                            exec(f"class {now}:\n    pass")
                            exec(f"self{head}.{now}={now}")
                        head += f'.{now}'
                        now = ''
                        tail = tail[1:]
                    now += tail[0]
                    tail = tail[1:]
                # 固定转发器
                exec(
                    f"self.{function['name']}=self._transport_{simple_name}._transport")
            self._mapped = True

        def _action_status(self, action_id: str):
            """查询action状态

            Args:
                action_id (str): action id

            Returns:
                dict: action信息
            """
            res = self._request('/device/command/query', {"id": action_id})
            return res

        class _transport:
            """
            转发器,将对被映射函数的调用转为网络请求
            """

            def __init__(self, id: str, function: dict):
                self.id = id
                self.name = function['name']
                self.description = function['description']
                self.args = function['args']
                self.access = function['access']

            def _transport(self, **kwargs):
                """转发函数

                Raises:
                    Exception: 参数缺失

                Returns:
                    str: 返回action_id
                """
                args = []
                for arg in self.args:
                    if arg['required'] and arg['name'] not in kwargs:
                        raise Exception('missing parameter')
                    if arg['name'] in kwargs:
                        args.append(
                            {'name': arg['name'], 'value': kwargs[arg['name']]})
                data = {
                    'id': self.id,
                    'function': self.name,
                    'args': args
                }
                action_id = self._request('/device/command/submit', data)['id']
                if '_async' in kwargs and kwargs['_async']:
                    return action_id
                while True:
                    res = self._action_status(action_id)
                    if res['status'] in ['done', 'ok', 'finished']:
                        return True,res['return']
                    elif res['status'] in ['error']:
                        raise Exception(res['return'])

        def _register(self, description: str, functions: dict, default_access: int):
            """注册设备

            Args:
                description (str): 设备描述
                functions (dict): 设备支持函数
                default_access (int): 设备默认权限

            """
            # 默认权限
            for function in functions:
                if 'access' not in function:
                    function['access'] = default_access
            self._description = description
            self._functions = functions
            self._default_access = default_access
            self._data = {"id": self._device_id, "description": description,
                         "functions": functions, "default_access": default_access}
            self._request('/device/announce', self._data)
            # 注册设备后,提供bind
            self.bind = self._bind
            # 注册设备后,daemon持续检测
            self._daemon = _threading.Thread(target=self._monitor)
            self._daemon.daemon = True
            self._daemon.start()
            return True

        def _bind(self, mapping: dict):
            """绑定

            Args:
                mapping (dict): 外部名称与函数的对应关系
            """
            self._mapping = mapping

        def _announce(self):
            """
            设备声明
            """
            try:
                data = {"id": self._device_id, "description": self._description,
                        "functions": self._functions, "default_access": self._default_access}
                res = self._request('/device/announce', data)
                if res['got']:
                    t = _threading.Thread(
                        target=self._execute, args=(res['action'],))
                    t.daemon = True
                    t.start()
                    return True
            except:
                pass
            return False

        def _execute(self, res: dict):
            """执行action

            Args:
                res (dict): action信息

            Raises:
                Exception: 映射未找到

            Returns:
                bool: 是否成功
            """
            # 告知已接收
            self._callback(res['id'], 'processing', '')
            # 查找映射
            if res['command']['function'] not in self._mapping:
                raise Exception('mapping not found')
            func = self._mapping[res['command']['function']]
            # 准备参数
            args = ''
            num = 0
            for arg in res['command']['args']:
                exec(f"self._temp_{num}=arg['value']")
                args += f'{arg["name"]}=self._temp_{num},'
                num+=1
            args = args[:-1]
            # 运行
            try:
                ret = eval(f"func({args})")
                # 回报
                self._callback(res['id'], 'done', ret)
                return True
            except Exception as e:
                self._callback(res['id'], 'error', str(e))
                return False

        def _monitor(self):
            """
            指令检测
            """
            while True:
                res = self._announce()
                _time.sleep(0.2)

        def _callback(self, action_id: str, status: str, return_data):
            """回报信息

            Args:
                action_id (str): action id
                status (str): 设备状态
                return_data (any): 设备返回值

            Returns:
                dict: 返回信息
            """
            data = {
                'id': self._device_id,
                'action_id': action_id,
                'status': status,
                'return': return_data
            }
            return self._request('/device/callback', data)

    def file(self, path):
        """连接到webdav/下载文件

        Args:
            path (str): 路径

        Returns:
            object: 文件对象
        """
        f = self._file(path)
        f.lab_server = self.lab_server
        f.lab_server_address = self.lab_server_address
        f.key = self.key
        f._request = self.request
        return f

    class _file:
        """
        文件类
        """

        def __init__(self, path):
            self.path = path

        def get_free_volume(self):
            """获取空闲盘符

            Returns:
                str: 盘符
            """
            for i in _string.ascii_uppercase:
                if not _os.path.isdir(f'{i}:'):
                    return f'{i}:'
            raise Exception('no free drive letter')

        def mount(self, mountpoint=''):
            """挂载

            Args:
                mountpoint (str, optional): 挂载点(Linux)

            Returns:
                str: 挂载位置
            """
            # 请求webdav
            res = self._request('/file/webdav/mount', {"path": self.path})
            self.id = res['id']
            self.port = res['port']
            self.username = res['username']
            self.password = res['password']
            self.mountpoint = mountpoint
            if _platform.system() == 'Windows':
                self.volume = self.get_free_volume()
                command = f'net use {self.volume} {self.lab_server_address}:{self.port} /user:{self.username} {self.password}'
                _os.popen(command).read()
                return self.volume
            elif _platform.system() == 'Linux':
                if mountpoint=='':
                    raise Exception('mountpoint required')
                command = f"mount -t davfs -o username={self.username},iocharset=utf8 {self.lab_server_address}:{self.port} {self.mountpoint}\n"
                popen=_subprocess.Popen('bash', stdin=_subprocess.PIPE, stdout=_subprocess.PIPE, stderr=_subprocess.PIPE, universal_newlines=True)
                popen.stdin.write(command)
                popen.stdin.write(self.password+'\n')
                popen.stdin.close()
                out = popen.stdout.read()
                if 'Password' in out:
                    return mountpoint
                raise Exception('unknow error')

        def unmount(self):
            """解除挂载

            Returns:
                bool: 是否成功
            """
            if _platform.system() == 'Windows':
                command = f'net use {self.volume} /del'
                _os.popen(command).read()
            elif _platform.system() == 'Linux':
                command = f"umount {self.mountpoint}"
                _os.popen(command).read()
            res = self._request('/file/webdav/unmount', {"id": self.id})
            if res:
                return True
            raise Exception('unkown error')
        
        def download(self):
            res = self._request('/file/download', {"path": self.path})
            if res:
                src=res['base64']
                return _base64.b64edecode(src)
            raise Exception('unkown error')
    
    class _keys:
        """
        密钥管理类
        """
        def list(self):
            """列出密钥

            Returns:
                dict: 密钥列表
            """
            return self._request('/key/list')
        
        def create(self,access_code,description):
            """创建密钥

            Args:
                access_code (str): 密钥权限代码
                description (str): 密钥描述

            Returns:
                str: 生成的密钥
            """
            data={
                'access_code':access_code,
                'description':description
            }
            return self._request('/key/create',data)['key']
        
        def delete(self,id):
            """删除密钥

            Args:
                id (str): 密钥id

            Returns:
                bool: 是否被删除
            """
            data={
                'id':id
            }
            if self._request('/key/del',data):
                return True
            raise Exception('unkown error')