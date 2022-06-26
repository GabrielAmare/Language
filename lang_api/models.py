import dataclasses
import os

import tools.files

__all__ = [
    'File',
    'Lang'
]

LANGS_DIR = "../interactive_ide/src/assets/langs"
FILES_DIR = "../interactive_ide/src/assets/files"


@dataclasses.dataclass
class File:
    repo: str
    filename: str
    content: str
    lang: str | None
    
    @classmethod
    def save(cls, repo: str, filename: str, content: str):
        fp = f"{FILES_DIR}/{repo}/{filename}"
        tools.files.save_text_file(fp, content)
        return cls.load(repo, filename)
    

@dataclasses.dataclass
class Lang:
    name: str
    version: str
    data: list
    styles: dict
    
    @classmethod
    def load(cls, name: str, version: str):
        version = version.replace('_', '.')
        
        base = f"{LANGS_DIR}/{name}_{version.replace('.', '_')}"
        data = tools.files.load_json_file(f"{base}/data.json")
        
        try:
            styles = tools.files.load_json_file(f"{base}/styles.json")
        except FileNotFoundError:
            styles = {'default': {}}
        
        return cls(
            name=name,
            version=version,
            data=data,
            styles=styles
        )
    
    
