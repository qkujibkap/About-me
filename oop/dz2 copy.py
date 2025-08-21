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

calc_sort_line_file(fo_path)
print(list_file(fo_path))