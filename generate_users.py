import json
from faker import Faker
from hashlib import sha256
from datetime import date
import random

# Инициализируем Faker
fake = Faker("ru_RU")  # Используем русский язык для данных

# Загружаем роли из файла roles.json
def load_roles(filename="static/roles.json"):
    with open(filename, "r", encoding="utf-8") as f:
        roles = json.load(f)
    # Создаем словарь с соответствием имени роли и ее ID
    role_mapping = {
        "Admin": 1,
        "User": 2,
        "Moderator": 3
    }
    return role_mapping

# Класс для представления данных пользователя
class AccountData:
    def __init__(self, username, email, password_hash, profile_image_path, role_id):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.profile_image_path = profile_image_path
        self.role_id = role_id

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "profile_image_path": self.profile_image_path,
            "role_id": self.role_id  # Используем ID роли
        }

# Функция для генерации одного пользователя
def create_fake_user(role_id: int) -> AccountData:
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    password_hash = sha256(password.encode()).hexdigest()  # Хешируем пароль
    profile_image_path = f"profile_images/{username}.jpg"  # Путь к изображению профиля
    return AccountData(username, email, password_hash, profile_image_path, role_id)

# Класс для представления данных профиля пользователя
class UserProfileData:
    def __init__(self, user_id, name, surname, patronymic, phone_number, email, birthday):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.phone_number = phone_number
        self.email = email
        self.birthday = birthday

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "surname": self.surname,
            "patronymic": self.patronymic,
            "phone_number": self.phone_number,
            "email": self.email,
            "birthday": self.birthday.isoformat()  # Преобразуем дату в строку
        }

# Функция для генерации одного профиля пользователя
def create_fake_user_profile(user_id: int) -> UserProfileData:
    return UserProfileData(
        user_id=user_id,
        name=fake.first_name(),
        surname=fake.last_name(),
        patronymic=fake.middle_name(),
        phone_number=fake.phone_number(),
        email=fake.unique.email(),
        birthday=fake.date_of_birth(minimum_age=18, maximum_age=70)
    )

# Генерация списка пользователей и сохранение в JSON файл
def generate_fake_users_and_profiles(user_count: int, user_filename: str, profile_filename: str):
    role_mapping = load_roles()  # Загружаем соответствие ролей и их ID
    roles = list(role_mapping.values())  # Получаем список ID ролей
    users = []
    profiles = []
    
    for user_id in range(1, user_count + 1):
        # Генерация случайной роли для пользователя
        role_id = random.choice(roles)
        
        # Генерация пользователя
        user = create_fake_user(role_id)
        users.append(user.to_dict())
        
        # Генерация профиля пользователя
        profile = create_fake_user_profile(user_id)
        profiles.append(profile.to_dict())
    
    # Сохранение пользователей в файл users.json
    with open(user_filename, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
    print(f"Сохранено {user_count} пользователей в файл {user_filename}")
    
    # Сохранение профилей пользователей в файл user_profiles.json
    with open(profile_filename, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)
    print(f"Сохранено {user_count} профилей пользователей в файл {profile_filename}")

# Запуск генерации
generate_fake_users_and_profiles(5, "static/accounts.json", "static/user_profiles.json")
