from xml.etree.ElementTree import (
    fromstring,
    ElementTree,
    Element,
    tostring
)
from .dataset_xml_editor_base import ERDDAPDatasetXMLEditorBase


class ERDDAPDatasetXMLEditor(ERDDAPDatasetXMLEditorBase):
    def __init__(self, xml):
        if isinstance(xml, str):
            self._tree = ElementTree(fromstring(xml))
        else:
            self._tree = ElementTree(xml)
        self._root = self._tree.getroot()
        self._add_attr_index = None

    def set_header(self, name, content):
        self._set_header(self._root, name, content)

    def get_header(self):
        return self._get_header(self._root)

    def get_all_attr(self):
        _attr = {}
        for child in self._root:
            t = child.tag
            te = child.text
            if t != "addAttributes" and t != "dataVariable":
                _attr[t] = te
        return _attr

    def get_unit(self):
        res = {}
        for index, child in self._get_element_by_tag_generator("dataVariable"):
            unit = None
            for sub in child:
                if sub.tag == "sourceName":
                    source_name = sub.text
                if sub.tag == "addAttributes":
                    for ssub in sub:
                        attrib = ssub.attrib
                        if attrib['name'] == "units":
                            unit = ssub.text

                if unit and source_name:
                    res[source_name] = unit
        return res

    def add_unit(self):
        unit = self.get_unit()
        if unit:
            for attr in unit:
                self.set_data_variable_add_attribute(attr, 'units', unit.get(attr))

    def set_attr(self, tag, text):
        if type(text) is int:
            text = str(text)
        for child in self._root:
            if child.tag == tag:
                child.text = text
                break
        else:
            new_element = Element(tag)
            new_element.text = text
            self._root.insert(0, new_element)

    def get_all_added_attr(self):
        _add_attr = {}
        added_attr_element = self._get_added_attr_section()

        for child in added_attr_element:
            attrib = child.attrib
            te = child.text
            _add_attr[attrib["name"]] = te
        return _add_attr

    def _get_element_by_tag_generator(self, tag):
        for index, child in enumerate(self._root):
            if child.tag == tag:
                yield index, child

    def _get_added_attr_section(self):
        added_attr_element = None
        if self._add_attr_index is None:
            for index, child in enumerate(self._root):
                t = child.tag
                if t == "addAttributes":
                    self._add_attr_index = index
                    self._add_attr_index = index
                    added_attr_element = child
        else:
            added_attr_element = self._root[self._add_attr_index]
        return added_attr_element

    def _added_new_element_to_attr_section(self, name, text, added_attr_element):
        new_element = Element("att", attrib={'name': name})
        new_element.text = text
        new_element.tail = '\n\n   '
        added_attr_element.append(new_element)

    def _text_update_for_added_attr(self, name, text, child):
        UPDATED = True
        attrs = child.attrib
        if attrs["name"] == name:
            child.text = text
            return UPDATED
        else:
            return not UPDATED

    def set_added_attr(self, name, text):
        added_attr_element = self._get_added_attr_section()
        if added_attr_element:
            for child in added_attr_element:
                if self._text_update_for_added_attr(name, text, child):
                    break
            else:
                self._added_new_element_to_attr_section(name, text, added_attr_element)

    def remove_added_attr(self, name):
        added_attr_element = self._get_added_attr_section()
        for child in added_attr_element:
            attrs = child.attrib
            if attrs["name"] == name:
                added_attr_element.remove(child)
                break

    def remove_attr(self, name):
        attr = self._root.find(name)
        self._root.remove(attr)

    def write(self, path):
        self._tree.write(path)

    def to_string(self):
        return tostring(self._root, encoding='unicode', method='xml')

    def _find_data_variable_by_source_name(self, source_name):
        for index, child in self._get_element_by_tag_generator("dataVariable"):
            for sub in child:
                if sub.tag == "sourceName":
                    if sub.text == source_name:
                        return index, child
                    else:
                        break
        else:
            return None, None

    def remove_data_variable(self, source_name):
        index, child = self._find_data_variable_by_source_name(source_name)
        if child:
            self._root.remove(child)

    def edit_data_variable_destination_name(self, source_name, new_destination_name):
        index, child = self._find_data_variable_by_source_name(source_name)
        self.sub_element_text_change_by_tag(child, "destinationName", new_destination_name)

    def edit_data_variable_data_type(self, source_name, new_data_type):
        index, child = self._find_data_variable_by_source_name(source_name)
        self.sub_element_text_change_by_tag(child, "dataType", new_data_type)

    def set_data_variable_add_attribute(self, source_name, attr_name, new_attr_text):
        index, child = self._find_data_variable_by_source_name(source_name)
        add_attribute_element = self._get_data_variable_add_attributes(child)
        self.set_add_attribute(add_attribute_element, attr_name, new_attr_text)

    def remove_data_variable_add_attribute(self, source_name, attr_name):
        index, child = self._find_data_variable_by_source_name(source_name)
        add_attribute_element = self._get_data_variable_add_attributes(child)
        for sub in add_attribute_element:
            attrib_name = sub.attrib["name"]
            if attrib_name == attr_name:
                add_attribute_element.remove(sub)
                break
