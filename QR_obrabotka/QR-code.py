import requests
import datetime
from PIL import Image
from pyzbar.pyzbar import decode

headers = {
    "accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) "
                  "Version/11.0 Mobile/15A5341f Safari/604.1"
}


def get_data_from_QR(name_img):
    data = decode(Image.open(name_img))
    data_href = str(data[0][0]).replace("b'", "").replace("'", "")
    return data_href


def comparison(now, expiration):
    e = expiration.split(".")
    expiration_day, expiration_month, expiration_year = int(e[0]), int(e[1]), int(e[2])
    expiration_month = int(expiration.split(".")[1])
    expiration_year = int(expiration.split(".")[2])
    if expiration_year > now.year or (expiration_year == now.year and
                                      (expiration_month > now.month or (expiration_month == now.month
                                                                        and expiration_day > now.day))):
        return True
    return False


def get_data_from_json(url, value):
    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        response = response.json()
        now = datetime.datetime.now()

        if value == 1:
            unrz = response['unrz']
            print(unrz)

            FIO = response['fio'].replace("*", "")
            print(FIO)

            birthDate = response['birthdate']
            print(birthDate)

            passport = response['doc'].replace("*", "")
            print(passport)

            expiration = response['expiredAt']
            print(expiration)

            if comparison(now, expiration):
                return "successfully"
            return "unsuccessful"

        elif value == 2:
            unrz = response['items'][0]['unrz']
            print(unrz)

            FIO = response['items'][0]['attrs'][0]['value'].replace("*", "")
            print(FIO)

            birthDate = response['items'][0]['attrs'][1]['value']
            print(birthDate)

            passport = response['items'][0]['attrs'][2]['value'].replace("*", "")
            print(passport)

            expiration = response['items'][0]['expiredAt']
            print(expiration)

            if comparison(now, expiration):
                return "successfully"
            return "unsuccessful"

        elif value == 3:
            unrz = response['items'][0]['unrz']
            print(unrz)

            FIO = response['items'][0]['attrs'][2]['value'].replace("*", "")
            print(FIO)

            birthDate = response['items'][0]['attrs'][4]['value']
            print(birthDate)

            passport = response['items'][0]['attrs'][3]['value'].replace("*", "")
            print(passport)

            expiration = response['items'][0]['expiredAt']
            print(expiration)

            if comparison(now, expiration):
                return "successfully"
            return "unsuccessful"
    else:
        return "unsuccessful"


def get_expiration(data_href):
    data_href_1 = data_href.split("/")[-1]
    print(data_href)

    if "vaccine" in data_href:
        data_url = f"https://www.gosuslugi.ru/api/vaccine/v1/cert/verify/{data_href_1}"
        value = 1
    elif "covid-cert/status" in data_href:
        data_url = f"https://www.gosuslugi.ru/api/covid-cert/v2/cert/status/{data_href_1}"
        value = 2
    elif "covid-cert/verify" in data_href:
        data_url = f"https://www.gosuslugi.ru/api/covid-cert/v3/cert/check/{data_href_1}"
        value = 3
    else:
        return "unsuccessful"

    return get_data_from_json(data_url, value)


def main():
    data_href = get_data_from_QR("Ars_2.png")
    expiration = get_expiration(data_href)
    if expiration == "successfully":
        print("Congratulations, the QR code is entered into the database")
    else:
        print("Oops.. The code is not recognized, try again!")

    data_href = get_data_from_QR("Mum_new.png")
    expiration = get_expiration(data_href)
    if expiration == "successfully":
        print("Congratulations, the QR code is entered into the database")
    else:
        print("Oops.. The code is not recognized, try again!")

    data_href = get_data_from_QR("Mum_old.png")
    expiration = get_expiration(data_href)
    if expiration == "successfully":
        print("Congratulations, the QR code is entered into the database")
    else:
        print("Oops.. The code is not recognized, try again!")



if __name__ == "__main__":
    main()

# https://www.gosuslugi.ru/api/vaccine/v1/cert/verify/10ca491e-445e-4056-bcb7-bd42e5962863
# https://www.gosuslugi.ru/api/covid-cert/v2/cert/status/a88bfcc7-f65d-4f7f-9f8e-8fa907eff13d?lang=ru
