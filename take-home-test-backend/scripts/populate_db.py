from typing import Iterator, List
from itertools import chain
from datetime import datetime

from faker import Faker

from app import create_app, db
from app.tests import create_tables
from app.repositories.models import User, Post, Comment


def create_users(fake: Faker, num_users: int = 100) -> Iterator[User]:
    """ Populate the database with random users """
    return (
        User(username=fake.name())
        for _ in range(num_users)
    )


def create_posts(
        fake: Faker,
        users: List[User],
        num_posts: int = 20
) -> Iterator[Post]:
    """ Create random posts by some of the users """

    return (
        Post(
            user=fake.random.choice(users),
            created_at=fake.date_time_this_year(),
            title=fake.sentence(),
            content=fake.text(max_nb_chars=2500)
        )

        for _ in range(num_posts)
    )


def create_comment_trees(
        fake: Faker,
        users: List[User],
        posts: List[Post],
        max_comments_per_post=10,
        max_children=3,
        max_tree_depth=3
) -> Iterator[Comment]:
    """ Create random comment trees for each post """
    def generate_tree(
            post_to_comment: Post,
            start_date: datetime,
            current_depth: int = 0
    ) -> Comment:
        """ Generate a random comment tree """
        root = Comment(
            user=fake.random.choice(users),
            post=post_to_comment,
            created_at=fake.date_time_between(
                start_date=start_date, end_date='now'),
            content=fake.text(max_nb_chars=250)
        )

        num_children = (
            0 if current_depth == max_tree_depth
            else fake.random_int(0, max_children))

        root.children = [
            generate_tree(post_to_comment, root.created_at, current_depth + 1)
            for _ in range(num_children)
        ]

        return root

    for post in posts:
        num_comments = fake.random_int(1, max_comments_per_post)
        comments = [
            generate_tree(post, post.created_at)
            for _ in range(num_comments)
        ]
        yield from comments


def populate_db() -> None:
    """ Populate the database with random data """
    create_tables(db)

    faker = Faker()
    session = db.session()

    users = [*create_users(faker)]
    posts = [*create_posts(faker, users)]
    comments = [*create_comment_trees(faker, users, posts)]

    session.add_all(chain(users, posts, comments))
    session.commit()


if __name__ == '__main__':
    app = create_app()
    app_context = app.app_context()
    app_context.push()
    populate_db()
    app_context.pop()
