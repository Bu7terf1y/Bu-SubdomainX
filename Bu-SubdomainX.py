import requests
import os
import threading
import csv
import time
from datetime import datetime
from rich.console import Console

class SubdomainX:
    # 初始化类变量
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    domain = ""
    subdomains = []
    thread_count = 10
    dict_file = ""
    scan_lock = threading.Lock()
    result_file = None
    stop_flag = False

    # 清理子域名列表
    def clean(self):
        self.subdomains = []

    # 检查字典目录
    def check_dict_dir(self):
        if not os.path.exists("Dict"):
            os.makedirs("Dict", exist_ok=True)
            print("\033[31m[!] 字典目录 Dict 不存在！已创建。\033[0m")

    # 检查字典文件
    def check_dict_file(self):
        dict_path = f"Dict\\{self.dict_file}"
        if not os.path.exists(dict_path):
            with open(dict_path, "w", encoding="utf-8") as f:
                f.write("www\n")
                f.write("api\n")
                f.write("test\n")
                f.write("dev\n")
            print(f"\033[31m[!] 字典文件 {self.dict_file} 不存在！已创建默认字典。\033[0m")

    # 读取字典文件
    def read_dict(self, dict_file):
        try:
            with open(f"Dict\\{dict_file}", 'r') as f:
                lines = f.readlines()
                return [line.strip() for line in lines if line.strip()]
        except Exception as e:
            print(f"\033[31m[!] 读取字典文件失败: {e}\033[0m")
            return []

    # 手动输入域名并开始枚举
    def input_and_scan(self):
        try:
            domain = input("请输入要枚举的主域名（例如：example.com）：").strip()
            if not domain:
                print("\033[31m[!] 未输入域名！\033[0m")
                return
            self.domain = domain
            self.scan()
        except:
            print("\033[31m[!] 输入错误！\033[0m")

    # 设置线程数
    def set_thread_count(self):
        try:
            choice = input("请输入线程数：").strip()
            if not choice:
                print(f"\033[32m[*] 线程数保持为：{self.thread_count}\033[0m")
            if choice:
                self.thread_count = int(choice)
                print(f"\033[32m[*] 线程数已设置为：{self.thread_count}\033[0m")
        except:
            print("\033[31m[!] 输入错误！\033[0m")

    # 读取Dict目录下的所有文件
    def read_dict_files(self):
        if not os.path.exists("Dict"):
            os.makedirs("Dict", exist_ok=True)
            
        dict_files = [f for f in os.listdir("Dict") if os.path.isfile(os.path.join("Dict", f))]
        
        if not dict_files:
            print("\033[31m[!] Dict目录下没有字典文件！\033[0m")
            default_dict = "subdomains.txt"
            with open(f"Dict\\{default_dict}", "w", encoding="utf-8") as f:
                f.write("www\napi\ntest\ndev\n")
            print(f"\033[32m[*] 已创建默认字典文件：{default_dict}\033[0m")
            self.dict_file = default_dict
            return
        # 默认选择第一个字典
        self.dict_file = dict_files[0]
        
        print("\033[33m[*] Dict目录下的字典文件：\033[0m")
        for i, dict_file in enumerate(dict_files, 1):
            print(f"\033[32m{i}. {dict_file}\033[0m")

    # 设置字典文件
    def set_dict_file(self):
        try:
            dict_files = [f for f in os.listdir("Dict") if os.path.isfile(os.path.join("Dict", f))]
            
            if not dict_files:
                print("\033[31m[!] Dict目录下没有字典文件！\033[0m")
                default_dict = "subdomains.txt"
                with open(f"Dict\\{default_dict}", "w", encoding="utf-8") as f:
                    f.write("www\napi\ntest\ndev\n")
                print(f"\033[32m[*] 已创建默认字典文件：{default_dict}\033[0m")
                self.dict_file = default_dict
                return
            
            print("\033[33m[*] Dict目录下的字典文件：\033[0m")
            for i, dict_file in enumerate(dict_files, 1):
                print(f"\033[32m{i}. {dict_file}\033[0m")
            
            choice = input("请输入字典文件的序号：").strip()
            if not choice:
                print(f"\033[32m[*] 字典文件保持为：{self.dict_file}\033[0m")
                return
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(dict_files):
                    self.dict_file = dict_files[index]
                    print(f"\033[32m[*] 字典文件已设置为：{self.dict_file}\033[0m")
                else:
                    print("\033[31m[!] 输入的序号无效！\033[0m")
            except ValueError:
                print("\033[31m[!] 输入错误！请输入数字。\033[0m")
        except Exception as e:
            print(f"\033[31m[!] 设置字典文件失败: {e}\033[0m")

    # 线程停止
    def scan_worker(self, subdomains_list):
        for subdomain in subdomains_list:
            if self.stop_flag: # 收到撤退信号立即停车
                break
            self.scan_subdomain(subdomain)

    # 子域名枚举
    def scan_subdomain(self, subdomain):
        if self.stop_flag:
            return
        try:
            url = f"http://{subdomain}.{self.domain}"
            response = requests.get(url, headers=self.headers, timeout=2.5, allow_redirects=False)
            code = response.status_code
            # 定义有价值的高危状态码白名单
            valid_codes = [200, 301, 302, 307, 401, 403, 500]

            if code not in valid_codes:
                with self.scan_lock:
                    if not self.stop_flag:
                        print(f"\033[31m[-] 忽略状态码[{code}] -> {url}\033[0m")
                return

            code_str = str(code)
            if code_str.startswith('2'):
                code_color = "\033[32m"  # 绿色 (20x)
            elif code_str.startswith('3'):
                code_color = "\033[36m"  # 青色 (30x)
            elif code_str.startswith('4'):
                code_color = "\033[35m"  # 紫色 (40x)
            elif code_str.startswith('5'):
                code_color = "\033[91m"  # 亮红色 (50x)
            else:
                code_color = "\033[37m"  # 白色 (兜底)

            with self.scan_lock:
                if self.stop_flag:
                    return
                print(f"\033[33m[*] 命中状态码[{code_color}{code}\033[33m] -> {url}\033[0m")
                self.result_file.write(f"{url}, {code}\n")
                self.result_file.flush()
        except:
            pass

    # 开始枚举
    def scan(self):
        if not self.domain:
            print("\033[31m[!] 未设置域名！\033[0m")
            return

        self.check_dict_dir()
        self.check_dict_file()

        subdomain_list = self.read_dict(self.dict_file)
        if not subdomain_list:
            print("\033[31m[!] 字典文件为空或读取失败！\033[0m")
            return
        self.stop_flag = False

        print(f"\033[33m[+] 开始枚举子域名... (按 Ctrl+C 可紧急终止)\033[0m")
        print(f"\033[33m[+] 主域名：{self.domain}\033[0m")
        print(f"\033[33m[+] 字典文件：{self.dict_file}\033[0m")
        print(f"\033[33m[+] 线程数：{self.thread_count}\033[0m")

        if not os.path.exists("result"):
            os.makedirs("result", exist_ok=True)

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_path = os.path.join("result", f"{self.domain}_{current_time}.csv")

        try:
            self.result_file = open(csv_path, "w", encoding="utf-8", newline="")
            writer = csv.writer(self.result_file)
            writer.writerow(["子域名", "状态码"])

            thread_subdomains = [[] for _ in range(self.thread_count)]
            for i, subdomain in enumerate(subdomain_list):
                thread_subdomains[i % self.thread_count].append(subdomain)

            threads = []
            for subdomains in thread_subdomains:
                t = threading.Thread(target=self.scan_worker, args=(subdomains,))
                t.daemon = True
                t.start()
                threads.append(t)

            try:
                # 只要还有线程在活着，主线程就循环等待
                while any(t.is_alive() for t in threads):
                    for t in threads:
                        t.join(0.1) # 0.1秒超时，防主线程彻底阻塞
            except KeyboardInterrupt:
                # 触发 Ctrl+C 后，立刻设定停止标志位
                self.stop_flag = True
                print("\n\033[31m[!] 接收到紧急撤退信号，正在终止扫描，请稍候...\033[0m")
                time.sleep(1) # 给正在进行网络 I/O 的线程一点时间退出

            self.result_file.close()

            if os.path.getsize(csv_path) <= 20:
                print("\033[31m[!] 枚举结束或被中断！没有发现有价值的子域名！\033[0m")
                if os.path.exists(csv_path):
                    os.remove(csv_path)
            else:
                print(f"\033[33m[+] 枚举结束！高价值结果已保存到 {csv_path}\033[0m")
        except Exception as e:
            print(f"\033[31m[!] 保存结果失败: {e}\033[0m")

