from .base import *

if os.environ['FINNHIKE'] == 'prod':
    from .prod import *
else:
    from .dev import *
