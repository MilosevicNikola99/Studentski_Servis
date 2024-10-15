import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def measure_time(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()  # Početak merenja vremena
        result = await func(*args, **kwargs)  # Izvršavanje originalne funkcije
        end_time = time.time()  # Kraj merenja vremena
        execution_time = end_time - start_time  # Izračunavanje trajanja
        logger.info(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
        return result  # Vraćanje rezultata originalne funkcije
    return wrapper