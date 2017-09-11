from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import re
import requests
import json

# urlが列挙されたcsvファイルを指定する
url = "https://github.com/your/repository"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

p = urlparse(url)
response = urllib.request.urlopen(url)
# ココらへんはお決まりのBeautifulSoupの流れ〜
html = response.read()
soup = BeautifulSoup(html, "lxml")
html_list = soup.find_all(class_="js-navigation-item")
list = []
for s_html in html_list:
    list.append(s_html.find(class_="content"))
files = []
for s_file in list:
    if s_file != None:
        files.append(s_file.text.strip("\n").strip("."))
words = []
for file in files:
    url = "https://raw.githubusercontent.com/your/repository/master/" + file
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    a_text = soup.body.text
    words.extend(re.split(r'\s|\,|\.|\(|\)', a_text.lower()))
r = [i for i in words if i != ""]
text = "You have written " + str(len(r)) + "words totally."
requests.post('YOUR_SLACK_WEBHOCK_API', data = json.dumps({
    'text':text,
    'username': "Today's report",
    'link_names': 1
}))
