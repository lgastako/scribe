import time

import logging as log


def query_by_messages(model, messages):
    response = completion_via_requests(messages,
                                       model=model,
                                       functions=OPENAI_FUNCTIONS,
                                       temperature=0)
    message = response["choices"][0]["message"]
    messages.append(message)
    # TODO DRY up vs cliloop.py
    fn_call = message.get("function_call")
    if fn_call:
        log.debug("It's a function call...")
        fn_start_time = time.time()
        (fn_name, result) = call_function(abs_workspace_path, message)
        fn_end_time = time.time()
        log.debug(f"call_function took {fn_end_time - fn_start_time} seconds")
        log.debug(f"fn call results: {result}")
        message = {
            "role": "function",
            "name": fn_name,
            "content": result
        }
        messages.append(message)
    else:
        reply = message["content"]
        print(f"jr> {reply}")
    return messages
