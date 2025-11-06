import json
import os

FILENAME = "phonebook.json"

# ---------------------- Загрузка и сохранение ----------------------
def load_contacts() -> list:
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Файл пустой или повреждён.")
            return []
    return []

def save_contacts(contacts: list):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=4)

# ---------------------- Очистка справочника ----------------------
def clear_contacts():
    contacts = load_contacts()
    if not contacts:
        print("Справочник уже пуст.")
        return
    while True:
        confirm = input("Вы точно хотите очистить весь справочник? (д/н): ").lower()
        if confirm == 'д':
            save_contacts([])
            print("Справочник очищен!")
            return
        elif confirm == 'н':
            print("Очистка отменена.")
            return
        else:
            print("Неверное значение. Введите 'д' для Да или 'н' для Нет.")

# ---------------------- Проверка номера телефона ----------------------
def validate_phone(number: str, min_length=5) -> bool:
    if not number:
        return False
    num_body = number[1:] if number[0] == '+' else number
    if '#' in num_body and num_body.index('#') < min_length:
        return False
    if any(not (ch.isdigit() or ch == '#') for ch in num_body):
        return False
    digits_count = sum(c.isdigit() for c in num_body)
    if digits_count < min_length:
        return False
    return True

# ---------------------- Тестовые данные ----------------------
def fill_test_data():
    contacts = load_contacts()
    last_id = max([c["id"] for c in contacts], default=0)
    test_data = [
        {"id": last_id + 1, "contact_name": "Анна Симакова", "phones": [{"type": "mobile", "number": "+37494111222"}], "comment": "Коллега"},
        {"id": last_id + 2, "contact_name": "Иван Иванов", "phones": [{"type": "home", "number": "+37410555444"}], "comment": None},
        {"id": last_id + 3, "contact_name": "Мария Петрова", "phones": [{"type": "mobile", "number": "+79161234567"}], "comment": "Старший менеджер"},
    ]
    contacts.extend(test_data)
    save_contacts(contacts)
    print("Справочник заполнен тестовыми данными.")

# ---------------------- Показ контактов ----------------------
def show_contacts(contacts: list):
    print("\n--- Телефонный справочник ---")
    if not contacts:
        print("Список контактов пуст.")
        return
    for idx, c in enumerate(contacts, start=1):
        numbers = ", ".join([f"{p['type']}: {p['number']}" for p in c.get("phones", [])])
        comment = f" | {c['comment']}" if c.get("comment") else ""
        print(f"{idx}. {c['contact_name']} | {numbers}{comment}")

# ---------------------- Поиск контакта ----------------------
def find_contact(contacts: list, query: str = None, show_results=True):
    if query is None:
        query = input("Введите имя, номер или комментарий для поиска (0 для меню): ").lower()
        if query == '0':
            return []
    results = []
    for c in contacts:
        if (query in c["contact_name"].lower() or
            any(query in p["number"] for p in c.get("phones", [])) or
            (c.get("comment") and query in c["comment"].lower())):
            results.append(c)
    if show_results:
        if results:
            show_contacts(results)
        else:
            print("Контакт не найден.")
    return results

# ---------------------- Создание контакта ----------------------
def create_contact(contacts: list):
    print("\n--- Создание контакта ---")
    while True:
        contact_name = input("Введите наименование контакта (0 для меню): ").strip()
        if contact_name == '0':
            return
        if not contact_name:
            print("Имя не может быть пустым.")
            continue
        break

    phones = []
    while True:
        number = input("Введите номер телефона (0 для меню): ").strip()
        if number == '0':
            if phones:
                break
            else:
                return
        if not validate_phone(number):
            print("Неверный формат номера. Допустимо: + в начале, цифры, '#' после мин. 5 цифр.")
            continue

        while True:
            print("Тип номера: 1 - mobile, 2 - home, 3 - work")
            type_choice = input("Выберите тип номера (0 для меню): ").strip()
            if type_choice == '0':
                confirm_exit = input("Сохранить изменения перед выходом? (д/н): ").strip().lower()
                if confirm_exit == 'д':
                    if phones:
                        comment = input("Комментарий для контакта (Enter чтобы пропустить): ").strip() or None
                        new_id = max((c["id"] for c in contacts), default=0) + 1
                        contacts.append({"id": new_id, "contact_name": contact_name, "phones": phones, "comment": comment})
                        save_contacts(contacts)
                return
            if type_choice in ('1', '2', '3'):
                phone_type = {"1": "mobile", "2": "home", "3": "work"}[type_choice]
                break
            else:
                print("Выберите 1, 2 или 3.")

        exists = any(contact_name.lower() == c.get("contact_name", "").lower() and
                     any(number == p.get("number", "") for p in c.get("phones", []))
                     for c in contacts)
        if exists:
            while True:
                confirm = input("Такой контакт уже существует. Создать второй? (д/н или 0 для меню): ").strip().lower()
                if confirm == '0':
                    return
                elif confirm == 'д':
                    break
                elif confirm == 'н':
                    continue
                else:
                    print("Введите д, н или 0.")
                    continue

        phones.append({"type": phone_type, "number": number})
        another = input("Добавить ещё номер? (д/н или 0 для меню): ").strip().lower()
        if another == '0':
            break
        elif another != 'д':
            break

    comment = input("Комментарий для контакта (Enter чтобы пропустить, 0 для меню): ").strip()
    if comment == '0':
        comment = None

    new_id = max((c["id"] for c in contacts), default=0) + 1
    contacts.append({"id": new_id, "contact_name": contact_name, "phones": phones, "comment": comment})
    save_contacts(contacts)
    print("Контакт создан!")

