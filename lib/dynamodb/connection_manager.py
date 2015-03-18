from setup_dynamodb import getDynamoDBConnection
from boto.dynamodb2.table import Table
from uuid import uuid4

class ConnectionManager:

    def __init__(self, mode=None, config=None, endpoint=None, port=None, use_instance_metadata=False):
        self.db = None
        self.gamesTable = None
        
        if mode == "local":
            if config is not None:
                raise Exception('Cannot specify config when in local mode')
            if endpoint is None:
                endpoint = 'localhost'
            if port is None:
                port = 8000
            self.db = getDynamoDBConnection(endpoint=endpoint, port=port, local=True)
        elif mode == "service":
            self.db = getDynamoDBConnection(config=config, endpoint=endpoint, use_instance_metadata=use_instance_metadata)
        else:
            raise Exception("Invalid arguments, please refer to usage.");