import abc

import sqlalchemy.orm as so

from overhave import db
from overhave.storage import TestUserModel, TestUserSpecification
from overhave.utils import get_current_time


class BaseTestUserStorageException(Exception):
    """Base exception for :class:`FeatureStorage`."""


class TestUserDoesNotExistError(BaseTestUserStorageException):
    """Error for situation when test user not found."""

    __test__ = False


class TestUserUpdatingNotAllowedError(BaseTestUserStorageException):
    """Error for situation when test user has allow_update=False."""

    __test__ = False


class ITestUserStorage(abc.ABC):
    """Abstract class for Test User storage."""

    @staticmethod
    @abc.abstractmethod
    def get_test_user_by_id(user_id: int) -> TestUserModel | None:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_test_user_by_key(key: str) -> TestUserModel | None:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_test_users_by_feature_type_name(
        session: so.Session, feature_type_id: int, allow_update: bool
    ) -> list[TestUserModel]:
        pass

    @staticmethod
    @abc.abstractmethod
    def create_test_user(
        key: str,
        name: str,
        specification: TestUserSpecification,
        created_by: str,
        feature_type_id: int,
        allow_update: bool,
    ) -> TestUserModel:
        pass

    @staticmethod
    @abc.abstractmethod
    def update_test_user_specification(user_id: int, specification: TestUserSpecification) -> None:
        pass

    @staticmethod
    @abc.abstractmethod
    def delete_test_user(user_id: int) -> None:
        pass


class TestUserStorage(ITestUserStorage):
    """Class for Test User storage."""

    @staticmethod
    def get_test_user_by_id(user_id: int) -> TestUserModel | None:
        with db.create_session() as session:
            user = session.get(db.TestUser, user_id)
            if user is not None:
                return TestUserModel.from_orm(user)
            return None

    @staticmethod
    def get_test_user_by_key(key: str) -> TestUserModel | None:
        with db.create_session() as session:
            user: db.TestUser | None = session.query(db.TestUser).filter(db.TestUser.key == key).one_or_none()
            if user is not None:
                return TestUserModel.from_orm(user)
            return None

    @staticmethod
    def get_test_users_by_feature_type_name(
        session: so.Session, feature_type_id: int, allow_update: bool
    ) -> list[TestUserModel]:
        db_users = (
            session.query(db.TestUser)
            .filter(db.TestUser.feature_type_id == feature_type_id, db.TestUser.allow_update.is_(allow_update))
            .all()
        )
        return [TestUserModel.from_orm(user) for user in db_users]

    @staticmethod
    def create_test_user(
        key: str,
        name: str,
        specification: TestUserSpecification,
        created_by: str,
        feature_type_id: int,
        allow_update: bool,
    ) -> TestUserModel:
        with db.create_session() as session:
            test_user = db.TestUser(
                key=key,
                name=name,
                specification=specification,
                feature_type_id=feature_type_id,
                created_by=created_by,
                allow_update=allow_update,
                changed_at=get_current_time(),
            )
            session.add(test_user)
            session.flush()
            return TestUserModel.from_orm(test_user)

    @staticmethod
    def update_test_user_specification(user_id: int, specification: TestUserSpecification) -> None:
        with db.create_session() as session:
            test_user = session.get(db.TestUser, user_id)
            if test_user is None:
                raise TestUserDoesNotExistError(f"Test user with id {user_id} does not exist!")
            if not test_user.allow_update:
                raise TestUserUpdatingNotAllowedError(f"Test user updating with id {user_id} not allowed!")
            test_user.specification = specification
            test_user.changed_at = get_current_time()

    @staticmethod
    def delete_test_user(user_id: int) -> None:
        with db.create_session() as session:
            user = session.get(db.TestUser, user_id)
            if user is None:
                raise TestUserDoesNotExistError(f"Test user with id {user_id} does not exist!")
            session.delete(user)
