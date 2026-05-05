import json
import os
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

FAVORITES_FILE = "favorites.json"

if os.path.exists(FAVORITES_FILE):
    with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
        favorites = json.load(f)
else:
    favorites = {}  

print("Добро пожаловать в GitHub User Finder!")

while True:
    print("\n--- Меню ---")
    print("1 — Найти пользователя GitHub")
    print("2 — Показать избранное")
    print("3 — Выйти")
    choice = input("Выберите действие (1-3): ").strip()

    if choice == "1":
        username = input("Введите имя пользователя GitHub: ").strip()

        if not username:
            print("Ошибка: имя пользователя не может быть пустым!")
            continue

        url = f"https://api.github.com/users/{username}"

        try:
            with urlopen(url) as response:
                data = response.read().decode("utf-8")
                user = json.loads(data)  

            print("\n Пользователь найден!")
            print(f"Логин: {user['login']}")
            print(f"Имя: {user.get('name', 'Не указано')}")
            print(f"Местоположение: {user.get('location', 'Не указано')}")
            print(f"Публичных репозиториев: {user['public_repos']}")

            add = input("Добавить этого пользователя в избранное? (да/нет): ").lower()
            if add == "да":
                favorites[user['login']] = {
                    "name": user.get("name", "Не указано"), "location": user.get("location", "Не указано"), "repos": user["public_repos"]}
                with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
                    json.dump(favorites, f, indent=2, ensure_ascii=False)
                print("Пользователь добавлен в избранное!")

        except HTTPError as e:
            if e.code == 404:
                print("Пользователь не найден. Проверьте имя и попробуйте снова.")
            else:
                print(f"Ошибка HTTP: {e.code}")
        except URLError as e:
            print(f"Ошибка сети: не удалось подключиться к GitHub. Проверьте интернет-соединение. ({e})")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

    elif choice == "2":
        if not favorites:
            print("В избранном пока никого нет.")
        else:
            print("\n--- Ваши избранные пользователи ---")
            for login, data in favorites.items():
                print(f"- {login}: {data['name']} ({data['location']}), репозиториев: {data['repos']}")

    elif choice == "3":
        print("До свидания!")
        break

    else:
        print("Неверный выбор. Введите 1, 2 или 3.")
