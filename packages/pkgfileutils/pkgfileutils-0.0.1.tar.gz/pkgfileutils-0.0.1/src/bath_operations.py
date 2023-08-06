import os


# 1 — Напишите функцию группового переименования файлов. Она должна:
# * принимать в качестве аргумента желаемое конечное имя файлов.
# При переименовании в конце имени добавляется порядковый номер.
#
# * принимать в качестве аргумента расширение исходного файла.
# Переименование должно работать только для этих файлов внутри каталога.

# * принимать в качестве аргумента расширение конечного файла.
#
# Шаблон переименованного файла: <original_name>_<new_name>_<position>.<new_extention>

def batch_rename(folder, new_name, original_ext, new_extension):
    file_list = os.listdir(folder)
    position = 1

    for filename in file_list:
        if filename.endswith(original_ext):
            original_name = os.path.splitext(filename)[0]
            new_filename = f"{original_name}_{new_name}_{position}.{new_extension}"
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_filename)
            os.rename(old_path, new_path)
            position += 1
