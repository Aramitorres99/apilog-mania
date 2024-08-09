import requests
import logging
import random
import time
from datetime import datetime

SERVICE_NAME = 'Service-1'
SERVICE_URL = 'http://127.0.0.1:5000/logs'
API_TOKEN = 'service-1-token'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(SERVICE_NAME)

def generate_log():
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    level = random.choice(levels)
    message = f'Simulando log mensaje en el nivel {logging.getLevelName(level)}'
    return {
        "timestamp": datetime.now().isoformat(),
        "service": SERVICE_NAME,
        "level": logging.getLevelName(level),
        "message": message
    }

def send_log(log):
    try:
        headers = {'Authorization': API_TOKEN}
        response = requests.post(SERVICE_URL, json=log, headers=headers)
        if response.status_code == 200:
            logger.info(f'Exitoso envio de log: {response.status_code} - {response.json()}')
        else:
            logger.error(f"Fallo el envio del log: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f'Excepcion ocurrida enviando el log: {e}')

while True:
    log = generate_log()
    send_log(log)
    time.sleep(random.randint(1, 5))
