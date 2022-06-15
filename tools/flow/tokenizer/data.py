__all__ = [
    'ConditionData',
    'ActionData',
    'HandlerData',
    'ManagerData',
    'FlowData',
]

ConditionData = str
ActionData = tuple[int, int, str, int]
HandlerData = tuple[ConditionData, ActionData]
ManagerData = tuple[list[HandlerData], ActionData | int]
FlowData = tuple[list[ManagerData], list[str]]
