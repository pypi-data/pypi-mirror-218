class IConsumerConfiguration:
    def __init__(self, type: str, broker: str, consumer_group: str):
        self.type = type
        self.broker = broker
        self.consumer_group = consumer_group

