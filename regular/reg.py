import csv
import re
from pprint import pprint

# === Чтение исходного CSV ===
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# === Заголовок (поля) ===
header = contacts_list[0]
contacts = contacts_list[1:]

# === 1. Разбор ФИО ===
new_contacts = []
for contact in contacts:
    # Склеиваем первые три поля (в них может быть Ф, ИО или ФИО)
    full_name = " ".join(contact[:3]).split()
    # Добавляем пустые элементы, если чего-то не хватает
    while len(full_name) < 3:
        full_name.append("")
    lastname, firstname, surname = full_name[:3]

    # Остальные поля оставляем как есть
    organization = contact[3] if len(contact) > 3 else ""
    position = contact[4] if len(contact) > 4 else ""
    phone = contact[5] if len(contact) > 5 else ""
    email = contact[6] if len(contact) > 6 else ""

    new_contacts.append([lastname, firstname, surname, organization, position, phone, email])

# === 2. Приведение телефонов к формату ===
phone_pattern = re.compile(
    r"(\+7|8)?\s*\(?(?P<code>\d{3})\)?[-\s]*(?P<p1>\d{3})[-\s]*(?P<p2>\d{2})[-\s]*(?P<p3>\d{2})(?:\s*\(?(доб\.)\s*(?P<ext>\d+)\)?)?"
)

formatted_contacts = []
for contact in new_contacts:
    phone = contact[5]
    match = phone_pattern.search(phone)
    if match:
        code = match.group("code")
        p1, p2, p3 = match.group("p1"), match.group("p2"), match.group("p3")
        ext = match.group("ext")
        formatted_phone = f"+7({code}){p1}-{p2}-{p3}"
        if ext:
            formatted_phone += f" доб.{ext}"
        contact[5] = formatted_phone
    formatted_contacts.append(contact)

# === 3. Объединение дубликатов (по Фамилии + Имени) ===
merged = {}
for contact in formatted_contacts:
    key = (contact[0], contact[1])  # lastname + firstname
    if key not in merged:
        merged[key] = contact
    else:
        # объединяем непустые поля
        for i in range(len(contact)):
            if not merged[key][i] and contact[i]:
                merged[key][i] = contact[i]

result_contacts = list(merged.values())

# Добавляем заголовок
result_contacts.insert(0, header)

# === Запись в итоговый CSV ===
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(result_contacts)

print("✅ Файл 'phonebook.csv' успешно сформирован!")
pprint(result_contacts[:5])