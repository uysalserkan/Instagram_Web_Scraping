import os
import selenium.webdriver as webdir
import time
import urllib.request
from bs4 import BeautifulSoup

INSTAGRAM_LINK = 'https://instagram.com/'


def download_images(usr_id: str):
    counter = 0
    page_counter = 1
    image_len = int(
        input("How many image do you want to download (-1 for all): "))
    usr_url = INSTAGRAM_LINK + usr_id
    #
    driver = webdir.Firefox()
    driver.get(usr_url)

    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    try:
        driver.find_element_by_class_name('tCibT.qq7_A.z4xUb.w5S7h').click()
    except:
        pass

    match = False
    while(match == False):
        lastCount = lenOfPage
        time.sleep(1)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        page_counter += 1

        if (page_counter * 9) / image_len > 1:
            break

        if lastCount == lenOfPage:
            match = True

    usr_posts = []

    soup = BeautifulSoup(driver.page_source, 'lxml')

    source = soup.find_all('div', attrs={'class': 'v1Nh3 kIKUG _bz0w'})

    for link in source:
        usr_posts.append(INSTAGRAM_LINK + usr_id + link.find("a")["href"])

    for post in usr_posts:
        print("Post link:", post)
        driver.get(post)
        shortcode = driver.current_url.split("/")[-2]
        type = driver.find_element_by_xpath(
            '//meta[@property="og:type"]').get_attribute('content')
        if type == 'video':
            download_url = driver.find_element_by_xpath(
                "//meta[@property='og:video']").get_attribute('content')
            urllib.request.urlretrieve(
                download_url, '{}/{}.mp4'.format(usr_id, shortcode))
        else:
            download_url = driver.find_element_by_xpath(
                "//meta[@property='og:image']").get_attribute('content')
            urllib.request.urlretrieve(
                download_url, '{}/{}.jpg'.format(usr_id, shortcode))
        time.sleep(0.75)
        counter += 1
        if counter == image_len:
            break


def main():
    usr_id = input("Please enter instagram user id: ")
    if not os.path.exists(usr_id):
        os.mkdir(usr_id)
    download_images(usr_id=usr_id)


if __name__ == '__main__':
    main()
