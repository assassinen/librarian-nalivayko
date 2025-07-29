import pytest
import io
import sys
import main

data = [{'@timestamp': '2025-06-22T13:59:46+00:00', 'status': 200, 'url': '/api/context/...', 'request_method': 'GET',
         'response_time': 0.04, 'http_user_agent': '...'},
        {'@timestamp': '2025-06-22T13:59:47+00:00', 'status': 200, 'url': '/api/context/...', 'request_method': 'GET',
         'response_time': 0.01, 'http_user_agent': '...'},
        {'@timestamp': '2025-06-22T13:59:47+00:00', 'status': 200, 'url': '/api/context/...', 'request_method': 'GET',
         'response_time': 0.04, 'http_user_agent': '...'}]
result = [{'handler': '/api/context/...', 'total': 3, 'avg_response_time': 0.03}]

@pytest.mark.parametrize('data, result', [(data, result)])
def tests_average_report(data, result):
    assert result == main.get_average_report(data)


file_names = [['example_test_1.log'], ['example_test_1.log', 'example_test_2.log']]
result = [[{'@timestamp': '2025-06-22T13:57:32+00:00', 'status': 200, 'url': '/api/context/...',
            'request_method': 'GET', 'response_time': 0.024, 'http_user_agent': '...'},
           {'@timestamp': '2025-06-22T13:57:32+00:00', 'status': 200, 'url': '/api/context/...',
            'request_method': 'GET', 'response_time': 0.02, 'http_user_agent': '...'},
           {'@timestamp': '2025-06-22T13:57:32+00:00', 'status': 200, 'url': '/api/context/...',
            'request_method': 'GET', 'response_time': 0.024, 'http_user_agent': '...'}],
          [{'@timestamp': '2025-06-22T13:57:32+00:00', 'status': 200, 'url': '/api/context/...',
            'request_method': 'GET',
            'response_time': 0.024, 'http_user_agent': '...'},
           {'@timestamp': '2025-06-22T13:57:32+00:00', 'status': 200, 'url': '/api/context/...',
            'request_method': 'GET',
            'response_time': 0.02, 'http_user_agent': '...'},
           {'@timestamp': '2025-06-22T13:57:32+00:00', 'status': 200, 'url': '/api/context/...',
            'request_method': 'GET',
            'response_time': 0.024, 'http_user_agent': '...'},
           {'@timestamp': '2025-06-22T13:59:47+00:00', 'status': 200, 'url': '/api/homeworks/...',
            'request_method': 'GET',
            'response_time': 0.032, 'http_user_agent': '...'},
           {'@timestamp': '2025-06-22T13:59:47+00:00', 'status': 200, 'url': '/api/homeworks/...',
            'request_method': 'GET',
            'response_time': 0.068, 'http_user_agent': '...'}]
          ]
@pytest.mark.parametrize('file_name, result', zip(file_names, result))
def tests_read_data_from_file(file_name, result):
    assert result == main.read_data_from_file(file_name)


data = [{'handler': '/api/homeworks/...', 'total': 71, 'avg_response_time': 0.158},
        {'handler': '/api/context/...', 'total': 21, 'avg_response_time': 0.043}]
result = '''    handler               total    avg_response_time
--  ------------------  -------  -------------------
 0  /api/homeworks/...       71                0.158
 1  /api/context/...         21                0.043
'''

def tests_print_result():
    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput
    main.print_result(data)
    assert capturedOutput.getvalue() == result
