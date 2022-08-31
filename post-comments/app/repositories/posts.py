from typing import List, Optional

from .models import Post


def get_all_posts() -> List[Post]:
    """ Retrieve all posts, sorted from most to least recent """
    return (
        Post.query
        .order_by(Post.created_at.desc())
        .all())


def get_post_by_id(post_id: int) -> Optional[Post]:
    """ Return the post referenced by post_id, if it exists. Return None
        otherwise
    """
    return Post.query.get(post_id)
