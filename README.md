# Bu-SubdomainX - 子域名枚举工具

<img width="735" height="262" alt="image" src="https://github.com/user-attachments/assets/7e9fae12-a3c6-4249-a53d-29d99f079370" />

Bu-SubdomainX 是一个高效的子域名枚举工具，支持多线程扫描和自定义字典，用于渗透测试和安全评估。

## 功能特点

- ✅ 多线程扫描，提高枚举速度
- ✅ 支持自定义字典文件
- ✅ 自动检查并创建字典目录和默认字典
- ✅ 实时显示扫描结果
- ✅ 结果保存为CSV文件，方便后续分析
- ✅ 彩色终端输出，提升用户体验

## 安装依赖

在项目目录下运行：

```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行 `Bu-SubdomainX.py`
2. 程序会自动检查Dict目录和字典文件
3. 选择菜单选项：
   - `1. 输入域名并开始枚举`：输入主域名后立即开始枚举
   - `2. 设置线程`：自定义扫描线程数（默认10）
   - `3. 设置字典文件`：选择Dict目录下的字典文件
   - `4. 退出`：退出程序

### 示例

```bash
$ python Bu-SubdomainX.py

# 输入域名并开始枚举
请输入1.输入域名并开始枚举 2.设置线程（当前：10） 3.设置字典文件（当前：subdomains.txt） 4.退出：1
请输入要枚举的主域名（例如：example.com）：example.com
[+] 开始枚举子域名...
[+] 主域名：example.com
[+] 字典文件：subdomains.txt
[+] 线程数：10
[*] 状态码[200] -> http://www.example.com
[*] 状态码[200] -> http://api.example.com
[+] 枚举结束！结果已保存到 result/example.com_2024-01-01_12-00-00.csv
```

## 字典文件

工具会在 `Dict` 目录下查找字典文件。如果目录不存在，会自动创建；如果没有字典文件，会创建默认的 `subdomains.txt` 文件。

您可以在 `Dict` 目录下添加自定义字典文件，然后通过菜单选项选择使用。

## 结果保存

扫描结果会保存到 `result` 目录下的 CSV 文件中，文件名格式为 `{域名}_{时间戳}.csv`。

CSV文件包含以下字段：
- 子域名
- 状态码

## 注意事项

- 本工具仅用于合法的安全测试和授权的渗透测试
- 请勿用于非法用途，否则后果自负
- 使用前请确保您有目标域名的测试授权
- 扫描速度过快可能会被目标服务器视为攻击，建议合理设置线程数

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 许可证

本项目采用 MIT 许可证。

## 作者

- Bu7terf1y
- GitHub: [https://github.com/Bu7terf1y](https://github.com/Bu7terf1y)

---

*"子域名枚举是渗透测试的重要步骤，找到更多攻击面。"*
