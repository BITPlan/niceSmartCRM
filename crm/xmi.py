"""
Created on 2024-01-14

@author: wf
"""
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class TaggedValue:
    name: str
    value: Optional[str] = field(
        default=None, metadata={"json": "@name", "value": "Value"}
    )

    @classmethod
    def from_dict(cls, node: Dict) -> "TaggedValue":
        """
        Create a TaggedValue instance from a dictionary.

        Args:
            node (Dict): A dictionary representing a TaggedValue, with keys '@name' and 'Value'.

        Returns:
            TaggedValue: An instance of TaggedValue.
        """
        name = node.get("@name")
        value = node.get("Value")
        return cls(name=name, value=value)


@dataclass
class ModelElement:
    """
    Base model element class
    """

    parent: "ModelElement"
    name: str
    id: str
    stereotype: str
    visibility: str
    documentation: str
    tagged_values: Dict[str, TaggedValue] = field(default_factory=dict)

    @property
    def short_name(self) -> str:
        """
        for name: Logical View::com::bitplan::smartCRM::Organisation::Name
        return "Name"
        """
        return self.name.split("::")[-1]

    @classmethod
    def from_dict(cls, parent: "ModelElement", node: Dict) -> "ModelElement":
        """
        Create a ModelElement instance from a dictionary.

        Args:
            parent(ModelElement): the parent ModelElement or None for the Model itself
            node (Dict): A dictionary representing a ModelElement.

        Returns:
            ModelElement: An instance of ModelElement.
        """
        element = cls(
            parent=parent,
            name=node.get("@name"),
            id=node.get("@id"),
            stereotype=node.get("@stereotype"),
            visibility=node.get("@visibility"),
            documentation=node.get("Documentation"),
        )

        for tv_list in node.get("taggedValues", {}).values():
            for tv in tv_list:
                tagged_value = TaggedValue.from_dict(tv)
                element.tagged_values[tagged_value.name] = tagged_value

        return element


@dataclass
class Attribute(ModelElement):
    is_static: Optional[str] = None
    type: Optional[str] = None

    @classmethod
    def from_dict(cls, parent: ModelElement, node: Dict) -> "Attribute":
        attribute = super().from_dict(parent, node)
        attribute.is_static = node.get("@isStatic")
        attribute.type = node.get("@type")

        return attribute
    
@dataclass
class Parameter(ModelElement):
    # Add any specific fields for Parameter if needed

    @classmethod
    def from_dict(cls, parent: ModelElement, node: Dict) -> 'Parameter':
        return super().from_dict(parent, node)
    
@dataclass
class Operation(ModelElement):
    is_static: Optional[str] = None
    is_abstract: Optional[str] = None
    parameters: Dict[str, 'Parameter'] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, parent: ModelElement, node: Dict) -> 'Operation':
        operation = super().from_dict(parent, node)
        operation.is_static = node.get('@isStatic')
        operation.is_abstract = node.get('@isAbstract')

        # Process parameters
        for param_list in node.get('parameters', {}).values():
            # return parameter
            if isinstance(param_list,dict):
                param_list=[param_list]
            for param in param_list:
                parameter = Parameter.from_dict(operation, param)
                operation.parameters[parameter.name] = parameter

        return operation



@dataclass
class Class(ModelElement):
    is_abstract: Optional[str] = None
    attributes: Dict[str, Attribute] = field(default_factory=dict)
    operations: Dict[str, Operation] = field(default_factory=dict)
 
    @classmethod
    def from_dict(cls, parent: ModelElement, node: Dict) -> "Class":
        class_ = super().from_dict(parent, node)
        class_.is_abstract = node.get("@isAbstract")
        # Process attributes
        for attr_list in node.get("attributes", {}).values():
            for attr in attr_list:
                attribute = Attribute.from_dict(class_, attr)
                class_.attributes[attribute.name] = attribute
    
        # Process operations
        for op_list in node.get('operations', {}).values():
            if isinstance(op_list,dict):
                op_list=[op_list]
            for op in op_list:
                operation = Operation.from_dict(class_, op)
                class_.operations[operation.name] = operation

        return class_
    

@dataclass
class Package(ModelElement):
    packages: Dict[str, "Package"] = field(default_factory=dict)
    packages_by_name: Dict[str, "Package"] = field(default_factory=dict)
    classes: Dict[str, "Class"] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, parent: ModelElement, node: Dict) -> "Package":
        """
        Create a Package instance from a dictionary.

        Args:
            node (Dict): A dictionary representing a Package, with keys for package attributes.

        Returns:
            Package: An instance of Package.
        """
        # top level package handling
        if "Package" in node:
            pnode = node["Package"]
        else:
            pnode = node

        package = super().from_dict(parent, pnode)

        # Process classes
        for cl_list in pnode.get("classes", {}).values():
            for cl in cl_list:
                class_ = Class.from_dict(package, cl)
                package.classes[class_.name] = class_

        # Process sub-packages
        for sp in pnode.get("packages", {}).values():
            sub_package = Package.from_dict(package, sp)
            package.packages[sub_package.id] = sub_package
            package.packages_by_name[sub_package.name] = sub_package
        return package


class Model(Package):
    """
    Model with option to read from
    XMI files which have been converted to JSON
    """

    @classmethod
    def raw_read_xmi_json(cls, file_path: str) -> Dict:
        """
        read the XMI file which has been converted to JSON with xq

        Args:
            file_path(str): the file_path to read from
        """
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    @classmethod
    def from_xmi_json(cls, file_path) -> "XMI":
        """
        read the XMI file which has been converted to JSON with xq

        Args:
            file_path(str): the file_path to read from

        Returns:
            Model: the Model instance
        """
        data = cls.raw_read_xmi_json(file_path)
        model = cls.from_dict(None, data)
        return model

    def to_plant_uml(self) -> str:
        """
        Generate a PlantUML representation of the model.

        Returns:
            str: The PlantUML string.
        """
        plant_uml = "@startuml\n"
        plant_uml += self._generate_plant_uml(self)
        plant_uml += "@enduml"
        return plant_uml

    def _generate_plant_uml(self, element, indent="") -> str:
        uml = ""
        if isinstance(element, Package):
            uml = f"{indent}package {element.short_name} {{\n"
            for pkg in element.packages.values():
                uml += self._generate_plant_uml(pkg, indent + "  ")
            for _class in element.classes.values():
                uml += self._generate_plant_uml(_class, indent + "  ")
            uml += f"{indent}}}\n"
        if isinstance(element, Class):
            uml += f"{indent}class {element.short_name} {{\n"
            for _attr_name, attr in element.attributes.items():
                uml += f"{indent}  {attr.short_name} : {attr.type}\n"
            uml += f"{indent}}}\n"
        return uml
