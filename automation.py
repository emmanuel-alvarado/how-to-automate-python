import os
import json
import re

root = 'node'

def scanDir(subdir_path):
    vars()['subdir_{}'.format(subdir_path.replace('\\','_'))] = listDir(subdir_path)
    vars()['files_{}'.format(subdir_path.replace('\\','_'))] = listFiles(subdir_path)
    if vars()['subdir_{}'.format(subdir_path.replace('\\','_'))]:
        for dir in vars()['subdir_{}'.format(subdir_path.replace('\\','_'))]:
            scanDir(os.path.join(subdir_path, dir))
    mapFilesLinks(subdir_path, vars()['files_{}'.format(subdir_path.replace('\\','_'))])

def scanFile(file):
    match_string = '(?<=\s|\(|\<)https://nodejs.org.*?(?=\s|\)|\>)'
    f = open(file, encoding='utf8').read()
    list_links = re.findall(match_string, f)
    if list_links:
        list_mapping = dict()
        for link in list_links:
            list_mapping[link] = ''
        return {'file_path': file,
                'links': list_mapping}

def mapFilesLinks(root_path, list_files):
    for file in list_files:
        scan_result = scanFile(os.path.join(root_path, file))
        if scan_result:
            list_all_links.append(scan_result)
        else:
            continue

def listDir(root_path):
    list_dir = list()
    for dir in os.listdir(root_path):
        if os.path.isdir(os.path.join(root_path, dir)) \
            and (dir != '.git' and dir != '.github'):
            list_dir.append(dir)
        else:
            continue
    return list_dir

def listFiles(root_path):
    list_files = list()
    for file in os.listdir(root_path):
        if os.path.isfile(os.path.join(root_path, file)) \
            and '.md' in file:
            list_files.append(file)
        else:
            continue
    return list_files

def generateLinks(root):
    global list_all_links
    list_all_links = list()

    list_root_files = listFiles(root)
    list_root_dir = listDir(root)

    mapFilesLinks(root, list_root_files)

    for dir in list_root_dir:
        scanDir(os.path.join(root, dir))

    f = open(f'{root}.json', 'w')
    f.write(json.dumps(list_all_links, indent=4))

def updateLinks(root):
    f = open(f'{root}.json')
    load_file = json.load(f)
    for file in load_file:
        f = open(file['file_path'], encoding='utf8').read()
        for link in file['links'].keys():
            f = f.replace(link, f'{link}/v2')
        f_u = open(file['file_path'], 'w', encoding='utf8')
        f_u.write(f)
    print('All files updated')