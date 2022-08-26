from typing import Dict, Any
from app.repositories.models import Comment



def _comment_to_dict(comment: Comment) -> Dict[str, Any]:
    """ Represent a Comment as a dictionary """
    return {
        "id": comment.id,
        "timestamp": comment.created_at,
        "content": comment.content,
        "author": {
            "id": comment.user.id,
            "name": comment.user.username
        },
        "post": {
            "id": comment.post.id,
            "title": comment.post.title
        },
        "parent": {
            "id": comment.parent_comment.id,
            "author": comment.parent_comment.user.username
        } if comment.parent_comment else None
    }
