import json

from webcrawler import TestSolver
from terma import TermArt


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
    print(f"выполнение теста за {user_data.get('student_number')}...")
    solver.login(user_data)
    solver.complete_test()
    solver.logout
    
print(TermArt.LINE)
print("решение завершено")