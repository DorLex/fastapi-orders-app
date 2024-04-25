class MockKafkaProducer:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def send_and_wait(self, *args, **kwargs):
        return True


async def mock_get_producer():
    return MockKafkaProducer()
