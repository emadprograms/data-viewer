"""
Configuration and constants for the market data viewer.
"""
from pytz import timezone

# Timezone Configuration
US_EASTERN = timezone('US/Eastern')
UTC = timezone('UTC')

# Data Schema
SCHEMA_COLS = ['timestamp', 'symbol', 'open', 'high', 'low', 'close', 'volume', 'session']
