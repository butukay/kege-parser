import os
from os.path import isdir

class Problem:
    task_type: int
    task_id: int

    task_text: str

    input_file_url: str | None = None

    def get_file_path(self):
        if not os.path.isdir(os.path.join(os.getcwd(), f"Задание {self.task_type}")):
            os.mkdir(f"Задание {self.task_type}")

        return os.path.join(os.getcwd(), f"Задание {self.task_type}/{self.task_id}.py")

    def get_input_file_path(self):
        if not os.path.isdir(os.path.join(os.getcwd(), f"Задание {self.task_type}")):
            os.mkdir(os.path.join(os.getcwd(), f"Задание {self.task_type}"))

        if not os.path.isdir(os.path.join(os.getcwd(), f"Задание {self.task_type}/input")):
            os.mkdir(os.path.join(os.getcwd(), f"Задание {self.task_type}/input"))

        return os.path.join(os.getcwd(), f"Задание {self.task_type}/input/{self.task_id}.txt")

    def __str__(self):
        return f"Задание №{self.task_type} - {self.task_id} [https://inf-ege.sdamgia.ru/problem?id={self.task_id}]"

