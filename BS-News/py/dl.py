import os
import requests
from time import sleep

# 定义地区列表
regions = ['ar', 'fr', 'de', 'es', 'it', 'ja', 'zh', 'ko', 'nl', 'pt', 'ru', 'tr', 'id', 'ms', 'vi', 'th', 'fi']

# 定义文件类型列表
file_types = ['news', 'community', 'esport']

# 获取当前脚本所在目录
script_directory = os.path.dirname(os.path.abspath(__file__))

# 设置最大重试次数和超时时间
max_retries = 2
timeout = 10

# 循环遍历各个地区
for region in regions:
    print(f"开始下载地区：{region}")
    
    # 循环遍历各个文件类型
    for file_type in file_types:
        retries = 0
        while retries <= max_retries:
            # 构建下载链接
            url = f"https://brawlstars.inbox.supercell.com/data/{region}/{file_type}/content.json"
            
            print(f"正在尝试下载：{url}")
            
            try:
                # 发起GET请求，设置超时
                response = requests.get(url, timeout=timeout)
                
                # 检查响应状态码
                if response.status_code == 200:
                    # 获取服务器上的路径
                    server_path = f"/{region}/{file_type}/"
                    
                    # 构建目标文件路径
                    file_path = os.path.join(script_directory, server_path[1:], 'content.json')
                    
                    # 创建目标目录（如果不存在）
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    # 将响应内容保存到文件
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                        
                    print(f"已下载并保存 {server_path}content.json")
                    break  # 成功下载后跳出重试循环
                else:
                    print(f"下载失败：{url}")
                    retries += 1
            except requests.exceptions.RequestException as e:
                print(f"下载失败：{url}，原因：{e}")
                retries += 1
            
            if retries < max_retries:
                print("等待2秒后重试...")
                sleep(2)  # 等待2秒后重试
            else:
                print(f"无法下载 {url}content.json")
                break
    
    print(f"地区 {region} 下载完成\n")

print("所有地区下载完成")
