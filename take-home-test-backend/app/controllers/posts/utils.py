from typing import Dict, Any
from app.repositories.models import Post


def _post_to_dict(post: Post, with_content: bool = False) -> Dict[str, Any]:
    """ Return some basic information about a post as a dictionary """
    post_dict = {
        "id": post.id,
        "title": post.title,
        "timestamp": post.created_at,
        "author": {
            "id": post.user.id,
            "name": post.user.username
        },
        "num_comments": post.num_comments,
    }

    if with_content:
        post_dict["content"] = post.content

    return post_dict
