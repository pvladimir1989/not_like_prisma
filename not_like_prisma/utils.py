import os


def make_folders():
    os.makedirs('input', exist_ok=True)  # добавляется папка input
    os.makedirs('output', exist_ok=True)  # добавляется папка output
