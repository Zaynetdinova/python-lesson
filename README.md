# python-lesson

Учебный репозиторий: изучаю Python с нуля для работы с API, данными и AI-автоматизацией.

## Что внутри

Все файлы лежат в корне репозитория. В каждом уроке сначала короткая теория, затем решения заданий:

- `lesson1.py`: переменные, f-строки, условия, ввод данных
- `lesson2.py`: списки, словари, циклы
- `lesson3.py`: функции, чтение и запись JSON
- `lesson4.py`: запрос к API (курсы валют ЦБ РФ)
- `lesson5.py`: обработка ошибок (`try/except`), настройки из `.env`
- `lesson6.py`: pandas (таблицы, фильтры, сортировка, группировка, экспорт в CSV)
- `make_flats.py`: создаёт `flats.json` с тестовыми данными для уроков 6 и 9
- `lesson7.py`: мини-проект. Курсы валют из API ЦБ РФ, расчёт изменения за день в pandas и отправка сводки в Telegram
- `claude_utils.py`: общая функция `ask_claude` для запросов к Claude API с обработкой ошибок
- `lesson8.py`: первые запросы к Claude API (system prompt, `max_tokens`, `usage`)
- `lesson8b.py`: мини-проект. Сводка курсов валют с комментарием Claude, отправка в Telegram
- `lesson9.py`: структурированный JSON-ответ (разбор заявок клиентов в `leads.json`) и tool use (Claude вызывает функции: ипотечный платёж, цена за м², поиск квартир в `flats.json`)
- `requirements.txt`: список зависимостей

## Как запустить

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python lesson5.py
```

Для Windows активация окружения: `.venv\Scripts\activate`.

Для уроков 6 и 9 сначала создайте данные, затем запустите нужный урок:

```
python make_flats.py
python lesson6.py
```

## Настройки

Скрипты, которым нужны ключи, читают их из файла `.env` в корне проекта (он не хранится в репозитории). Создайте его сами с нужными переменными:

```
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_CHAT_ID=ваш_chat_id
ANTHROPIC_API_KEY=ваш_ключ_claude_api
```

- `TELEGRAM_BOT_TOKEN` выдаёт @BotFather в Telegram. Перед запуском нужно открыть своего бота и нажать Start.
- `ANTHROPIC_API_KEY` создаётся в Claude Console (раздел API Keys). Использование API оплачивается отдельно от подписки.
- Для уроков 7 и 8б нужны Telegram-переменные, для уроков 8-9 нужен ключ Claude.