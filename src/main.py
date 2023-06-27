from typing import List, Union

import argparse
import itertools
import os

from functools import reduce

from pydantic import BaseModel

import config

def main():
    print("Scribe initializing...")
    print(f"Default config: {config.DEFAULT}")
    env_config  = config.from_env()
    print(f"Environment config: {env_config}")
    args_config = config.from_args()
    print(f"Args config: {args_config}")
    merged_config = config.merge_many([
        config.DEFAULT,
        env_config,
        args_config
    ])
    print(f"Final (merged) config: {merged_config}")

    print(f"Bot name: {merged_config.bot_name}")
    print(f"Models: {merged_config.models}")
    print(f"Initial system prompt: {merged_config.initial_system_prompt}")
    print(f"Personal system prompt: {merged_config.personal_system_prompt}")
    print(f"Temperature: {merged_config.temperature}")
    print(f"Disable message logging: {merged_config.disable_msg_log}")
    print(f"Log level: {merged_config.log_level}")

    print(f"Scribe {merged_config.bot_name} Online.")

if __name__ == '__main__':
    main()
