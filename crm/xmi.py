'''
Created on 2024-01-14

@author: wf
'''
from dataclasses import dataclass,field
import json
from typing import Dict, List, Optional

@dataclass
class TaggedValue:
    name: str
    value: Optional[str] = field(default=None, metadata={"json": "@name", "value": "Value"})

    @classmethod
    def from_dict(cls, node: Dict) -> 'TaggedValue':
        """
        Create a TaggedValue instance from a dictionary.

        Args:
            node (Dict): A dictionary representing a TaggedValue, with keys '@name' and 'Value'.

        Returns:
            TaggedValue: An instance of TaggedValue.
        """ 
        name = node.get('@name')
        value = node.get('Value')
        return cls(name=name, value=value)
        
@dataclass
class ModelElement:
    """
    Base model element class
    """
    name: str
    id: str
    stereotype: str
    visibility: str
    documentation: str
    tagged_values: Dict[str, TaggedValue] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, node: Dict) -> 'ModelElement':
        """
        Create a ModelElement instance from a dictionary.

        Args:
            node (Dict): A dictionary representing a ModelElement.

        Returns:
            ModelElement: An instance of ModelElement.
        """
        element = cls(
            name=node.get('@name'),
            id=node.get('@id'),
            stereotype=node.get('@stereotype'),
            visibility=node.get('@visibility'),
            documentation=node.get('Documentation')
        )

        for tv_list in node.get('taggedValues', {}).values():
            for tv in tv_list:
                tagged_value = TaggedValue.from_dict(tv)
                element.tagged_values[tagged_value.name] = tagged_value

        return element
    
@dataclass
class Attribute(ModelElement):
    is_static: Optional[str]=None
    type: Optional[str] =None

    @classmethod
    def from_dict(cls, node: Dict) -> 'Attribute':
        attribute = super().from_dict(node)
        attribute.is_static = node.get('@isStatic')
        attribute.type = node.get('@type')

        return attribute
    
@dataclass
class Class(ModelElement):
    is_abstract: Optional[str]=None
    attributes: Dict[str, Attribute] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, node: Dict) -> 'Class':
        class_ = super().from_dict(node)
        class_.is_abstract = node.get('@isAbstract')
        # Process attributes
        for attr_list in node.get('attributes', {}).values():
            for attr in attr_list:
                attribute = Attribute.from_dict(attr)
                class_.attributes[attribute.name] = attribute
        return class_
    

@dataclass
class Package(ModelElement):
    packages: Dict[str, 'Package'] = field(default_factory=dict)
    packages_by_name: Dict[str, 'Package'] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, node: Dict) -> 'Package':
        """
        Create a Package instance from a dictionary.

        Args:
            node (Dict): A dictionary representing a Package, with keys for package attributes.

        Returns:
            Package: An instance of Package.
        """
        # top level package handling
        if "Package" in node:
            pnode=node["Package"]
        else:
            pnode=node
            
        package = super().from_dict(pnode)

        #Process tagged values
        for tv_list in pnode.get('taggedValues', {}).values():
            for tv in tv_list:
                tagged_value = TaggedValue.from_dict(tv)
                package.tagged_values[tagged_value.name] = tagged_value

        # Process sub-packages
        for sp in pnode.get('packages', {}).values():
            sub_package = cls.from_dict(sp)
            package.packages[sub_package.id] = sub_package
            package.packages_by_name[sub_package.name] =sub_package
        return package

    
class Model(Package):
    """
    Model with option to read from
    XMI files which have been converted to JSON
    """
    
    @classmethod
    def raw_read_xmi_json(cls, file_path:str)->Dict:
        """
        read the XMI file which has been converted to JSON with xq
        
        Args:
            file_path(str): the file_path to read from
        """
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    
    @classmethod
    def from_xmi_json(cls,file_path)->'XMI':
        """
        read the XMI file which has been converted to JSON with xq
        
        Args:
            file_path(str): the file_path to read from
            
        Returns:
            Model: the Model instance
        """
        data=cls.raw_read_xmi_json(file_path)
        model=cls.from_dict(data)
        return model
        