console = Console()
text=[
"\n",
"██████╗ ██╗   ██╗              ███████╗██╗   ██╗██████╗ ██████╗  ██████╗ ███╗   ███╗ █████╗ ██╗███╗   ██╗██╗  ██╗",
"██╔══██╗██║   ██║              ██╔════╝██║   ██║██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██║████╗  ██║╚██╗██╔╝",
"██████╔╝██║   ██║    █████╗    ███████╗██║   ██║██████╔╝██║  ██║██║   ██║██╔████╔██║███████║██║██╔██╗ ██║ ╚███╔╝ ",
"██╔══██╗██║   ██║    ╚════╝    ╚════██║██║   ██║██╔══██╗██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║██║╚██╗██║ ██╔██╗ ",
"██████╔╝╚██████╔╝              ███████║╚██████╔╝██████╔╝██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║██║ ╚████║██╔╝ ██╗",
"╚═════╝  ╚═════╝               ╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝",
"—————————————————————————————————————— Bu-SubdomainX.py v1.0.0 - 子域名枚举工具 ——————————————————————————————————————",
"[*] 项目地址:[blue]https://github.com/Bu7terf1y/Bu-SubdomainX[/blue]",
"[*] By.Bu7terf1y",
"[*] 说明:自动读取Dict目录下的字典文件，可自行选择"
]

start = (255, 182, 193)
end = (128, 0, 128)

lines = len(text)

for i, line in enumerate(text):
    r = int(start[0] + (end[0] - start[0]) * i / (lines - 1))
    g = int(start[1] + (end[1] - start[1]) * i / (lines - 1))
    b = int(start[2] + (end[2] - start[2]) * i / (lines - 1))
    console.print(line, style=f"rgb({r},{g},{b})", highlight=False)

subdomainx = SubdomainX()
subdomainx.read_dict_files()

while True:
    print("\n=================================================================================================")
    choice = input(f"请输入1.输入域名并开始枚举 2.设置线程（当前：{subdomainx.thread_count}） 3.设置字典文件（当前：{subdomainx.dict_file}） 4.退出：").strip()
    if choice == "1":
        subdomainx.clean()
        subdomainx.input_and_scan()
    elif choice == "2":
        subdomainx.set_thread_count()
    elif choice == "3":
        subdomainx.set_dict_file()
    elif choice == "4":
        print("\033[33m[+] 程序退出！\033[0m")
        break
    else:
        print("\033[31m[!] 输入错误！请输入1、2、3或4。\033[0m")