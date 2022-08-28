import requests
import re
import os

url = input("Paste a Missevan drama or single sound link here: ")
cookie = input("Please paste your cookie here or press enter skip it: ")
target_folder = input("Input target folder or press enter to skip it: ")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
    "Host": "www.missevan.com",
}

if cookie:
    headers["Cookie"] = cookie

def dl_mp3(id, target_folder = './'):
    json_url = "https://www.missevan.com/sound/getsound?soundid=" + id
    danmu_url = "https://www.missevan.com/sound/getdm?soundid=" + id
    r = requests.get(json_url, headers = headers)
    json_content = r.content.decode('utf-8')
    sound_title = re.findall(r"soundstr\":\"(.*?)\"", json_content)[0]
    mp3_fname = sound_title + '.mp3'
    danmu_fname = sound_title + '.xml'
    invalid = "<>:\"/\\|?*"
    for char in invalid:
        mp3_fname = mp3_fname.replace(char, "_")
        danmu_fname = danmu_fname.replace(char, "_")
    sound_url = re.findall(r"soundurl\":\"(.*?)\"", json_content)[0]
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    mp3_stream = requests.get(sound_url)
    danmu = requests.get(danmu_url)
    if target_folder != './':
        mp3_path = target_folder + '/' + mp3_fname
        danmu_path = target_folder + '/' + danmu_fname
    else:
        mp3_path = './' + mp3_fname
        danmu_path = './' + danmu_fname
    with open(mp3_path, 'wb') as f:
        f.write(mp3_stream.content)
    with open(danmu_path, 'wb') as f:
        f.write(danmu.content)
    print(mp3_fname +" and " + danmu_fname + " downloaded in folder " + target_folder)

def get_mp3s(drama_id):
    json_url = "https://www.missevan.com/dramaapi/getdrama?drama_id=" + drama_id
    r = requests.get(json_url, headers = headers)
    json_content = r.content.decode('utf-8')
    # 后面乱七八糟的直接删掉
    stop_sign = "\"group\""
    endplace = json_content.find(stop_sign)
    cleaned_data = json_content[:endplace]
    mp3_ids = re.findall(r"sound_id\":(.*?),", cleaned_data)
    return mp3_ids

if "drama" in url:
    is_drama = True
else:
    is_drama = False

if is_drama == False:
    id = url.split("=")[-1]
    if target_folder:
        dl_mp3(id, target_folder)
    else:
        dl_mp3(id)
else:
    drama_id = url.split('/')[-1]
    mp3_list = get_mp3s(drama_id)
    for id in mp3_list:
        if target_folder:
            dl_mp3(id, target_folder)
        else:
            dl_mp3(id)
