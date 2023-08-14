import requests
from bs4 import BeautifulSoup

def get_page_soup(url):
    headers = {
    "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    return soup

def get_name_deputies(soup, db:list):
    base_url = "https://www.assemblee-nationale.fr/dyn/deputes/"
    ul_deputies = soup.find_all("ul",attrs={"class": "col3"})
    for i in ul_deputies:
        li_deputies = i.find_all("li")
        for j in li_deputies:
            a_deputies = j.find("a").text
            deputy_link = j.a.get("href")
            cleaned_link = deputy_link.replace('/deputes/fiche/OMC_', '')
            target_URL = base_url + cleaned_link 
            deputy = {
                "details_link" : target_URL,
                "deputy_name" : a_deputies                   
            }
            db.append(deputy)
    return db

def get_deputy_details(db):
    headers = {
    "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
    }
    counter = 1
    for deputy in db:
        detailsPage = requests.get(deputy["details_link"], headers=headers)
        soup = BeautifulSoup(detailsPage.content, "lxml")
        div_container = soup.find_all("div" , attrs={"class" : "_gutter-xxs _vertical"})
        for i in div_container:
            p_biographie = i.find("p").text
            deputy["biographie"] = p_biographie
        for i in div_container:
            a_commission = i.find("a").text
            deputy["commission"] = a_commission
        for i in div_container:
            ul_circonscription = i.find_all("ul", attrs={"class": "_no-style _gutter-xxxs _vertical"})
            for i in ul_circonscription:
                span_circonscription = i.find_all("span")
                for i in span_circonscription:
                    if not i.has_attr("class"):
                        noneLabelSpans = i.get_text()
                        deputy["contactInfos"] = noneLabelSpans
                    else:
                        pass
        ul_mailadress = soup.find_all("ul", attrs={"class": "pipe-list _pb-small _justify-center"})
        for i in ul_mailadress:
            span_mailadress = i.find_all("span")
            for i in span_mailadress:
                if not i.has_attr("class"):
                    p_mailadress = i.get_text()
                    deputy["mailadress"] = p_mailadress
        print(f"{counter}. deputy is prepared")
        counter += 1
    return db