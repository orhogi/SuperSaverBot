import re
from json import loads
from random import choice
from random import shuffle
import requests
from bs4 import BeautifulSoup


users = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"]


def instagram_media(url: str):
    post = r'https://www\.instagram\.com/p/([A-Za-z0-9-_]+)'
    reel = r'https://www\.instagram\.com/(reel|reels)/([A-Za-z0-9-_]+)'
    if not re.match(post, url) and not re.match(reel, url):
        return {"status": False, "message": "This link does not belong to the Instagram platform"}
    hosts = ["https://saveig.app/api/ajaxSearch",
             "https://v3.saveinsta.app/api/ajaxSearch"]
    for host in hosts:
        shuffle(hosts)
        data = {"q": url, 't': "media", "lang": "en"}
        sessions = requests.Session()
        sessions.cookies.clear()
        sessions.max_redirects = 30
        sessions.headers.update(
            {
                "User-Agent": choice(users)
            }
        )
        response = sessions.post(host, data=data, headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
        if response.status_code not in [404, 401, 403, 400, 409]:
            break

    try:
        if not response.json().get('mess'):
            docs = response.json()['data']
            soup = BeautifulSoup(docs, 'html.parser')
            data = soup.find_all('a', {"class": 'abutton is-success is-fullwidth btn-premium mt-3'})
            if re.match(post, url):
                links = {"images": [], "videos": []}
                for item in data:
                    if item['href'][0:33] == "https://scontent.cdninstagram.com":
                        links['images'].append(item['href'])
                    else:
                        links['videos'].append(item['href'])
                return {"status": True, "developer": "Oybek Rozievich", "type": "post", "post_links": links}
            if re.match(reel, url):
                return {"status": True, "developer": "Oybek Rozievich", "type": "reel", "link": data[0]['href']}
        else:
            return {"status": False, "message": "Error: Video is private. Please use the tool !"}
    except:
        pass


def pinterest_media(url: str):
    pin_regex = r"https://pin\.it/(\w+)"
    board_regex = r"https://www\.pinterest\.[a-z]+/(\w+)/"
    if not re.match(pin_regex, url) and not re.match(board_regex, url):
        return {"status": False, "message": "This link is not a Pinterest link!"}
    host = "https://dotsave.app"
    data = {"url": url, "lang": "en", "type": "redirect"}
    sessions = requests.Session()
    sessions.cookies.clear()
    sessions.headers.update(
        {"User-Agent": choice(users)}
    )
    response = sessions.post(host, data=data, headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            try:
                soup.find('a', {'class': 'button download-file mt-3'})['href']
                videos = []
                video = soup.find_all('a', {'class': 'button download-file mt-3'})
                for j in video:
                    videos.append(j['href'].split('=')[1])
                return {"status": True, "developer": "Oybek Rozievich", "type": "video", "link": videos}
            except:
                pass
            try:
                links = []
                image = soup.find_all('a', {'class': 'button download-file is-secondary mt-3'})
                for i in image:
                    links.append(i['href'].split('=')[1])
                return {"status": True, "developer": "Oybek Rozievich", "type": "image", "link": links}
            except:
                pass
        except:
            return {"status": False, "type": None, "message": "Bad request"}


def tiktok_media(url: str):
    post = r'https://www\.tiktok\.com/@[A-Za-z0-9_-]+/video/([0-9]+)'
    mobile = r'https://vt\.tiktok\.com/[A-Za-z0-9]+/'
    if not re.match(post, url) and not re.match(mobile, url):
        return {"status": False, "message": "This link is not a TikTok link!"}
    host = "https://ssstik.io/abc?url=dl"
    data = {"id": url, 'locale': "en", "tt": "VndXNlE5"}
    sessions = requests.Session()
    sessions.cookies.clear()
    sessions.max_redirects = 30
    sessions.headers.update(
        {
            "User-Agent": choice(users)
        }
    )
    response = sessions.post(host, data=data, headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        video = soup.find('a', {"class": 'pure-button pure-button-primary is-center u-bl dl-button download_link without_watermark vignette_active notranslate'})['href']
        music = soup.find('a', {"class": "pure-button pure-button-primary is-center u-bl dl-button download_link music vignette_active notranslate"})['href']
    except:
        return {"status": False, "message": "Error: Video is private. Please use the tool !"}
    return {"status": True, "developer": "Oybek Rozievich", "type": "mp4", "video": video, "music": music}


def likee_media(url: str):
    post = r"https:\/\/likee\.video\/@[\w-]+\/video\/\d+"
    reel = r"https://l\.likee\.video/v/(\w+)"
    if not re.match(post, url) and not re.match(reel, url):
        return {"status": False, "message": "This link does not belong to the Likee platform"}
    host = "https://likeedownloader.com/process"
    data = {"id": url, "locale": 'en'}
    sessions = requests.Session()
    sessions.cookies.clear()
    sessions.max_redirects = 30
    sessions.headers.update(
        {
            "User-Agent": choice(users)
        }
    )
    response = sessions.post(host, data=data, headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
    json_data = response.content.decode('utf-8-sig')
    response = loads(json_data)
    if response.get('template'):
        try:
            soup = BeautifulSoup(response['template'], 'html.parser')
            data = soup.find('a', {'class': 'btn btn-primary download_link with_watermark notranslate'})['href']
        except:
            return {"status": False, "message": "Error: Video is private. Please use the tool !"}
        else:
            return {"status": True, "developer": "Oybek Rozievich", "type": "mp4", "link": data}
    else:
        return {"status": False, "type": type, "message": "Bad request"}