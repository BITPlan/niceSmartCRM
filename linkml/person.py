# Auto generated from person_linkml.yaml by pythongen.py version: 0.9.0
# Generation date: 2024-01-13T16:35:10
# Schema: person
#
# id: https://smartcrm.bitplan.com/linkml/person
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PERSON = CurieNamespace('person', 'https://smartcrm.bitplan.com/linkml/person')
DEFAULT_ = PERSON


# Types

# Class references
class PersonPersonNumber(extended_str):
    pass


@dataclass
class Person(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSON.Person
    class_class_curie: ClassVar[str] = "person:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = PERSON.Person

    person_number: Union[str, PersonPersonNumber] = None
    kind: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.person_number):
            self.MissingRequiredField("person_number")
        if not isinstance(self.person_number, PersonPersonNumber):
            self.person_number = PersonPersonNumber(self.person_number)

        if self.kind is not None and not isinstance(self.kind, str):
            self.kind = str(self.kind)

        super().__post_init__(**kwargs)


@dataclass
class Persons(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSON.Persons
    class_class_curie: ClassVar[str] = "person:Persons"
    class_name: ClassVar[str] = "Persons"
    class_model_uri: ClassVar[URIRef] = PERSON.Persons

    persons: Optional[Union[Dict[Union[str, PersonPersonNumber], Union[dict, Person]], List[Union[dict, Person]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="persons", slot_type=Person, key_name="person_number", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.person__person_number = Slot(uri=PERSON.person_number, name="person__person_number", curie=PERSON.curie('person_number'),
                   model_uri=PERSON.person__person_number, domain=None, range=URIRef)

slots.person__kind = Slot(uri=PERSON.kind, name="person__kind", curie=PERSON.curie('kind'),
                   model_uri=PERSON.person__kind, domain=None, range=Optional[str])

slots.persons__persons = Slot(uri=PERSON.persons, name="persons__persons", curie=PERSON.curie('persons'),
                   model_uri=PERSON.persons__persons, domain=None, range=Optional[Union[Dict[Union[str, PersonPersonNumber], Union[dict, Person]], List[Union[dict, Person]]]])
