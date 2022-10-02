from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)

    results = []
    for page in range(pages):
        browser = open_browser()

        base_url = 'https://kr.indeed.com/jobs'
        target_url = f'{base_url}?q={keyword}&start={page*10}'
        print("Requesting...", target_url)

        browser.get(target_url)
        res = browser.page_source

        soup = BeautifulSoup(res, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)

        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")
                job_data = {
                    'link': f"https://indeed.com{link}",
                    'company': company.string.replace(',', ' ') if company.string != None else " ",
                    'location': location.string.replace(',', ' ') if location.string != None else " ",
                    'position': title.replace(',', ' ') if title != None else " "
                }
                results.append(job_data)
    return results

def open_browser():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(options=options)
    return browser

def get_page_count(keyword):
    browser = open_browser()
    
    base_url = 'https://kr.indeed.com/jobs?q='

    browser.get(f'{base_url}{keyword}')
    res = browser.page_source

    soup = BeautifulSoup(res, "html.parser")
    pagination = soup.find("ul", class_="pagination-list")
    if pagination == None:
        return 1
    pages = pagination.find_all("li", recursive=False)
    count = len(pages)
    if count >= 5:
        return 5
    else:
         return count