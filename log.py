import logzero
from logzero import logger

logzero.logfile("logs/monitor.log", maxBytes=1e6, backupCount=10)