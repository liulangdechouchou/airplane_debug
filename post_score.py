# coding=utf-8
import paramiko,sys
"""
ip=None 什么意思
"""
class SFTP():
    def __init__(self,ip=None,filename=None,choose="-h"):
        self.ip = ip
        if not self.ip:
            self.ip = "47.110.10.111"
        self.filename = filename
        self.choose = choose

        self.justice()
    def justice(self):
        """根据参数判断用户需要的功能"""
        if self.choose == "-d":
            self.do_it = self.download
        elif self.choose == "-u":
            self.do_it = self.upload
        elif self.choose == "-h":
            self.do_it = self.help
        else:
            self.do_it = self.help
    def start(self):
        """执行"""
        self.do_it()

    def help(self):
        # 帮助文档
        print("\n", end="")
        print("参数:")
        print("-d[download]  下载文件")
        print("-u[upload]    上传文件")
        print("-h[help]      帮    助")
        print("\n", end="")
        print("格式:")
        print("python3 post_score.py [ip] [filename] [-u|-d|-h]")

    def connet(self):
        """尝试连接服务器"""
        try:
            # 获取transport实例
            conn = paramiko.Transport(self.ip,22)
        #Exception表示什么错误
        except Exception as e:
            print("e:",e)
        else:
            self.name = "root"
            password = input("请输入密码：")
            try:
                # 用账号密码连接ssh服务端
                conn.connect(username=self.name, password=password)
                # 获取SFTP实例
                self.sftp_ob = paramiko.SFTPClient.from_transport(conn)
            except Exception as e:
                print("e:",e)
                return
            else:
                print("连接成功")
    def download(self):
        self.connet()
        print("下载中……")
        localpath = "D:/python_work/plane/src/" + self.filename
        remotepath = "/home/airplane_highscore/"+ self.filename
        self.sftp_ob.get(remotepath, localpath)
        print("下载完成！")
    def upload(self):
        self.connet()
        print("上传中……")
        localpath = r"D:/python_work/plane/src/" + self.filename
        remotepath = r"/home/airplane_highscore/"+ self.filename
        self.sftp_ob.put(localpath,remotepath)
        print("上传完成！")

def main():
    try:

        # 实例这个自己写的SFTP类
        # 这一步只是实现一个功能：把do_it函数确实具体是变为哪个函数
        sftp = SFTP(sys.argv[1],sys.argv[2],sys.argv[3])
    except:
        if "-h" in sys.argv:
            sftp = SFTP(choose=sys.argv[1])
        else:
            sftp = SFTP()
    sftp.start()



main()