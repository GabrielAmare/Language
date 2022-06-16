__all__ = [
    'ConditionData',
    'ActionData',
    'HandlerData',
    'ManagerData',
    'FlowData',
]

ConditionData = str
ActionData = tuple[int, int, int, str, bool, int]
HandlerData = tuple[ConditionData, ActionData]
ManagerData = tuple[list[HandlerData], ActionData | int]
FlowData = list[ManagerData]
