from website.language.semi.lang.models import *

ALWAYS = Group(items=String(content=repr('')), inverted=Inverted())
NEVER = Group(items=String(content=repr('')), inverted=None)

VALID = Valid()
ERROR = Error()
EXCLUDED = Excluded()
