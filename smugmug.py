import requests
import yaml
import json
import os
import logging
import hashlib
import mimetypes
import time
from rauth import OAuth1Session

headers = {
    'X-Smug-ResponseType': 'JSON',
    'X-Smug-Verson': 'v2'
}


def createTable(connection):
    connection.execute("""
        CREATE TABLE smugmugAlbums (
            startDate text NOT NULL UNIQUE,
            name text NOT NULL)""")


def addEntry(connection, dateString, albumId):
    connection.execute(
        "INSERT INTO smugmugAlbums (startDate, name) Values (?,?)",
        (dateString, albumId))


def getAlbum(connection, dateString):
    lastGood = ""
    for row in connection.execute(
            "SELECT * from smugmugAlbums ORDER BY startDate ASC"):
        if row[0] > dateString:
            break
        lastGood = row[1]
    return lastGood


def upload_data(connection, filename, img_data, config, dateString):
    headers['X-Smug-AlbumURI'] = getAlbum(connection, dateString)

    session = OAuth1Session(consumer_key=config['app_key'],
                            consumer_secret=config['app_secret'],
                            access_token=config['user_token'],
                            access_token_secret=config['user_secret'])
    print("*****************" + filename)
    headers['X-Smug-FileName'] = filename
    headers['Content-Length'] = str(len(img_data))
    headers['Content-Type'] = image_type = mimetypes.guess_type(filename)[0]
    headers['Content-MD5'] = hashlib.md5(img_data).hexdigest()

    r = session.post('https://upload.smugmug.com/',
                     headers=headers,
                     header_auth=True,
                     data=img_data)
    imgKey = r.json()['Image']['Key']
    print(imgKey)

    return imgKey

def upload_file(filename, config, year):
    img_data = open(filename, 'rb').read()
    return upload_data(filename, img_data, year)

  


base_api = 'https://www.smugmug.com/api/v2/image/'


def get_medium_link(imgKey, config):
    headers = {'Accept': 'application/json'}
    params = {'APIKey': config['app_key']}
    r = requests.get(base_api + imgKey + '-0!sizes',
                     headers=headers,
                     params=params)
    try:
        link = r.json()['Response']['ImageSizes']['MediumImageUrl']
    except KeyError:  # In case it was a tiny image and there wasn't anything stored for medium
        link = r.json()['Response']['ImageSizes']['LargestImageUrl']
    return link


def getLargestImage(imgKey, config):
    headers = {'Accept': 'application/json'}
    params = {'APIKey': config['app_key']}
    r = requests.get(base_api + imgKey + '-0!sizes',
                     headers=headers,
                     params=params)
    return r.json()['Response']['ImageSizes']['LargestImageUrl']


if __name__ == "main":

    # need test code here
    pass
