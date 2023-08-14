from bs4 import BeautifulSoup
import requests

URL = 'https://www2.assemblee-nationale.fr/deputes/liste/alphabetique'
headers = {
    "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
    }
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, "lxml")
deputies = []
links = []
biographie = []
commission = []
contactInfos = []
mailadress = []
base_url = "https://www.assemblee-nationale.fr/dyn/deputes/"
ul_deputies = soup.find_all("ul",attrs={"class": "col3"})
for i in ul_deputies:
    li_deputies = i.find_all("li")
    for i in li_deputies:
        a_deputies = i.find("a").text
        link_deputies = i.a.get("href")
        links.append(link_deputies)
        deputies.append(a_deputies)
cleaned_links = [link.replace('/deputes/fiche/OMC_', '') for link in links]
target_URL = [base_url + i for i in cleaned_links]
for i in target_URL:
    detailsPage = requests.get(i, headers=headers)
    soup = BeautifulSoup(detailsPage.content, "lxml")
    div_container = soup.find_all("div" , attrs={"class" : "_gutter-xxs _vertical"})
    for i in div_container:
        p_biographie = i.find("p").text
        biographie.append(p_biographie)
    for i in div_container:
        a_commission = i.find("a").text
        commission.append(a_commission)
    for i in div_container:
        ul_circonscription = i.find_all("ul", attrs={"class": "_no-style _gutter-xxxs _vertical"})
        for i in ul_circonscription:
            span_circonscription = i.find_all("span")
            for i in span_circonscription:
                if not i.has_attr("class"):
                    noneLabelSpans = i.get_text()
                    contactInfos.append(noneLabelSpans)
                    print(noneLabelSpans)
                else:
                    pass
    ul_mailadress = soup.find_all("ul", attrs={"class": "pipe-list _pb-small _justify-center"})
    for i in ul_mailadress:
        span_mailadress = i.find_all("span")
        for i in span_mailadress:
            if not i.has_attr("class"):
                p_mailadress = i.get_text()
                mailadress.append(p_mailadress)