import json
from datetime import date
from app.database import engine, SessionLocal
from app.models import Base, Category, Genre, Role, Account, UserProfile
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


# Создаем таблицы (если их еще нет)
Base.metadata.create_all(bind=engine)

def add_unique_entry(db: Session, model, **kwargs):
    """Утилита для добавления уникальной записи в базу данных."""
    instance = db.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        db.add(instance)
    return instance

def populate_categories():
    with open("static/categories.json") as f:
        categories = json.load(f)

    with SessionLocal() as db:
        for category in categories:
            add_unique_entry(db, Category, name=category["name"])
        db.commit()

def populate_genres():
    with open("static/genres.json") as f:
        genres = json.load(f)

    with SessionLocal() as db:
        for genre in genres:
            add_unique_entry(db, Genre, name=genre["name"])
        db.commit()

def populate_roles():
    with open("static/roles.json") as f:
        roles = json.load(f)

    with SessionLocal() as db:
        for role in roles:
            # Теперь добавляем роль с уникальным id_role
            add_unique_entry(db, Role, id=role["id_role"], name=role["name"])
        db.commit()

def populate_accounts():
    with open("static/accounts.json") as f:
        accounts = json.load(f)

    with SessionLocal() as db:
        for account in accounts:
            # Проверка уникальности аккаунта по имени
            existing_account = db.query(Account).filter_by(username=account["username"]).first()
            if existing_account:
                print(f"Аккаунт '{account['username']}' уже существует. Пропускаем.")
                continue

            # Получаем роль по role_id
            role = db.query(Role).filter_by(id=account["role_id"]).first()
            if not role:
                print(f"Роль с id '{account['role_id']}' не найдена для пользователя '{account['username']}'. Пропускаем.")
                continue

            db_account = Account(
                username=account["username"],
                email=account["email"],
                role_id=role.id
            )
            db_account.set_password(account["password_hash"])
            db.add(db_account)
        db.commit()

def populate_user_profiles():
    with open("static/user_profiles.json", encoding="utf-8") as f:
        user_profiles = json.load(f)

    with SessionLocal() as db:
        for profile in user_profiles:
            # Проверка уникальности профиля
            existing_profile = db.query(UserProfile).filter_by(user_id=profile["user_id"]).first()
            if existing_profile:
                print(f"Профиль пользователя с ID {profile['user_id']} уже существует. Пропускаем.")
                continue

            db_profile = UserProfile(
                user_id=profile["user_id"],
                name=profile["name"],
                surname=profile["surname"],
                patronymic=profile["patronymic"],
                phone_number=profile["phone_number"],
                email=profile["email"],
                birthday=date.fromisoformat(profile["birthday"])
            )
            db.add(db_profile)
        db.commit()

if __name__ == "__main__":
    try:
        populate_categories()
        populate_genres()
        populate_roles()
        populate_accounts()
        populate_user_profiles()
    except IntegrityError as e:
        print(f"Ошибка целостности данных: {e}")
        # Печать дополнительной информации для отладки
        db.rollback()  # Отменить изменения в случае ошибки
    except Exception as e:
        print(f"Произошла ошибка: {e}")
