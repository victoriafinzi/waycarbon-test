from typing import List, Optional
from .models import Comment


def get_comment_by_id(comment_id: int) -> Optional[Comment]:
    """ Return the comment referenced by comment_id. Return None otherwise. """
    return Comment.query.get(comment_id)


def get_post_comments(post_id: int) -> List[Comment]:
    """ Retrieve all comments associated with a post, sorted from most to least
        recent
    """
    return (
        Comment.query
        .order_by(Comment.created_at.desc())
        .filter_by(post_id=post_id)
        .all()
    )
