from typing import List, Dict
from pydantic_core import ErrorDetails
from pydantic import ValidationError


CUSTOM_MESSAGES = {
    "int_parsing": "This is not an integer! 🤦",
    "url_scheme": "Hey, use the right URL scheme! I wanted {expected_schemes}.",
    "string_too_short": "Terlalu pendek",
    "missing": "Harus diisi",
}


def convert_errors(
    e: ValidationError, custom_messages: Dict[str, str]
) -> List[ErrorDetails]:
    new_errors: List[ErrorDetails] = []
    for error in e.errors():
        custom_message = custom_messages.get(error["type"])
        if custom_message:
            ctx = error.get("ctx")
            error["msg"] = custom_message.format(**ctx) if ctx else custom_message
        new_errors.append(error)
    return new_errors
