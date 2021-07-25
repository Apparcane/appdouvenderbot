import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

number = 18
link = "www.ksau.kherson.ua/files/raspisanie/" + str(number) + "%20тиждень.rar"
# link = "http://www.ksau.kherson.ua/files/raspisanie/?C=M;O=A"

# f = open(r'D:\projects\appdouvenderbot\temp\123.zip', "wb")

r = requests.get(link)
print(r)
# f.write(r.content)
# f.close()
