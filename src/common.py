from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import customtkinter
from PIL import Image, ImageTk

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = Path(__file__).resolve().parent
ASSETS_DIR = ROOT_DIR / "assets" / "images"
DATA_DIR = ROOT_DIR / "data"
FONTS_DIR = ROOT_DIR / "fonts"
USER_DB = DATA_DIR / "users.db"
ICON_NAME = "icon1.png"


def setup_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    FONTS_DIR.mkdir(parents=True, exist_ok=True)


def get_asset_path(name: str) -> Path:
    return ASSETS_DIR / name


def get_db_path() -> Path:
    setup_dirs()
    return USER_DB


def ensure_database() -> None:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS user_info (
            name TEXT,
            lastname TEXT,
            email TEXT PRIMARY KEY,
            password TEXT
        )
        '''
    )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS user_profile (
            name TEXT,
            lastname TEXT,
            email TEXT PRIMARY KEY
        )
        '''
    )
    conn.commit()
    conn.close()


def init_theme() -> None:
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("blue")


def open_script(script_name: str, *args: str) -> None:
    script_path = SRC_DIR / script_name
    subprocess.Popen([sys.executable, str(script_path), *args], cwd=str(SRC_DIR))
    sys.exit(0)


def load_photo_image(name: str, size: tuple[int, int] | None = None) -> customtkinter.CTkImage:
    return load_ctk_image(name, size)


def load_ctk_image(name: str, size: tuple[int, int] | None = None) -> customtkinter.CTkImage:
    path = get_asset_path(name)
    image = Image.open(path)
    if size is not None:
        image = image.resize(size, Image.Resampling.LANCZOS)
    return customtkinter.CTkImage(image)


def load_icon(root: object) -> None:
    icon_path = get_asset_path(ICON_NAME)
    if icon_path.exists():
        icon = ImageTk.PhotoImage(Image.open(icon_path))
        root.iconphoto(False, icon)
        setattr(root, 'icon_image', icon)
