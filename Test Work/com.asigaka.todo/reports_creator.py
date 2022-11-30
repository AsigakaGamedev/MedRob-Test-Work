import json
import requests
import datetime
import reports_files

todos_url = "https://json.medrocket.ru/todos"
users_url = "https://json.medrocket.ru/users"
max_chars_in_title = 46


def get_json_from_url(url):
    try:
        request = requests.get(url)
        json_from_request = request.text

        return json.loads(json_from_request)
    except Exception as conEx:
        print(conEx)


def get_user_tasks(user_id):
    all_tasks = get_json_from_url(todos_url)
    user_tasks = []

    for task in all_tasks:
        if 'userId' in task and 'title' in task:
            if task['userId'] == user_id:
                user_tasks.append(task)

    return user_tasks


def get_verified_task_title(task_title):
    if len(task_title) > max_chars_in_title:
        task_title = task_title[: max_chars_in_title] + "..."

    return task_title


def get_verified_reported_tasks(tasks_count, tasks_enumeration, tasks_success_placeholder,
                                tasks_not_enough_placeholder):
    tasks_report = ""
    if tasks_count > 0:
        tasks_report = f"## {tasks_success_placeholder} ({tasks_count}) {tasks_enumeration}"
    else:
        tasks_report = f"## {tasks_not_enough_placeholder}"

    return tasks_report


def get_tasks_report_str(users_tasks):
    actual_tasks_count = 0
    completed_tasks_count = 0

    actual_tasks_enumeration = ""
    completed_tasks_tasks_enumeration = ""

    for task in users_tasks:
        if 'userId' in task and 'title' in task:
            if task['completed']:
                actual_tasks_enumeration += f"\n- {get_verified_task_title(task['title'])}"
                actual_tasks_count += 1
            else:
                completed_tasks_tasks_enumeration += f"\n- {get_verified_task_title(task['title'])}"
                completed_tasks_count += 1

    tasks_report_str = f"{get_verified_reported_tasks(actual_tasks_count, actual_tasks_enumeration, 'Актуальные задачи', 'Актуальных задач нет')}" \
                       f"\n\n{get_verified_reported_tasks(completed_tasks_count, completed_tasks_tasks_enumeration, 'Завершённые задачи', 'Завершённых задач нет')}"

    return tasks_report_str


def write_reports():
    users_list = get_json_from_url(users_url)
    report_time = datetime.datetime.today().strftime("%d.%m.%Y %H:%M")

    try:
        for user in users_list:
            user_tasks = get_user_tasks(user['id'])

            report_str = f"# Отчёт для {user['company']['name']}." \
                         f"\n{user['name']} <{user['email']}> {report_time}" \
                         f"\nВсего задач: {len(user_tasks)}" \
                         f"\n" \
                         f"\n{get_tasks_report_str(user_tasks)}"

            print()
            reports_files.create_report_file(user['name'], report_str)
    except TypeError as ex:
        print(ex)
