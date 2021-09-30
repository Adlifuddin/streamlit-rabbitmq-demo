from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")

def crawler(links):
    temp = []
    for l in range(len(links)):

        #  for local
        driver = webdriver.Chrome('../driver/chromedriver.exe')

        # # for docker
        # driver = webdriver.Remote("http://selenium:4444/wd/hub", options=chrome_options)

        driver.get(links[l])

        text = driver.find_elements_by_xpath('//div[@class="field field-body"]/p')

        for p in range(len(text)):
            if text[p].text != '':
                temp.append(text[p].text)

        driver.close()
    
    return temp

