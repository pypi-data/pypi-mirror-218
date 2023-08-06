A minimal Logger-module for your projects.

---

## How to use:
Initiate the Root-Logger
```python
from samus_logging import Samus_Logging
import logging

Samus_Logging()
logging.info('Your Message goes here.')
```

Create a Logger:
```python
from samus_logging import Samus_Logging

logger = Samus_Logging.create_logger()
logger.info('Your Message goes here.')
```