from bs4 import BeautifulSoup
import requests
import csv


def crawl_main():
    num = 1

    url1 = 'https://urlhaus-api.abuse.ch/v1/urls/recent/'
    url2 = 'https://www.phishtank.com/phish_search.php?page={}&Search=Search'.format(num)
    url3 = "https://www.sites.google.com/site/top10000alexadomains/top-10000-alexa-domains"


    page3 = requests.get(url3)
    resource_3 = []

    soup = BeautifulSoup(page3.content, 'html.parser')

    mydivs = soup.find_all("table", {"class": "sites-layout-name-one-column sites-layout-hbox"})[0]
    count = 0
    valid_urls = []

    tr = mydivs.find_all('tr')[0]
    tds = tr.find_all('td')
    all_urls_not_parsed = tds[0].text.split('\n')
    table_len = len(all_urls_not_parsed)
    for i in range(0, table_len):
        valid_urls.append(all_urls_not_parsed[i].split(' ')[2])
        count += 1

    print(count)
    with open('legit_urls.csv', "w") as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        for line in valid_urls:
            writer.writerow([line])


    page1 = requests.get(url1)
    resource_1 = [url['url'] for url in page1.json()['urls']]
    for i in range(1, 225):
        url2 = 'https://www.phishtank.com/phish_search.php?page={}&Search=Search'.format(i)
        page2 = requests.get(url2)

        soup = BeautifulSoup(page2.content, 'html.parser')

        mydivs = soup.find_all("table", {"class": "data"})[0]

        for tr in mydivs.find_all('tr')[2:]:
            tds = tr.find_all('td')
            resource_1.append(tds[1].text.split('added')[0])


    with open('verified_online.csv', "w") as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        for line in resource_1:
            writer.writerow([line])
    print("Done")