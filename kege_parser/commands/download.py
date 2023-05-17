import subprocess
import os

from kege_parser.typing import Problem
from kege_parser.api import get_test_problems, download_file
from kege_parser.utils import comment_text, align_text

def generate_comment_text(problem: Problem) -> str:
    task_comment_text = f"Задание {problem.task_type} - №{problem.task_id}\n"
    task_comment_text += f"[https://inf-ege.sdamgia.ru/problem?id={problem.task_id}]\n"
    task_comment_text += "\n"
    task_comment_text += align_text(problem.task_text).strip()
    task_comment_text += "\n\n"
    task_comment_text += "Условие загружено с помощью butukay-sdamgia-parser"

    return comment_text(task_comment_text)


def generate_input_file_sinppet(problem: Problem) -> str:
    input_file_path = problem.get_input_file_path()

    with open(input_file_path, "r") as f: # read first 3 lines or 240 chars
        file_contents_head = "\n".join([ l.strip() for l in align_text(f.read(240)).split("\n")[:3] ])

    snippet_text = "\n\n"
    snippet_text += f"f = open('{input_file_path}', 'r')\n"
    snippet_text += comment_text(f"Содержание файла: [{problem.input_file_url}]")
    snippet_text += comment_text(file_contents_head)
    snippet_text += comment_text("...")

    return snippet_text


def download(test_id: int, quiet: bool):
    problems = get_test_problems(test_id)

    test_folder_path = f"{test_id}"

    if not os.path.isdir(test_folder_path): # TODO: handle --force
        print("Создаю папку с тестом...")
        os.mkdir(test_folder_path)
    else:
        print("Папка с тестом уже существует")

    for i, p in enumerate(problems, 1):
        print(f"Задача №{str(i).zfill(2)}")
        if os.path.exists(p.get_file_path()): # TODO: handle --force
            print("Эта задача уже загружена") # TODO: hunan readable msg and do smth

            if p.input_file_url:
                if os.path.exists(p.get_input_file_path()):
                    print("Файл к задаче уже загружен")
                else:
                    a = input("Файл к задаче не найден в загрузках. Загрузить заново? (Y/n):")
                    if not a or a == "y":
                        download_file(url=p.input_file_url, path=p.get_input_file_path())

        else:
            with open(p.get_file_path(), 'w') as f:
                f.write(generate_comment_text(p))

                if p.input_file_url:
                    download_file(url=p.input_file_url, path=p.get_input_file_path())

                    f.write(generate_input_file_sinppet(p))

        alias_file_path = os.path.join(os.getcwd(), f"{test_id}/{str(i).zfill(2)}_{p.task_id}.py")
        if not os.path.exists(alias_file_path):
            subprocess.run(["ln", "-s", p.get_file_path(), alias_file_path])
        else:
            print("Линк уже существует") # TODO: hunan readable msg and do smth

