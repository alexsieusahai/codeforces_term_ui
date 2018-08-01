import webStash
from bs4 import BeautifulSoup


def scrape_problem_page(contestId, index):
    stash = webStash.WebStash()
    link_stem = 'http://codeforces.com/problemset/problem/'
    link = link_stem + '/' + contestId + '/' + index
    html = stash.get_web_data(link).html
    soup = BeautifulSoup(html, 'lxml')
    problem_header_elem = soup.select('div.problem-statement')[0]
    for div in problem_header_elem.find_all('div', recursive=False)[1:]:
        print(div.get_text())


if __name__ == "__main__":
    scrape_problem_page('1000', 'A')
