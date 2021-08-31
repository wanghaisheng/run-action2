import re
import json
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment
import urllib.request
from bs4.element import ResultSet
from matplotlib.pyplot import text, title

# imports
import pandas as pd
import os
import base64
from requests import exceptions
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, WebDriverException

import multiprocessing.dummy as mp

# proxies = {'socks5': '127.0.0.1:1080'}
# print("Using HTTP proxy %s" % proxies['socks5'])
proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}


def getUrl(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
    }
    # out = requests.get(url, headers=header,proxies=proxies)

    # assert out.status_code == 200
    # soup = BeautifulSoup(out.content, 'lxml')
    # captcha_img = soup.find("form").find("img")['src']

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
    chrome_options.add_argument("proxy-server=socks5://127.0.0.1:1080")
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])
    web_driver = webdriver.Chrome(
        executable_path=r"D:\Download\audio-visual\youtubechannelAll\chromedriver.exe", chrome_options=chrome_options)

    out = web_driver.get(url)
    out = web_driver.page_source
    # webdriver.quit()
    soup = BeautifulSoup(out, 'lxml')
    return soup


def get_user_agent():
    # some fake one I found :/
    return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'


proxy_support = urllib.request.ProxyHandler({'socks5': '127.0.0.1:1080'})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)


def b64e(s):
    return base64.b64encode(s.encode()).decode()


def getlinks(link):
    soup = getUrl(link)
    pagination_Links = []
    all_topic_links = []
    # Pages1 = soup.find('div',attrs={"class":"PageNav"})
    # print(Pages1)
    if link == 'https://www.thefastlaneforum.com/community/pages/most_viewed_threads/#most_viewed_year' or link=='https://www.thefastlaneforum.com/community/pages/most_viewed_threads/#most_viewed_six':
        all_topic_links.extend(get_topics_links(link))
    else:
        Pages = soup.findAll('li', attrs={"class": "pageNavWrapper"})
        # print(Pages)
        if soup.find('li', attrs={"class": "pageNav-page pageNav-page--skip pageNav-page--skipEnd"}):
            Pages = soup.findAll('li', attrs={"class": "pageNav-page"})
            tmp_pageno = []
            link = ''

            for page in Pages:

                Pages = page.find('a')
                # print(Pages)
                if not page.find('a').text == '…':
                    tmp_pageno.append(int(page.find('a').text))
                    link = page.find('a').attrs['href']
                    # print('---m', link)
                    # tmp_pageno.append()
                
                maxpageno = max(tmp_pageno)
                for pageno in range(maxpageno):

                    pagination_Links.append(
                        'https://www.thefastlaneforum.com'+link+'page-'+str(pageno))

                for pagination in pagination_Links:
                    all_topic_links.extend(get_topics_links(pagination))
    print('!!!\n', all_topic_links)
    return pagination_Links, all_topic_links


def getCategoryPaginationLink(option, keywords, link):
    if option == 0:
        link = 'https://www.thefastlaneforum.com/community/search/925563/?q='+keywords+'&o=date'
    elif option == 1:
        link = 'https://www.thefastlaneforum.com/community/prefixess/notable.56'
    elif option == 2:
        link = 'https://www.thefastlaneforum.com/community/prefixess/gold.47/'
    elif option == 3:
        link = 'https://www.thefastlaneforum.com/community/prefixess/hot-topic.83/'

    elif option == 4:
        link = 'https://www.thefastlaneforum.com/community/pages/most_viewed_threads/#most_viewed_six'
        # specific topic
    elif option == 5:
        link = 'https://www.thefastlaneforum.com/community/pages/most_viewed_threads/#most_viewed_year'
    # over=urlopen(link).read()
    pagination_Links, all_topic_links = getlinks(link)
    return pagination_Links, all_topic_links


def getTopicPaginationLinks(link):
    # over=urlopen(link).read()
    print('==process\n', link)

    soup = getUrl(link)

    Links = [link]
    if not soup.findAll('nav', attrs={"class": "pageNavWrapper"}):
        # Links.append(link)
        pass
    else:
        Pages = soup.findAll('nav', attrs={"class": "pageNavWrapper"})
        topic_title = soup.find(
            'h1', attrs={'class': 'p-title-value'}).get_text().strip()
        # print('00000011',soup.find('div',attrs={"class":"pageNav"}))
        if soup.find('div', attrs={"class": "pageNav"}):
            Pages = soup.findAll('li', attrs={"class": "pageNav-page"})
            tmp_pageno = []
            link = ''
            Pages = dict.fromkeys(Pages)

            for page in Pages:

                Pages = page.find('a')
                print('11111111111',Pages)
                if not page.find('a').text == '…':
                    tmp_pageno.append(int(page.find('a').text))
                    link = page.find('a').attrs['href']
                    # print('88',link)
                    # tmp_pageno.append(int((link.split('/page-')[-1])))

                maxpageno = max(tmp_pageno)+1
                print('00000',maxpageno)
                if not '/page-' in link:
                    pass
                else:
                    end = link.rfind('/page-')
                    link = link[:end]
                    # print('99',link)
                    for pageno in range(maxpageno):
                        Links.append(
                            'https://www.thefastlaneforum.com'+link+'/page-'+str(pageno))
            
            Links = list(dict.fromkeys(Links))
            Links.pop(0)
            Links.pop(1)
    return Links


