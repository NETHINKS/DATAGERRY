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

import logging

from datetime import datetime
from ldap3 import Server, Connection

from cmdb.manager.errors import ManagerGetError, ManagerInsertError
from cmdb.search import Query
from cmdb.security.auth.auth_errors import AuthenticationError
from cmdb.security.auth.auth_providers import AuthenticationProvider
from cmdb.security.auth.provider_config import AuthProviderConfig
from cmdb.security.security import SecurityManager
from cmdb.user_management.managers.group_manager import GroupManager
from cmdb.user_management.managers.user_manager import UserModel, UserManager

LOGGER = logging.getLogger(__name__)


class LdapAuthenticationProviderConfig(AuthProviderConfig):
    DEFAULT_CONFIG_VALUES = {
        'active': False,
        'default_group': 2,
        'server_config': {
            'host': 'localhost',
            'port': 389,
            'use_ssl': False
        },
        'connection_config': {
            'user': 'cn=reader,dc=example,dc=com',
            'password': 'secret1234',
            'version': 3
        },
        'search': {
            'basedn': 'dc=example,dc=com',
            'searchfilter': '(uid=%username%)'
        }
    }

    def __init__(self, active: bool, default_group: int, server_config: dict, connection_config: dict, search: dict,
                 **kwargs):
        self.default_group = default_group
        self.server_config: dict = server_config
        self.connection_config: dict = connection_config
        self.search: dict = search
        super(LdapAuthenticationProviderConfig, self).__init__(active, **kwargs)


class LdapAuthenticationProvider(AuthenticationProvider):
    PASSWORD_ABLE: bool = False
    EXTERNAL_PROVIDER: bool = True
    PROVIDER_CONFIG_CLASS = LdapAuthenticationProviderConfig

    def __init__(self, config: LdapAuthenticationProviderConfig = None, user_manager: UserManager = None,
                 group_manager: GroupManager = None, security_manager: SecurityManager = None):

        self.__ldap_server = Server(**config.server_config)
        self.__ldap_connection = Connection(self.__ldap_server, **config.connection_config)
        super(LdapAuthenticationProvider, self).__init__(config, user_manager=user_manager,
                                                         group_manager=group_manager,
                                                         security_manager=security_manager)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__ldap_connection:
            self.__ldap_connection.unbind()

    def connect(self) -> bool:
        return self.__ldap_connection.bind()

    def authenticate(self, user_name: str, password: str, **kwargs) -> UserModel:
        try:
            ldap_connection_status = self.connect()
            LOGGER.debug(f'[LdapAuthenticationProvider] Connection status: {ldap_connection_status}')
        except Exception as e:
            LOGGER.error(f'[LdapAuthenticationProvider] Failed to connect to LDAP server - error: {e}')
            raise AuthenticationError(LdapAuthenticationProvider.get_name(), e)
        ldap_search_filter = self.config.search['searchfilter'].replace("%username%", user_name)
        LOGGER.debug(f'[LdapAuthenticationProvider] Search Filter: {ldap_search_filter}')
        search_result = self.__ldap_connection.search(self.config.search['basedn'], ldap_search_filter)
        LOGGER.debug(f'[LdapAuthenticationProvider] Search result: {search_result}')

        if not search_result or len(self.__ldap_connection.entries) == 0:
            raise AuthenticationError(LdapAuthenticationProvider.get_name(), 'No matching entry')

        for entry in self.__ldap_connection.entries:
            LOGGER.debug(f'[LdapAuthenticationProvider] Entry: {entry}')
            entry_dn = entry.entry_dn
            try:
                entry_connection_result = Connection(self.__ldap_server, entry_dn, password,
                                                     auto_bind=True)
                LOGGER.debug(f'[LdapAuthenticationProvider] UserModel connection result: {entry_connection_result}')
            except Exception as e:
                LOGGER.error(f'[LdapAuthenticationProvider] UserModel auth result: {e}')
                raise AuthenticationError(LdapAuthenticationProvider.get_name(), e)

        # Check if user exists
        try:
            user_instance: UserModel = self.user_manager.get_by(Query({'user_name': user_name}))
        except ManagerGetError as umge:
            LOGGER.warning(f'[LdapAuthenticationProvider] UserModel exists on LDAP but not in database: {umge}')
            LOGGER.debug(f'[LdapAuthenticationProvider] Try creating user: {user_name}')
            try:
                new_user_data = dict()
                new_user_data['user_name'] = user_name
                new_user_data['active'] = True
                new_user_data['group_id'] = self.config.default_group
                new_user_data['registration_time'] = datetime.now()
                new_user_data['authenticator'] = LdapAuthenticationProvider.get_name()

            except Exception as e:
                LOGGER.debug(f'[LdapAuthenticationProvider] {e}')
                raise AuthenticationError(LdapAuthenticationProvider.get_name(), e)
            LOGGER.debug(f'[LdapAuthenticationProvider] New user was init')
            try:
                user_id = self.user_manager.insert(new_user_data)
            except ManagerInsertError as umie:
                LOGGER.debug(f'[LdapAuthenticationProvider] {umie}')
                raise AuthenticationError(LdapAuthenticationProvider.get_name(), umie)
            try:
                user_instance: UserModel = self.user_manager.get(public_id=user_id)
            except ManagerGetError as umge:
                LOGGER.debug(f'[LdapAuthenticationProvider] {umge}')
                raise AuthenticationError(LdapAuthenticationProvider.get_name(), umge)
        return user_instance

    def is_active(self) -> bool:
        return self.config.active
