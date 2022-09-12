import os
import random
from datetime import datetime

today = datetime.now().strftime('%d-%m-%y')
fname_daily = "./daily_words/" + today + ".txt"
lines = []
size_lines = 0
fname = ""
fname_all = "all_words.txt"


def openFile():
    global fname, size_lines, lines
    lines = []
    os_root = '/' if os.name != 'nt' else '\\'
    fn_list = []
    path = '.' + os_root
    for root, dirs, files in os.walk('.'):
        i = 0
        if fname and path + fname != root:
            continue
        if len(dirs) > 0:
            print("\nDirectories list:")
            for dir in dirs:
                i += 1
                print(f"{i}. {dir}")
                fn_list.append(dir)

        print("\nFiles list:")
        for fn in files:
            if fn.find('.txt') != -1:
                i += 1
                print(f"{i}. {fn}")
                fn_list.append(fn)

        i = input("\nSelect the number (--c to create): ")
        if i.find('--c') != -1:
            fname = input("\nEnter the filename (without .txt): ") + ".txt"
            fname = root + os_root + fname if root != '.' else fname
            return
        else:
            fname = fn_list[int(i) - 1]

        if fname.find('.txt') != -1:
            fname = root + os_root + fname if root != '.' else fname
            break
        else:
            if root != '.':
                path = root + os_root
            fn_list = []

    with open(fname, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            lines.append(line)

    size_lines = len(lines)


def en_ua_ex(line):
    return line.split(' = ')


def ua_to_en():
    print("\nTranslate to English ...")
    global size_lines
    incorrect = []
    count, k = 0, 0
    for i in lines:
        k += 1
        answ = ""
        en, ua, se = en_ua_ex(i)
        # ex = ex.replace(' / ', '\n')
        # se = se.replace(' / ', '\n')
        print(f"\n{k}/{size_lines}| Sentence: {ua}")

        answ = input("Your answer: ").lower()
        if answ == en:
            count += 1
            print(f"+ True +")
        elif answ == '--q' or answ == '--й':
            return
        else:
            print(f"- False - | Correct answer: {en}\nEx: {se}")
            incorrect.append(i)

    print(f"\nResult: {count}/{len(lines)}\n", *incorrect, sep="\n")


def en_to_ua():
    print("\nTranslate to Ukrainian ...")
    incorrect = []
    global size_lines
    count, k = 0, 0
    for i in lines:
        k += 1
        answ = ""
        ua_list = []
        en, ua, se = en_ua_ex(i)
        if ua.find(' / ') != -1:
            ua_list = ua.split(' / ')
        print(f"\n{k}/{size_lines}| Sentence: {en}")

        answ = input("Your answer: ").lower()
        flag = False
        if len(ua_list) > 0:
            for i in ua_list:
                if i == answ:
                    flag = True
                    break
        if answ == ua or flag:
            count += 1
            print(f"+ True + | {ua}")
        elif answ == '--q' or answ == '--й':
            return
        else:
            print(f"- False - | Correct answer: {ua}\nEx: {se}")
            incorrect.append(i)

    print(f"\nResult: {count}/{len(lines)}\n", *incorrect, sep="\n")


def add_word():
    # global fname, fname_daily
    while True:
        rows = []
        word = input("\nEnter the word ('--q' for exit): ").lower()
        if word == '--q' or word == '--й':
            break

        translate = input("Enter Ukrainian translate: ").lower()
        exmple = input("Enter the sentences for example: ")

        with open(fname, 'a', encoding='utf-8') as f, open(fname_all, 'a', encoding='utf-8') as f2:
            f.write(f"{word} = {translate} = {exmple}\n")
            f2.write(f"{word} = {translate} = {exmple}\n")
            

        if fname != fname_daily:
            with open(fname_daily, 'a', encoding='utf-8') as f3:
               f3.write(f"{word} = {translate} = {exmple}\n")


def menu():
    while True:
        openFile()
        random.shuffle(lines)
        md = int(input("""
Select the checking mode ...
1 - Translate UA --> EN
2 - Translate EN --> UA
3 - Add new words
0 - Quit\n"""))
        if md == 1:
            ua_to_en()
        elif md == 2:
            en_to_ua()
        elif md == 3:
        	add_word()
        elif md == 0:
            return
        else:
            print("Incorrect mode!")


if __name__ == "__main__":
    menu()
    input('Press Enter to close ...')
