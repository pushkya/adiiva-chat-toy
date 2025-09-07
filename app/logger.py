import logging, json, time

logging.basicConfig(filename="interactions.log", level=logging.INFO, format='%(message)s')
METRICS = {"total_requests": 0, "unsafe_requests": 0, "last_latency": 0.0}

def log_interaction(question, response, safe, latency):
    event = {
        "timestamp": time.time(),
        "question": question,
        "response": response,
        "safe": safe,
        "latency": latency
    }
    logging.info(json.dumps(event))
