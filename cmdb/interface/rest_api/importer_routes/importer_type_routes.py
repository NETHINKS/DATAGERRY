# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
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

import json
import logging

from datetime import datetime, timezone
from flask import current_app, request, abort

from cmdb.framework import TypeModel
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.interface.rest_api.import_routes import importer_blueprint
from cmdb.interface.route_utils import login_required, make_response
from cmdb.interface.blueprint import NestedBlueprint
from cmdb.utils.error import CMDBError
from cmdb.framework.managers.type_manager import TypeManager

importer_type_blueprint = NestedBlueprint(importer_blueprint, url_prefix='/type')

LOGGER = logging.getLogger(__name__)

with current_app.app_context():
    object_manager = CmdbObjectManager(current_app.database_manager, current_app.event_queue)


@importer_type_blueprint.route('/create/', methods=['POST'])
@login_required
def add_type():
    from bson import json_util

    type_manager = TypeManager(database_manager=current_app.database_manager)

    error_collection = {}
    upload = request.form.get('uploadFile')
    new_type_list = json.loads(upload, object_hook=json_util.object_hook)
    for new_type_data in new_type_list:
        try:
            new_type_data['public_id'] = object_manager.get_new_id(TypeModel.COLLECTION)
            new_type_data['creation_time'] = datetime.now(timezone.utc)
        except TypeError as e:
            LOGGER.warning(e)
            return abort(400)
        try:
            type_instance = TypeModel.from_data(new_type_data)
        except CMDBError:
            return abort(400)
        try:
            type_manager.insert(type_instance)
        except Exception as ex:
            error_collection.update({"public_id": type_instance.public_id, "message": ex.message})

    resp = make_response(error_collection)
    return resp


@importer_type_blueprint.route('/update/', methods=['POST'])
@login_required
def update_type():
    from bson import json_util

    error_collection = {}
    upload = request.form.get('uploadFile')
    data_dump = json.loads(upload, object_hook=json_util.object_hook)
    for add_data_dump in data_dump:
        try:
            update_type_instance = TypeModel.from_data(add_data_dump)
        except CMDBError:
            return abort(400)
        try:
            old_fields = object_manager.get_type(update_type_instance.get_public_id()).get_fields()
            new_fields = update_type_instance.get_fields()

        except Exception as ex:
            error_collection.update({"public_id": add_data_dump['public_id'], "message": ex.message})
        try:
            object_manager.update_type(update_type_instance)
        except Exception as ex:
            error_collection.update({"public_id": update_type_instance.public_id, "message": ex.details})

    resp = make_response(error_collection)
    return resp