def getMessages(topic_link):
    Links = getTopicPaginationLinks(topic_link)
    topic_title = ''
    Pages_contents = []
    # over1=urlopen(topic_link).read()

    # soup = BeautifulSoup(r.content, features="lxml")
    soup1 = getUrl(topic_link)
#    if len(Links) == 0:
    print('当前主题中所有分页的url', Links)
    # print(soup1)
    topic_title = soup1.find('h1', attrs={'class', 'p-title-value'})
    # print(topic_title)
    for child in topic_title.find_all(['blockquote', 'br', 'a', 'span', 'bbCodeBlock']):
        child.decompose()
    if topic_title.get_text().strip():
        topic_title = topic_title.get_text().strip()
    invalid = '<>:"/\|?*()'
    for char in invalid:
        topic_title = topic_title.replace(char, '')
    # Pages_contents.append({'title':topic_title})
    for link in Links:
        print('处理当前主题分页的url ', link)

        soup = getUrl(link)
        articles_Results = soup.findAll(
            'article', attrs={'class', 'message message--post js-post js-inlineModContainer'})
        # print(6,Results)
        for res in articles_Results:
            author = res.attrs['data-author']
            messages_Results = res.findAll(
                'article', attrs={'class': 'message-body js-selectToQuote'})
            for res in messages_Results:
                message = res.find('div', attrs={'class': 'bbWrapper'}).findAll(
                    text=True, recursive=False)
                message = [x.replace('\n', '') for x in message]
                message = list(filter(None, message))
# print([x.replace('\n', '') for x in list1])
# print([list1.pop(i) for i, v in enumerate(list1) if not v in ['\n']] )
            if message:
                Pages_contents.append({'user': author, 'reply': message})
    # print(json.dumps(Replies))
    # Pages_contents.append(('replies',Replies))

    # Pages_contents['replies'] = Replies
    # Pages_contents['title']=topic_title
    # print(json.dumps(Pages_contents))

    return Pages_contents, topic_title


def get_keyword_search(link):

    soup = getUrl(link)
    Results = soup.findAll(
        'li', attrs={"class": "searchResult post primaryContent"})
    print(Results)
    Comments = []
    Dict = {}

    for res in Results:
        Dict['username'] = res.find('a', attrs={"class": "username"}).text

        title = str(res.find('h3', attrs={"class": "title"}).find('a').text)
        print(title)

        if title.find('</span>'):
            start = title.find('</span>')+len('</span>')
            end = title.find("</a>")
            Dict['title'] = title[start:end]
        else:
            Dict['title'] = res.find('h3', attrs={"class": "title"}).text
        #Dict['Comment'] = res.find('blockquote',attrs={"class":"snippet"}).text
        Dict['link'] = 'https://www.thefastlaneforum.com/community/' + \
            res.find('h3', attrs={"class": "title"}).find('a')["href"]
        print(1, Dict['link'])
        Dict['Pages'] = getMessages(Dict['link'])
    return Dict


def get_topics_links(link):
    print('current  pagination', link)

    soup = getUrl(link)

    Results = soup.findAll(
        'div', attrs={"class": "structItem structItem--thread js-trendingThreadItem"})
#     print(Results)
    topic_links = []
    Dict = {}
    topic_title = ''
    topic_links_results = soup.findAll(
        'div', attrs={"class": "structItem-title"})
#     print(topic_links_results)
    for res in topic_links_results:
        # print('---',res.find('a').attrs["href"])
        topic_links.append('https://www.thefastlaneforum.com' +
                           res.find('a').attrs["href"])
    for res in Results:
        # Dict = {}
        Dict['username'] = res.find('a', attrs={"class": "username"}).text

        title = str(
            res.find('div', attrs={"class": "structItem-title"}).find('a').text)
        print(4, title)

        # Dict['Comment'] =
        max_no = res.find(
            'dl', attrs={"class": "pairs pairs--justified"}).find('dd').text
        # print(Dict['Comment'])
        max_no = max_no.replace('K', '000')

        # if int(max_no) >5:
        Dict['link'] = 'https://www.thefastlaneforum.com' + \
            res.find('div', attrs={
                     "class": "structItem-title"}).find('a').attrs["href"]
        print('当前主题的链接', Dict['link'])
        # topic_links.append('https://www.thefastlaneforum.com'+res.find('div',attrs={"class":"structItem-title"}).find('a').attrs["href"])
        # Dict['Pages'],topic_title = getMessages(Dict['link'])
        Dict['title'] = topic_title
        invalid = '<>:"/\|?*'
        for char in invalid:
            topic_title = topic_title.replace(char, '')
        # with open(topic_title+'.json', 'w') as fp:
        # 	json.dump(Dict, fp)
    # return Dict,topic_title
    # print(json.dumps(topic_links))

    return topic_links


