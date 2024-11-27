import re
import os
import json
import requests
import time
import csv
import pandas as pd

# Helper functions for reading and writing CSV files
def write_csv(filepath, data, head=None):
    if head:
        data = [head] + data
    with open(filepath, mode='w', encoding='UTF-8-sig', newline='') as f:
        writer = csv.writer(f)
        for i in data:
            writer.writerow(i)

def read_csv(filepath):
    data = []
    if os.path.exists(filepath):
        with open(filepath, mode='r', encoding='latin-1') as f:
            lines = csv.reader(f)
            for line in lines:
                data.append(line)
        return data
    else:
        print('filepath is wrong: {}'.format(filepath))
        return []

# Function to grab image from Baidu
def grab_img_baidu(_url, _headers=None):
    if _headers is None:
        headers = {
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            "Referer": "https://map.baidu.com/",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }
    else:
        headers = _headers
    response = requests.get(_url, headers=headers)

    if response.status_code == 200 and response.headers.get('Content-Type') == 'image/jpeg':
        return response.content
    else:
        return None

# Function to fetch content from URL
def openUrl(_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    response = requests.get(_url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        return None

# Function to get Pano ID based on coordinates
def getPanoId(_lng, _lat):
    url = f"https://mapsv0.bdimg.com/?&qt=qsdata&x={_lng}&y={_lat}&l=17.031000000000002&action=0&mode=day&t=1530956939770"
    response = openUrl(url).decode("utf8")
    if response is None:
        return None
    reg = r'"id":"(.+?)",'
    pat = re.compile(reg)
    try:
        svid = re.findall(pat, response)[0]
        return svid
    except:
        return None

# Function to convert coordinates to Baidu Map
def wgs2bd09mc(wgs_x, wgs_y):
    url = 'http://api.map.baidu.com/geoconv/v1/?coords={}+&from=1&to=6&output=json&ak={}'.format(
        wgs_x + ',' + wgs_y,
        'mYL7zDrHfcb0ziXBqhBOcqFefrbRUnuq'
    )
    res = openUrl(url).decode()
    temp = json.loads(res)
    bd09mc_x = 0
    bd09mc_y = 0
    if temp['status'] == 0:
        bd09mc_x = temp['result'][0]['x']
        bd09mc_y = temp['result'][0]['y']

    return bd09mc_x, bd09mc_y

# Function to fetch data based on SID
def fetch_data(sid):
    url = f"http://mapsv0.bdimg.com/get?&qt=sdata&sid={sid}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print(f"Failed to fetch data for SID: {sid}")
        return None

def getPanoIdTime(svid):
    url = f"http://mapsv0.bdimg.com/get?&qt=sdata&sid={svid}"
    response = openUrl(url).decode("utf8")
    if response is None:
        return None
    reg = r'"TimeLine":"(.+?)",'
    pat = re.compile(reg)
    try:
        timeline_list = re.findall(pat, response)
        return timeline_list
    except:
        return None

def getPanoIdDate(svid):
    url = f"http://mapsv0.bdimg.com/get?&qt=sdata&sid={svid}"
    response = openUrl(url).decode("utf8")
    if response is None:
        return None
    reg = r'"Date":"(.+?)",'
    pat = re.compile(reg)
    try:
        date = re.findall(pat, response)
        return date
    except:
        return None

def getAllPanoId(svid):
    url = f"http://mapsv0.bdimg.com/get?&qt=sdata&sid={svid}"
    response = openUrl(url).decode("utf8")
    if response is None:
        return None
    reg_timelinelist = r'"TimeLine":"(.+?)",'
    pat_tiamelinelist = re.compile(reg_timelinelist)
    reg_svidlist = r'"ID":"(.+?)",'
    pat_svidlist = re.compile(reg_svidlist)
    try:
        timeline_list = re.findall(pat_tiamelinelist, response)
        svid_list = re.findall(pat_svidlist, response)
        svid_count = len(timeline_list)
        svid_list = svid_list[-svid_count:]
        return svid_list
    except:
        return None

# Main script
if __name__ == "__main__":
    root = r'BaiduStreetViewSpider-main\dir'
    read_fn = r"D:\WuHan_PolygonToLi_FeatureVertic011.csv"
    svid_fn = r"BaiduStreetViewSpider-main\dir\panoid.csv"
    dir = r"D:\images"
    max_photos = 1000  # 设置下载图片的最大数量
    photo_count = 0  # 记录下载图片的数量

    # 读取CSV文件
    data = read_csv(read_fn)
    header = data[0]
    data = data[1:]
    df = pd.DataFrame(columns=['ID', 'svid', 'date', 'querylat', 'querylon', 'img'])
    ID = 0

    for i in range(0, 10):
        print('Processing No. {} point...'.format(i + 1))
        wgs_x, wgs_y = data[i][0], data[i][1]

        try:
            bd09mc_x, bd09mc_y = wgs2bd09mc(wgs_x, wgs_y)
            print(bd09mc_x,bd09mc_y)
        except Exception as e:
            print(str(e))  # 打印异常原因
            continue

        svid = getPanoId(bd09mc_x, bd09mc_y)
        if svid is None:
            print("未能获取到svid")
            continue
        else:
            # 获取JSON数据
            svid_list = getAllPanoId(svid)
            print('svid_list:', svid_list)



            for i in range(0,len(svid_list)):
                svid = svid_list[i]
                try:
                    date = getPanoIdDate(svid)[0]  # 直接尝试访问第一个元素
                except IndexError:  # 如果列表为空或没有第一个元素，则捕获异常
                    date = 'None'

                json_data = fetch_data(svid)
                if json_data is None:
                    print("未能获取到JSON数据")
                    continue
                # 处理JSON数据
                heading = '0'  # 设置图片的方向，90为示例值
                print('Date:', date)
                img_name = f"{wgs_x}_{wgs_y}_{date}.png"
                file_path = os.path.join(dir, f"{img_name}")
                if os.path.exists(file_path):
                    print(f"Image for location {img_name},already exists. Skipping...")
                    continue
                    # 注意：此时不记录在csv表格中！！！

                url = f'https://mapsv0.bdimg.com/?qt=pr3d&fovy=90&quality=100&panoid={svid}&heading={heading}&pitch=30&width=1024&height=1024'
                img = grab_img_baidu(url)
                if img is None:
                    print(f"Error downloading image for sid: {svid}, timeline: {date}, heading: {heading}")
                    continue
                else:
                    print(f"Successfully downloaded image for sid: {svid}, timeline: {date}, heading: {heading}")
                    with open(file_path, "wb") as img_file:
                        img_file.write(img)
                    photo_count += 1

                    new_row = {'ID': ID, 'svid': svid, 'date': date, 'querylat': wgs_y, 'querylon': wgs_x, 'img': img_name}
                    df = df.append(new_row, ignore_index=True)
                    ID += 1

                if photo_count >= max_photos:
                    print("Reached maximum photo limit. Stopping download.")
                    break
            print('photo_count:', photo_count)
            time.sleep(5)  # 控制下载频率，避免请求过于频繁
    df.to_csv(r'D:\Wuhan_images\imagestest.csv', index=False)
    print("Processing complete.")

