# Кинопоиск и ПоискКино API: диплом QA

Три функции: поиск фильма, карточка фильма и сведения о персоне.
Интерфейс: https://www.kinopoisk.ru/.
API из задания: https://kinopoisk.dev/, перенаправляющий на https://poiskkino.dev/.
API является отдельным сервисом, а не внутренним API сайта Кинопоиска.
Документация: https://api.poiskkino.dev/documentation.

Стек: Python 3.12, pytest, Requests, Selenium, Allure.
6 позитивных UI-тестов и 6 API-тестов (4 позитивных, 2 негативных).
Настройки находятся в config.json. Каждый UI-тест запускает новую сессию Chrome или Firefox,
а каждый API-тест использует отдельную сессию Requests.

## Установка

```sh
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
```

Для UI нужен установленный Google Chrome. Selenium Manager подбирает драйвер.
Бинарные драйверы в репозиторий не включаются. Для Firefox задайте BROWSER=firefox.

## Ключ API

Получите собственный ключ на сайте сервиса. Передайте его через переменную среды
POISKKINO_API_KEY. Ключ не хранится в config.json или коде. Не добавляйте его в Git.
При отсутствии ключа позитивные API-тесты завершаются ошибкой настройки.
Представление объекта ключа в pytest скрывает значение. Не включайте --showlocals.

## Режимы запуска

```sh
python -m pytest tests -m ui --tb=short --alluredir=allure-results-ui
python -m pytest tests -m api --tb=short --alluredir=allure-results-api
python -m pytest tests --tb=short --alluredir=allure-results
```

Опционально WEBDRIVER_URL задает адрес доступного Selenium Server.
CHROME_BINARY задает путь к обычному Chrome, когда он установлен нестандартно.
Подмена профилей, обход капчи и отключение защит браузера не применяются.
При появлении капчи нужно остановить прогон и зафиксировать блокировку.

## Allure

Установите Allure Commandline по https://allurereport.org/docs/install/.

```sh
allure serve allure-results
allure generate allure-results --clean -o allure-report
```

## Проверка кода

Ruff — отдельный инструмент разработки, не зависимость запуска тестов:

```sh
python -m pip install ruff==0.14.2
ruff check . --select E,F,I,ANN
```

## GitHub Actions

Workflow запускается вручную через Actions после создания репозитория.
Для полного прогона необходим секрет POISKKINO_API_KEY.
Артефакты Allure и JUnit сохраняются и при падении тестов.
Данные фильма и персоны стабильны, рейтинги и счетчики голосов не фиксируются.

## Состояние проверки

26.10.2026: полный набор из 12 тестов (6 UI и 6 API) успешно выполнен
в GitHub Actions, сохраненный JUnit: 12 passed, 71.419 с.
Дополнительный Firefox-прогон: 6 UI passed, 89.27 с.
Последний запуск: https://github.com/Karins257/kinopoisk-qa-diploma/actions/runs/40361182942.
Сохраненный полный Allure: прогон 40358733408, попытка 2.
В истории был один тайм-аут поиска. Причина не установлена, позднее набор
прошел повторно без изменения утверждений и без автоматических ретраев.

Визуальное замечание: региональная подсказка частично перекрывает заголовок
персоны в гостевом Chrome/Linux. Успех функциональных тестов не исключает
этого замечания. Смотрите отчет диплома UX-01.

Страница проекта Yonote:
https://karinasuleymanovaqa132-2.yonote.ru/doc/diplom-kinopoisk-i-poiskkino-api-f5YgypM4aB.
Пока доступ закрыт по решению автора для предварительного просмотра.
Публичную ссылку проверим после разрешения на публикацию. Видеозащита ожидается.

27.10.2026: по результатам сверки с XLS усилены проверки названия и года
в поиске, строк режиссера/жанра, адресов карточек и полного заголовка фильма.
API-05 дополнительно проверяет непустое сообщение об ошибке. Новый прогон
этих изменений необходимо подтвердить отдельно от сохраненного отчета 26.10.
