import json
import os

FILENAME = "phonebook.json"

# ---------------------- Загрузка и сохранение ----------------------
def load_contacts():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_contacts(contacts):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=4)
    print("Контакты сохранены!")

# ---------------------- Тестовые данные ----------------------
def fill_test_data():
    contacts = [
        {"id": 1, "название": "Анна Симакова", "phones": [{"type": "mobile", "number": "+37494111222"}], "comment": "Коллега"},
        {"id": 2, "название": "Иван Иванов", "phones": [{"type": "home", "number": "+37410555444"}], "comment": ""},
        {"id": 3, "название": "Мария Петрова", "phones": [{"type": "mobile", "number": "+79161234567"}], "comment": "Старший менеджер"},
    ]
    save_contacts(contacts)

# ---------------------- Показ контактов ----------------------
def show_contacts(contacts):
    if not contacts:
        print("Список контактов пуст.")
        return
    for c in contacts:
        numbers = ", ".join([p["number"] for p in c.get("phones", [])])
        comment = f" | {c['comment']}" if c.get("comment") else ""
        print(f"ID {c['id']}: {c['название']} | {numbers}{comment}")

# ---------------------- Поиск контакта ----------------------
def find_contact(contacts, query=None):
    if query is None:
        query = input("Введите имя или номер для поиска: ").lower()
    results = []
    for c in contacts:
        if query in c["название"].lower() or any(query in p["number"] for p in c.get("phones", [])):
            results.append(c)
    if results:
        show_contacts(results)
    else:
        print("Контакт не найден.")
    return results

# ---------------------- Создание нового контакта ----------------------
def create_contact(contacts):
    название = input("Введите название контакта: ").strip()
    comment = input("Комментарий (необязательно): ").strip()
    phones = []

    while True:
        number = input("Введите номер телефона: ").strip()
        phone_type = input("Тип номера (mobile/home/work): ").strip()
        phones.append({"type": phone_type, "number": number})

        another = input("Добавить ещё номер? (y/n): ").lower()
        if another != "y":
            break

    new_id = max([c["id"] for c in contacts], default=0) + 1
    contacts.append({"id": new_id, "название": название, "phones": phones, "comment": comment})
    print("Контакт создан!")

# ---------------------- Изменение контакта ----------------------
def edit_contact(contacts):
    results = find_contact(contacts)
    if not results:
        return
    try:
        cid = int(input("Введите ID контакта для редактирования: "))
        contact = next(c for c in contacts if c["id"] == cid)
    except:
        print("Контакт не найден.")
        return

    contact["название"] = input(f"Название ({contact['название']}): ") or contact["название"]
    contact["comment"] = input(f"Комментарий ({contact.get('comment','')}): ") or contact.get("comment","")

    for idx, p in enumerate(contact.get("phones", []), start=1):
        print(f"{idx}. {p['type']}: {p['number']}")
        edit_phone = input("Редактировать этот номер? (y/n): ").lower()
        if edit_phone == "y":
            p["type"] = input(f"Тип ({p['type']}): ") or p["type"]
            p["number"] = input(f"Номер ({p['number']}): ") or p["number"]

    add_new = input("Добавить новый номер? (y/n): ").lower()
    if add_new == "y":
        while True:
            number = input("Введите номер телефона: ").strip()
            phone_type = input("Тип номера (mobile/home/work): ").strip()
            contact["phones"].append({"type": phone_type, "number": number})
            another = input("Добавить ещё номер? (y/n): ").lower()
            if another != "y":
                break

    print("Контакт обновлён!")

# ---------------------- Удаление контакта ----------------------
def delete_contact(contacts):
    results = find_contact(contacts)
    if not results:
        return
    try:
        cid = int(input("Введите ID контакта для удаления: "))
        contact = next(c for c in contacts if c["id"] == cid)
    except:
        print("Контакт не найден.")
        return

    contacts.remove(contact)
    print("Контакт удалён!")

# ---------------------- Основное меню ----------------------
def main():
    contacts = load_contacts()

    while True:
        print("\n--- Телефонный справочник ---")
        print("1. Показать все контакты")
        print("2. Создать контакт")
        print("3. Найти контакт")
        print("4. Изменить контакт")
        print("5. Удалить контакт")
        print("6. Заполнить тестовыми данными")
        print("7. Сохранить контакты")
        print("8. Выход")

        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            show_contacts(contacts)
        elif choice == "2":
            create_contact(contacts)
        elif choice == "3":
            find_contact(contacts)
        elif choice == "4":
            edit_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            fill_test_data()
            contacts = load_contacts()
            print("Справочник заполнен тестовыми данными.")
        elif choice == "7":
            save_contacts(contacts)
        elif choice == "8":
            save = input("Сохранить изменения перед выходом? (y/n): ").lower()
            if save == "y":
                save_contacts(contacts)
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
