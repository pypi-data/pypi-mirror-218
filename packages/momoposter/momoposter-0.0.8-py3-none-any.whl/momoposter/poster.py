from telegraph import Telegraph
import random
import os
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import wait
import spintax

def pickAnchor():
    anchors = ["Learn more", "View Source", "Visit Site", "Original Content", "Reference", "Citation", "Visit Here", "Official source", "See page", "Find Out More", "View it", "Full Article", "Original Article", "Read Full Report", "Click here to find out more", "Published here", "Original source", "Visit the site", "Click for source", "More information", "Site link", "View now", "Resource", "Click here for more info", "Extra resources", "Click here for more", "Click here for info", "See original website", "Visit Them", "Click Here", "Source"]
    anchor = random.choice(anchors)
    return anchor


def listToArray(file):
    list = []
    with open(file) as f:
        for line in f:
            # in alternative, if you need to use the file content as numbers
            # inner_list = [int(elt.strip()) for elt in line.split(',')]
            line = line.strip('\n')
            list.append(line)
    return list



def getTierLinks(links):
    choices = listToArray(links)
    return random.choice(choices)


def pickArticle(articles):
    res = []
    # Iterate directory
    for file in os.listdir(articles):
        # check only text files
        if file.endswith('.txt'):
            res.append(file)
    choice = random.choice(res)
    article = articles + '/' + choice
    return article


def genContentFromSpintax(content):
    result = spintax.spin(content)
    return result


def getTitle(article):
    with open(article, 'r') as fp:
        first_item = fp.readline().strip()
    result = genContentFromSpintax(first_item)
    # print(result)
    return result


def getContent(article):
    with open(article, 'r') as fp:
        first_item = fp.readline().strip()
    content = open(article, 'r').read()
    content = content.replace(first_item, "")
    content = genContentFromSpintax(content)
    # print(content)
    return content


def createTelegraPost(links, articles):
    try:
        article = pickArticle(articles)
        title = getTitle(article)
        content = getContent(article)
        title = title.replace("\n", "")
        telegraph = Telegraph()
        short_name = str(random.randint(300, 9999999))
        telegraph.create_account(short_name=short_name)
        linkUrl = getTierLinks(links)
        anchor = pickAnchor()
        content = content + " <a href='" + linkUrl + "'>" + anchor + "</a>"
        response = telegraph.create_page(
            title,
            html_content=content
            )
        createdUrl = response['url']
        with open('createdUrls.txt', 'a') as file:
            file.writelines(createdUrl + "\n")
        file.close()
    except Exception:
        pass


def buildLinks(links, articles):
    threadList = []
    with ThreadPoolExecutor() as executor:
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        threadList.append(executor.submit(createTelegraPost(links, articles)))
        # threadList.append(executor.submit(buildTheJuiceComments))
    wait(threadList)


def juiceIt(links, articles):
    x = 0
    cycle = 0
    while x == 0:
        buildLinks(links, articles)
        cycle = cycle + 1
        print(str(cycle * 100) + " pages created!")

