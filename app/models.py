from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import Base


class MediaFile(Base):
    """
    Модель для представления музыкальных произведений и связанных медиафайлов.
    
    Attributes:
        id (int): Уникальный идентификатор медиафайла.
        name_music (str): Название музыкального произведения.
        description (str, optional): Описание музыкальной композиции.
        file_name (str): Имя файла медиа.
        file_path (str): Путь к файлу медиа.
        cover_image_path (str, optional): Путь к обложке музыкальной композиции.
        category_id (int): Идентификатор категории, к которой относится медиафайл.
        genre_id (int): Идентификатор жанра медиафайла.
        youtube_url (str, optional): Ссылка на YouTube.
        rutube_url (str, optional): Ссылка на RuTube.
        plvideo_url (str, optional): Ссылка на Plvideo.
    """
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, index=True)
    name_music = Column(String(100), nullable=False, index=True, comment="Название музыкального произведения")
    description = Column(Text, nullable=True, comment="Описание музыкальной композиции")
    
    file_name = Column(String, nullable=False, index=True, comment="Имя файла")
    file_path = Column(String, nullable=False, comment="Путь к файлу")
    cover_image_path = Column(String, nullable=True, comment="Путь к обложке композиции")
    
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)

    youtube_url = Column(String(255), nullable=True, comment="Ссылка на YouTube")
    rutube_url = Column(String(255), nullable=True, comment="Ссылка на RuTube")
    plvideo_url = Column(String(255), nullable=True, comment="Ссылка на Plvideo")
    
    category = relationship("Category", back_populates="media_files")
    genre = relationship("Genre", back_populates="media_files")


class Category(Base):
    """
    Модель для представления категории медиафайлов.

    Attributes:
        id (int): Уникальный идентификатор категории.
        name (str): Название категории.
        media_files (list of MediaFile): Связанные медиафайлы данной категории.
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True, comment="Название категории")
    
    media_files = relationship("MediaFile", back_populates="category", cascade="all, delete")


class Genre(Base):
    """
    Модель для представления жанра медиафайлов.

    Attributes:
        id (int): Уникальный идентификатор жанра.
        name (str): Название жанра.
        media_files (list of MediaFile): Связанные медиафайлы данного жанра.
    """
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True, comment="Название жанра")
    
    media_files = relationship("MediaFile", back_populates="genre", cascade="all, delete")


class Account(Base):
    """
    Модель для представления аккаунта пользователя.

    Attributes:
        id (int): Уникальный идентификатор пользователя.
        username (str): Имя пользователя (уникальное).
        email (str): Электронная почта пользователя (уникальная).
        password_hash (str): Хеш пароля пользователя.
        profile_image_path (str, optional): Путь к изображению профиля.
        is_active (bool): Статус активности пользователя.
        role_id (int): Идентификатор роли пользователя.
        role (Role): Связанная роль пользователя.
        profile (UserProfile): Персональные данные профиля.
    """
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True, comment="Имя пользователя")
    email = Column(String(100), unique=True, nullable=False, index=True, comment="Электронная почта")
    password_hash = Column(String(128), nullable=False, comment="Хешированный пароль")
    profile_image_path = Column(String, nullable=True, comment="Путь к фотографии профиля")
    is_active = Column(Boolean, default=True, comment="Статус активности пользователя")
    
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    # Связь с ролью
    role = relationship("Role", back_populates="accounts")

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete")

    def set_password(self, password):
        """Сохраняет хэшированный пароль."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверяет пароль."""
        return check_password_hash(self.password_hash, password)


class UserProfile(Base):
    """
    Модель для представления персональных данных пользователя.

    Attributes:
        id (int): Уникальный идентификатор профиля.
        user_id (int): Идентификатор пользователя, связанный с профилем.
        name (str, optional): Имя пользователя.
        surname (str, optional): Фамилия пользователя.
        patronymic (str, optional): Отчество пользователя.
        phone_number (str, optional): Номер телефона пользователя.
        email (str, optional): Электронная почта пользователя.
        birthday (date, optional): Дата рождения пользователя.
        user (User): Связанный пользователь.
    """
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("accounts.id"), unique=True, nullable=False, comment="ID аккаунта пользователя")
    name = Column(String(50), nullable=True, comment="Имя пользователя")
    surname = Column(String(50), nullable=True, comment="Фамилия пользователя")
    patronymic = Column(String(50), nullable=True, comment="Отчество пользователя")
    phone_number = Column(String(15), nullable=True, unique=True, comment="Номер телефона")
    email = Column(String(100), nullable=True, unique=True, index=True, comment="Электронная почта (дополнительно)")
    birthday = Column(Date, nullable=True, comment="Дата рождения пользователя")

    user = relationship("Account", back_populates="profile")


class Role(Base):
    """
    Модель для представления роли пользователя.

    Attributes:
        id (int): Уникальный идентификатор роли.
        name (str): Название роли, например, admin или user.
        users (list of User): Пользователи, которым присвоена данная роль.
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True, comment="Название роли, например, admin, user")

    # Добавление связи с моделью Account (или User)
    accounts = relationship("Account", back_populates="role")  # В зависимости от того, как вы назвали модель
