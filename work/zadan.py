import datetime
import sys, os

def svaz(slovs, vetka: str, visited=None):
    # Используем множество, чтобы отслеживать уже обработанные узлы
    if visited is None:
        visited = set()

    # Проверяем, не обрабатывали ли уже эту ветку
    if vetka in visited:
        return []  # Если уже обработана, возвращаем пустой список

    visited.add(vetka)  # Помечаем текущую ветку как посещённую

    # Создание массива зависимостей
    deps = []
    p = 0
    if slovs[vetka][0]["whot"] != "commit (initial)":
        if "merge" in slovs[vetka][0]["whot"]:
            link = (slovs[vetka][0], slovs[vetka][1])
            deps.append(link)
        for ii in svaz(slovs, slovs[vetka][0]["line"], visited):
            deps.append(ii)

    for i in range(p, len(slovs[vetka]) - 1):
        if slovs[vetka][i]["whot"] == "commit" or slovs[vetka][i]["whot"] == "commit (initial)":
            link = (slovs[vetka][i], slovs[vetka][i+1])
            deps.append(link)
            if "merge" in slovs[vetka][i+1]["whot"]:
                st = slovs[vetka][i+1]["whot"].split(" ")[1]
                link = (slovs[st][-1], slovs[vetka][i+1])
                deps.append(link)
                if len(slovs[st]) != 1:
                    for ii in svaz(slovs, st, visited):
                        deps.append(ii)
        if "rebase" in slovs[vetka][i+1]["whot"]:
            link = (slovs[vetka][i], slovs[vetka][i+1])
            deps.append(link)
            if "merge" in slovs[vetka][i+1]["whot"]:
                st = slovs[vetka][i+1]["whot"].split(" ")[1]
                link = (slovs[vetka][i+1], slovs[st][-1])
                deps.append(link)
                if len(slovs[st]) != 1:
                    for ii in svaz(slovs, st, visited):
                        deps.append(ii)

    return deps



def fetch_apk_dependencies(package_name: str, vetka: str):
    """Получение зависимостей пакета из Alpine Linux."""
    file_list = os.listdir(package_name + '/logs/refs/heads')
    tekush = "master"
    prosh = ""
    slovs = {}
    for i in file_list:
        slovs[i] = []
    head_file = package_name + '/logs/HEAD'
    with open(head_file, 'r', encoding='utf-8') as log_file:
        for line in log_file:
            spl_line = line.split(" ")
            if spl_line[5][6:] == "commit":
                slovs[tekush].append({"whot": "commit (initial)", "when": datetime.datetime.fromtimestamp(int(spl_line[4])).strftime("%Y-%m-%d %H:%M"), "who": spl_line[2], "line": tekush})
            else:
                if spl_line[5][6:] == "commit:":
                    slovs[tekush].append({"whot": "commit", "when": datetime.datetime.fromtimestamp(int(spl_line[4])).strftime("%Y-%m-%d %H:%M"), "who": spl_line[2], "line": tekush})
                elif spl_line[5][6:] == "checkout:":
                    prosh = spl_line[-3]
                    tekush = spl_line[-1][:-1]
                    if slovs[tekush] == []:
                        slovs[tekush].append(slovs[prosh][-1])
                elif spl_line[5][6:] == "merge":
                    slovs[tekush].append({"whot": "merge" + " " + spl_line[6][:-1], "when": datetime.datetime.fromtimestamp(int(spl_line[4])).strftime("%Y-%m-%d %H:%M"), "who": spl_line[2], "line": tekush})
                elif spl_line[5][6:] == "rebase" and spl_line[6] == "(start):":
                    p = 0
                    for i in slovs[spl_line[-1][:-1]]:
                        if p == 1:
                            slovs[tekush].append(i)
                        if slovs[tekush][0] == i:
                            p = 1

    print(slovs)
    deps = svaz(slovs, vetka)
    return deps

def build_graphviz(deps):
    """Формирование Graphviz диаграммы."""
    graphviz_code = 'digraph G {\n'  
    # Инициализируем строку с началом графа в формате Graphviz (ориентированный граф).
    
    added_links = set()  
    # Создаём множество для хранения добавленных связей, чтобы избежать дублирования.

    for src, dest in deps:  
        # Проходим по каждой паре зависимостей (источник, назначение).
        
        link = f'"{src["whot"]} {src["when"]} {src["who"]}" -> "{dest["whot"]} {dest["when"]} {dest["who"]}"'  
        # Формируем строку для Graphviz, представляющую связь между двумя пакетами.
        
        if link not in added_links:  
            # Проверяем, была ли уже добавлена эта связь в граф.
            
            graphviz_code += f'  {link};\n'  
            # Если нет, добавляем её в код графа.
            
            added_links.add(link)  
            # Добавляем связь в множество, чтобы избежать её повторного добавления.
    
    graphviz_code += '}\n'  
    # Закрываем описание графа.
    
    return graphviz_code  # Возвращаем строку с кодом Graphviz.

def main():
    print(0)
    if len(sys.argv) != 5:  
        # Проверяем, что было передано ровно 4 аргумента: путь к программе для визуализации графов имя пакета и путь к файлу для записи результатов.
        
        print("Использование: python zadan.py <visualizer_path> <package_name> <output_path>")  
        
        sys.exit(1)  
        # Завершаем выполнение программы с ошибкой.

    visializer_path = sys.argv[1]  # Первый аргумент — путь к программе для визуализации графов.
    package_name = sys.argv[2]  # Второй аргумент — Путь к анализируемому репозиторию.
    output_path = sys.argv[3]  # Третий аргумент — путь к файлу для записи результатов.
    vetka = sys.argv[4]  # Четвёртый аргумент — ветка

    # Получаем зависимости для указанного пакета
    dependencies = fetch_apk_dependencies(package_name, vetka)  
    # Вызываем функцию fetch_apk_dependencies для получения всех зависимостей пакета.

    if not dependencies:  
        # Если зависимости не найдены, выводим сообщение и завершаем выполнение программы.
        
        print(f"Не удалось найти зависимости для пакета {package_name}")
        sys.exit(1)

    # Строим Graphviz диаграмму
    graphviz_code = build_graphviz(dependencies)  
    
    # Сохраняем результат в указанный файл
    with open(output_path, 'w', encoding='utf-8') as file:  
        # Открываем файл для записи с указанным путём и кодировкой UTF-8.
        
        file.write(graphviz_code)  
        # Записываем код Graphviz в файл.
    
    print(graphviz_code)  

    # Инъекция в командную строку того, что написано, как аргумент у os.system()
    # Если   py task_2.py dot curl output.dot   то:
    # "dot" -Tsvg output.dot > output.svg
    os.system(f'\"{visializer_path}\" -Tsvg {output_path} > {output_path.split(".")[0] + ".svg"}')

if __name__ == "__main__":
    main() 