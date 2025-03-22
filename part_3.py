import csv
import re
import os
from datetime import datetime


def logger(path):
    path_file = path  
    def __logger(old_function):
        start_date_and_time = datetime.now().strftime('%Y-%m-%d, %H:%M:%S.%f')
        name_old_function = old_function.__name__
        def new_function(*args, **kwargs):
            attr_args = args
            attr_kwargs = kwargs
            result = old_function(*args, **kwargs)
            with open(path_file, 'a', encoding='utf-8') as file:
                file.write(f'\nDate and time create: <{start_date_and_time}>. '
                       f'Function\'s name: <{name_old_function}>. ' 
                       f'Arguments: args={args if args else 'hasn\'t'}, '
                       f'kwargs={kwargs if kwargs else 'hasn\'t'} '
                       f'Returned value <{result}>\n')              
            return result
        return new_function
    return __logger


@logger('phone_book.log')
def full_name_correction(contacts_list:list) -> list:
    """Функция распределяет lastname, firstname, surname по соответствующим позициям"""
    for i, row in enumerate(contacts_list):
        if i == 0:
            continue
        else:
            temp_full_name = " ".join(row[:3]).split()
            lastname, firstname, *surname = temp_full_name
            row[0] = lastname
            row[1] = firstname
            row[2] = surname[0] if surname else ""
    return contacts_list

@logger('phone_book.log')
def phone_correction(contacts_list:list) -> list:
    """Функция приводит телефоны к формату +7(999)999-99-99 доб.9999"""
    pattern = re.compile(r'(8|\+7)\s?\(?(\d{3})\)?\s?-?(\d{3})\s?-?(\d{2})\s?-?(\d{2})\s?\(?(доб.)?\s?(\d+)?\)?')
    phone_format = r'+7(\2)\3-\4-\5 \6\7'    
    
    for i, row in enumerate(contacts_list):
        if i == 0:
            continue
        phone_number = row[5]
        if phone_number:                   
            row[5] = pattern.sub(phone_format, phone_number).replace('  ',' ').strip()
    return contacts_list

@logger('phone_book.log')
def group_rows(contacts_list:list) -> list:
    """Функция объединяет повторые строки если совпадает имя и фамилия"""
    unique_contacts = {}
    for i, row in enumerate(contacts_list[1:], start=1):
        key = (row[0], row[1])
        if key not in unique_contacts:
            unique_contacts[key] = row
        else:
            for j in range(len(row)):
                if not unique_contacts[key][j]:
                    unique_contacts[key][j] = row[j] 
    return [contacts_list[0]] + list(unique_contacts.values())





if __name__ == '__main__':

   # Читаем файл в список
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
                     
    # Корректируем список функциями
    group_rows(phone_correction(full_name_correction(contacts_list)))

    # Сохраняем откорректированныей список в новый файл
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)