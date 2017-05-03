import re


def get_task_path_and_exc(file_path):
    """Get the task path and exception from the file by using its file path"""
    with open(file_path, 'r') as f:
        for line in f:
            reg = re.search('Task (.*) with id (?:[0-9a-f\-]+) raised '
                            'exception:', line)
            if reg:
                task_name = reg.group(1)
                return task_name, f.readline().strip()


def get_task_args_and_kwargs(file_path):
    """Get the args and kwargs for the task."""
    text = ''
    with open(file_path, 'r') as f:
        for line in f:
            text += line.strip() + ' '

    reg = re.search('Task was called with args: (\(.*?\)) '
                    'kwargs: ({.*?})', text)

    if reg:
        return reg.group(1), reg.group(2)

    # Can't parse arguments b/c they're not in the email.
    return None, None
