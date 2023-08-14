from functions import get_name_deputies, get_page_soup, get_deputy_details

def main(url):   
    db = []
    soup = get_page_soup(url)
    db = get_name_deputies(soup, db)
    db = get_deputy_details(db)
    print(db)

if __name__ == "__main__":
    URL = 'https://www2.assemblee-nationale.fr/deputes/liste/alphabetique'
    main(URL)    