import json
import os
import time

import flask
from flask import Flask
from flask_cors import CORS

from tools import files

__all__ = [
    'app'
]

app = Flask(__name__)
CORS(app)

ASSETS_DIR = "../interactive_ide/src/assets"
LANGS_DIR = ASSETS_DIR + "/langs"
FILES_DIR = ASSETS_DIR + "/files"


class Errors:
    REPOSITORY_NOT_FOUND = "REPOSITORY_NOT_FOUND"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"


class Routes:
    LANGS = '/langs'
    LANG = '/langs/<lang_name>/<lang_version>'
    REPOS = '/repos'
    REPO = '/repos/<repo_name>'
    FILE = '/repos/<repo_name>/files/<file_name>'


def _valid_json(data, code: int = 200):
    return flask.jsonify(data), code


def _error_json(data, code: int):
    return flask.jsonify({'error': data}), code


@app.route(Routes.LANGS, methods=['GET'])
def get_lang_list():
    """Return the list of langs available."""
    data = []
    for versioned_name in os.listdir(LANGS_DIR):
        name, version = versioned_name.split('_', 1)
        version = version.replace('_', '.')
        data.append({'name': name, 'version': version})
    
    return _valid_json(data, 200)


@app.route(Routes.LANG, methods=['GET'])
def get_lang(lang_name: str, lang_version: str):
    lang_version = lang_version.replace('_', '.')
    
    base = f"{LANGS_DIR}/{lang_name}_{lang_version.replace('.', '_')}"
    lang_data = files.load_json_file(f"{base}/data.json")
    
    # TODO : this should not belong here.
    try:
        lang_styles = files.load_json_file(f"{base}/styles.json")
    except FileNotFoundError:
        lang_styles = {'default': {}}
    
    return _valid_json({
        'name': lang_name,
        'version': lang_version,
        'data': lang_data,
        'styles': lang_styles
    }, 200)


@app.route(Routes.REPOS, methods=['GET'])
def get_repo_list():
    """Return the list of repos available."""
    return _valid_json(['public'], 200)


@app.route(Routes.REPO, methods=['GET'])
def get_repo(repo_name: str):
    repo_path = os.path.join(FILES_DIR, repo_name)
    
    if not os.path.isdir(repo_path):
        return _error_json({
            'code': Errors.REPOSITORY_NOT_FOUND,
            'args': {'name': repo_name}
        }, 404)
    
    return _valid_json({
        'name': repo_name,
        'files': [
            filename
            for filename in os.listdir(repo_path)
        ]
    }, 200)


EXTENSION_DEFAULT_LANG = {
    '.dbd': {'name': 'database', 'version': '1.2.0'},
    '.db_1_2_0': {'name': 'database', 'version': '1.2.0'},
    '.json': {'name': 'json', 'version': '1.0.0'},
    '.bnf': {'name': 'bnf', 'version': '1.0.0'},
}


@app.route(Routes.FILE, methods=['GET'])
def get_file(repo_name: str, file_name: str):
    fp = f"{FILES_DIR}/{repo_name}/{file_name}"
    
    if not os.path.isfile(fp):
        return _error_json({
            'code': Errors.FILE_NOT_FOUND,
            'args': {'repo_name': repo_name, 'file_name': file_name}
        }, 404)
    
    content = files.load_text_file(fp)
    
    ext = os.path.splitext(file_name)[1]
    
    return _valid_json({
        'repo': repo_name,
        'name': file_name,
        'content': content,
        'lang': EXTENSION_DEFAULT_LANG.get(ext)
    }, 200)


@app.route(Routes.FILE, methods=['PUT'])
def save_file(repo_name: str, file_name: str):
    fp = f"{FILES_DIR}/{repo_name}/{file_name}"
    data = json.loads(flask.request.data)
    content = data['content']
    content = content.rstrip() + '\n'
    files.save_text_file(fp, content)
    return get_file(repo_name, file_name)
