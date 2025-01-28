from typing import TypedDict

class Follow(TypedDict):
    did : str
    handle : str
    displayName : str

class FollowsContainer(TypedDict):
    follows : list[Follow]
    subject : Follow
    cursor : str

class WorkOrderDto(TypedDict):
    username : str

class WorkAnswerDto(TypedDict):
    username : str
    followers : list[str]