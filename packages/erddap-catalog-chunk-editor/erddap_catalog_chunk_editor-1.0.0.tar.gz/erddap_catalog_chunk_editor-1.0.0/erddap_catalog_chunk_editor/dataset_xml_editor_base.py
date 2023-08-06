from xml.etree.ElementTree import (
    fromstring,
    ElementTree,
    Element,
    tostring
)


class ERDDAPDatasetXMLEditorBase:
    @staticmethod
    def _get_data_variable_add_attributes(data_variable_element):
        for sub in data_variable_element:
            if sub.tag == "addAttributes":
                return sub

    @staticmethod
    def create_new_att_element(name, text):
        new_element = Element("att", attrib={'name': name})
        new_element.text = text
        new_element.tail = '\n\n   '
        return new_element

    @staticmethod
    def update_att_element_text(ele, name, text):
        UPDATED = True
        attrs = ele.attrib
        if attrs["name"] == name:
            ele.text = text
            return UPDATED
        else:
            return not UPDATED

    def set_add_attribute(self, ele, name, new_attr_text):
        for sub in ele:
            if self.update_att_element_text(sub, name, new_attr_text):
                break
        else:
            new_element = self.create_new_att_element(name, new_attr_text)
            ele.append(new_element)

    @staticmethod
    def _set_header(ele, name, content):
        if type(content) is int:
            content = str(content)
        ele.set(name, content)

    @staticmethod
    def _get_header(ele):
        return ele.attrib

    @staticmethod
    def sub_element_text_change_by_tag(ele, tag, new_text):
        for sub in ele:
            if sub.tag == tag:
                sub.text = new_text
