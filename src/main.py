from typing import List, Union

import argparse
import itertools
import logging as log
import os

from functools import reduce

from pydantic import BaseModel

import ai
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

    log.basicConfig(level=merged_config.log_level)

    log.info(f"Bot name: {merged_config.bot_name}")
    log.info(f"Models: {merged_config.models}")
    log.debug(f"Initial system prompt: {merged_config.initial_system_prompt}")
    log.debug(f"Personal system prompt: {merged_config.personal_system_prompt}")
    log.info(f"Temperature: {merged_config.temperature}")
    if merged_config.disable_msg_log:
        log.info(f"Disable message logging: {merged_config.disable_msg_log}")
    else:
        log.debug(f"Disable message logging: {merged_config.disable_msg_log}")

    log.debug(f"Log level: {merged_config.log_level}")
    log.info(f"Scribe {merged_config.bot_name} Online.")

    print("Ctrl-C to reload, Ctrl-D to exit.")

    # OpenAI system prompt
    messages =[
        { "role": "system", "content": merged_config.initial_system_prompt },
    ]
    if merged_config.personal_system_prompt:
        messages.append({ "role": "system", "content": merged_config.personal_system_prompt })
    current_model = merged_config.models[0]
    while True:
        print("me> ", end="")
        query = input()
        messages.append({ "role": "user", "content": query })
        response = ai.query_by_messages(current_model, messages)
        messages.append({ "role": "assistant", "content": response })

if __name__ == '__main__':
    main()
