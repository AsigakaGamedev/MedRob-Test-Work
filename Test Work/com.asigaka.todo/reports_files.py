import datetime
import os


reports_path = os.getcwd() + "\\tasks"


def create_report_file(report_username, report_text):
    try:
        if not os.path.exists(reports_path):
            os.mkdir(reports_path)

        path_to_report = reports_path + f"\\{report_username}.txt"

        if os.path.exists(path_to_report):
            raw_creation_time = os.path.getmtime(path_to_report)
            report_creation_time = datetime.datetime.fromtimestamp(raw_creation_time).strftime("%Y-%m-%dT%H-%M")
            old_file_name = f"{reports_path}\\old_{report_username}_{report_creation_time}.txt"

            if not os.path.exists(old_file_name):
                os.rename(path_to_report, old_file_name)

        new_report = open(path_to_report, "w")
        new_report.write(report_text)
        new_report.close()
        print(f"Новый репорт {report_username} записан")
    except Exception as ex:
        print(ex)
