from typing import List, Union

import argparse
import itertools
import os

from functools import reduce

from pydantic import BaseModel

# TODO
__FIELD_NAMES__ = [
    "bot_name",
    "models",
    "initial_system_prompt",
    "personal_system_prompt",
    "temperature",
    "disable_msg_log",
    "log_level"
]

class Config(BaseModel):
    bot_name: str = "Ezra"
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
    if a is None:
        return b
    if b is None:
        return a
    merged = a.copy()
    if not b.bot_name == DEFAULT_CONFIG.bot_name:
        merged.bot_name = b.bot_name
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

def from_env() -> Config:
    config = DEFAULT_CONFIG.copy()
    for field_name in __FIELD_NAMES__:
        if field_name.upper() in os.environ:
            setattr(config, field_name, os.environ[field_name])
    return config

def from_dict(json: dict) -> Config:
    config = DEFAULT_CONFIG.copy()
    # is this good?
    for field_name in __FIELD_NAMES__:
        if field_name in json:
            setattr(config, field_name, json[field_name])
    return config

def from_file(path: str) -> Config:
    config = DEFAULT_CONFIG.copy()
    try:
        with open(path, "r") as f:
            return Config.from_dict(json.loads(f.read()))
    except FileNotFoundError:
        return config

def from_args(args) -> Config:
    parser = create_arg_parser()
    print(f"Args: {args}")

    config = DEFAULT_CONFIG.copy()
    for field_name in __FIELD_NAMES__:
        if hasattr(args, field_name):
            val = getattr(args, field_name)
            if val is not None:
                setattr(config, field_name, val)
    return config

def create_arg_parser():
    parser = argparse.ArgumentParser(description='Program configuration')

    parser.add_argument('--bot_name', type=str, help='Name of the bot')
    parser.add_argument('--models', nargs='+', help='List of models')
    parser.add_argument('--initial_system_prompt', type=str, help='Initial system prompt')
    parser.add_argument('--personal_system_prompt', type=str, help='Personal system prompt')
    parser.add_argument('--temperature', type=float, help='Temperature value')
    parser.add_argument('--disable_msg_log', action='store_true', help='Disable message logging')
    parser.add_argument('--log_level', type=lambda x: int(x) if x.isdigit() else x, help='Log level')

    return parser

def main():
    print("Scribe initializing...")
    parser      = create_arg_parser()
    args        = parser.parse_args()

    print(f"Default config: {DEFAULT_CONFIG}")

    env_config  = from_env()
    print(f"Environment config: {env_config}")
    args_config = from_args(args)
    print(f"Args config: {args_config}")

    config      = merge_many([DEFAULT_CONFIG,
                              env_config,
                              args_config
                              ])
    print(f"Final config: {config}")

    print(f"Bot name: {config.bot_name}")
    print(f"Models: {config.models}")
    print(f"Initial system prompt: {config.initial_system_prompt}")
    print(f"Personal system prompt: {config.personal_system_prompt}")
    print(f"Temperature: {config.temperature}")
    print(f"Disable message logging: {config.disable_msg_log}")
    print(f"Log level: {config.log_level}")

    print(f"Scribe {config.bot_name} Online.")

if __name__ == '__main__':
    main()
