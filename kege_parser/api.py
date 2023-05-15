import requests

from bs4 import BeautifulSoup

from kege_parser.typing import Problem


def get_task_type(prob) -> int:
    nums = prob.find('span', class_="prob_nums")
    return int(nums.text.replace("\xa0", " ").split(" ")[1])


def get_task_id(prob) -> int:
    nums = prob.find('span', class_="prob_nums")
    return int(nums.text.split("№")[-1].strip())


def get_task_text(prob) -> str:
    pbody = prob.find('div', class_="pbody")

    task_text = ""
    for e in pbody.find_all('p'):
        task_text += e.text.strip() + "\n"

    task_text = task_text.replace("Задание 24", "").replace("Задание 26", "")

    return task_text.strip()


def get_task_input_file_url(prob) -> str | None:
    pbody = prob.find('div', class_="pbody")
    href = str(pbody.find('a')['href'])

    if "https://" not in href:
        return "https://inf-ege.sdamgia.ru" + href

    return href


def download_file(url: str, path: str):
    response = requests.get(url)

    if response.status_code == 200:
        with open(path, 'wb') as input_file:
            input_file.write(response.content)


def get_variant_html(test_id: int) -> str: # TODO: exception for invalid test_id
    headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15" }
    url = f"https://inf-ege.sdamgia.ru/test?id={test_id}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html = response.text
    else:
        raise Exception("Не могу загрузить страницу")

    html = html.replace("\xa0", " ") # some strange symbol
    html = html.replace("<sup>", "^").replace("</sup>", "") # replace 10<sup>6</sup> with 10^6

    return html


def get_test_problems(test_id: int) -> list[Problem]:
    html = get_variant_html(test_id)

    soup = BeautifulSoup(html, "lxml")

    problems = []
    for prob in soup.find_all('div', class_='prob_maindiv'):
        problem = Problem()

        problem.task_id = get_task_id(prob)
        problem.task_type = get_task_type(prob)

        problem.task_text = get_task_text(prob)

        if problem.task_type in [24, 26]:
            problem.input_file_url = get_task_input_file_url(prob)

        # print(problem)
        problems.append(problem)

    return problems


def get_results_html(test_id: int) -> str: # TODO: exception for invalid test_id
    headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15" }
    url = f"https://inf-ege.sdamgia.ru/test?id={test_id}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html = response.text
    else:
        raise Exception("Не могу загрузить страницу")

    html = html.replace("\xa0", " ") # some strange symbol
    html = html.replace("<sup>", "^").replace("</sup>", "") # replace 10<sup>6</sup> with 10^6

    return html

def get_test_submit_form_inputs_data(test_id: int):
    html = get_variant_html(test_id)
    soup = BeautifulSoup(html, "lxml")

    form = {}
    for inp in soup.find_all('input', class_='test_inp'):
        form[inp['name']] = inp.get('value', "")

    return form

def get_test_answers(test_id: int) -> list[dict]:
    form_data = get_test_submit_form_inputs_data(test_id)
    response = requests.post("https://inf-ege.sdamgia.ru/test", data=form_data)

    soup = BeautifulSoup(response.text, "lxml")

    table = soup.find_all('table', class_='res_table')[0]

    answers = []
    for row in table.find_all('tr'):
        cells = [ col.text.strip() for col in row.find_all('td') ]

        if len(cells) == 5:
            answers.append({
                "i": cells[0],
                "id": cells[1],
                "type": cells[2],
                "answer": cells[4]
            })


    return answers


