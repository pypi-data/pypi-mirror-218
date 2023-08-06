from language_agent.module import call_openai_api

def agent_prompt(context, text):
    complete_text = f"{context} {text}"
    return call_openai_api(complete_text)
