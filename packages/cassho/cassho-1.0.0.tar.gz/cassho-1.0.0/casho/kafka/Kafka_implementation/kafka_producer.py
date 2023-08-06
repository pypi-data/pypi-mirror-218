import json
import logging
from confluent_kafka import Producer
from ..interfaces.ievent import IEvent 
from ..interfaces.imetadata import IMetadata 
from ..interfaces.iproducer import IProducer 

logger = logging.getLogger()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyMeta(type(IProducer), type(Singleton)):
    pass
class KafkaProducer(IProducer,metaclass=MyMeta):
    def __init__(self, broker: str):
        self.producer = Producer({'bootstrap.servers': broker})

    def acked(self, err, msg):
        if err is not None:
            logger.error(f'Failed to deliver message: {msg.value()}: {err.str()}')
        else:
            logger.info(f'Message produced: {msg.value()}')

    def send_message(self, metadata: IMetadata, message: IEvent) -> None:
        topic = metadata.topic
        serialized_message = json.dumps(message.__dict__())

        try:
            self.producer.produce(topic, serialized_message.encode('utf-8'), callback=self.acked)
            logger.info(f"Message sent to Kafka from django: {serialized_message}")
            self.producer.flush()
        except Exception as e:
            logger.error(f"Error occurred while producing to Kafka: {e}")
    
    @staticmethod
    def get_instance(broker: str) -> IProducer:
        return KafkaProducer(broker)
