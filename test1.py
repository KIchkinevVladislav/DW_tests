"""
Необходимо написать скрипт (на любом языке, на выбор кандидата), который будет собирать библиотеку zlib из публичного репозитория. Скрипт должен: 
- выкачивать актуальную версию исходного кода проекта: https://github.com/madler/zlib ; 
- собирать проект любым способом из доступных (с помощью Makefile или с использованием проектов для MS Visual Studio, расположенных в каталоге contrib/vstudio); 
- в случае успешной сборки копировать собранные файлы в отдельный каталог, чтобы можно было их затем использовать. 

Сборка должна производится на платформе Windows, с помощью инструментария (toolchain) MS Visual Studio 2015.
Достаточно собрать динамическую библиотеку (dll) в обоих разрядностях. 
"""

import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

# URL проекта
url = "https://github.com/madler/zlib/archive/master.zip"
# Имя временной директории
temp_dir = tempfile.mkdtemp()
# Имя директории для сборки проекта
build_dir = os.path.join(temp_dir, "zlib-master")
# Имя директории для скопированных файлов
output_dir = os.path.join(temp_dir, "output")

# Скачиваем и распаковываем исходники проекта
urllib.request.urlretrieve(url, os.path.join(temp_dir, "zlib.zip"))
with zipfile.ZipFile(os.path.join(temp_dir, "zlib.zip"), 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

# Собираем проект для 32-битной архитектуры
try:
    subprocess.check_call(['msbuild', 'build\\win32\\zlib.sln', '/p:Configuration=Release', '/p:Platform=Win32'])
except subprocess.CalledProcessError:
    print("Сборка проекта для 32-битной архитектуры не удалась.")
    sys.exit(1)

# Собираем проект для 64-битной архитектуры
try:
    subprocess.check_call(['msbuild', 'build\\win32\\zlib.sln', '/p:Configuration=Release', '/p:Platform=x64'])
except subprocess.CalledProcessError:
    print("Сборка проекта для 64-битной архитектуры не удалась.")
    sys.exit(1)

# Проверяем, что файлы были собраны успешно
if os.path.exists(os.path.join(build_dir, 'contrib', 'vstudio', 'vc14', 'Win32', 'Release', 'zlib.dll')) \
        and os.path.exists(os.path.join(build_dir, 'contrib', 'vstudio', 'vc14', 'Win32', 'Release', 'zlib.lib')) \
        and os.path.exists(os.path.join(build_dir, 'contrib', 'vstudio', 'vc14', 'x64', 'Release', 'zlib.dll')) \
        and os.path.exists(os.path.join(build_dir, 'contrib', 'vstudio', 'vc14', 'x64', 'Release', 'zlib.lib')):
    # Копируем файлы в отдельную директорию
    shutil.copy2(os.path.join(build_dir, 'contrib', 'vstudio', 'vc14', 'Win32', 'Release', 'zlib.dll'), output_dir)
    shutil.copy2(os.path.join(build_dir, 'contrib', 'vstudio', 'vc14', 'Win32', 'Release', 'zlib.lib'), output_dir)
    shutil.copy2(os.path.join(build_dir, 'contrib', 'vstudio', 'vc14', 'x64', 'Release', 'zlib.dll'), output_dir)
    shutil.copy2(os.path.join(build_dir, 'contrib', 'vstudio', 'vc14', 'x64', 'Release', 'zlib.lib'), output_dir)
    # выходим из скрипта с кодом 0 (успех)
    sys.exit(0)
else:
    # выходим из скрипта с кодом 1 (ошибка)
    sys.exit(1)
