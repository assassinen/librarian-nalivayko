# work-mate
https://docs.google.com/document/d/1aJnkKaaVAl4nyjt_FRnxMSEt6n42pufxhMfXUCOiSCg/edit?tab=t.0

# установка зависимостей
```
pip install -r ./requirements.txt
```

# запуск скрипта
```
python main.py --file example1.log --report average 
python main.py --file example1.log --report average --date 2025-22-06
```

![img_1.png](img_1.png)

```
python main.py --file example1.log --report by_agent
python main.py --file example1.log --report by_agent --date 2025-22-06
```
![img_2.png](img_2.png)
# запуск тестов

```
 pytest --cov=main  tests/tests.py 
```

![img_3.png](img_3.png)