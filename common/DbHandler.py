# NOTE: This class is for handling all calls to database

from sqlalchemy.sql.sqltypes import DateTime
from common.Link import Link
from common.User import User
from common.Category import Category

from db import db

from datetime import datetime
import json

# Load config file
with open('config.json', mode='r') as config_file:
    MAX_LINKS_PER_PAGE = json.load(config_file).get('pagination', {}).\
        get('maximum_links_per_page')
DATE_FORMAT = '%Y-%m-%d %H:%M'


class DbHandler():
    @staticmethod
    def get_user_object(username: str) -> User:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_id(username: str) -> int:
        user_id = (User.query.
                   with_entities(User.id).filter_by(username=username).first())
        if user_id:
            return(user_id[0])
        else:
            return(-1)

    @staticmethod
    def validate_login(username: str, password: str) -> User:
        user = (User.query.filter_by(username=username).first())

        # Check if user exists and password is correct
        if user and user.check_password(password):
            return user
        else:
            return None

    @staticmethod
    def add_new_user(username: str, password: str) -> str:
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        if user:
            return "USER_EXISTS"

        user = User(username=username, password_hash=password)
        db.session.add(user)
        db.session.commit()

        return "OK"

    @staticmethod
    def append_new_link(username: str, url: str, categories_name: list) -> int:
        """Check if category is already exists or not.
        If category exists, create object. Else create new one
        and then connect new link to categories
        """
        current_user_object = DbHandler.get_user_object(
            username=username
        )
        new_link = Link(
            url=url,
            owner=current_user_object
        )

        if categories_name:
            for category_name in categories_name:
                category_object = Category.query.filter_by(
                    name=category_name
                ).first()
                if not category_object:
                    category_object = Category(name=category_name)

                category_object.related_link.append(new_link)

        User.query.filter_by(username=username).update(
            dict(time_new_link_added=datetime.now())
        )
        db.session.add(new_link)
        db.session.commit()
        return new_link.id

    @staticmethod
    def remove_link(username: str, link_id: int) -> str:
        link_object = Link.query.filter_by(id=link_id).first()

        # Check if id exists and it's owner sends request
        if link_object:
            if link_object.owner_id == DbHandler.get_user_id(username):
                db.session.delete(link_object)
                db.session.commit()
                return "OK"
            else:
                return "USER_IS_NOT_OWNER"
        else:
            return "ID_NOT_FOUND"

    @staticmethod
    def append_new_categories(link: Link, categories: list) -> str:
        for category in categories:
            category.related_link.append(link)
        db.session.commit()
        return "OK"

    @staticmethod
    def get_links(user_id: int, link_id: int = None,
                  page: int = 1, page_size: int = MAX_LINKS_PER_PAGE,
                  date_from: DateTime = None) -> list:
        """ Return links by their Id, their created date
        or paginated links if those two are not provided.
        """
        if link_id is not None:
            link_objects = Link.query.filter_by(
                owner_id=user_id,
                id=link_id
            ).all()
        elif date_from is not None:
            link_objects = Link.query.filter(Link.owner_id == user_id).\
                filter(Link.time_created > date_from).\
                order_by(Link.time_created.desc()).\
                paginate(page, page_size, False).items
        else:
            link_objects = Link.query.filter_by(owner_id=user_id).\
                order_by(Link.time_created.desc()).\
                paginate(page, page_size, False).items

        if not link_objects:
            return('LINK_NOT_FOUND')

        links_values = [
            {
                "id": link.id,
                "url": link.url,
                "added_date": link.time_created.strftime(DATE_FORMAT),
                "categories": [
                    {
                        "id": category.id,
                        "name": category.name
                    }
                    for category in link.categories
                ]
            }
            for link in link_objects
        ]

        return links_values

    @staticmethod
    def get_categories(username: str, category_id: int) -> list:
        user_id = DbHandler.get_user_id(username)

        categories_objects = db.session.query(Category).\
            join(Category, Link.categories).\
            filter(Link.owner_id == user_id).all()

        if category_id:
            categories_values = [
                {
                    "id": category.id,
                    "name": category.name,
                }
                for category in categories_objects
                if category.id == category_id
            ]
        else:
            categories_values = [
                {
                    "id": category.id,
                    "name": category.name,
                }
                for category in categories_objects
            ]

        if categories_values:
            return categories_values
        else:
            return 'ID_NOT_FOUND'

    @staticmethod
    def get_links_by_category(username: str, category_id: int) -> list:
        user_id = DbHandler.get_user_id(username)

        link_objects = db.session.query(Link).\
            join(Category, Link.categories).\
            filter(Link.owner_id == user_id).\
            filter(Category.id == category_id).\
            order_by(Link.time_created.desc()).\
            all()

        requested_category_object = Category.query.filter_by(
            id=category_id
        ).first()

        if requested_category_object is None:
            return 'CATEGORY_NOT_FOUND'

        links_values = {
            "category": {
                "id": requested_category_object.id,
                "name": requested_category_object.name,
                "links": [
                    {
                        "id": link.id,
                        "url": link.url
                    }
                    for link in link_objects
                ]
            }
        }

        return links_values

    @staticmethod
    def get_links_by_pattern(username: str, pattern: str) -> list:
        user_id = DbHandler.get_user_id(username)
        search_pattern = f'%{pattern}%'

        link_objects = Link.query.filter(Link.owner_id == user_id).\
            filter(Link.url.like(search_pattern)).order_by(
                Link.time_created.desc()
            ).all()

        if not link_objects:
            return 'PATTERN_NOT_FOUND'

        links_values = {
            "search": {
                "pattern": pattern,
                "links": [
                    {
                        "id": link.id,
                        "url": link.url
                    }
                    for link in link_objects
                ]
            }
        }

        return links_values

    @staticmethod
    def reset_user_forgotten_password(user_id: int, new_password: str) -> str:
        user = User.query.filter_by(id=user_id).first()
        user.update_password(new_password)
        user.time_profile_updated = datetime.now()
        db.session.commit()
        return 'OK'

    @staticmethod
    def update_link_categories(username: str, new_categories: list,
                               link_id: int) -> str:
        """ Update categories related to a link ID. """
        link = Link.query.\
            filter(Link.owner_id == DbHandler.get_user_id(username)).\
            filter(Link.id == link_id).first()

        if link is None:
            return('LINK_NOT_FOUND')

        link.categories = []
        if new_categories:
            for category_name in new_categories:
                category_object = Category.query.filter_by(
                    name=category_name
                ).first()
                if not category_object:
                    category_object = Category(name=category_name)

                category_object.related_link.append(link)

        db.session.add(link)
        db.session.commit()
        return 'OK'

    @staticmethod
    def update_user_publicity(username: str, publicity: bool) -> str:
        """ Changes user publicity. """
        User.query.filter_by(username=username).update(
            dict(is_public=publicity)
        )
        User.query.filter_by(username=username).update(
            dict(time_profile_updated=datetime.now())
        )
        db.session.commit()
        return 'OK'

    @staticmethod
    def get_users_activity_list(date_from: str = None) -> list:
        """ Return users activity as a list, starting
        from `date_from` parameter (If provided) """
        users_list = db.session.\
            query(User.id, User.username, User.time_new_link_added).\
            filter(User.is_public, User.time_new_link_added).\
            order_by(User.time_new_link_added.desc())

        if date_from is None:
            users_list = users_list.all()
        else:
            try:
                date_from_object = datetime.strptime(
                    date_from,
                    DATE_FORMAT
                )
            except ValueError:
                return('WRONG_FORMAT')
            users_list = users_list.filter(
                User.time_new_link_added > date_from_object).all()

        if not users_list:
            return('NOT_FOUND')

        users_activity = []
        for user in users_list:
            total_num_of_links = Link.query.\
                filter(Link.owner_id == user[0])
            if date_from is None:
                total_num_of_links = total_num_of_links.count()
            else:
                total_num_of_links = total_num_of_links.filter(
                    Link.time_created > date_from).count()

            users_activity.append(dict(
                user_id=user[0],
                username=user[1],
                last_link_added_date=user[2].strftime(DATE_FORMAT),
                total_links_added_after_given_time=total_num_of_links
                )
            )

        return(users_activity)

    @staticmethod
    def get_public_user_links(user_id: int, date_from: str = None) -> list:
        user_status = User.query.with_entities(User.is_public).\
            filter_by(id=user_id).first()

        if user_status is None:
            return('USER_NOT_FOUND')
        elif user_status[0] is False:
            return('USER_NOT_PUBLIC')

        if date_from:
            try:
                date_from_object = datetime.strptime(
                    date_from,
                    DATE_FORMAT
                )
            except ValueError:
                return('WRONG_DATE_FORMAT')

            return(DbHandler.get_links(user_id, date_from=date_from_object))

        return(DbHandler.get_links(user_id))

    @staticmethod
    def get_user_publicity(user_id: int) -> bool:
        """ Returns user's publicity. """
        return(User.query.with_entities(User.is_public).
               filter_by(id=user_id).first()[0])
