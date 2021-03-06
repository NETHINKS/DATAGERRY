# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2020 NETHINKS GmbH
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from pymongo.errors import DuplicateKeyError

from cmdb.database.errors import DataBaseError


class DatabaseAlreadyExists(DataBaseError):
    def __init__(self, database_name: str):
        message = f'Database with the name {database_name} already exists'
        super(DatabaseAlreadyExists, self).__init__(message)


class DatabaseNotExists(DataBaseError):
    def __init__(self, database_name: str):
        message = f'Database with the name {database_name} doesn`t exists'
        super(DatabaseNotExists, self).__init__(message)


class CollectionAlreadyExists(DataBaseError):
    """
    Error if you try to create a collection that alrady exists
    """

    def __init__(self, collection_name):
        super().__init__()
        self.message = "Collection {} already exists".format(collection_name)


class FileImportError(DataBaseError):
    """
    Error if json file import to database failed
    """

    def __init__(self, collection_name):
        super().__init__()
        self.message = "Collection {} could not be imported".format(collection_name)


class PublicIDAlreadyExists(DuplicateKeyError):
    """
    Error if public_id inside database already exists
    """

    def __init__(self, public_id):
        super().__init__("Public ID Exists")
        self.message = "Object with this public id already exists: {}".format(public_id)


class NoDocumentFound(DataBaseError):
    """
    Error if no document was found
    """

    def __init__(self, collection, public_id):
        super().__init__()
        self.message = "No document with the id {} was found inside {}".format(public_id, collection)


class DocumentCouldNotBeDeleted(DataBaseError):
    """
    Error if document could not be deleted from database
    """

    def __init__(self, collection, public_id):
        super().__init__()
        self.message = "The document with the id {} could not be deleted inside {}".format(public_id, collection)
