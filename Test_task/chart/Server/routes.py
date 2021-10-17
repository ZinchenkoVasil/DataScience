from controllers import (get_response, get_message, log_out)

routes = [
    {'action': 'presence', 'controller': get_response},
    {'action': 'message', 'controller': get_message},
    {'action': 'logout', 'controller': log_out}
]