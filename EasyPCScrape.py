import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC

def getProducts():
    try:
        elements = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "bc-sf-filter-product-bottom"))
            )


        products = {e.find_element_by_tag_name("a").text : e.find_element_by_class_name("hidePrice").text.encode('utf-8') for e in elements}

    except: 
        print("products not found")

    return products


def pagination():

    #either xpath start at one
    #or while loop to check if next page is existing
    current_page_num = 1
    products = {}
    while True:
        try:
            products.update(getProducts())
            current_page_num += 1
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            pagination_div = browser.find_element_by_id("bc-sf-filter-bottom-pagination")
            page = pagination_div.find_element_by_xpath(f'.//li/a[@href = "https://easypc.com.ph/search?page={current_page_num}&type=product&q=videocard"]')
            page.click()
            time.sleep(10)
            
            print(f'current page: {current_page_num}')
        except:
            print(f"Exiting. Last page: {current_page_num}.")
            browser.close()
            break
    

    return products


if __name__ == '__main__':
    browser = webdriver.Firefox(executable_path="./geckodriver")
    browser.get('http://www.easypc.com.ph')

    browser.find_element_by_class_name('velaSearchIcon').click()
    search = browser.find_element_by_name('q')

    search.send_keys("videocard")
    search.send_keys(Keys.RETURN) # hit return after you enter search text
    time.sleep(10) # time.sleep(10) sleep for 10 seconds so you can see the results

    print(pagination())
    




