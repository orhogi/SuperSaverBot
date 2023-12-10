import re
import requests
from aiogram.types import InputMediaVideo, InputMediaPhoto


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
            params = {'url': url}
            response = requests.get(self.HOST + 'media/insta/', params=params).json()
            if response['status']:
                if response['type'] == "post":
                    image_medias = [InputMediaPhoto(media=i, caption="@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥" if v == 0 else None) for v, i in enumerate(response['post_links']['images'])]
                    video_medias = [InputMediaVideo(media=i, caption="@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥" if not image_medias and v == 0 else None) for v, i in enumerate(response['post_links']['videos'])]
                    all_media = image_medias + video_medias
                    return {"type": "insta", "post": True, "data": all_media}
                elif response['type'] == "reel":
                    return {"type": "insta", "post": False, "data": response['link']}
            else:
                return False
                
        elif re.match(self.LIKEE, url) or re.match(self.LIKEE_MOBILE, url):
            params = {'url': url}
            response = requests.get(self.HOST + 'media/likee/', params=params).json()
            if response['status']:
                return {"type": "likee", "post": False, "data": response['link']}
            else:
                return False
            
        elif re.match(self.TIK, url) or re.match(self.TIK_MOBILE, url):
            params = {'url': url}
            response = requests.get(self.HOST + 'media/tiktok/', params=params).json()
            if response['status']:
                return {"type": "tiktok", "data": response['video']}
            else:
                return False
            
        elif re.match(self.PIN_POST, url) or re.match(self.PIN_VIDEO, url):
            params = {'url': url}
            response = requests.get(self.HOST + 'media/pin/', params=params).json()
            if response['status']:
                if response['type'] == 'image':
                    if response['link'][1][-4:] == '.gif':
                        return {"type": "pin", "post": 'gif', "data": response['link'][1]}
                    return {"type": "pin", "post": 'image', "data": response['link'][1]}
                elif response['type'] == 'video':
                    return {"type": "pin", "post": 'video', "data": response['link'][1]}
            else:
                return False
        else:
            return None