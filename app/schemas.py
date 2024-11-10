from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional

# Общая схема для описания базовой модели
class IDModelMixin(BaseModel):
    """Базовая схема для моделей с ID."""
    id: int

    class Config:
        from_attributes = True

# Схемы для категорий

class CategoryBase(BaseModel):
    """Схема для базовой категории с названием."""
    name: str = Field(..., min_length=1, max_length=100, example="Pop", description="Название категории")

class CategoryCreate(CategoryBase):
    """Схема для создания новой категории."""
    pass

class Category(IDModelMixin, CategoryBase):
    """Схема для просмотра категории с ID."""
    pass

# Схемы для жанров

class GenreBase(BaseModel):
    """Схема для базового жанра с названием."""
    name: str = Field(..., min_length=1, max_length=100, example="Rock", description="Название жанра")

class GenreCreate(GenreBase):
    """Схема для создания нового жанра."""
    pass

class Genre(IDModelMixin, GenreBase):
    """Схема для просмотра жанра с ID."""
    pass

# Схемы для медиа файлов

class MediaFileBase(BaseModel):
    """Схема для базового описания медиафайла."""
    name_music: str = Field(..., max_length=255, example="Song Title", description="Название музыкального произведения")
    description: Optional[str] = Field(None, max_length=500, example="A great song description.", description="Описание композиции")
    file_name: str = Field(..., max_length=255, example="song.mp3", description="Имя файла медиа")
    file_path: str = Field(..., example="/media/files/song.mp3", description="Путь к файлу медиа")
    cover_image_path: Optional[str] = Field(None, example="/media/covers/cover.jpg", description="Путь к изображению обложки")
    category_id: int = Field(..., gt=0, example=1, description="ID категории")
    genre_id: int = Field(..., gt=0, example=2, description="ID жанра")
    youtube_url: Optional[HttpUrl] = Field(None, example="https://www.youtube.com/watch?v=xyz", description="Ссылка на YouTube")
    rutube_url: Optional[HttpUrl] = Field(None, example="https://rutube.ru/video/xyz", description="Ссылка на RuTube")
    plvideo_url: Optional[HttpUrl] = Field(None, example="https://pl.video/xyz", description="Ссылка на Plvideo")

class MediaFileCreate(MediaFileBase):
    """Схема для создания нового медиафайла."""
    pass

class MediaFile(IDModelMixin, MediaFileBase):
    """Схема для просмотра медиафайла с ID."""
    pass

# Схемы для пользователей

class UserBase(BaseModel):
    """Базовая схема для данных пользователя."""
    username: str = Field(..., max_length=50, example="user123", description="Имя пользователя")
    email: EmailStr = Field(..., example="user@example.com", description="Электронная почта пользователя")

class UserCreate(UserBase):
    """Схема для создания нового пользователя, включая пароль."""
    password: str = Field(..., min_length=6, example="password123", description="Пароль пользователя")

class UserRead(IDModelMixin, UserBase):
    """Схема для просмотра данных пользователя, включая статус и роль."""
    is_active: bool = Field(..., description="Статус активности пользователя")
    role_id: Optional[int] = Field(None, description="ID роли пользователя")
    profile_image_path: Optional[str] = Field(None, example="/profile_images/user123.jpg", description="Путь к фотографии профиля")

class UserUpdate(BaseModel):
    """Схема для обновления данных пользователя, включая изменяемые поля."""
    username: Optional[str] = Field(None, max_length=50, description="Новое имя пользователя")
    email: Optional[EmailStr] = Field(None, description="Новая электронная почта пользователя")
    password: Optional[str] = Field(None, min_length=6, description="Новый пароль пользователя")
    is_active: Optional[bool] = Field(None, description="Новый статус активности пользователя")
    profile_image_path: Optional[str] = Field(None, example="/profile_images/new_user123.jpg", description="Новый путь к фотографии профиля")

# Схемы для ролей пользователей

class RoleBase(BaseModel):
    """Базовая схема для роли пользователя с названием."""
    name: str = Field(..., max_length=50, example="user", description="Название роли")

class RoleRead(IDModelMixin, RoleBase):
    """Схема для просмотра роли пользователя с ID."""
    pass
