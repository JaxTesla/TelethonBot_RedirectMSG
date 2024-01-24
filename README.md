**Telegram Message Forwarding Script**
Описание

Этот скрипт на Python использует библиотеку Telethon для автоматической пересылки сообщений в Telegram. Он предназначен для автоматизации процесса перенаправления сообщений между различными чатами и группами в Telegram.


Особенности

Автоматическое перенаправление сообщений из одного чата в другой.
Поддержка различных типов медиа: текст, изображения, видео, документы.
Гибкая настройка ID чатов и уровней логирования.
Расширенная обработка ошибок и корректное завершение сессии клиента.


Требования

Для работы скрипта требуется:

Python 3.6 или выше.
Библиотека Telethon.

Установка

Установите Python 3.6 или выше.
Установите библиотеку Telethon, используя pip install telethon.



==============================================================

Инструкция по использованию скрипта для работы с Telegram API

==============================================================

Важно: Перед использованием скрипта убедитесь, что вы внимательно прочитали и поняли все шаги.

1. Настройка Telegram API

- Перейдите на сайт https://my.telegram.org и войдите в систему, используя свой номер телефона Telegram.
- В разделе 'API development tools' зарегистрируйте новое приложение. 
  * Введите название в 'App title' (например, 'MyTelethonApp').
  * Введите краткое название в 'Short name' (например, 'myapp').
  * Остальные поля заполнять не обязательно.
- Запишите полученные 'api_id' и 'api_hash'.
----------------------------

2. Настройка скрипта

- Откройте скрипт в текстовом редакторе.
- При первом запуске вам будет предложено ввести 'api_id' и 'api_hash', а также ID чата или группы для мониторинга и чата или группы куда сообщения будут перенаправляться.
-----------------------

3. Получение ID чата или группы

- Чтобы узнать ID чата в Telegram, используйте специальные боты, например @userinfobot.
- Отправьте сообщение в интересующий чат или добавьте бота в группу, чтобы получить ID.
----------------------------------

4. Запуск скрипта

- Запустите скрипт. При первом запуске скрипт запросит данные для авторизации.
- Данные сохраняются в файл настроек, после авторизации создается файл сессии.
-------------------

5. Важные моменты

- Всегда корректно завершайте сессию клиента с помощью клавиш Ctrl+C.
- Не удаляйте файлы настроек и сессии, если не хотите вводить данные заново.
- Скрипт создает папку для временного хранения файлов, полученных от Telegram. После отправки в целевую группу, файлы удаляются.
-------------------

6. Режимы логирования

- При запуске скрипта можно выбрать режим логирования событий.
- По умолчанию установлен уровень INFO.
- Доступны следующие уровни: DEBUG, INFO, WARNING, ERROR, CRITICAL.
----------------------
Пожалуйста, убедитесь, что вы следуете этим инструкциям, чтобы избежать ошибок или непредвиденных ситуаций во время работы скрипта.----------------------
