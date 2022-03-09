from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import json
import time
from constant import *
import random


def is_Chinese(ch):
    if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


class Fetcher:

    def __init__(self):
        return
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        # chrome_options.add_argument("window-size=1024,768")
        # 添加沙盒模式
        chrome_options.add_argument("--no-sandbox")

        self.writing_browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver',
                                   chrome_options=chrome_options)
        self.writing_browser.maximize_window()

        self.writing_browser.get('https://asoulcnki.asia/rank')
        time.sleep(0.2)
        self.writing_browser.get('https://asoulcnki.asia/rank')
        time.sleep(0.2)
        self.writing_browser.get('https://asoulcnki.asia/rank')

        chrome_options = Options()
        chrome_options.add_argument('--headless')

        chrome_options.add_argument('--disable-gpu')

        # chrome_options.add_argument("window-size=1024,768")
        # 添加沙盒模式
        chrome_options.add_argument("--no-sandbox")

        self.cnki_browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver',
                                   chrome_options=chrome_options)

        select_button = self.writing_browser.find_element_by_xpath("//span[@class='filter-button']")
        select_button.click()
        all_time_button = self.writing_browser.find_element_by_xpath("//div[contains(text(),'全部时间')]")
        all_time_button.click()
        self.writing_browser.find_element_by_xpath("//button[@class='button submit']").click()

        self.cnki_browser.get('https://asoulcnki.asia/')
        checkbox = self.cnki_browser.find_element_by_class_name('el-checkbox')
        checkbox.click()

    def __del__(self):
        self.writing_browser.quit()
        self.cnki_browser.quit()

    def random_writing(self):
        random.seed()

        time.sleep(0.2)

        page_input = self.writing_browser.find_element_by_class_name('page-input')
        next_page = self.writing_browser.find_element_by_xpath("//span[contains(text(),'下一页')]")
        print(page_input)

        ActionChains(self.writing_browser).double_click(page_input).perform()
        time.sleep(0.2)
        page_num = random.randint(1, PAGE_NUM)
        page_input.send_keys(str(page_num))

        ActionChains(self.writing_browser).click(next_page).perform()

        time.sleep(3)

        html = self.writing_browser.page_source

        soup = BeautifulSoup(html, 'html.parser')

        articles = soup.find_all(name='div', attrs={'class': 'article-text'})

        article_index = random.randint(1, len(articles))

        time.sleep(ASOUL_WAIT)

        return articles[article_index - 1].text


    def check_duplicate(self, text: str):
        random.seed()
        self.cnki_browser.get('https://asoulcnki.asia/')
        tmp = str()
        for ch in text:
            if is_Chinese(ch) or ch.isascii():
                tmp += ch
        text = tmp
        input_textarea = self.cnki_browser.find_element_by_tag_name('textarea')

        xpath = "//button[@class='text-button button submit-ready']"
        submit_button = self.cnki_browser.find_element_by_xpath(xpath)

        ActionChains(self.cnki_browser).double_click(input_textarea).perform()
        time.sleep(0.2)
        input_textarea.send_keys(text)

        time.sleep(0.2)
        ActionChains(self.cnki_browser).click(submit_button).perform()

        time.sleep(0.2)

        html = self.cnki_browser.page_source

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
            pattern = 'https://'
            pos = content_str.find(pattern)
            for i in range(pos + 1, len(content_str) - 1):
                if content_str[i] == "\"":
                    content_str = content_str[pos: i]
                    break
            content_str = content_str.replace(" ", "")
            info_dict['link'] = content_str

        time.sleep(ASOUL_WAIT)

        return info_dict
