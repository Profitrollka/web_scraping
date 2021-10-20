from bs4 import BeautifulSoup as soup
import re
import requests


def receive_page(url, num_of_page):
    """Function generates and returns web address of a page.
    :param url: resource address for scraping.
    :param num_of_page: number of the page.
    :return: url address of the page.
    """
    page_url = '/новостройки-москвы'
    if num_of_page == 1:
        page = url + page_url
    else:
        page = url + page_url + '/?p-' + str(num_of_page)
    return page


def extract_price(text, index):
    """Function extracts digits from the given text and returns the element of the list
     depending on the passed index.
    :param text: text for extracting data.
    :param index: index of the element to get.
    :return: digit
    """
    pattern = r'\d+[.,]\d+'
    prices = text.find_all('div', {'class': 'b-params__value'})[0].text.lstrip()
    matches = re.findall(pattern, prices)
    if index == 0:
        if len(matches) == 1:
            price = matches[index].replace(',', '.')
        else:
            price = ''
    else:
        if len(matches) == 2:
            price = matches[index].replace(',', '.')
        else:
            price = ''
    return price


def main(url, file_name, headers):
    """Function makes web scraping and saves result to the CSV file
    :param url: resource address for scraping.
    :param file_name: file name for save data.
    :param headers: headers for the file.
    """

    with open(file_name, 'w') as f:
        f.write(headers)

    for num in range(1, 11):
        page = receive_page(url, num)
        page_content = requests.get(page).text
        page_content_soup = soup(page_content, 'html.parser')
        announcements = page_content_soup.find_all('div', {'class': 'b-offer-plate__plate'})

        for announcement in announcements:
            name = announcement.a.img['title']
            underground = announcement.find_all('div', {'class': 'b-offer-plate__additional-line'})[0].text.strip()
            terms = announcement.find_all('div', {'class': 'b-offer-plate__additional-line'})[1].text.strip()[6:11]
            one_room_flat = \
                announcement.find_all('div', {'class': 'b-params__label'})[0].text.lstrip().rstrip().split(' ')[0][0]
            square = announcement.find_all('div', {'class': 'b-params__label'})[0].text.lstrip().rstrip().split(' ')[-2]
            price_begin = extract_price(announcement, 0)
            price_end = extract_price(announcement, 1)

            if one_room_flat == '1':
                with open(file_name, 'a') as f:
                    f.write(name + ',' + underground.replace(',', ';') + ',' + terms + ',' + one_room_flat + ',' +
                            square + ',' + price_begin + ',' + price_end + "\n")


if __name__ == "__main__":
    main(url='https://vsenovostroyki.ru', file_name='flats.csv',
         headers='ЖК, Метро, Срок сдачи, Количество комнат, Площадь (кв.м), Цена от (млн. руб), Цена до (млн. руб)\n')
