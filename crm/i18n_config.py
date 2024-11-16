"""
Created on 2024-11-16

@author: wf
"""

import os

import i18n


class I18nConfig:
    """
    Internationalization module configuration
    """

    @classmethod
    def config(cls, debug: bool = False):
        module_path = os.path.dirname(os.path.abspath(__file__))
        translations_path = os.path.join(module_path, "resources", "i18n")
        if debug:
            print(f"Loading translations from: {translations_path}")
            print(f"Files in directory: {os.listdir(translations_path)}")
        i18n.load_path.append(translations_path)
        i18n.set("filename_format", "{locale}.{format}")
        i18n.set("file_format", "yaml")
        i18n.set("fallback", "en")
