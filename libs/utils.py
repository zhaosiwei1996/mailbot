import orjson as json
import time
import platform
import requests
import subprocess
import csv
import socket


class BaseUtils:
    @staticmethod
    def get_timestamp():
        return int(time.time() * 1000)

    @staticmethod
    def json_to_string(data):
        return json.dumps(data)

    @staticmethod
    def string_to_json(data):
        return json.loads(data)

    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def write_file(file_path, content):
        with open(file_path, 'w') as file:
            file.write(content)

    @staticmethod
    def append_to_file(file_path, content):
        with open(file_path, 'a') as file:
            file.write(content)

    @staticmethod
    def get_system_type():
        return platform.system()

    @staticmethod
    def send_post_request(url, data):
        response = requests.post(url, json=data)
        return response.json()

    @staticmethod
    def send_get_request(url, params=None):
        response = requests.get(url, params=params)
        return response.json()

    @staticmethod
    def send_delete_request(url):
        response = requests.delete(url)
        return response.json()

    @staticmethod
    def send_put_request(url, data):
        response = requests.put(url, json=data)
        return response.json()

    @staticmethod
    def get_client_ip():
        return socket.gethostbyname(socket.gethostname())

    @staticmethod
    def execute_command(command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        return {
            'output': output.decode('utf-8'),
            'error': error.decode('utf-8'),
            'returncode': process.returncode
        }

    @staticmethod
    def save_csv_file(file_path, data, headers=None):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            if headers:
                writer.writerow(headers)
            writer.writerows(data)

    @staticmethod
    # access logs
    def send_default_info(httpcode, clientip, uri, response):
        data = '''{"httpcode":%s,"clientip":"%s","uri":"%s","response":"%s","timestamp":%s}''' % (
            httpcode, clientip, uri, response, int(time.time() * 1000))
        return json.loads(data)
