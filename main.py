from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeFilename, MessageMediaWebPage
import asyncio
import json
import os
import logging


print(
    "!!!!!!!!!!!!!!!!!!!!!!!! ВАЖНО ПРИ ПЕРВОМ ЗАПУСКЕ !!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
    "Для настройки и запуска скрипта выполните следующие шаги:\n"
    "1. Перейдите на сайт https://my.telegram.org и войдите, используя свой номер телефона Telegram.\n"
    "2. После входа в систему нажмите на 'API development tools' и заполните необходимые поля для регистрации нового приложения.\n"
    "   - В поле 'App title' введите название вашего приложения (например, 'MyTelethonApp').\n"
    "   - В поле 'Short name' введите краткое название (например, 'myapp').\n"
    "   - Остальные поля можно оставить пустыми или заполнить по желанию.\n"
    "3. После создания приложения вы увидите 'api_id' и 'api_hash'. Скопируйте эти данные.\n"
    "4. Вернитесь к этому скрипту и введите скопированные 'api_id' и 'api_hash', когда это будет запрошено.\n"
    "5. Также вам будет нужно указать ID чата или группы, который вы хотите мониторить, и ID чата или группы, куда будут перенаправляться сообщения.\n"
    "   - Чтобы узнать ID чата в Telegram, можно воспользоваться специальными ботами, например @userinfobot.\n"
    "   - Отправьте сообщение в интересующий чат или добавьте бота в группу и он вернет ID.\n"
    "6. После ввода всех необходимых данных скрипт будет готов к работе.\n"
    "7. После запуска клиента, может потребоваться отправить сообщение в мониторимые чаты вручную, чтобы они стали доступны для клиента.\n\n"
    "ОЧЕНЬ ВАЖНО: корректно завершать сессию клиента, для этого используйте клавиши Ctrl+C.\n"
    "Введенные данные сохраняются в файле настроек, а после авторизации создается файл сессии. Не рекомендуется удалять эти файлы, если вы не хотите вводить данные заново.\n"
    "Скрипт также создает папку в том каталоге, где он находится, и в эту папку временно сохраняются файлы, получаемые от Telegram. После отправки в целевую группу файлы удаляются.\n\n"
    "Обратите внимание: для работы скрипта необходимо, чтобы аккаунт, под которым запускается скрипт, был добавлен в мониторимый чат или группу.\n"
)

# Настройка логирования для вывода в файл и на консоль
# Определение соответствия между вводом пользователя и уровнями логирования
log_levels = {
    "1": logging.INFO,  # INFO теперь первый пункт
    "2": logging.DEBUG,
    "3": logging.WARNING,
    "4": logging.ERROR,
    "5": logging.CRITICAL
}

while True:
    print("Выберите уровень логирования событий в сеансе:")
    print("1. INFO (по умолчанию)")
    print("2. DEBUG")
    print("3. WARNING")
    print("4. ERROR")
    print("5. CRITICAL")
    print("6. Выход")

    log_level_choice = input(
        "Введите номер выбранного уровня логирования или '6' для выхода: ")

    if log_level_choice in log_levels:
        # Установка выбранного уровня логирования
        logger = logging.getLogger()
        logger.setLevel(log_levels[log_level_choice])
        break
    elif log_level_choice == "6":
        print("Завершение работы программы")
        exit(0)
    else:
        print("Некорректный ввод. Пожалуйста, введите число от 1 до 6.")

