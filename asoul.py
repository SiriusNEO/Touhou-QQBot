from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import json
import time
from constant import *
import random


def random_writing():
    random.seed()
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(executable_path=r'C:\Users\17138\Desktop\Mirai\Graia\chromedriver.exe',
                               chrome_options=chrome_options)

    browser.get('https://asoulcnki.asia/rank?')
    browser.get('https://asoulcnki.asia/rank?')

    time.sleep(0.2)

    page_input = browser.find_element_by_class_name('page-input')

    print(page_input)

    ActionChains(browser).double_click(page_input).perform()
    time.sleep(0.2)
    page_num = random.randint(1, PAGE_NUM)
    page_input.send_keys(str(page_num))
    ActionChains(browser).move_by_offset(200, 100).click().perform()

    time.sleep(0.2)

    html = browser.page_source

    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find_all(name='div', attrs={'class':'article-content'})

    article_index = random.randint(1, len(articles))

    time.sleep(ASOUL_WAIT)

    return articles[article_index-1].text


def check_duplicate(text: str):
    random.seed()
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(executable_path=r'C:\Users\17138\Desktop\Mirai\Graia\chromedriver.exe',
                               chrome_options=chrome_options)

    browser.get('https://asoulcnki.asia/')

    input_textarea = browser.find_element_by_tag_name('textarea')
    checkbox = browser.find_element_by_class_name('el-checkbox')
    xpath = "//button[@class='text-button button submit-ready']"
    submit_button = browser.find_element_by_xpath(xpath)

    print(submit_button)

    ActionChains(browser).click(input_textarea).perform()
    time.sleep(0.2)
    input_textarea.send_keys(text)
    checkbox.click()
    time.sleep(0.2)
    ActionChains(browser).click(submit_button).perform()

    time.sleep(0.2)

    html = browser.page_source

    soup = BeautifulSoup(html, 'html.parser')

    data_list = soup.find_all(name='ul')

    info_dict = dict()

    if len(data_list) > 1:
        contents = data_list[1].contents
        for i in range(len(contents)):
            print(i, contents[i])
        info_dict['time'] = contents[0].text
        info_dict['rate'] = contents[2].text
        info_dict['author'] = contents[4].text
        info_dict['author'] = info_dict['author'].replace(' ', '')
        info_dict['author'] = info_dict['author'].replace('\n', '')
        info_dict['author'] = info_dict['author'].replace(':', ': ')
        content_str = str(contents[6])
        pattern = 'https://www.bilibili.com/video/'
        pos = content_str.find(pattern)
        for i in range(pos+1, len(content_str)-1):
            if content_str[i] == "\"":
                content_str = content_str[pos : i]
                break
        info_dict['link'] = content_str

    time.sleep(ASOUL_WAIT)

    return info_dict

