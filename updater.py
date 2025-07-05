import tkinter as tk
from tkinter import messagebox
import requests
import os

GITHUB_API_RELEASES = "https://api.github.com/repos/<USER>/<REPO>/releases/latest"
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

check_btn = tk.Button(root, text="Проверить обновление", command=check_update)
check_btn.pack(padx=20, pady=20)

root.mainloop()