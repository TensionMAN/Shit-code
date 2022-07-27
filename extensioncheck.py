import imghdr
import os
import os.path
import time

start_time = time.time()
checkdir = r"D:\user\Designers2Managers\эскизы"
deleted_files_dir = r"C:\Users\sadmin\Desktop\d2m_check\deleted_files"
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
		if extension != "jpeg": #Проверка условия что картинка не является jpegом
                        if file == "Thumbs.db" or file == "sync.ffs_db": #исключение из логирования системных файлов
                                #print(file + " системный файл") #debug
                                os.remove(file_directory + file) #все равно удаляем, во измежание попыток мимикрирования под системный файл
                        else:
                                deleted_file_counter += 1
                                print(file + " WARNING, FILE WILL BE DELETED")
                                os.replace(file_directory.replace("\\","/") + file, deleted_files_dir.replace("\\","/") + file) #Переносим файл в карантин для аудита
                                log_deleted_file.write(full_path + '\n') #пишем в лог полный путь и имя файла
		else:
                        pass
                        #print(file + " FILE IS JPEG") #не трогаем


log_deleted_file.close() #закрываем запись в лог

#Debug info
print("Обработано " + str(file_counter) + " файлов")
print("Перемещено в карантин " + str(deleted_file_counter) + " файлов")
print("--- %s seconds ---" % (time.time() - start_time))

