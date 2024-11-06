import json
import sqlite3

# Путь к базе данных и JSON файлу
DB_PATH = 'c:/Users/maksi/Documents/GitHub/fast_api_media_platform/media_platform.db'
JSON_PATH = 'c:/Users/maksi/Documents/GitHub/fast_api_media_platform/zametki/musicians.json'

# Обязательные поля
REQUIRED_FIELDS = ['name_music', 'file_name', 'file_path', 'category_id', 'genre_id']

def validate_record(record):
    """Проверка, содержит ли запись все необходимые поля с непустыми значениями, кроме file_name."""
    for field in REQUIRED_FIELDS:
        if field == 'file_name' and not record.get(field):
            record['file_name'] = 'default_file_name.mp3'  # значение по умолчанию
        elif not record.get(field):  # Проверка на наличие и непустое значение
            print(f"Пропущено поле {field} в записи: {record}")
            return False
    return True

def load_data_to_db():
    # Чтение JSON файла
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            musicians_data = json.load(f)
    except FileNotFoundError:
        print(f"Файл JSON не найден: {JSON_PATH}")
        return
    except json.JSONDecodeError:
        print("Ошибка при чтении JSON файла.")
        return

    # Подключение к базе данных SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # SQL-запрос для вставки данных
    insert_query = """
    INSERT INTO media_files (id, name_music, description, file_name, file_path, cover_image_path, 
                             category_id, genre_id, youtube_url, rutube_url, plvideo_url) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    # Обработка каждой записи
    for record in musicians_data:
        # Проверка валидности записи
        if not validate_record(record):
            print(f"Пропуск записи из-за отсутствующих обязательных полей: {record}")
            continue

        # Подготовка данных для вставки
        data_tuple = (
            record.get('id'),
            record.get('name_music'),
            record.get('description', ''),  # Использование пустой строки по умолчанию
            record['file_name'],
            record['file_path'],
            record.get('cover_image_path', ''),
            record['category_id'],
            record['genre_id'],
            record.get('youtube_url', ''),
            record.get('rutube_url', ''),
            record.get('plvideo_url', '')
        )

        # Вставка данных с обработкой ошибок
        try:
            cursor.execute(insert_query, data_tuple)
        except sqlite3.IntegrityError as e:
            print(f"Ошибка вставки данных: {e} для записи {record}")
            continue

    # Сохранение изменений и закрытие подключения
    conn.commit()
    conn.close()
    print("Данные успешно загружены в базу данных.")

# Запуск загрузки данных
load_data_to_db()

'''
📔 Автор: Дуплей Максим Игоревич | Dupley Maxim Igorevich
📲 Номер телефона: +7-915-048-02-49
📅 Дата: 19.10.2024
'''
