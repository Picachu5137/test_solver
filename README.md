# narcotest solver

# How to use
To start using, you need to configure webdriver for selenium. In **webcrawler.py** you need set path to chromedriver

In main.py you need set path to answers.json which contain encoded dict with pairs "answer": "value from 1 to 10" and add dicts in users with keys "student_number", "password", "district_code", "organization_code". For examble

main.py
```py
users = [
{
    "student_number": "1", "password": "1111", "district_code": "24", "organization_code": "10"
},
        ]
```

# How to run
```bash
python main.py
```
