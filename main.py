import unittest
import logging
import pandas as pd
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from ru_key import type as t
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument(f'--profile={os.getenv("PROFILE_PATH")}')
        self.counter = 0
        self.driver = webdriver.Firefox(options=options)

    def test_messages(self):

        logging.info(f"{'-' * 5}Запуск файла{'-' * 5}")

        file_path = 'Обращения в техподдержку.xlsx'
        df = pd.read_excel(file_path)

        for index, row in df.iterrows():
            organization = row['Организация']
            number_date = row['Договор / Отчет']
            data_type = row['Тип']
            sout_id = row['ID']
            status = row['Статус']

            da = row['Дата последнего обращения']

            last_date = pd.to_datetime(row['Дата последнего обращения'], errors='coerce').date() if not pd.isna(
                da) else None

            if pd.isna(number_date):
                break

            if last_date == datetime.now().date():
                continue

            logging.info(f"Открываем и заполняем письмо {number_date}")

            driver = self.driver
            driver.get("https://e.mail.ru/templates/")

            # template
            template_xpath = '//*[@id="app-canvas"]/div/div[1]/div[1]/div/div[2]/span/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/div/a'

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, template_xpath))
            )

            element = driver.find_element(By.XPATH, template_xpath)
            element.click()

            # send text
            text_xpath = '//*[@id="style_17017587461547243630_BODY_mr_css_attr"]/div/div[2]/span[3]'

            time.sleep(5)

            title_element = driver.find_element(By.XPATH,
                                                '//input[@class="container--H9L5q size_s--3_M-_"][@type="text"][@name="Subject"][@tabindex="400"]')
            title_element.send_keys(
                f'{f" - повторно" if status in ("Повторно", "Первично") else ""}, организация - {organization}')

            element = driver.find_element(By.XPATH, text_xpath)
            element.click()
            element.clear()

            text_type = None

            match data_type:
                case 'Присвоение ID':
                    text_type = f'в информационную систему учета сведений о заключении с работодателем {organization} по гражданско-правовому договору № {number_date} о проведении СОУТ и получения для предстоящей СОУТ ID'
                case 'Загрузка отчета':
                    sout_id = f'({int(sout_id)})' if sout_id else ''
                    text_type = f'во ФГИС сведений о результатах проведения СОУТ в организации {organization} по гражданско-правовому договору № {number_date}{sout_id}'

            t(f' {text_type}', 0.1)

            file_input = driver.find_element(By.XPATH, '//input[@class="desktopInput--3cWPE"]')

            current_file = os.path.realpath(__file__)
            current_directory = os.path.dirname(current_file)

            file_input.send_keys(fr"{current_directory}\Текущий.png")

            time.sleep(5)

            send_message = driver.find_element(By.XPATH, '//button[@data-test-id="send"]')
            send_message.click()

            logging.info(f"Отправляем письмо {number_date}")

            current_date = datetime.now().date()
            current_date_np = pd.to_datetime(current_date)

            df.loc[df['Договор / Отчет'] == number_date, 'Дата последнего обращения'] = current_date_np

            match status:
                case 'Не отправлено':
                    status = 'Первично'
                    if not os.path.isdir(fr'{os.getenv("SCREEN_LINK_PATH")}\{organization}'):
                        os.mkdir(fr'{os.getenv("SCREEN_LINK_PATH")}\{organization}')

                case 'Первично':
                    status = 'Повторно'

            df.loc[df['Договор / Отчет'] == number_date, 'Статус'] = status

            if pd.isna(row['Ссылка на скрин']):
                df.loc[df[
                           'Договор / Отчет'] == number_date, 'Ссылка на скрин'] = fr'{os.getenv("SCREEN_LINK_PATH")}\{organization}'

            df.to_excel(file_path, index=False)

            self.counter += 1

            logging.info(f"{'-' * 5}Обновляем Excel{'-' * 5}")

            time.sleep(5)

        logging.info(f"Писем отправлено - {self.counter}")
        logging.info(f"{'-' * 5}Конец Файла{'-' * 5}")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":

    unittest.main()
