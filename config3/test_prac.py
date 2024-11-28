def readd(line: str, pom: int, slov):
    line = line.split(' ')
    line = ' '.join([i for i in line if i != ''])
    if pom == 1:
        if line == "]]":
            return "конец коментария"
        else:
            return "коментарий"
    if len(slov) >= 1:
        if line == ")":
            return "закрытие словаря"
        if line == ").":
            return "закрытие словаря в словаре"
        sp_line = line.split(" ")
        if sp_line[0].isalpha():
            if sp_line[1] == "=>":
                if sp_line[2] == "table(":
                    return "открытие словаря в словаре"
                elif sp_line[2][:3] == '@"' and sp_line[-1][-3:] == '",':
                    return "значение словоря"
                elif sp_line[2][:3] == '${' and sp_line[2][-3:] == '},' and sp_line[2][2:-1].isalpha():
                    return "значение словоря"
                elif sp_line[2][:-1].isdigit() and sp_line[2][-1] == ",":
                    return "значение словоря"
                else:
                    return "ошибка в задании словоря"
    sp_line = line.split(" ")
    if line[:3] == "REM":
        return "однострочный коментарий"
    elif line == "--[[":
        return "Начался коментарий"
    elif sp_line[0] == "set" and sp_line[1].isalpha() and sp_line[2] == "=" and sp_line[3] == "table(":
        return "Начался словарь в переменной"
    elif sp_line[0] == "set" and sp_line[1].isalpha() and sp_line[2] == "=":
            if sp_line[3][:2] == '@"' and sp_line[-1][-1] == '"':
                return "значение переменной"
            elif sp_line[3][:2] == '${' and sp_line[-1][-1] == '}' and sp_line[3][2:-1].isalpha() and len(sp_line) == 4:
                return "значение переменной"
            elif sp_line[3].isdigit() and len(sp_line) == 4:
                return "значение переменной"
            else:
                return "неправильный синтаксис"
    else:
        return "неправильный синтаксис"


    

def all_read(lines):
    slov = {"One line comment": [], "Multiline comments": [], "Variable": {}}
    kom = 0
    slo = []
    for li in lines:
        otv = readd(li, kom, slo)
        if otv == "однострочный коментарий":
            slov["One line comment"].append(li[3:])
        elif otv == "Начался коментарий":
            kom = 1
            slov["Multiline comments"].append("")
        elif otv == "коментарий":
            slov["Multiline comments"][-1] += li + "\n"
        elif otv == "конец коментария":
            kom = 0
        elif otv == "Начался словарь в переменной":
            slo = [li.split(" ")[1]]
            slov["Variable"][li.split(" ")[1]] = {}
        elif  otv == "открытие словаря в словаре":
            li = li.split(' ')
            li = ' '.join([i for i in li if i != ''])
            slo.append(li.split(" ")[0])
            if len(slo) > 1:
                p = 0
                item_slov = slov["Variable"]
                for i in slo:
                    p +=1
                    item_slov = item_slov[i]
                    if len(slo) - 1 == p:
                        item_slov[slo[-1]] = {}
                        break
            else: 
                slov["Variable"][slo[0]] = {}
        elif  otv == "значение словоря":
            li = li.split(' ')
            li = ' '.join([i for i in li if i != ''])
            if len(slo) > 1:
                p = 0
                item_slov = slov["Variable"]
                for i in slo:
                    p +=1
                    item_slov = item_slov[i]
                    if len(slo) - 1 == p:
                        item_slov[slo[-1]][li.split(" ")[0]] = li[li.find(li.split(" ")[2]):-1]
                        break
            else: 
                slov["Variable"][slo[0]][li.split(" ")[0]] = li[li.find(li.split(" ")[2]):-1]
        elif  otv == "закрытие словаря" or otv == "закрытие словаря в словаре":
            slo.pop(-1)
        elif  otv == "значение переменной":
            slov["Variable"][li.split(" ")[1]] = li[li.find(li.split(" ")[3]):]
        elif  otv == "ошибка в задании словоря":
            return "ошибка в задании словоря"
        elif  otv == "неправильный синтаксис":
            return "неправильный синтаксис"
    return slov


lines = '''
REM Это однострочный комментарий
--[[
Это многострочный
комментарий
]]
set a = 8
set vm = table(
    IP => table(
    memory => 1024,
    )
    memory => 1024,
    mem => 1024,
)
set str = @"Цветочки"
set test = ${str}
'''
lines2 = lines.split("\n")
lines2.pop(0)
lines2.pop(-1)
otv = {'One line comment': [' Это однострочный комментарий'], 'Multiline comments': ['Это многострочный\nкомментарий\n'], 'Variable': {'a': '8', 'vm': {'IP': {'memory': '1024'}, 'memory': '1024', 'mem': '1024'}, 'str': '@"Цветочки"', 'test': '${str}'}}
if all_read(lines2) == otv:
    print("Функция all_read работает корректно")
line1 = "mem => 1024"
line2 = "set test = ${str}"
line3 = 'REM Это однострочный комментарий'
otv1 = "неправильный синтаксис"
otv2 = "значение переменной"
otv3 = "однострочный коментарий"
if readd(line1, 0, []) == otv1:
    print("Функция readd работает корректно")
if readd(line2, 0, []) == otv2:
    print("Функция readd работает корректно")
if readd(line3, 0, []) == otv3:
    print("Функция readd работает корректно")