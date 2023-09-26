import re

import requests

from models.model import Pin, InstaLikeeTik


class UniversalAPI:
    INSTA_POST = r'https://www\.instagram\.com/p/([A-Za-z0-9-_]+)'
    INSTA_REEL = r'https://www\.instagram\.com/(reel|reels)/([A-Za-z0-9-_]+)'
    LIKEE = r"https:\/\/likee\.video\/@[\w-]+\/video\/\d+"
    LIKEE_MOBILE = r"https://l\.likee\.video/v/(\w+)"
    TIK = r'https://www\.tiktok\.com/@[A-Za-z0-9_-]+/video/([0-9]+)'
    TIK_MOBILE = r'https://vt\.tiktok\.com/[A-Za-z0-9]+/'
    PIN_POST = r"https://pin\.it/(\w+)"
    PIN_VIDEO = r"https://www\.pinterest\.[a-z]+/(\w+)/"
    HOST = 'https://allsaver.onrender.com/'

    def get_media(self, url):
        if re.match(self.INSTA_POST, url) or re.match(self.INSTA_REEL, url):
            data_obj = InstaLikeeTik('instagram')
            data = data_obj.get_media(url)
            if not data:
                params = {'url': url}
                response = requests.get(self.HOST + 'media/insta/', params=params).json()
                if response['status']:
                    if response['type'] == "post":
                        medias = [{"media": i, "type": "photo"} for i in response['post_links']['images']]
                        videos = [{"media": i, "type": "video"} for i in response['post_links']['videos']]
                        return {"type": "insta", "post": True, "data": medias + videos}
                    elif response['type'] == "reel":
                        data_obj.create_media(url=url, media=response['link'])
                        return {"type": "insta", "post": False, "data": response['link']}
                else:
                    return False
            else:
                return {"type": "insta", "post": False, "data": data['media']}
        elif re.match(self.LIKEE, url) or re.match(self.LIKEE_MOBILE, url):
            data_obj = InstaLikeeTik('likee')
            data = data_obj.get_media(url)
            if not data:
                params = {'url': url}
                response = requests.get(self.HOST + 'media/likee/', params=params).json()
                if response['status']:
                    data_obj.create_media(url=url, media=response['link'])
                    return {"type": "likee", "post": False, "data": response['link']}
                else:
                    return False
            else:
                return {"type": "likee", "post": False, "data": data['media']}
        elif re.match(self.TIK, url) or re.match(self.TIK_MOBILE, url):
            data_obj = InstaLikeeTik('tiktok')
            data = data_obj.get_media(url)
            if not data:
                params = {'url': url}
                response = requests.get(self.HOST + 'media/tiktok/', params=params).json()
                if response['status']:
                    data_obj.create_media(url=url, media=response['video'])
                    return {"type": "tiktok", "data": response['video']}
                else:
                    return False
            else:
                return {"type": "tiktok", "data": data['media']}
        elif re.match(self.PIN_POST, url) or re.match(self.PIN_VIDEO, url):
            data_obj = Pin('pinterest')
            data = data_obj.get_media(url)
            if not data:
                params = {'url': url}
                response = requests.get(self.HOST + 'media/pin/', params=params).json()
                if response['status']:
                    if response['type'] == 'image':
                        if response['link'][0][-4:] == '.gif':
                            data_obj.create_media(url=url, media=response['link'][0], types="gif")
                            return {"type": "pin", "post": 'gif', "data": response['link'][0]}
                        data_obj.create_media(url=url, media=response['link'][0], types="image")
                        return {"type": "pin", "post": 'image', "data": response['link'][0]}
                    elif response['type'] == 'video':
                        data_obj.create_media(url=url, media=response['link'][0], types="video")
                        return {"type": "pin", "post": 'video', "data": response['link'][0]}
                else:
                    return False
            else:
                return {"type": "pin", "post": data['types'], "data": data['media']}
        else:
            return None