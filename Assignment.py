from bs4 import BeautifulSoup
import requests
import csv

try:
    session = requests.Session()
    base_url = "https://www.stfrancismedicalcenter.com/find-a-provider/"
    source = session.get(base_url)
    source.raise_for_status()  # this is used to check if url is valid. If url is a invalid then it will raise an error.
    c = session.cookies.get_dict()

    soup = BeautifulSoup(source.text, "html.parser")
    content = soup.find("div", class_="doctor-results")
    page_no = int(content.find('footer').find('span', class_="end").string)

    data = {"headers": {
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "Referer": "https://www.stfrancismedicalcenter.com/find-a-provider/",
        "Referrer-Policy": "no-referrer-when-downgrade"
    },
        "body": "_m_=FindAPhysician&PhysicianSearch%24HDR0%24PhysicianName=&PhysicianSearch%24HDR0%24SpecialtyIDs=&PhysicianSearch%24HDR0%24Distance=5&PhysicianSearch%24HDR0%24ZipCodeSearch=&PhysicianSearch%24HDR0%24Keywords=&PhysicianSearch%24HDR0%24LanguageIDs=&PhysicianSearch%24HDR0%24Gender=&PhysicianSearch%24HDR0%24InsuranceIDs=&PhysicianSearch%24HDR0%24AffiliationIDs=&PhysicianSearch%24HDR0%24NewPatientsOnly=&PhysicianSearch%24HDR0%24InNetwork=&PhysicianSearch%24HDR0%24HasPhoto=&PhysicianSearch%24FTR01%24PagingID={}"
    }

    doctors = []
    for i in range(1, page_no + 1):
        source = requests.post(base_url, data=data['body'].format(str(i)), headers=data['headers'], cookies=c)
        soup = BeautifulSoup(source.text, "html.parser")
        content = soup.find("div", class_="doctor-results")
        table = content.find("ul").find_all('li', class_='half')

        for tr in table:
            link = "https://www.stfrancismedicalcenter.com" + tr.find('a')['href']
            if link == "https://www.stfrancismedicalcenter.com":
                continue
            doctors.append(link)

    print("========================", len(doctors), '==========================')

    with open('scrap_data.csv', 'w', newline="") as f:
        field_name = ["Full_Name", "Specialty", "Add_Specialty", "Full_Address", "Practice", "Address", "City", "State",
                      "Zip", "Phone", "URL"]
        write = csv.DictWriter(f, fieldnames=field_name)
        write.writeheader()

        x = 1
        for doc_url in doctors:
            # for _ in range(1):
            #     doc_url = "https://www.stfrancismedicalcenter.com/find-a-provider/ryan-n-chan-pa/"

            print(x, doc_url)
            x += 1

            Full_Name = None
            Specialty = None
            Add_Specialty = None
            Full_Address = None
            Practice = None
            Address = None
            City = None
            State = None
            Zip = None
            Phone = None
            URL = None

            # for checking
            flag = False

            doc_page = requests.get(doc_url)
            doc_soup = BeautifulSoup(doc_page.text, "html.parser")
            doc_content = doc_soup.find('body').find("main", id="MainZone").find('section').find('div', class_="main")
            try:
                Full_Name = doc_content.find("section",
                                             class_="system-style system-entry no-padding physician ui-repeater").get_text(
                    strip=True)
                if flag:
                    print('Full_Name ===>', Full_Name)
            except:
                if flag:
                    print('Full_Name ===>', Full_Name)
            try:
                Specialty = doc_content.find('div', class_="sub-zone content-zone").find('li',
                                                                                         class_="full flex-between-spaced-middle-wrap-block-550 mar-b-tiny ui-repeater").find(
                    'span').get_text(strip=True)
                if flag:
                    print('Specialty ===>', Specialty)
            except:
                if flag:
                    print('Specialty ===>', Specialty)
            try:
                Add_Specialty = doc_content.find('div', class_="sub-zone content-zone").find('li',
                                                                                             class_="flex-between-spaced-middle-wrap-block-550 mar-b-tiny ui-repeater").find(
                    'span').get_text(strip=True)
                if flag:
                    print('Add_Specialty ===>', Add_Specialty)
            except:
                if flag:
                    print("Add_Specialty ===>")
            try:
                doc_address = doc_content.find('div', class_="sub-zone content-zone").find('div',
                                                                                           class_="physician-locations content-style ui-repeater").find(
                    'ul', class_="full")

                if flag:
                    print(doc_address.prettify())

                try:
                    Practice = doc_address.strong.get_text()
                    if flag:
                        print('Practice ===>', Practice)
                except:
                    if flag:
                        print('Practice ===>')
                    Practice = ""
            except:
                pass
            try:
                Address = doc_address.find('address').get_text().split("\n")[0]
                if flag:
                    print('Address ===>', Address)

                Full_Address = Practice + " " + Address
                if flag:
                    print('Full_Address ===>', Full_Address)

                City = Address.split(" ")[-3].replace(",", "")
                if flag:
                    print('City ===>', City)

                State = Address.split(" ")[-2]
                if flag:
                    print('State ===>', State)

                Zip = Address.split(" ")[-1]
                if flag:
                    print('Zip ===>', Zip)

                Phone = doc_address.a.get_text(strip=True)
                if flag:
                    print('Phone ===>', Phone)

                URL = doc_url
                if flag:
                    print("URL ===>", URL)
            except:
                pass

            if URL:
                write.writerow({
                    "Full_Name": Full_Name,
                    "Specialty": Specialty,
                    "Add_Specialty": Add_Specialty,
                    "Full_Address": Full_Address,
                    "Practice": Practice,
                    "Address": Address,
                    "City": City,
                    "State": State,
                    "Zip": Zip,
                    "Phone": Phone,
                    "URL": URL
                })


except Exception as e:
    print(e)
