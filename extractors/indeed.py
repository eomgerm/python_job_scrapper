from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def open_browser():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(options=options)
    return browser

def extract_indeed_jobs(keyword):
    browser = open_browser()

    base_url = 'https://kr.indeed.com/jobs?q='
    search_term = keyword

    browser.get(f'{base_url}{search_term}')
    res = browser.page_source

    soup = BeautifulSoup(res, "html.parser")
    job_list = soup.find("ul", class_="jobsearch-ResultsList")
    jobs = job_list.find_all("li", recursive=False)

    for job in jobs:
        results = []
        zone = job.find("div", class_="mosaic-zone")
        if zone == None:
            anchor = job.select_one("h2 a")
            title = anchor['aria-label']
            link = anchor['href']
            company = job.find("span", class_="companyName")
            location = job.find("div", class_="companyLocation")
            job_data = {
                'link': f"https://indeed.com{link}",
                'company': company.string,
                'location': location.string,
                'position': title
            }
            results.append(job_data)
        return results