#!/usr/bin/env python3
"""
DB module for handling database operations
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class to interact with the database"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a user to the database.

        Arguments:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary keyword arguments and return the first result.

        Arguments:
            **kwargs: The filtering criteria passed as key-value pairs.

        Returns:
            User: The first matching user.

        Raises:
            NoResultFound: If no user is found matching the criteria.
            InvalidRequestError: If an invalid query argument is passed.
        """
        try:
            # Query the users table based on the keyword arguments
            user = self._session.query(User).filter_by(**kwargs).first()

            if user is None:
                raise
            NoResultFound(
                "No user found matching the provided criteria.")

            return user

        except NoResultFound:

            raise
            NoResultFound("No user found matching the provided criteria.")

        except InvalidRequestError as e:
            # This
            raise InvalidRequestError(
                "Invalid query argument passed.") from e
