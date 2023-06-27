from typing import List, Union

import itertools
from functools import reduce

from pydantic import BaseModel

class Config(BaseModel):
    botName: str = "Ezra"
    models: List[str] = [
        "openai://gpt-4-0613",
        "openai://gpt-3.5-turbo-0613"
    ]
    initial_system_prompt: str = "You are a friendly AI."
    personal_system_prompt: str = ""
    temperature: float = 0.0
    disable_msg_log: bool = False
    log_level: Union[str, int] = "INFO"

DEFAULT_CONFIG = Config()

def merge(a: Config, b: Config):
    # There's gotta be a better way.
    merged = a.copy()
    if not b.botName == DEFAULT_CONFIG.botName:
        merged.botName = b.botName
    if not b.models == DEFAULT_CONFIG.models:
        merged.models = b.models
    if not b.initial_system_prompt == DEFAULT_CONFIG.initial_system_prompt:
        merged.initial_system_prompt = b.initial_system_prompt
    if not b.personal_system_prompt == DEFAULT_CONFIG.personal_system_prompt:
        merged.personal_system_prompt = b.personal_system_prompt
    if not b.temperature == DEFAULT_CONFIG.temperature:
        merged.temperature = b.temperature
    if not b.disable_msg_log == DEFAULT_CONFIG.disable_msg_log:
        merged.disable_msg_log = b.disable_msg_log
    if not b.log_level == DEFAULT_CONFIG.log_level:
        merged.log_level = b.log_level
    return merged

def merge_many(configs:[Config]) -> Config:
    return reduce(merge, configs)

print(f"DEFAULT_CONFIG: {DEFAULT_CONFIG}")

a = Config()
a.botName = "bot 1"
a.temperature = 0.5
a.log_level = "INFO"
print(f"A: {a}")

b = Config()
b.botName = "bot 2"
b.log_level = "DEBUG"
print(f"B: {b}")

c = merge(a, b)
print(f"C: {c}")
d = merge_many([a, b])
print(f"D: {d}")

