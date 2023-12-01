### Парсер документации Python

*  Парсер ссылок на статьи о нововведениях и информации об авторах и редакторах статей в Python.
*  Парсер данных актуальных версий Python.
*  Парсинг документов PEP.
*  Парсер, который скачивает архив с документацией Python.


### Как запустить проект:

* Клонировать репозиторий и перейти в него в командной строке:

    ```
    git@github.com:Evgenmater/bs4_parser_pep.git
    ```

* Перейти в директорию проекта:

    ```
    cd bs4_parser_pep
    ```

* Создайте и активируйте виртуальное окружение, обновите менеджер пакетов pip и установите зависимости из файла requirements.txt:

    ```
    python -m venv venv
    source venv/Scripts/activate
    pip install --upgrade pip
    pip install -r requirements.txt 
    ```

* Команды для работы с парсингом(Вывод данных по умолчанию):
* Перейдите в директорию cd src

    ```
    python main.py whats-new - ссылки на статьи о нововведениях
    python main.py latest-versions - версии Python
    python main.py pep - документы PEP
    python main.py download - скачивает архив с документацией Python
    ```

### Дополнительные способы вывода данных:

* Запись данных в файл - *python main.py "функция" --output file*, например:

    ```
    python main.py whats-new --output file 
    ```

* Вывод данных в формате таблицы - *python main.py "функция" --pretty*, например:

    ```
    python main.py whats-new --pretty 
    ```

* Справка для команд:

    ```
    python main.py -h
    ```

### Автор:  
Хлебнев Евгений Юрьевич<br>
**email**: hlebnev@yandex.ru<br>
**telegram** @Evgen0991