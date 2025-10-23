import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

l = logging.getLogger(__name__)

def logger(alert):
    return l.info(alert)