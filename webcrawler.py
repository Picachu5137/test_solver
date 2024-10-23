import re
import random
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

from terma import TermArt


CHROMEDRIVER_PATH = "./chromedriver"


class TestSolver(webdriver.Chrome):
    SITE_LOGIN_URL = "http://test.appo.iac.spb.ru/Account/Login"
    
    def __init__(self, timeout: int = 6):
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        super().__init__(service=Service(CHROMEDRIVER_PATH), options=options)
        self.timeout = timeout

    def login(self, student_data: dict):
        """
        login with student_data
        student_data must contain following keys:
        student_number: str
        district_code: str
        organization_code: str
        password: str
        
        """
        self.get(TestSolver.SITE_LOGIN_URL)
        
        student_number = self.find_element(By.NAME, "StudentNumber")
        student_number.send_keys(student_data.get("student_number"))

        district_code = Select(self.find_element(By.NAME, "DistrictCode"))
        district_code.select_by_value(student_data.get("district_code"))
        
        organization_code = self.find_element(By.NAME, "OrganizationCode")
        organization_code.send_keys(student_data.get("organization_code"))
        
        password = self.find_element(By.NAME, "Password")
        password.send_keys(student_data.get("password"))
        
        age = self.find_element(By.NAME, "Age")
        amount = str(random.randint(17, 20))
        age.send_keys(amount)
        
        gender = Select(self.find_element(By.NAME, "Gender"))
        index = random.randint(0, 1)
        gender.select_by_index(index)
        
        team = Select(self.find_element(By.NAME, "Team"))
        index = random.randint(7, 9) # 2, 4 курс
        team.select_by_index(index)
        
        letter = self.find_element(By.NAME, "Letter")
        letter.send_keys("_")
        
        continue_button = self.find_element(By.ID, "LoginFormSubmit")
        continue_button.click()
        time.sleep(2)
        
        continue_button = WebDriverWait(self, self.timeout).until(EC.presence_of_element_located((By.XPATH, "//input[@value='Приступить к тестированию']")))
        continue_button.click()        
    
    
    # get question
    def answer_question(driver: webdriver.Chrome, answers: dict):
        try:
            raw_question = driver.find_element(By.XPATH, "//form//td[@colspan='10']")
            question: str = re.sub(r" +", " ", raw_question)
            question = question.strip()
            
            if answers.get(question):
                answer = answers.get(question)
            else:
                print(f"Вопрос: {question}")
                answer = int(input("Введите ответ (от 1 до 10 по умолчанию 5): "))
            answer_selector = driver.find_element(By.XPATH, f"//form//tr[@class='qRow2' and not(ancestor::tr[@style='display: none;'])]/td[{answer}]")
            answer_selector.click()
            
            confirmbtn = driver.find_element(By.XPATH, "//form//input[@value='Далее']")
            confirmbtn.click()
        except Exception as e:
            print(f"Ошибка: {e}")
        
        
    def complete_test(self):
        try:
            while True:
                self.answer_question()
                try:
                    submitbtn = self.find_element(By.XPATH, "//input[@value='Завершить тестирование (170 из 170)']")
                    submitbtn.click()
                    break
                except:
                    pass
                    
        except Exception as e:
            print(f"завершение теста: {e}")
        print("тест пройден")
        
    
    def logout(self):
        self.delete_all_cookies()
    


if __name__ == "__main__":    
    
    # student_number: "просто строка", password: "тоже строка", district_code: "значение элемента списка выбранной организации", organization_code: "код организации"
    users = [
    {
        "student_number": "7", "password": "9821", "district_code": "24", "organization_code": "1"
    },
            ]

    with open("answers1.json") as file:
        answers: dict = json.loads(file.read())
        
    print(TermArt.WELCOME)
    print(TermArt.LINE)
    print("пользователи:")
    for i in users:
        print(f"номер: {i["student_number"]:<4} пароль: {i["password"]:^5}")
    print(f"всего пользователей: {len(users)}")
    print(TermArt.LINE)
    print("ответы: ")
    for key, val in answers.items():
        print(f"{key:<120}  {val}")
    print(f"всего ответов: {len(answers.keys())}")
    print(TermArt.LINE)
    
    print("начинаю заполнение...")
    
    solver = TestSolver()
    
    for user_data in users:
        solver.login(user_data)
        solver.complete_test()
        solver.logout
    