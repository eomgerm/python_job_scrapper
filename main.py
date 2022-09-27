from requests import get
from bs4 import BeautifulSoup

base_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="
search_term = "python"

res = get(f"{base_url}{search_term}")
if res.status_code != 200:
    print("Can't request website!")
else:
    soup = BeautifulSoup(res.text, "html.parser")
    jobs = soup.find_all('section', class_="jobs")