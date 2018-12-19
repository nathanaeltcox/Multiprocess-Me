#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests

url = "https://devleague.com"

def get_soup(url):
    content = requests.get(url).content
    return BeautifulSoup(content, "html.parser")

def get_links(url):
    soup = get_soup(url)
    links = soup.find_all("a")
    link_ref = []
    for link in links:
        link_ref.append(link.get("href"))
    return link_ref

def main():
    items = []
    lnk_refs = get_links(url)
    items.append(lnk_refs)
    for link in range(len(lnk_refs)):
        print("Items : {}".format(len(items)))
        lnk_refs = get_links(url + lnk_refs[link])
        items.append(lnk_refs)
        if len(items) > 800:
            break
    f = open("result.txt", "w")
    for item in items:
        f.write(item + "\n")

if __name__ == "__main__":
    main()