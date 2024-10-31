# Config1
Вариант №26
Задание №1
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
tar. Эмулятор должен работать в режиме CLI.
Конфигурационный файл имеет формат ini и содержит:
• Имя компьютера для показа в приглашении к вводу.
• Путь к архиву виртуальной файловой системы.
• Путь к лог-файлу.
• Путь к стартовому скрипту.
Лог-файл имеет формат xml и содержит все действия во время последнего
сеанса работы с эмулятором. Для каждого действия указаны дата и время.
Стартовый скрипт служит для начального выполнения заданного списка
команд из файла.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:
1. echo.
2. uptime.
Все функции эмулятора должны быть покрыты тестами, а для каждой из
поддерживаемых команд необходимо написать 3 теста.

## Обзор

**Shell Emulator CLI** — это эмулятор командной строки, написанный на Python, который имитирует интерфейс терминала, похожего на Unix. Эмулятор позволяет выполнять базовые операции, такие как:
- вывод содержимого каталогов;
- переход между директориями;
- создание новых файлов;
- отображение текущей даты и времени;
- проверка размера файлов и директорий внутри виртуальной файловой системы, загружаемой из архива `.tar`.

## Функционал

- **Загрузка файловой системы**: Виртуальная файловая система загружается из архива `.tar`, указанного в конфигурационном файле.
- **Команда `ls`**: Отображение содержимого текущего каталога.
- **Команда `cd`**: Переход в указанный каталог.
- **Команда `echo`**: Вывод сообщения.
- **Команда `uptime`**: Вывод времени прошедшего с начала программы.
- **Команда `exit`**: Завершение работы эмулятора.
