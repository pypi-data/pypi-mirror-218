ERRDAP Catalog Chunk editor

ERDDAP Catalog Chunk editor can help you edit ERRDAP configuration by Python easily!

usage:

dataset_xml_parser  can help you read ERRDAP dataset xml file and return str

ERDDAPDatasetXMLEditor can help edit the ERRDAP datast xml

Errdap configuration contain 4 sections

those were header, database behaviour, dataset global attribute, variables attribute

change header:
set_header
get_header

database behaviour:
set_attr
get_all_attr
remove_attr(name)

dataset global attribute:
get_all_added_attr()
set_added_attr(name, text)
remove_added_attr(name)

variables attribute:
remove_data_variable(source_name)
edit_data_variable_destination_name(source_name, new_destination_name)
edit_data_variable_data_type(source_name, new_data_type)
set_data_variable_add_attribute(source_name, attr_name, new_attr_text)
remove_data_variable_add_attribute(source_name, attr_name)


Reusable python application code

# This repo will auto update the PyPI package when there is a push to master
## for trouble shooting look at steps below
- Check `~/resources/dinkum/.pypirc` on the ceotr dev server, ensure it's present and contains the correct token

## To update the ceotr_file package on PyPI **manually** you will need to do the following:
- ensure the python package "twine" is installed using `pip install twine`
- change the version number in [version/__init__.py](version/__init__.py)
- run the following commands:
    - `python setup.py sdist`
    - `twine upload dist/*`
- enter the CEOTR PyPI username and password, or use token authentication



# File Handle

This module provide a function which allow you interact with local or remote server

To be finished

```
from linux_file_handle import fsm
command choice make_directory, list_files, create_file
change_directory, move_files, remove_file, bash_script, whoami,
current_path, compress_files, uncompress_files, copy_file, make_soft_link
scp, scp_file, scp_files.
fsm.local.{you linux command}
```
