# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from enum import Enum


class FieldMapperMode(Enum):
    MATCH = 0
    MANUALLY = 1


class BaseImporterConfig:
    DEFAULT_MAPPING = {}

    def __init__(self, mapping: dict = None):
        _mapping = mapping or self.DEFAULT_MAPPING
        self.mapping: dict = {**self.DEFAULT_MAPPING, **_mapping}

    def get_mapping(self) -> dict:
        return self.mapping


class ObjectImporterConfig(BaseImporterConfig):
    DEFAULT_MAPPING = {
        'properties': {},
        'field_mode': FieldMapperMode.MATCH,
        'fields': {}
    }

    def __init__(self, type_id: int, mapping: dict = None, start_element: int = 0, max_elements: int = 0,
                 overwrite_public: bool = True, *args, **kwargs):
        self.type_id: int = type_id
        self.start_element: int = start_element
        self.max_elements: int = max_elements
        self.overwrite_public: bool = overwrite_public
        super(ObjectImporterConfig, self).__init__(mapping=mapping)

    def get_type_id(self):
        return self.type_id