__all__ = [
    'ConditionData',
    'ActionParamsData',
    'ActionData',
    'HandlerData',
    'ManagerData',
    'FlowData',
]

ConditionData = str
ActionParamsData = tuple[int, str]
ActionData = tuple[ActionParamsData, int]
HandlerData = tuple[ConditionData, int]
ManagerData = tuple[list[HandlerData], int | None]
FlowData = tuple[list[ManagerData], list[ActionData]]
