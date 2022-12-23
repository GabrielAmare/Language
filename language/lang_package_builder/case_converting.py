import re

__all__ = [
    'pascal_case_to_snake_case'
]


def pascal_case_to_snake_case(class_name: str) -> str:
    """
    Extract the method name from a class name in PascalCase format and convert it to snake_case format.

    Args:
    - class_name (str): The class name in PascalCase format to process.

    Returns:
    - str: The method name in snake_case format.

    Examples:
    - _extract_method_name("FooBarBaz") -> "_foo_bar_baz"
    - _extract_method_name("Foo123Bar456Baz") -> "_foo123_bar456_baz"
    - _extract_method_name("ExampleGR") -> "_example_g_r"
    """
    if not re.match(r'^_?(?:[A-Z][a-z\d_]*)+$', class_name):
        raise ValueError('`class_name` must be in PascalCase format.')
    
    return re.sub(r'[A-Z][a-z\d_]*', lambda m: '_' + m.group(0).lower(), class_name)