# ---------------------- Изменение контакта ----------------------
def edit_contact(contacts: list):
    print("\n--- Изменение контакта ---")
    results = find_contact(contacts)
    if not results:
        return
    if len(results) == 1:
        contact = results[0]
        print("Найден один контакт:")
        show_contacts([contact])
    else:
        while True:
            try:
                idx = int(input("Укажите номер контакта для изменения (0 для меню): "))
                if idx == 0:
                    return
                if 1 <= idx <= len(results):
                    contact = results[idx - 1]
                    break
            except ValueError:
                pass
            print("Неверный номер. Попробуйте снова.")

    while True:
        print("\nЧто хотите изменить?")
        print("1 - Наименование контакта")
        print("2 - Добавить телефон")
        print("3 - Изменить телефон")
        print("4 - Удалить телефон")
        print("5 - Изменить комментарий")
        print("6 - Выйти из редактирования")
        choice = input("Выберите пункт (0 для меню): ").strip()
        if choice == '0':
            confirm = input("Сохранить изменения перед выходом? (д/н): ").strip().lower()
            if confirm == 'д':
                save_contacts(contacts)
            return
        elif choice == '1':
            contact["contact_name"] = input(f"Наименование ({contact['contact_name']}): ").strip() or contact["contact_name"]
        elif choice == '2':
            while True:
                number = input("Новый номер телефона (0 для меню): ").strip()
                if number == '0':
                    break
                if not validate_phone(number):
                    print("Неверный формат номера.")
                    continue
                while True:
                    print("Тип номера: 1 - mobile, 2 - home, 3 - work")
                    type_choice = input("Выберите тип (0 для меню): ").strip()
                    if type_choice == '0':
                        break
                    if type_choice in ('1', '2', '3'):
                        phone_type = {"1": "mobile", "2": "home", "3": "work"}[type_choice]
                        break
                    else:
                        print("Неверный тип.")
                else:
                    continue
                contact["phones"].append({"type": phone_type, "number": number})
                break
        elif choice == '3':
            # Логика изменения телефона (поиск по индексу)
            if not contact["phones"]:
                print("Телефонов нет.")
                continue
            show_contacts([contact])
            while True:
                try:
                    idx = int(input("Укажите номер телефона для изменения (0 для меню): "))
                    if idx == 0:
                        break
                    if 1 <= idx <= len(contact["phones"]):
                        phone = contact["phones"][idx - 1]
                        new_number = input(f"Новый номер ({phone['number']}): ").strip() or phone['number']
                        if not validate_phone(new_number):
                            print("Неверный формат.")
                            continue
                        while True:
                            type_choice = input(f"Тип номера: 1 - mobile, 2 - home, 3 - work ({phone['type']}): ").strip()
                            if type_choice in ('1','2','3'):
                                phone['type'] = {"1":"mobile","2":"home","3":"work"}[type_choice]
                                break
                            elif type_choice == '':
                                break
                            else:
                                print("Неверный тип.")
                        phone['number'] = new_number
                        break
                except ValueError:
                    print("Некорректный ввод.")
        elif choice == '4':
            if not contact["phones"]:
                print("Телефонов нет.")
                continue
            show_contacts([contact])
            while True:
                try:
                    idx = int(input("Укажите номер телефона для удаления (0 для меню): "))
                    if idx == 0:
                        break
                    if 1 <= idx <= len(contact["phones"]):
                        del contact["phones"][idx-1]
                        print("Телефон удалён.")
                        break
                except ValueError:
                    print("Некорректный ввод.")
        elif choice == '5':
            contact["comment"] = input(f"Комментарий ({contact.get('comment') or 'нет'}): ").strip() or contact.get('comment')
        elif choice == '6':
            save_contacts(contacts)
            print("Изменения сохранены.")
            return
        else:
            print("Выберите 1-6 или 0 для выхода.")

# ---------------------- Удаление контакта ----------------------
def delete_contact(contacts: list):
    print("\n--- Удаление контакта ---")
    results = find_contact(contacts)
    if not results:
        return
    if len(results) == 1:
        contact = results[0]
        print("Найден один контакт:")
        show_contacts([contact])
    else:
        while True:
            try:
                idx = int(input("Укажите номер контакта для удаления (0 для меню): "))
                if idx == 0:
                    return
                if 1 <= idx <= len(results):
                    contact = results[idx-1]
                    break
            except ValueError:
                print("Некорректный ввод.")

    confirm = input("Вы уверены, что хотите удалить этот контакт? (д/н): ").lower()
    if confirm != 'д':
        print("Удаление отменено.")
        return

    contacts.remove(contact)
    save_contacts(contacts)
    print("Контакт удалён!")

# ---------------------- Основное меню ----------------------
def main():
    contacts = load_contacts()
    print("\n--- Меню ---")
    print("1. Показать все контакты")
    print("2. Создать контакт")
    print("3. Найти контакт")
    print("4. Изменить контакт")
    print("5. Удалить контакт")
    print("6. Заполнить тестовыми данными")
    print("7. Очистить справочник")
    print("8. Выход")

    while True:
        choice = input("\nВыберите пункт меню или 0 для показа меню: ").strip()
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
        elif choice == "7":
            clear_contacts()
            contacts = load_contacts()
        elif choice == "8":
            print("Выход из программы.")
            break
        elif choice == "0":
            print("\n--- Меню ---")
            print("1. Показать все контакты")
            print("2. Создать контакт")
            print("3. Найти контакт")
            print("4. Изменить контакт")
            print("5. Удалить контакт")
            print("6. Заполнить тестовыми данными")
            print("7. Очистить справочник")
            print("8. Выход")
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()
