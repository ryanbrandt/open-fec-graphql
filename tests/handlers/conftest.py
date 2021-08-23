from unittest.mock import patch

patch('app.cache.cached_query.cached_query', lambda x: x).start()
