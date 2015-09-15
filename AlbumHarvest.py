'''
    @author:  Baron Daugherty
    @date:    2015-08-30
    @desc:    This program harvests all images
              in all albums for a particular Imgur user.
'''
#necessary imports
from bs4 import BeautifulSoup as bs
import os
import urllib.request

#drives the program
def main():
    #collect user and directory information
    user = input("Username: ")
    folder = input("Directory to save to: ")
    path = folder+user

    #make the directory to save to
    os.mkdir(path)

    #go get 'em, tiger...
    harvest(user, path+"\\")

#download ALL the pictures
def harvest(user, local_path):
    #a list of albums and full url
    albums = []
    url = "https://" +user +".imgur.com"

    #get the html document for parsing
    soup = get_soup(url)

    #find all of the album links and put them in the list
    for link in soup.find_all('a'):
        href = link.get('href')
        if href[2:-5] == "imgur.com/a/":
            albums.append(href[2:])

    #for each album make a directory, then pass it to download_album
    for a in albums:
        path = local_path +a[-5:]
        os.mkdir(path)
        print("Processing album " +a +" " +str(albums.index(a)) + " out of " +str(len(albums)))
        download_album(a, path)

#this actually downloads the individual pics in an album
def download_album(album, path):
    #url and path, plus a list of pictures
    url = "https://" +album
    pics = []
    path = path + "\\"

    #get the html doc for parsing
    soup = get_soup(url)

    #find all the meta tags, get the image name and put it in the pics list
    #(god this is ugly...)
    for tag in soup.find_all('meta'):
        if str(tag)[22:-35] == "i.imgur.com":
            pics.append('http://' +str(tag)[22:-23])

    #for each pic, open the file and write to disk
    for pic in pics:
        with urllib.request.urlopen(pic) as response, open(path +pic[-9:], 'wb') as out_file:
            data = response.read()
            out_file.write(data)

#creates a soup object of the parsed html
def get_soup(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()

    return bs(html, 'html.parser')


main()
