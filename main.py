import argparse
import json
from datetime import datetime

from tabulate import tabulate


def get_count_by_agent(data):
    result = {}
    for item in data:
        user_agent = item['http_user_agent']
        if user_agent not in result:
            result[user_agent] = 0
        result[user_agent] += 1

    tables_data = [{'http_user_agent': k, 'total': v} for k, v in result.items()]
    tables_data.sort(key=lambda x: x['total'], reverse=True)
    return tables_data


def get_average_report(data):
    result = {}
    for item in data:
        handler = item['url']
        if handler not in result:
            result[handler] = {'response_time': 0, 'total': 0}
        result[handler]['total'] += 1
        result[handler]['response_time'] += item['response_time']

    tables_data = [{'handler': k,
                    'total': v['total'],
                    'avg_response_time': round(v['response_time'] / v['total'], 3)}
                   for k, v in result.items()]

    tables_data.sort(key=lambda x: x['total'], reverse=True)
    return tables_data


def print_result(data):
    if len(data) == 0:
        print('Нет данных для выводаю')
        return
    _data = [k.values() for k in data]
    _headers = [k.keys() for k in data][0]
    table = tabulate(_data, _headers, showindex="always")
    print(table)


def read_data_from_file(files, date=None):
    report = []
    if date is not None:
        year, day, month = map(int, date.split('-'))
    for file in files:
        try:
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    item = json.loads(line)
                    item_data = datetime.strptime(item['@timestamp'], "%Y-%m-%dT%H:%M:%S+00:00").date()

                    if date is None or item_data.year == year and item_data.month == month and item_data.day == day:
                        report.append(item)

        except json.JSONDecodeError as err:
            print(f"Ошибка декодирования JSON: {err}")  # Выведет сообщение об ошибке

    return report


report_list = {'average': get_average_report}
report_list = {'by_agent': get_count_by_agent}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', nargs='+', type=str, help='path to file/files with logs')
    parser.add_argument('--report', type=str, help='report name')
    parser.add_argument('-d', '--date', type=str, help='ate in format YYYY-MM-DD')
    args = parser.parse_args()

    logs_data = read_data_from_file(args.file, args.date)
    result = report_list[args.report](logs_data)
    print_result(result)
