import requests
import json
import os
import logging
import hashlib
import mimetypes
import time
from rauth import OAuth1Session

headers = {
    # this is a pointer to the 2019-2020 engineering notebook
    'X-Smug-AlbumURI': '/api/v2/album/VgQcSw',
    'X-Smug-ResponseType': 'JSON',
    'X-Smug-Verson': 'v2'
}

def upload_data(filename, img_data, config):
    session = OAuth1Session(consumer_key=config['app_key'],
                            consumer_secret=config['app_secret'],
                            access_token=config['user_token'],
                            access_token_secret=config['user_secret'])

    headers['X-Smug-FileName'] = filename
    headers['Content-Length'] = str(len(img_data))
    headers['Content-Type'] = image_type = mimetypes.guess_type(filename)[0]
    headers['Content-MD5'] = hashlib.md5(img_data).hexdigest()

    r = session.post('https://upload.smugmug.com/',
                     headers=headers,
                     header_auth=True,
                     data=img_data)
    imgKey = r.json()['Image']['Key']

    return imgKey

def upload_file(filename, config):
    img_data = open(filename, 'rb').read()
    return upload_data(filename, img_data, config)

  


base_api = 'https://www.smugmug.com/api/v2/image/'


def get_medium_link(imgKey, config):
    headers = {'Accept': 'application/json'}
    params = {'APIKey': config['app_key']}
    r = requests.get(base_api + imgKey + '-0!sizes',
                     headers=headers,
                     params=params)
    print(r.json())
    try:
        link = r.json()['Response']['ImageSizes']['MediumImageUrl']
    except KeyError:   # In case it was a tiny image and there wasn't anything stored for medium
        link = r.json()['Response']['ImageSizes']['LargestImageUrl']
    return link


if __name__ == "main":
    config = json.load(open('secrets.json', 'r'))
    imgKey = upload_file('Duck only.png', config)

    print(f'Image Key: {imgKey}')
    print('waiting 2 seconds')
    time.sleep(2)

    medium_link = get_medium_link(imgKey, config)
    print(medium_link)