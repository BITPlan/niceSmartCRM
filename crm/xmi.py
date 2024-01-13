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
class Package:
    name: str
    id: str
    stereotype: str
    visibility: str
    documentation: str
    tagged_values: Dict[str, TaggedValue] = field(default_factory=dict)
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
        package = cls(
            name=pnode.get('@name'),
            id=pnode.get('@id'),
            stereotype=pnode.get('@stereotype'),
            visibility=pnode.get('@visibility'),
            documentation=pnode.get('Documentation')
        )

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

    
class XMI(Package):
    """
    reader for XMI files which have been converted to JSON
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
            XMI: the XMI instance
        """
        data=cls.raw_read_xmi_json(file_path)
        xmi=cls.from_dict(data)
        return xmi
        