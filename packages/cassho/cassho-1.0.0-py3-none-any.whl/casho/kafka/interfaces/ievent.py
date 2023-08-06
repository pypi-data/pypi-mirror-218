class IEvent:
    def __init__(self, eventType: str, data: any, createdAt: str):
        self.eventType = eventType
        self.data = data
        self.createdAt = createdAt
        
    def __dict__(self):
        return {
            'eventType': self.eventType,
            'data': self.data,
            'createdAt': self.createdAt
        }