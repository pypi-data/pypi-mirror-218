class IProducerConfiguration:
    def __init__(self, type: str, broker: str):
        self.type = type
        self.broker = broker