def get_notebale_topics_links(link):
    print('current  pagination', link)

    soup = getUrl(link)

    Results = soup.findAll(
        'div', attrs={"class": "structItem structItem--thread js-trendingThreadItem"})
    print(Results)
    topic_links = []
    Dict = {}
    topic_title = ''
    topic_links_results = soup.findAll(
        'div', attrs={"class": "structItem-title"})
    print(topic_links_results)
    for res in topic_links_results:
        # print('---',res.find('a').attrs["href"])
        topic_links.append('https://www.thefastlaneforum.com' +
                           res.find('a').attrs["href"])
    for res in Results:
        # Dict = {}
        Dict['username'] = res.find('a', attrs={"class": "username"}).text

        title = str(
            res.find('div', attrs={"class": "structItem-title"}).find('a').text)
        print(4, title)

        # Dict['Comment'] =
        max_no = res.find(
            'dl', attrs={"class": "pairs pairs--justified"}).find('dd').text
        # print(Dict['Comment'])
        max_no = max_no.replace('K', '000')

        # if int(max_no) >5:
        Dict['link'] = 'https://www.thefastlaneforum.com' + \
            res.find('div', attrs={
                     "class": "structItem-title"}).find('a').attrs["href"]
        print('当前主题的链接', Dict['link'])
        # topic_links.append('https://www.thefastlaneforum.com'+res.find('div',attrs={"class":"structItem-title"}).find('a').attrs["href"])
        # Dict['Pages'],topic_title = getMessages(Dict['link'])
        Dict['title'] = topic_title
        invalid = '<>:"/\|?*'
        for char in invalid:
            topic_title = topic_title.replace(char, '')
        # with open(topic_title+'.json', 'w') as fp:
        # 	json.dump(Dict, fp)
    # return Dict,topic_title
    # print(json.dumps(topic_links))

    return topic_links
# options

# 0  keywords search results
# 1  notebale topic
# 2 golden topic
# 3 hot topic
# 4 specific topic


def getTopics(Links, option):
    Pages = {}
    # print(3,Links)
    for link in Links:
        # print(2,link)

        #Dict['DateTime'] = res.find('span',attrs={"class":"DateTime"})['title']
        # Comments.append(Dict)
        if option == 0:
            Pages['Page'+str(Links.index(link))] = get_keyword_search(link)
        elif option == 1:
            Pages, topic_title = get_notebale_topics_links(link)

        elif option == 2:
            pass
        elif option == 3:
            pass

    return Pages


def savetopiclink(option, category):
    gold_page_links, newgoldtopiclinks = getCategoryPaginationLink(
        option, '', '')
    goldtopiclinks = []
    if os.path.exists(category+'-topics-links.txt'):
        with open(category+'-topics-links.txt', 'r') as fp:
            goldtopiclinks = fp.readlines()
    # 	# print(json.dumps(alltopiclinks))
    newgoldtopiclinks = list(set(newgoldtopiclinks))
    goldtopiclinks = list(set(goldtopiclinks))
    diff = list(set(newgoldtopiclinks)-set(goldtopiclinks))
    if len(diff) > 0:
        for link in diff:
            if len(goldtopiclinks) == 0:
                with open(category+'-topics-links.txt', 'a+') as fp:

                    fp.write(link+'\n')
            elif link not in goldtopiclinks:
                with open(category+'-topics-links.txt', 'a+') as fp:

                    fp.write(link+'\n')
            else:
                print('no new topic in category')
    else:
        print('no new foundtopic in category')



def process_thread(topic):
    contents, topic_title = (getMessages(topic))


    return contents, topic_title

def downloadcategory(category):
    print('process==', category)
    alltopiclinks = []
    with open(category+'-topics-links.txt', 'r') as fp:
        alltopiclinks = fp.readlines()
    # 	# print(json.dumps(alltopiclinks))
    alltopiclinks = list(set(alltopiclinks))
    donealltopiclinks = []
    if os.path.exists('done-'+category+'-topics-links.txt'):

        with open('done-'+category+'-topics-links.txt', 'r') as fp:
            donealltopiclinks = fp.readlines()
    donealltopiclinks = list(set(donealltopiclinks))
    remainlinks = list(set(alltopiclinks)-set(donealltopiclinks))
    outputdir = 'post/'+category+os.sep
    if os.path.exists(outputdir):

        print('post directory exists', outputdir)
    else:
        os.makedirs(outputdir, exist_ok=True)
        print('create post directory', outputdir)


    if len(remainlinks) > 0:
        for topic in alltopiclinks:
            if not topic in donealltopiclinks:
                print('--process\n', topic)
                contents, topic_title = (getMessages(topic))


                with open(outputdir+topic_title+'.json', 'w') as fp:
                    json.dump(contents, fp)

                with open('done-'+category+'-topics-links.txt', 'a+') as fp:
                    fp.write(topic+'\n')
            print('no new post need to do')
    print('finished==', category)


# savetopiclink(1, 'noteable')
# savetopiclink(2, 'gold')
savetopiclink(3, 'hot')
# savetopiclink(4, 'mostview-six')

# savetopiclink(5, 'mostview-year')
# downloadcategory('noteable')
# downloadcategory('gold')
# downloadcategory('mostview-six')
downloadcategory('hot')
