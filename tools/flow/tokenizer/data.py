__all__ = [
    'ConditionData',
    'ActionParamsData',
    'ActionData',
    'HandlerData',
    'ManagerData',
    'FlowData',
]

ConditionData = str
ActionParamsData = tuple[int, int, int, int, str]
ActionData = tuple[ActionParamsData, int]
HandlerData = tuple[ConditionData, ActionData]
ManagerData = tuple[list[HandlerData], ActionData | int]
FlowData = list[ManagerData]
