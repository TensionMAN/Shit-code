import imghdr
import os
import os.path
import time
import shutil
import requests

start_time = time.time()
checkdir = r"D:\YOUR_PATH"
deleted_files_dir = r"C:\YOUR_PATH"
files_tree = os.walk(checkdir)
file_counter = 0
deleted_file_counter = 0
log_deleted_file = open("deleted.txt", "a") #открываем запись в лог
tg_url=r"https://api.telegram.org/bot[KEY]/sendMessage?chat_id=[CHAT_ID]&text=ACHTUNG!"

#Перебираем директорию
for address, dirs, files in files_tree:
        for file in files:
                file_counter += 1
                full_path = os.path.join(address, file).replace("\\","/") #вычисляем полный путь для передачи в imghdr
                file_directory = os.path.join(address)
                extension = imghdr.what(full_path) #узнаем формат изображения
                if extension != "jpeg": #Проверка условия что картинка не является jpegом
                        if file == "Thumbs.db" or file == "sync.ffs_db": #исключение из логирования системных файлов
                                        if full_path != "D:/YOUR_ROOT_MIRROR_SYNC_FOLDER_PATH/sync.ffs_db": #доп проверка на корневой файл синхронизации
                                                os.remove(os.path.join(file_directory, file)) #все равно удаляем, во измежание попыток мимикрирования под системный файл
                                        else:
                                                print(full_path + " файл синхронизации sync, не трогаем")
                        else:
                                deleted_file_counter += 1
                                print(file + " WARNING, FILE WILL BE DELETED")
                                shutil.move(os.path.join(file_directory, file), os.path.join(deleted_files_dir, file)) #Переносим файл в карантин для аудита
                                log_deleted_file.write(full_path + '\n') #пишем в лог полный путь и имя файла
                                requests.post(tg_url)
                else:
                        pass
                        #print(file + " FILE IS JPEG") #не трогаем


log_deleted_file.close() #закрываем запись в лог

#Debug info
print("Обработано " + str(file_counter) + " файлов")
print("Перемещено в карантин " + str(deleted_file_counter) + " файлов")
print("--- %s seconds ---" % (time.time() - start_time))

