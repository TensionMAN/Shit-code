import imghdr
import os
import os.path
import time

start_time = time.time()
checkdir = "ENTER_YOUR_PATH" #директория для работы скрипта
deleted_files_dir = "ENTER_YOUR_PATH" #директория карантин
files_tree = os.walk(checkdir)
file_counter = 0
deleted_file_counter = 0
log_deleted_file = open("deleted.txt", "a")

#Перебираем директорию
for address, dirs, files in files_tree:
	for file in files:
		file_counter += 1
		full_path = os.path.join(address, file).replace("\\","/") #вычисляем полный путь для передачи в imghdr
		file_directory = os.path.join(address) + "/"
		extension = imghdr.what(full_path) #узнаем формат изображения
		if extension == "jpeg": #Проверка условия что картинка является jpegом
			print(file + " PASSED") # не трогаем
		else:
			deleted_file_counter += 1
			print(file + " WARNING, FILE WILL BE DELETED")
			os.replace(file_directory + file, deleted_files_dir + file) #Переносим файл в карантин для аудита
			log_deleted_file.write(full_path + '\n') #пишем в лог полный путь и имя файла

#закрываем запись в лог
log_deleted_file.close()

#Debug info
print("Обработано " + str(file_counter) + " файлов")
print("Удалено " + str(deleted_file_counter) + " файлов")
print("--- %s seconds ---" % (time.time() - start_time))

