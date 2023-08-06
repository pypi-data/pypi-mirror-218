from typing import Any
import sqlalchemy
from perun.connector import AdaptersManager
from perun.connector import Logger
from pymongo import MongoClient
from pymongo.collection import Collection
from sqlalchemy import delete, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session

from perun.utils.ConfigStore import ConfigStore


class UserManager:
    def __init__(self, cfg):
        GLOBAL_CONFIG = ConfigStore.get_global_cfg(cfg.get("global_cfg_filepath"))
        ADAPTERS_MANAGER_CFG = GLOBAL_CONFIG["adapters_manager"]
        ATTRS_MAP = ConfigStore.get_attributes_map(GLOBAL_CONFIG["attrs_cfg_path"])

        self._ADAPTERS_MANAGER = AdaptersManager(ADAPTERS_MANAGER_CFG, ATTRS_MAP)
        self._SUBJECT_ATTRIBUTE = cfg.get("perun_person_principal_names_attribute")

        self.logger = Logger.get_logger(__name__)
        self._cfg = cfg

    def get_mongo_db_collection(self, cfg_db_name: str) -> Collection:
        client = MongoClient(self._cfg[cfg_db_name]["connection_string"])
        database_name = self._cfg[cfg_db_name]["database_name"]
        collection_name = self._cfg[cfg_db_name]["collection_name"]

        return client[database_name][collection_name]

    def _revoke_ssp_sessions(
        self, subject: str, ssp_sessions_collection: Collection
    ) -> int:
        result = ssp_sessions_collection.delete_many({"user": subject})
        return result.deleted_count

    def _revoke_satosa_grants(
        self, subject: str, satosa_sessions_collection: Collection
    ) -> int:
        result = satosa_sessions_collection.delete_many({"sub": subject})
        return result.deleted_count

    def _get_postgres_engine(self) -> Engine:
        connection_string = self._cfg["mitre_database"]["connection_string"]
        engine = sqlalchemy.create_engine(connection_string)

        return engine

    def _get_mitre_delete_statements(
        self, user_id: str, engine: Engine, include_refresh_tokens=False
    ) -> list[Any]:
        meta_data = sqlalchemy.MetaData(bind=engine)
        sqlalchemy.MetaData.reflect(meta_data)
        session = Session(bind=engine)

        AUTH_HOLDER_TBL = meta_data.tables["authentication_holder"]
        SAVED_USER_AUTH_TBL = meta_data.tables["saved_user_auth"]

        ACCESS_TOKEN_TBL = meta_data.tables["access_token"]
        delete_access_tokens_stmt = delete(ACCESS_TOKEN_TBL).where(
            ACCESS_TOKEN_TBL.c.auth_holder_id.in_(
                session.query(AUTH_HOLDER_TBL.c.id).filter(
                    AUTH_HOLDER_TBL.c.user_auth_id.in_(
                        session.query(SAVED_USER_AUTH_TBL.c.id).filter(
                            SAVED_USER_AUTH_TBL.c.name == user_id
                        )
                    )
                )
            )
        )

        AUTH_CODE_TBL = meta_data.tables["authorization_code"]
        delete_authorization_codes_stmt = delete(AUTH_CODE_TBL).where(
            AUTH_CODE_TBL.c.auth_holder_id.in_(
                session.query(AUTH_HOLDER_TBL.c.id).filter(
                    AUTH_HOLDER_TBL.c.user_auth_id.in_(
                        session.query(SAVED_USER_AUTH_TBL.c.id).filter(
                            SAVED_USER_AUTH_TBL.c.name == user_id
                        )
                    )
                )
            )
        )

        DEVICE_CODE = meta_data.tables["device_code"]
        delete_device_codes_stmt = delete(DEVICE_CODE).where(
            DEVICE_CODE.c.auth_holder_id.in_(
                session.query(AUTH_HOLDER_TBL.c.id).filter(
                    AUTH_HOLDER_TBL.c.user_auth_id.in_(
                        session.query(SAVED_USER_AUTH_TBL.c.id).filter(
                            SAVED_USER_AUTH_TBL.c.name == user_id
                        )
                    )
                )
            )
        )

        statements = [
            delete_access_tokens_stmt,
            delete_authorization_codes_stmt,
            delete_device_codes_stmt,
        ]

        if include_refresh_tokens:
            REFRESH_TOKEN_TBL = meta_data.tables["refresh_token"]
            delete_refresh_tokens_stmt = delete(REFRESH_TOKEN_TBL).where(
                REFRESH_TOKEN_TBL.c.auth_holder_id.in_(
                    session.query(AUTH_HOLDER_TBL.c.id).filter(
                        AUTH_HOLDER_TBL.c.user_auth_id.in_(
                            session.query(SAVED_USER_AUTH_TBL.c.id).filter(
                                SAVED_USER_AUTH_TBL.c.name == user_id
                            )
                        )
                    )
                )
            )
            statements.append(delete_refresh_tokens_stmt)

        return statements

    def _delete_mitre_tokens(self, user_id: str, include_refresh_tokens=False) -> int:
        deleted_mitre_tokens_count = 0

        engine = self._get_postgres_engine()
        statements = self._get_mitre_delete_statements(
            user_id, engine, include_refresh_tokens
        )

        for stmt in statements:
            result = engine.execute(stmt)
            deleted_mitre_tokens_count += result.rowcount

        return deleted_mitre_tokens_count

    def _get_satosa_sessions_collection(self) -> Collection:
        return self.get_mongo_db_collection("satosa_database")

    def _get_ssp_sessions_collection(self) -> Collection:
        return self.get_mongo_db_collection("ssp_database")

    def logout(self, user_id: str, include_refresh_tokens=False) -> None:
        user_attrs = self._ADAPTERS_MANAGER.get_user_attributes(
            int(user_id), [self._SUBJECT_ATTRIBUTE]
        )
        subject_candidates = user_attrs.get(self._SUBJECT_ATTRIBUTE, [])
        subject = subject_candidates[0] if subject_candidates else None

        ssp_sessions_collection = self._get_ssp_sessions_collection()
        revoked_sessions_count = self._revoke_ssp_sessions(
            subject, ssp_sessions_collection
        )

        satosa_sessions_collection = self._get_satosa_sessions_collection()
        revoked_grants_count = self._revoke_satosa_grants(
            subject, satosa_sessions_collection
        )

        deleted_tokens_count = self._delete_mitre_tokens(
            user_id, include_refresh_tokens
        )

        self.logger.info(
            f"Logged out user {subject} from {revoked_sessions_count} SSP "
            f"sessions, deleted {revoked_grants_count} SATOSA sessions and "
            f"deleted {deleted_tokens_count} mitre tokens."
        )

    def get_active_client_ids_for_user(self, user_id: str) -> set[str]:
        """
        Returns list of unique client ids retrieved from active user's sessions.
        :param user_id: user, whose sessions are retrieved
        :return: list of client ids
        """
        user_attrs = self._ADAPTERS_MANAGER.get_user_attributes(
            int(user_id), [self._SUBJECT_ATTRIBUTE]
        )
        subject_candidates = user_attrs.get(self._SUBJECT_ATTRIBUTE, [])
        subject = subject_candidates[0] if subject_candidates else None

        ssp_clients = self._get_ssp_entity_ids_by_user(subject)
        satosa_clients = self._get_satosa_client_ids(subject)
        mitre_clients = self._get_mitre_client_ids(user_id)

        return set(ssp_clients + satosa_clients + mitre_clients)

    def _get_mitre_client_ids(self, user_id: str) -> list[str]:
        engine = self._get_postgres_engine()
        meta_data = sqlalchemy.MetaData(bind=engine)
        sqlalchemy.MetaData.reflect(meta_data)
        session = Session(bind=engine)

        AUTH_HOLDER_TBL = meta_data.tables["authentication_holder"]
        SAVED_USER_AUTH_TBL = meta_data.tables["saved_user_auth"]
        ACCESS_TOKEN_TBL = meta_data.tables["access_token"]
        CLIENT_DETAILS_TBL = meta_data.tables["client_details"]

        stmt = select(CLIENT_DETAILS_TBL.c.client_id).where(
            CLIENT_DETAILS_TBL.c.id.in_(
                session.query(ACCESS_TOKEN_TBL.c.client_id).filter(
                    ACCESS_TOKEN_TBL.c.auth_holder_id.in_(
                        session.query(AUTH_HOLDER_TBL.c.id).filter(
                            AUTH_HOLDER_TBL.c.user_auth_id.in_(
                                session.query(SAVED_USER_AUTH_TBL.c.id).filter(
                                    SAVED_USER_AUTH_TBL.c.name == user_id
                                )
                            )
                        )
                    )
                )
            )
        )

        result = engine.execute(stmt)
        return [r[0] for r in result]

    def _get_ssp_entity_ids_by_user(self, sub: str):
        ssp_sessions_collection = self._get_ssp_sessions_collection()
        entries = ssp_sessions_collection.find(
            {"user": sub}, {"entityIds": 1, "_id": 0}
        )
        entries = [entry.get("entityIds", []) for entry in entries]
        return [el for lst in entries for el in lst]

    def _get_ssp_entity_ids_by_session(self, session_id: str):
        ssp_sessions_collection = self._get_ssp_sessions_collection()
        entries = ssp_sessions_collection.find(
            {"key": session_id}, {"entityIds": 1, "_id": 0}
        )
        entries = [entry.get("entityIds", []) for entry in entries]
        return [el for lst in entries for el in lst]

    def _get_satosa_client_ids(self, sub: str):
        satosa_sessions_collection = self._get_satosa_sessions_collection()
        result = satosa_sessions_collection.find(
            {"sub": sub}, {"client_id": 1, "_id": 0}
        )
        return list(result)
