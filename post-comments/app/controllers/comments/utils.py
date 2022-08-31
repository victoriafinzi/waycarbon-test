from typing import Dict, Any
from app.repositories.models import Comment

def _comment_to_dict(comment: Comment) -> Dict[str, Any]:
    """ Represent a Comment as a dictionary """
    return {
        "id": comment.id,
        "timestamp": comment.created_at,
        "author": {
            "id": comment.user.id,
            "name": comment.user.username
        },
        "post": {
            "id": comment.post.id,
            "title": comment.post.title
        },
        "content": comment.content,
        "parent": {
            "id": comment.parent_comment.id,
            "author": comment.parent_comment.user.username,
            "content": comment.content
        } if comment.parent_comment else None
    }


def add_children(nested_list, list_comments):
    for i in range(len(nested_list)): 
        for comment in list(list_comments): 
            if comment["parent"]["id"] == nested_list[i]["id"]: 
                del comment["parent"]
                comment["children"] = [] 
                nested_list[i]["children"].append(comment) 
                list_comments.remove(comment)
                add_children(nested_list[i]["children"], list_comments) 

