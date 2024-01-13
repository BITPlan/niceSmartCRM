"""
Created on 2024-01-14

@author: wf
"""
import json
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Dict, List, Optional
import textwrap

@dataclass_json
@dataclass
class TaggedValue:
    name: str
    value: Optional[str] = field(
        default=None
    )

    @classmethod
    def from_xmi_dict(cls, node: Dict) -> "TaggedValue":
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

@dataclass_json
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

    @property
    def short_name(self) -> str:
        """
        for name: Logical View::com::bitplan::smartCRM::Organisation::Name
        return "Name"
        """
        short_name=ModelElement.as_short_name(self.name)
        return short_name
    
    def multi_line_doc(self, limit: int) -> str:
        """
        Returns the documentation as a multiline string with a limited length per line.
        Lines are broken at whitespace.
        
        :param limit: The maximum length of each line.
        :return: Multiline string.
        """
        text='\n'.join(textwrap.wrap(self.documentation, width=limit))
        return text
    
    @classmethod
    def as_short_name(cls,name:str)->str:
        if name is None:
            return None
        short_name=name.split("::")[-1]
        return short_name

    @classmethod
    def from_xmi_dict(cls, parent: "ModelElement", node: Dict) -> "ModelElement":
        """
        Create a ModelElement instance from a dictionary.

        Args:
            parent(ModelElement): the parent ModelElement or None for the Model itself
            node (Dict): A dictionary representing a ModelElement.

        Returns:
            ModelElement: An instance of ModelElement.
        """
        element = cls(
            name=node.get("@name"),
            id=node.get("@id"),
            stereotype=node.get("@stereotype"),
            visibility=node.get("@visibility"),
            documentation=node.get("Documentation"),
        )
        element.parent=parent

        for tv_list in node.get("taggedValues", {}).values():
            for tv in tv_list:
                tagged_value = TaggedValue.from_xmi_dict(tv)
                element.tagged_values[tagged_value.name] = tagged_value

        return element

    def as_plantuml(self, _indentation=""):
        return ""
   
@dataclass_json
@dataclass 
class Attribute(ModelElement):
    is_static: Optional[str] = None
    type: Optional[str] = None

    @classmethod
    def from_xmi_dict(cls, parent: ModelElement, node: Dict) -> "Attribute":
        attribute = super().from_xmi_dict(parent, node)
        attribute.is_static = node.get("@isStatic")
        attribute.type = node.get("@type")

        return attribute
    
@dataclass_json
@dataclass
class Parameter(ModelElement):
    type: Optional[str]=None

    @classmethod
    def from_xmi_dict(cls, parent: ModelElement, node: Dict) -> 'Parameter':
        param=super().from_xmi_dict(parent, node)
        param.type = node.get("@type")
        return param
   
@dataclass_json
@dataclass 
class Operation(ModelElement):
    is_static: Optional[str] = None
    is_abstract: Optional[str] = None
    parameters: Dict[str, 'Parameter'] = field(default_factory=dict)

    @classmethod
    def from_xmi_dict(cls, parent: ModelElement, node: Dict) -> 'Operation':
        operation = super().from_xmi_dict(parent, node)
        operation.parameters={}
        operation.is_static = node.get('@isStatic')
        operation.is_abstract = node.get('@isAbstract')

        # Process parameters
        for param_list in node.get('parameters', {}).values():
            # return parameter
            if isinstance(param_list,dict):
                param_list=[param_list]
            for param in param_list:
                parameter = Parameter.from_xmi_dict(operation, param)
                operation.parameters[parameter.name] = parameter

        return operation
    
    def as_plantuml(self, indentation=""):
        """
        Generate PlantUML representation for this Operation.

        Args:
            indentation (str): Indentation for the PlantUML code.

        Returns:
            str: The PlantUML representation for this Operation.
        """
        plantuml = f"{indentation}{self.short_name}("
        
        # Add parameters
        params = []
        return_type=None
        for param_name, param in self.parameters.items():
            type_short=ModelElement.as_short_name(param.type)
            if not param_name.endswith("::return") and not param_name=="return":
                param_str = f"{param.short_name}: {type_short}"
                params.append(param_str)
            else:
                return_type=type_short
                
        # Handle return type
        if return_type:
            params.append(f"return: {return_type}")
        plantuml += ", ".join(params)
        plantuml += ")"
        return plantuml

@dataclass_json
@dataclass
class Role(ModelElement):
    is_navigable: Optional[str] = None
    multiplicity: Optional[str] = None
    aggregate: Optional[str] = None
    type: Optional[str] = None
    itemid: Optional[str] = None

    @classmethod
    def from_xmi_dict(cls, parent: ModelElement, node: Dict) -> "Role":
        role = super().from_xmi_dict(parent, node)
        role.is_navigable = node.get("@isNavigable")
        role.multiplicity = node.get("@multiplicity")
        role.aggregate = node.get("@aggregate")
        role.type = node.get("@type")
        role.itemid = node.get("@itemid")
        return role

