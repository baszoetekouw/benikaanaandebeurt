# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import smtplib
from email.message import EmailMessage
from time import sleep
from datetime import datetime

SEND_MAIL = False
SMTP_SERVER = "localhost"
EMAIL_FROM = "ubentaandebeurt@localhost"
EMAIL_TO = ["jan@example.com"]


def benikalaandebeurt(jaar: int) -> bool:
    url = f"https://user-api.coronatest.nl/vaccinatie/programma/bepaalbaar/{jaar}/NEE/NEE"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Got response {response.status_code}")
    json = response.json()
    if "success" not in json:
        raise Exception(f"Got invalid response: '{response.text}'")
    return json["success"] is True


def stuurmail(jaar: int, aan: str) -> None:
    if not SEND_MAIL:
        return

    bericht = f"""
    Goed nieuws!
    Geboortejaar {jaar} is nu aan de beurt voor een Coronavaccinatie.
    Ga nu direct naar https://coronatest.nl/ik-wil-me-laten-vaccineren om een afspraak te maken
    """

    msg = EmailMessage()
    msg.set_content(bericht)
    msg['Subject'] = f"Geboortejaar {jaar} is aan de beurt voor een prik!"
    msg['From'] = EMAIL_FROM
    msg['To'] = ",".join(EMAIL_TO)

    s = smtplib.SMTP(SMTP_SERVER)
    s.send_message(msg)
    s.quit()


def main() -> None:
    jaar: int = 1961
    while True:
        print(f"Wachten tot geboortejaar {jaar} aan de beurt is", end="")
        while not benikalaandebeurt(jaar):
            sleep(600)
            print(".", end="")

        print()
        nu = datetime.now().isoformat(sep=" ", timespec="seconds")

        print(f"Joepie, geboortejaar {jaar} is aan de beurt! ({nu})")
        stuurmail(aan="bas@zoetekouw.net", jaar=jaar)

        jaar += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
