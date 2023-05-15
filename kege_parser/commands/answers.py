import json

from kege_parser.api import get_test_answers

def answers(test_id: int, rjson: bool, quiet: bool):
    if not quiet:
        print(f"[i] Получаю ответы на тест №{test_id}")

    answers = get_test_answers(test_id)

    if not quiet:
        print(f"[i] Получены ответы на тест №{test_id}")

    if rjson:
        print(json.dumps(answers))
        return

    print(f"Ответы на тест №{test_id}")

    t = "{:^5s} {:^5s} {:^10s} {}"

    print(t.format('№', 'Тип', 'Задание №', 'Ответ'))
    for row in answers:
        print(t.format(row['i'], row['type'], row['id'], row['answer']))

