from pprint import pprint
from functools import reduce
import csv
import re


# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ

# Чтение адресной книги из CSV-файла
def load_data(filename):
    with open(filename, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


# Запись правильной адресной книги в CSV-файл
def save_data(filename, contacts):
    with open(filename, "w", encoding="utf-8", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts)


# парсинг телефона и возврат строки формата
# +7(999)999-99-99 доб.9999
def parse_phone(phone):
    pattern_phone = r"\+?\s?([78]?)\s?[(]?(\d{3})[)]?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})[\s(]*[a-zA-Zа-яА-Я]*[.]?\s*(\d*)\)?"
    phone_split = re.split(pattern_phone, phone)
    if len(phone_split) > 1:
        result = '+' + ('7' if phone_split[1] == '8' else phone_split[1]) \
                 + '(' + phone_split[2] + ')' \
                 + phone_split[3] + '-' + phone_split[4] + '-' + phone_split[5]
        if phone_split[6]:
            result += ' доб.' + phone_split[6]
    else:
        result = phone_split[0]
    return result


# парсинг адресной книги
# Одна запись - это список
# [lastname,firstname,surname,organization,position,phone,email]
def parse(contacts):
    result = []
    for c in contacts:
        # pprint(c)
        new_record = []
        # lastname, firstname, secondname
        for i in range(0, 3):
            names = re.findall(r"([a-zA-Zа-яА-ЯёЁ]+)\s?", c[i])
            new_record += names
        # проверка, что все 3 поля (lastname,firstname,surname) есть
        # иначе добавляем пустые записи
        while len(new_record)<3:
            new_record.append('')
        # organiZation
        new_record.append(c[3])
        # position
        new_record.append(c[4])
        # phone
        phone = parse_phone(c[5])
        new_record.append(phone)
        # email
        new_record.append(c[6])

        # pprint(new_record)
        result.append(new_record)

    return result

# объединение дублирующихся записей
def merge_duplicate_contacts(contacts_list):
    unique_contacts = []
    # цикл по каждой записи в адресной книге
    # contact[0] - lastname
    # contact[1] - firstname
    # contact[2] - surname
    for contact in contacts_list:
        # находим все записи, у которых одинаковые lastname,firstname,
        # и surname одинаковые или пустые
        items = list(filter(lambda x: x[0] == contact[0] and x[1] == contact[1]
                                      and (x[2] == contact[2] or x[2] == '' or contact[2] == ''),
            contacts_list))
        # склеиваем все записи из items:
        # берем i-й элемент у того из items, у которого он заполнен
        joined_item = reduce(lambda x, y: [x[i] or y[i] for i in range(len(contact))], items)
        # добавляем склеенную запись, если ее еще нет в unique_contacts
        # на все одинаковые записи из contact_list будет формироваться
        # один и тот же joined_item
        if joined_item not in unique_contacts:
            unique_contacts.append(joined_item)
    # возврат результата
    return unique_contacts


# ГЛАВНАЯ ФУНКЦИЯ

def main():
    # загрузка адресной книги из файла
    contacts = load_data("phonebook_raw.csv")

    #pprint(contacts)

    # парсинг информации из контактной книги
    result = parse(contacts)

    #pprint(result)

    # объединение дублирующихся записей
    result = merge_duplicate_contacts(result)

    # сохранение в файл
    save_data("phonebook.csv", result)


# КОНСТРУКЦИЯ ДЛЯ ЗАПУСКА ГЛАВНОЙ ФУНКЦИИ

if __name__ == '__main__':
    main()