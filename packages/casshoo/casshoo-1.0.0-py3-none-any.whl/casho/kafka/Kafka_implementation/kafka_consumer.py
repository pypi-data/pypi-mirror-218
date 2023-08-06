import logging
from confluent_kafka import Consumer
from typing import Callable
from ..interfaces.ievent import IEvent 
from ..interfaces.iconsumer import  IConsumer

logger = logging.getLogger()

class KafkaConsumer(IConsumer):
    def __init__(self, broker: str,consumer_group: str):
        self.consumer = Consumer({
            'bootstrap.servers': broker,
            'group.id': consumer_group,
            'auto.offset.reset': 'earliest'
        })

    def subscribe(self, topic: str,  callback: Callable[[IEvent], None]) -> None:
        self.consumer.subscribe(topics=[topic])
                    
        while True:
            message = self.consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                logger.error(
                    f'Error occurred while consuming from Kafka: {message.error().str()}')
                continue
            callback(message.value)
            logger.info(f"Received Message on Common django: {message.value.decode('utf-8')}")

            
        