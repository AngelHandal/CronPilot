from cron_descriptor import get_description
from croniter import croniter
from datetime import datetime

def translate_cron(cron_expression: str):
    try:
        return get_description(cron_expression)
    except Exception as e:
        return f"Could not translate: {e}"

def get_next_execution(cron_expression: str):
    try:
        now = datetime.now()
        iter = croniter(cron_expression, now)
        next_time = iter.get_next(datetime)
        return next_time.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return f"Error: {e}"
