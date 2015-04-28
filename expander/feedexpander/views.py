from django.shortcuts import render
from django.http import HttpResponse
import feedparser
import string
import urllib2
from BeautifulSoup import BeautifulSoup


def getImages(imgs):
    response = ""
    try:
        for img in imgs:
            response += str(img).encode("utf8") + "<br/>"
    except UnicodeDecodeError:
        print "Couldn't get all images"
    return response


def getUrlContent(url):
    response = ""
    try:
        urlDescriptor = urllib2.urlopen(url)
    except urllib2.HTTPError:
        print "wrong url:", url
        return response
    html = urlDescriptor.read()
    urlDescriptor.close()
    soup = BeautifulSoup(''.join(html))
    p = soup.find('p')
    if p != None and p.string != None:
        response = p.string + "<br/>"
    imgs = soup.findAll('img')
    if imgs != None:
        response += getImages(imgs)
    return response


def getLinks(tweet):
    response = ""
    index = string.find(tweet, "http://")
    while index != -1:
        url = tweet[index:].split("&")[0]
        index += len(url)
        index = string.find(tweet[index:], "http://")
        response += "URL:   <a href='" + url + "'>" + url + "</a><br/>"
        response += getUrlContent(url)
    return response


def printTwets(request, username):
    url = 'http://twitrss.me/twitter_user_to_rss/?user=' + username
    dict = feedparser.parse(url)
    response = ""
    try:
        for index in range(5):
            tweet = dict.entries[index].title + "<br/>"
            response += tweet + getLinks(tweet) + "<br/>"
    except IndexError:
        response += "Could not get all tweets"
    return HttpResponse(response)
