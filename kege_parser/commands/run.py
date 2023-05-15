import subprocess
import time
import sys
import os

from kege_parser.api import get_test_answers

def get_run_status_text(start_time: float, processes: list[subprocess.Popen], results: dict, times: dict, test: bool, answers_dict: dict, my_answers: bool, right_answers: bool, kb_interrupt: bool = False) -> str:
    text = ""

    time_since_start = time.time() - start_time

    for k in range(1, len(processes)+1):
        path = str(processes[k-1].args).split(" ")[-1]

        with open(path, "r") as f:
            test_icon = ""

            if test:
                if k not in results:
                    test_icon = "[.]"

                    if kb_interrupt:
                        test_icon = "\033[34m[*]\033[0m - INT"
                elif not results[k]:
                    test_icon = "[ ]"
                elif "time limit" in results[k]:
                    test_icon = "\033[93m[*]\033[0m - TLE"
                elif answers_dict[k].strip() == results[k].replace("\n", " ").strip():
                    test_icon = "\033[92m[+]\033[0m"
                else:
                    test_icon = "\033[91m[-]\033[0m"

            secs_len = len(f"{time_since_start:.3f}")
            text += f"{k:>2} {f.readline()[:-1]:<21} {times.get(k, time_since_start):{secs_len}.3f} сек. {test_icon}" + "\n"

        if my_answers:
            my_ans = results.get(k, "...").replace('\n', '').strip()
            text += f"Ваш ответ: {my_ans}" + "\n"

        if right_answers:
            r_ans = answers_dict.get(k, "").replace("\n", "").strip()
            text += f"Правильный ответ: {r_ans}" + "\n"

        if my_answers or right_answers:
            text += "\n"

    return text


def run(test_id: int, test: bool, my_answers: bool, right_answers: bool, time_limit: int | float, quiet: bool):
    answers_dict = {int(a['i']): a['answer'] for a in (get_test_answers(test_id) if test else [])}

    print()
    print(f"Запускаю тест №{test_id}...")

    paths = [ f"{test_id}/{path}" for path in sorted(os.listdir(str(test_id))) ]
    commands = [ f"python3 {path}" for path in paths ]

    processes = [
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for cmd in commands
    ]

    print('\033[?25l', end="")

    start_time = time.time()
    results, times = {}, {}

    cursor_start_buffer = True
    linesc = 0

    try:
        while len(results.keys()) < len(commands):
            for i, proc in enumerate(processes, 1):
                status = proc.poll()

                if status == None:
                    if time.time() - start_time > time_limit:
                        results[i] = "time limit :("
                        times[i] = time_limit

                        proc.kill()

                    continue

                if i not in results:
                    assert proc.stdout is not None
                    assert proc.stderr is not None

                    results[i] = proc.stdout.read().decode()
                    results[i] += proc.stderr.read().decode()

                    if status != 0:
                        results[i] += f"command{i} failed with status {status}"

                    times[i] = time.time() - start_time


            text = get_run_status_text(start_time, processes, results, times, test, answers_dict, my_answers, right_answers)
            linesc = len(text.split('\n'))

            print(text)
            cursor_start_buffer = False

            time.sleep(0.01)

            sys.stdout.write(f"\u001b[{linesc}A") # move cursor up
            cursor_start_buffer = True

    except KeyboardInterrupt:
        if not cursor_start_buffer:
            sys.stdout.write(f"\u001b[{linesc}A") # move cursor up
            sys.stdout.write(f"\u001b[0G") # moves cursor to column 0

        text = get_run_status_text(start_time, processes, results, times, test, answers_dict, my_answers, right_answers, kb_interrupt=True)
        print(text)
        cursor_start_buffer = False

        print("\rKeyboardInterrupt")

        for p in processes:
            if p.poll() is None:
                p.terminate()

        print("Все запущенные процесы завершены")

    if cursor_start_buffer:
        sys.stdout.write(f"\u001b[{linesc}B") # move cursor down

    sys.stdout.write('\033[?25h') # show cursor

