import json
import os

DEFAULT_PATH = ''



def save_file_json(name_of_file, data, path=DEFAULT_PATH, rewrite=True):
    writepath = f'{path}{name_of_file}.json'
    if os.path.exists(writepath) == True and not rewrite:
        raise Exception('File already exists')
    with open(writepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_file_txt(name_of_file, data, path=DEFAULT_PATH, rewrite=False):
    writepath = f'{path}{name_of_file}.json'
    if os.path.exists(writepath) == True and not rewrite:
        raise Exception('File already exists')
    with open(f'{path}{name_of_file}.txt', 'w', encoding='utf-8') as f:
        f.write(data)