@dataclass_json
@dataclass
class Class(ModelElement):
    is_abstract: Optional[str] = None
    attributes: Dict[str, Attribute] = field(default_factory=dict)
    operations: Dict[str, Operation] = field(default_factory=dict)
    roles: Dict[str, Role] = field(default_factory=dict)  

    @classmethod
    def from_xmi_dict(cls, parent: ModelElement, node: Dict) -> "Class":
        class_ = super().from_xmi_dict(parent, node)
        class_.attributes={}
        class_.operations={}
        class_.roles={}
        class_.is_abstract = node.get("@isAbstract")
        # Process attributes
        for attr_list in node.get("attributes", {}).values():
            for attr in attr_list:
                attribute = Attribute.from_xmi_dict(class_, attr)
                class_.attributes[attribute.name] = attribute
    
        # Process operations
        for op_list in node.get('operations', {}).values():
            if isinstance(op_list,dict):
                op_list=[op_list]
            for op in op_list:
                operation = Operation.from_xmi_dict(class_, op)
                class_.operations[operation.name] = operation

        for role_list in node.get('roles', {}).values():
            if isinstance(role_list,dict):
                role_list=[role_list]
            for role_node in role_list:
                role=Role.from_xmi_dict(class_, role_node)
                class_.roles[role.name] = role
        return class_
    
    def as_plantuml(self, indentation=""):
        """
        Generate PlantUML representation for this Class and its contents.

        Args:
            indentation (str): Indentation for the PlantUML code.

        Returns:
            str: The PlantUML representation for this Class and its contents.
        """
        plantuml = f"{indentation}class {self.short_name} {{\n"

        # Add attributes
        for _attr_name, attr in self.attributes.items():
            attr_type=attr.type
            if "enum" in attr_type:
                attr_type="enum"
            # [[{{{attr.documentation}}} {attr.short_name} ]] 
            plantuml += f"{indentation}  {attr.short_name}: {attr_type}\n"

        # Add operations
        for _op_name, op in self.operations.items():
            operation_plantuml = op.as_plantuml(indentation + "  ")
            plantuml += f"{operation_plantuml}\n"

        plantuml += f"{indentation}}}\n"
        plantuml += f"""note top of {self.short_name}
{self.multi_line_doc(40)}
end note
"""
        return plantuml
    
@dataclass_json
@dataclass
class Package(ModelElement):
    packages: Dict[str, "Package"] = field(default_factory=dict) 
    classes: Dict[str, "Class"] = field(default_factory=dict)

    @classmethod
    def from_xmi_dict(cls, parent: ModelElement, node: Dict) -> "Package":
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

        package = super().from_xmi_dict(parent, pnode)
        package.classes={}
        package.packages={}
        package.packages_by_name={}
        # Process classes
        for cl_list in pnode.get("classes", {}).values():
            for cl in cl_list:
                class_ = Class.from_xmi_dict(package, cl)
                package.classes[class_.name] = class_

        # Process sub-packages
        for sp in pnode.get("packages", {}).values():
            sub_package = Package.from_xmi_dict(package, sp)
            package.packages[sub_package.id] = sub_package
            package.packages_by_name[sub_package.name] = sub_package
        return package
    
    def as_plantuml(self, indentation=""):
        """
        Generate PlantUML representation for this Package and its contents.

        Args:
            indentation (str): Indentation for the PlantUML code.

        Returns:
            str: The PlantUML representation for this Package and its contents.
        """
        plantuml = f"{indentation}package {self.short_name} {{\n"

        # Add classes within the package
        for _class_name, class_obj in self.classes.items():
            class_plantuml = class_obj.as_plantuml(indentation + "  ")
            plantuml += f"{class_plantuml}\n"

        # Add sub-packages within the package
        for _sub_package_name, sub_package_obj in self.packages.items():
            sub_package_plantuml = sub_package_obj.as_plantuml(indentation + "  ")
            plantuml += f"{sub_package_plantuml}\n"

        plantuml += f"{indentation}}}\n"
        plantuml+=f"""note top of {self.short_name}
{self.documentation}
end note
"""
        return plantuml

@dataclass_json
@dataclass
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
        model = cls.from_xmi_dict(None, data)
        return model

    def to_plant_uml(self) -> str:
        """
        Generate a PlantUML representation of the model.

        Returns:
            str: The PlantUML string.
        """
        skinparams="""
' BITPlan Corporate identity skin params
' Copyright (c) 2015-2023 BITPlan GmbH
' see http://wiki.bitplan.com/PlantUmlSkinParams#BITPlanCI
' skinparams generated by com.bitplan.restmodelmanager
skinparam note {
  BackGroundColor #FFFFFF
  FontSize 12
  ArrowColor #FF8000
  BorderColor #FF8000
  FontColor black
  FontName Technical
}
skinparam component {
  BackGroundColor #FFFFFF
  FontSize 12
  ArrowColor #FF8000
  BorderColor #FF8000
  FontColor black
  FontName Technical
}
skinparam package {
  BackGroundColor #FFFFFF
  FontSize 12
  ArrowColor #FF8000
  BorderColor #FF8000
  FontColor black
  FontName Technical
}
skinparam usecase {
  BackGroundColor #FFFFFF
  FontSize 12
  ArrowColor #FF8000
  BorderColor #FF8000
  FontColor black
  FontName Technical
}
skinparam activity {
  BackGroundColor #FFFFFF
  FontSize 12
  ArrowColor #FF8000
  BorderColor #FF8000
  FontColor black
  FontName Technical
}
skinparam classAttribute {
  BackGroundColor #FFFFFF
  FontSize 12
  ArrowColor #FF8000
  BorderColor #FF8000
  FontColor black
  FontName Technical
}
skinparam interface {
  BackGroundColor #FFFFFF
  FontSize 12
  ArrowColor #FF8000
  BorderColor #FF8000
  FontColor black
  FontName Technical
}
skinparam class {
  BackGroundColor #FFFFFF
  FontSize 12
  ArrowColor #FF8000
  BorderColor #FF8000
  FontColor black
  FontName Technical
}
skinparam object {
  BackGroundColor #FFFFFF
  FontSize 12
  ArrowColor #FF8000
  BorderColor #FF8000
  FontColor black
  FontName Technical
}
hide circle
' end of skinparams '"""
        plant_uml = "@startuml\n"
        plant_uml += f"{skinparams}\n"
        plant_uml += self.as_plantuml("")
        plant_uml += "@enduml"
        return plant_uml


