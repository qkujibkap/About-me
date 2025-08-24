#Задание №%1
def c_b(f):
    cook_book = {}
    with open(f, encoding="utf-8") as file:
        while True:
            dish_name = file.readline().strip()
            if not dish_name:
                break
            ingredients_count = int(file.readline().strip())
            ingredients = []
            for _ in range(ingredients_count):
                ingredient_name, quantity, measure = file.readline().strip().split(" | ")
                ingredients.append({
                    "ingredient_name": ingredient_name,
                    "quantity": int(quantity),
                    "measure": measure
                })
            cook_book[dish_name] = ingredients
            file.readline()
    return cook_book

print(f'Задача №1: \n {c_b("oop/recipes.txt")}')


#Задание №2
print(f'Задание №2')

person_count = 2
dishes = ['Омлет', 'Фахитос', 'Чай', 'Омлет']
print(f'Персон: {person_count}')
print(f'Блюда:\n {dishes}')
def get_shop_list_by_dishes(person_count, dishes):
    shop_list = {}
    cook_book1 = c_b("oop/recipes.txt")
    for dish in dishes:
        if dish in cook_book1:
            for ingr in cook_book1[dish]:
                item = dict(ingr)
                qua = item['quantity'] * person_count
                name = item['ingredient_name']
                meas = item['measure']
                if name in shop_list:
                    shop_list[name]['quantity'] +=qua
                else:
                    shop_list[name] = {'measure': meas, 'quantity': qua}
        else:
            print(f'⚠️ Блюда "{dish}" нет в книге рецептов. ⚠️')
    return shop_list

print(f'Список покупок: \n {get_shop_list_by_dishes(person_count, dishes)}')


#Задание №3
#Получения списка файлов
import os

fo_path = 'oop/data/'
def list_file(folder_path):
    files = [f for f in os.listdir(folder_path) if not f.startswith(".")]
    return files

#Основная часть кода
def line_c(file_path):
    with open(file_path, 'r') as file:
        line_count = sum(1 for line in file)
    return line_count

def calc_sort_line_file(fo_path):
    file_line = []
    for i in list_file(fo_path):
        full_path = fo_path + i
        line_count = line_c(full_path)
        name_file = i
        with open(full_path, 'r') as f:
            text_file = f.read()
        file_line.append((name_file, line_count, text_file))
    file_line.sort(key=lambda x: x[1])
    with open(fo_path + "result.txt", "w") as result:
        for filename, lines, text in file_line:
            result.write(f"В файле: {filename}\n{lines} строк.\n Текст файла: {text}\n")
    return
print(f'Список файлов до выполнения: {list_file(fo_path)}')
calc_sort_line_file(fo_path)
print(f'Список файлов после выполнения: {list_file(fo_path)}')
