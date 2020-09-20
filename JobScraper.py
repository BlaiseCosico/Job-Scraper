import time
import pandas as pd

from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC


def find_jobs(link):
    driver.get(link)
    try: 
        search_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "search_job_link"))
            )

        search_btn.click()
    except:
        print("Search Jobs Button not here this time")

    try: 
        search_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "search_job_link"))
            )

        search_btn.click()
    except:
        print("Search Jobs Button not here this time")

    try:

        search_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "searchKeywordsField"))
            )
        search_field.send_keys("Programming")
        

        location_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "locationAutoSuggest"))
            )
        location_field.send_keys("National Capital Reg")
        location_field.send_keys(Keys.RETURN)
        
    except:
        print("Search field not found")

    job_title = []
    job_link = []
    company = []
    location = []
    salary = []
    description = []

    time.sleep(5)
    for i in range(2, 6): #loop of page
        
        try:
            section_div = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, ".//div[@class='FYwKg _31UWZ fB92N_1 _1pAdR_1 FLByR_1 _2QIfI_1 _2cWXo _1Swh0 HdpOi']"))
        )
        except:
            print("Section div not found")
            
        # section_div = driver.find_elements_by_xpath(".//div[@class='FYwKg _31UWZ fB92N_1 _1pAdR_1 FLByR_1 _2QIfI_1 _2cWXo _1Swh0 HdpOi']")
        
        for e in section_div: #loop of job posts per page

            #title
            try:
                title = e.find_element_by_xpath(".//div[@class='FYwKg _2j8fZ_1 sIMFL_1 _1JtWu_1']").text
            except:
                title = "None"

            #job link
            try:
                link = e.find_element_by_xpath(".//a[@class='DvvsL_1 _1p9OP']").get_attribute('href')
            except:
                link = "None"

            #company
            try:
                comp = e.find_element_by_xpath(".//span[@class='FYwKg _1GAuD C6ZIU_1 _1_nER_1 _27Shq_1 _29m7__1']/span[@class='FYwKg _1gtjJ _1GAuD _29LNX']/a[@class='_1p9OP']").text
            except:
                comp = "None"

            #location
            try:
                loc = e.find_element_by_xpath(".//span[@class='FYwKg _1GAuD C6ZIU_1 _1_nER_1 _27Shq_1 sQuda_1']").text
                # loc = e.find_element_by_xpath(".//a[@href='_1p9OP']").text
            except:
                loc = "None"

            #salary
            try:
                sal = e.find_element_by_xpath(".//span[@class='FYwKg _1GAuD C6ZIU_1 _1_nER_1 _27Shq_1 sQuda_1'][2]").text
            except:
                sal = "None"

            desc = []
            try:
                desc_div = e.find_elements_by_xpath(".//div[@class='FYwKg _20Cd9 _32Ekc _3RqUb_1']/span[@class='FYwKg _1GAuD C6ZIU_1 _1_nER_1 _27Shq_1 _29m7__1 _1PM5y_1']")

                for span in desc_div:
                    desc.append(span.text)
            except:
                desc = "None"

            job_title.append(title)
            job_link.append(link)
            company.append(comp)
            location.append(loc)
            salary.append(sal)
            description.append(desc)

        try:
            time.sleep(5)
            next_btn = driver.find_element_by_xpath(f".//a[@href='/en/job-search/programming-jobs-in-national-capital-reg/{i}/']")
            next_btn.click()

            
        except:
            print("next btn not found", i)
            driver.close()
            break

    
    df = pd.DataFrame(columns=["Job Title", "Link", "Company", "Location", "Salary", "Description"])
    df["Job Title"] = job_title
    df["Link"] = job_link
    df["Company"] = company
    df["Location"] = location
    df["Salary"] = salary
    df["Description"] = description

    df.to_excel("Month - Jobstreet Jobs.xlsx")

    print("Done")
    driver.close()
  

if __name__ == '__main__':
    # chromedriver = "./Chromedriver"
    # driver = webdriver.Chrome(chromedriver)
    driver = webdriver.Firefox(executable_path="./geckodriver")
 
    find_jobs("https://www.jobstreet.com.ph")

