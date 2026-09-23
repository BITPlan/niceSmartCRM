"""
Created on 2024-11-16

@author: wf
"""

import i18n

from crm.fields import Fields


class I18nConfig:
    """
    Internationalization module configuration: the labels come from fields.yaml
    """

    languages = ["en", "de"]

    @classmethod
    def config(cls, debug: bool = False):
        fields = Fields.get()
        for lang in cls.languages:
            labels = fields.labels(lang)
            if debug:
                print(f"{len(labels)} {lang} labels from {fields.yaml_path}")
            for key, label in labels.items():
                i18n.add_translation(key, label, locale=lang)
        i18n.set("fallback", "en")