# Форматирование логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Логирование в файл с кодировкой UTF-8
file_handler = logging.FileHandler('telethon_log.log', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Логирование в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Название файла настроек
config_file = 'config.json'

# Значения по умолчанию
default_config = {
    "device_model": 'Custom Device',
    "system_version": '4.16.30-vxCUSTOM',
    "app_version": '1.0',
    "temp_files_dir": "temp_files",
    "api_id": "",
    "api_hash": "",
    "monitored_chat_id": "",
    "chat_id_to_redirect_messages": ""
}

# Проверка наличия файла настроек и создание при необходимости
if not os.path.exists(config_file):
    with open(config_file, 'w') as file:
        json.dump(default_config, file, indent=4)

# Загрузка настроек
with open(config_file) as file:
    config = json.load(file)

# Преобразование строковых значений в числа, где это необходимо
config["api_id"] = int(config["api_id"]) if str(
    config["api_id"]).isdigit() else None
config["monitored_chat_id"] = int(config["monitored_chat_id"]) if str(
    config["monitored_chat_id"]).isdigit() else None
config["chat_id_to_redirect_messages"] = int(config["chat_id_to_redirect_messages"]) if str(
    config["chat_id_to_redirect_messages"]).isdigit() else None

# Запрос недостающих параметров у пользователя
for key in config:
    while not config[key]:
        value = input(f"Введите значение для '{key}': ")

        if key in ["api_id", "monitored_chat_id", "chat_id_to_redirect_messages"]:
            if value.isdigit():
                config[key] = int(value)
            else:
                print(
                    f"Значение для '{key}' должно быть числом. Пожалуйста, попробуйте снова.")
        else:
            config[key] = value

# Сохранение обновленных настроек
with open(config_file, 'w') as file:
    json.dump(config, file, indent=4)

# Использование настроек
api_id = config["api_id"]
api_hash = config["api_hash"]
monitored_chat_id = config["monitored_chat_id"]
chat_id_to_redirect_messages = config["chat_id_to_redirect_messages"]
device_model = config["device_model"]
system_version = config["system_version"]
app_version = config["app_version"]
temp_files_dir = config["temp_files_dir"]

# Создает директорию, если она не существует
os.makedirs(temp_files_dir, exist_ok=True)

# Создание клиента с пользовательскими параметрами
client = TelegramClient('telethon', api_id, api_hash,
                        device_model=device_model,
                        system_version=system_version,
                        app_version=app_version)


async def download_and_send_media(client, message, chat_id_to_redirect_messages, temp_dir):
    media = message.media
    caption = message.text

    # Определение имени файла с учетом типа медиа
    file_name = None
    if media and hasattr(media, 'document'):
        for attr in media.document.attributes:
            if isinstance(attr, DocumentAttributeFilename):
                file_name = attr.file_name
                break

    if not file_name:
        # Установка стандартного имени файла в зависимости от типа медиа
        if message.photo:
            file_name = f"temp_photo_{message.id}.jpg"
        elif message.video:
            file_name = f"temp_video_{message.id}.mp4"
        elif message.voice:
            file_name = f"temp_voice_{message.id}.ogg"
        else:
            file_name = f"temp_file_{message.id}"

    file_path = os.path.join(temp_dir, file_name)
    await client.download_media(message, file=file_path)

    if os.path.exists(file_path):
        await client.send_file(chat_id_to_redirect_messages, file=file_path, caption=caption)
        os.remove(file_path)


# Обработчик для пересылки сообщений и их вывода в терминал
@client.on(events.NewMessage(chats=monitored_chat_id))
async def handler(event):
    # Вывод сообщения в терминал
    logging.info(f'Зафиксировано входящее сообщение:\n{event.message}')
    text_for_msg = event.message.text if event.message.text else None
    # Пересылка сообщения в целевую группу
    try:

        if event.message.grouped_id:
            logging.info('Зашли в обработку медиа коллекций\n')
            # Проверяем, была ли уже обработана эта медиа-группа
            if not hasattr(handler, 'processed_groups'):
                handler.processed_groups = set()

            if event.message.grouped_id in handler.processed_groups:
                return  # Медиа-группа уже обработана

            handler.processed_groups.add(event.message.grouped_id)
            media_files = []

            async for message in client.iter_messages(event.chat_id, limit=10):
                if message.grouped_id == event.message.grouped_id:
                    file_path = os.path.join(
                        temp_files_dir, f"temp_photo_{message.id}.jpg")
                    await message.download_media(file=file_path)
                    media_files.append(file_path)

            if media_files:
                await client.send_file(chat_id_to_redirect_messages, media_files, caption=text_for_msg)

                for file_path in media_files:
                    if os.path.exists(file_path):
                        os.remove(file_path)

        # Обработка веб-страниц
        elif isinstance(event.message.media, MessageMediaWebPage):
            logging.info('Зашли в обработку ссылок\n')
            # Извлечение URL, если возможно
            url = event.message.media.webpage.url if event.message.media.webpage else None
            text_for_msg = f"{event.message.text}\n{url}" if event.message.text else url

            if text_for_msg:
                await client.send_message(chat_id_to_redirect_messages, text_for_msg)

        # Обработка фотографий
        elif event.message.photo:
            logging.info('Зашли в обработку фотографий\n')
            await download_and_send_media(client, event.message, chat_id_to_redirect_messages, temp_files_dir)

        # Обработка видео- и голосовых сообщений
        elif event.message.video or event.message.voice:
            logging.info('Зашли в обработку видео и голосовых сообщений\n')
            await download_and_send_media(client, event.message, chat_id_to_redirect_messages, temp_files_dir)

        # Обработка файлов
        elif event.message.file:
            logging.info('Зашли в обработку файлов\n')
            await download_and_send_media(client, event.message, chat_id_to_redirect_messages, temp_files_dir)

        elif event.message.text:
            logging.info('Зашли в обработку текстовых сообщений\n')
            # text_for_msg = event.message.text

            await client.send_message(chat_id_to_redirect_messages, text_for_msg)

    except Exception as e:
        # Обработка других ошибок
        logging.error(f"Произошла ошибка: {e}\n")


async def main():
    global monitored_chat_id, chat_id_to_redirect_messages

    try:
        await client.start()
        logging.warning("Клиент запущен\n")

        # Попытка "обнаружить" сущности и запрос на изменение ID, если необходимо
        while True:
            try:
                await client.get_dialogs()
                monitored_entity = await client.get_entity(monitored_chat_id)
                redirect_entity = await client.get_entity(chat_id_to_redirect_messages)

                # Проверка и подтверждение правильности настроек чатов
                monitored_chat_name = monitored_entity.title if hasattr(
                    monitored_entity, 'title') else monitored_entity.username
                redirect_chat_name = redirect_entity.title if hasattr(
                    redirect_entity, 'title') else redirect_entity.username

                confirmation = input(
                    f"Пересылать сообщения из '{monitored_chat_name}' в '{redirect_chat_name}'? Y(да) / N(нет)): ").strip().lower()
                if confirmation in ['y', 'yes', 'да']:
                    break  # Пользователь подтвердил настройки
                elif confirmation in ['n', 'no', 'нет']:
                    # Запрос новых ID чатов с проверкой корректности ввода
                    while True:
                        try:
                            monitored_chat_id = int(
                                input("Введите новый ID чата для мониторинга(monitored_chat_id): "))
                            break
                        except ValueError:
                            print(
                                "Ошибка: ID чата должен быть числом. Пожалуйста, попробуйте снова.")

                    while True:
                        try:
                            chat_id_to_redirect_messages = int(
                                input("Введите новый ID чата для пересылки сообщений(chat_id_to_redirect_messages): "))
                            break
                        except ValueError:
                            print(
                                "Ошибка: ID чата должен быть числом. Пожалуйста, попробуйте снова.")

                    break  # Выход из цикла после обновления настроек
                elif confirmation in ['выход', 'exit']:
                    await shutdown()
                    return  # Завершение работы скрипта
                else:
                    print("Некорректный ответ! Пожалуйста, введите Y (да) / N (нет).")

            except ValueError as e:
                logging.error(f"Ошибка: {e}")
                new_id = input(
                    "Введите другой ID чата или 'exit' для выхода: ")
                if new_id.lower() == 'exit':
                    await shutdown()
                    return  # Завершение работы скрипта
                elif new_id.isdigit():
                    monitored_chat_id = int(new_id)  # Обновление ID
                else:
                    logging.error("Введенное значение должно быть числом.")

        logging.warning(
            f"Доступ к чату/каналу '{monitored_chat_name}' ({monitored_entity.id}) подтвержден.")
        logging.warning(
            f"Пересылаем сообщения в '{redirect_chat_name}' ({redirect_entity.id}).")

        await client.run_until_disconnected()

    except KeyboardInterrupt:
        logging.warning(
            "Обнаружено прерывание с клавиатуры. Завершение работы клиента...")
    finally:
        await shutdown()


async def shutdown():
    logging.warning("Завершение работы клиента")
    await client.disconnect()
    logging.warning("Клиент отключен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.warning("Клиент завершил работу по команде пользователя")
