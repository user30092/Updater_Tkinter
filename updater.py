import tkinter as tk
from tkinter import messagebox
import requests
import os

GITHUB_API_RELEASES = "https://api.github.com/repos/user30092/RandomBot/releases/latest"
VERSION_FILE = "version.txt"

def get_current_version():
    if not os.path.exists(VERSION_FILE):
        return "0.0.0"
    with open(VERSION_FILE, "r") as f:
        return f.read().strip()

def set_current_version(version):
    with open(VERSION_FILE, "w") as f:
        f.write(version)

def download_asset(url, filename):
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось скачать обновление:\n{e}")
        return False

def check_update():
    try:
        response = requests.get(GITHUB_API_RELEASES, timeout=5)
        response.raise_for_status()
        data = response.json()
        latest = data["tag_name"]
        current = get_current_version()
        if latest != current:
            if messagebox.askyesno("Обновление", f"Доступна новая версия: {latest}\nОбновить сейчас?"):
                # Найти первый asset (например, .zip или .exe)
                assets = data.get("assets", [])
                if not assets:
                    messagebox.showerror("Ошибка", "Нет доступных файлов для загрузки.")
                    return
                asset = assets[0]
                url = asset["browser_download_url"]
                filename = asset["name"]
                if download_asset(url, filename):
                    set_current_version(latest)
                    messagebox.showinfo("Готово", f"Файл {filename} скачан.\nВерсия обновлена до {latest}.")
        else:
            messagebox.showinfo("Обновление", "У вас последняя версия.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось проверить обновление:\n{e}")

root = tk.Tk()
root.title("Обновлятор")
root.resizable(False, False)
root.geometry("300x180")
check_btn = tk.Button(root, text="Проверить обновление", command=check_update)
check_btn.pack(padx=10, pady=10)
version_lbl = tk.Label(root, text=f"Текущая версия: {get_current_version()}")
version_lbl.pack(padx=10, pady=5)
author_btn = tk.Button(root, text="О Авторе", command=lambda: messagebox.showinfo("Автор", "Автор: user30092\nРепозиторий:user30092/Updater"))
author_btn.pack(padx=10, pady=10)

root.mainloop()