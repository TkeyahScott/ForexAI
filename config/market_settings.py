
# ==========================================
# FOREXAI: MARKET CONFIGURATION
# ==========================================

# Broker server time configuration.
#
# Current verified broker offset: AS AT 11/11/2026 12:24 AM.
# UTC+2 = 2 hours = 7,200 seconds.
#
# IMPORTANT:
# This is the currently observed offset for
# the MetaQuotes-Demo server. It may change
# seasonally due to daylight saving time.
#
# Keep this value centralised so that all
# ForexAI market-data components use the
# same timestamp configuration.

BROKER_UTC_OFFSET_SECONDS = 7200
