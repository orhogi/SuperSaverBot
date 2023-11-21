import re

import requests
from aiogram.types import InputMediaVideo, InputMediaPhoto
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
    HOST = 'http://16.171.63.222/'

    def get_media(self, url):
        if re.match(self.INSTA_POST, url) or re.match(self.INSTA_REEL, url):
            data_obj = InstaLikeeTik('instagram')
            data = data_obj.get_media(url)
            if not data:
                params = {'url': url}
                response = requests.get(self.HOST + 'media/insta/', params=params).json()
                if response['status']:
                    if response['type'] == "post":
                        image_medias = [InputMediaPhoto(media=i, caption="@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥" if v == 0 else None) for v, i in enumerate(response['post_links']['images'])]
                        video_medias = [InputMediaVideo(media=i, caption="@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥" if not image_medias and v == 0 else None) for v, i in enumerate(response['post_links']['videos'])]
                        all_media = image_medias + video_medias
                        return {"type": "insta", "post": True, "data": all_media}
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
                        if response['link'][1][-4:] == '.gif':
                            data_obj.create_media(url=url, media=response['link'][1], types="gif")
                            return {"type": "pin", "post": 'gif', "data": response['link'][1]}
                        data_obj.create_media(url=url, media=response['link'][1], types="image")
                        return {"type": "pin", "post": 'image', "data": response['link'][1]}
                    elif response['type'] == 'video':
                        data_obj.create_media(url=url, media=response['link'][1], types="video")
                        return {"type": "pin", "post": 'video', "data": response['link'][1]}
                else:
                    return False
            else:
                return {"type": "pin", "post": data['types'], "data": data['media']}
        else:
            return None
