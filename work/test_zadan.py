import datetime
log_file = ["0000000000000000000000000000000000000000 d08e111b1c24a01f11c49fe8cf15a13d7540b896 OlgaBug <olgahaipriv7177@gmail.com> 1732021347 +0300	commit (initial): first commit\n", "d08e111b1c24a01f11c49fe8cf15a13d7540b896 d08e111b1c24a01f11c49fe8cf15a13d7540b896 OlgaBug <olgahaipriv7177@gmail.com> 1732022463 +0300	checkout: moving from master to firbranch\n", "d08e111b1c24a01f11c49fe8cf15a13d7540b896 5fd60be680f97f74383122fcb76b4e7c62f4dfa7 OlgaBug <olgahaipriv7177@gmail.com> 1732022592 +0300	commit: second commit\n", "5fd60be680f97f74383122fcb76b4e7c62f4dfa7 d08e111b1c24a01f11c49fe8cf15a13d7540b896 OlgaBug <olgahaipriv7177@gmail.com> 1732022773 +0300	checkout: moving from firbranch to master\n", "d08e111b1c24a01f11c49fe8cf15a13d7540b896 5fd60be680f97f74383122fcb76b4e7c62f4dfa7 OlgaBug <olgahaipriv7177@gmail.com> 1732022793 +0300	merge firbranch: Fast-forward\n"]
vetks = ["master", "firbranch"]
def fetch_apk_dependencies(package_name, vetka: str, vetks):
    log_file = package_name
    tekush = "master"
    prosh = ""
    slovs = {}
    for i in vetks:
        slovs[i] = []
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
    return slovs
otv = {'master': [{'whot': 'commit (initial)', 'when': '2024-11-19 16:02', 'who': 'OlgaBug', 'line': 'master'}, {'whot': 'merge firbranch', 'when': '2024-11-19 16:26', 'who': 'OlgaBug', 'line': 'master'}], 'firbranch': [{'whot': 'commit (initial)', 'when': '2024-11-19 16:02', 'who': 'OlgaBug', 'line': 'master'}, {'whot': 'commit', 'when': '2024-11-19 16:23', 'who': 'OlgaBug', 'line': 'firbranch'}]}
if fetch_apk_dependencies(log_file, "master", vetks) == otv:
    print("Функция fetch_apk_dependencies работает корректно")
#
#
#
def svaz(slovs, vetka: str):
    # создание массива зависимостей текущего к следующему
    deps = []
    p = 0
    if slovs[vetka][0]["whot"] != "commit (initial)":
        if "merge" in slovs[vetka][0]["whot"]:
            link = (slovs[vetka][0], slovs[vetka][1])
            deps.append(link)
        # возможно ненужный код
        for ii in svaz(slovs, slovs[vetka][0]["line"]):
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
                    for ii in svaz(slovs, st):
                        deps.append(ii)
        if "rebase" in slovs[vetka][i+1]["whot"]:
            link = (slovs[vetka][i], slovs[vetka][i+1])
            deps.append(link)
            if "merge" in slovs[vetka][i+1]["whot"]:
                st = slovs[vetka][i+1]["whot"].split(" ")[1]
                link = (slovs[vetka][i+1], slovs[st][-1])
                deps.append(link)
                if len(slovs[st]) != 1:
                    for ii in svaz(slovs, st):
                        deps.append(ii)
    return deps
otv2 = [({'whot': 'commit (initial)', 'when': '2024-11-19 16:02', 'who': 'OlgaBug', 'line': 'master'}, {'whot': 'merge firbranch', 'when': '2024-11-19 16:26', 'who': 'OlgaBug', 'line': 'master'}), ({'whot': 'commit', 'when': '2024-11-19 16:23', 'who': 'OlgaBug', 'line': 'firbranch'}, {'whot': 'merge firbranch', 'when': '2024-11-19 16:26', 'who': 'OlgaBug', 'line': 'master'}), ({'whot': 'commit (initial)', 'when': '2024-11-19 16:02', 'who': 'OlgaBug', 'line': 'master'}, {'whot': 'commit', 'when': '2024-11-19 16:23', 'who': 'OlgaBug', 'line': 'firbranch'})]
if svaz(fetch_apk_dependencies(log_file, "master", vetks), "master") == otv2:
    print("Функция svaz работает корректно")