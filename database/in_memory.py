"""In-memory database connection for testing."""

memory_db = {"Users": {}}

class MemoryDBConnection:
    """Singleton for in-memory DB connection."""
    _instance = None

    class MemoryTable:
        """In-memory DynamoDB table."""
        def __init__(self, name):
            self.name = name
            memory_db.setdefault(name, {})

        def get_item(self, key):
            """Get item by key."""
            item = memory_db[self.name].get(key["email"])
            return {"Item": item} if item else {}

        def put_item(self, item):
            """Put item into table."""
            memory_db[self.name][item["email"]] = item
            return {"ResponseMetadata": {"HTTPStatusCode": 200}}

        def update_item(self, key, update_expression, _expression_attribute_names, expression_attribute_values):
            """Update item in table."""
            table = memory_db[self.name]
            item = table.get(key["email"])
            if not item:
                raise Exception("Item not found")
            # Simple SET support
            for _k, v in expression_attribute_values.items():
                attr = update_expression.split("SET")[1].split("=")[0].strip()[1:]
                item[attr] = v
            return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    def __init__(self):
        self._tables = {}

    @classmethod
    def get_instance(cls):
        """Returns a MemoryDBConnection instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def Table(self, name):
        """Returns a MemoryTable instance."""
        if name not in self._tables:
            self._tables[name] = self.MemoryTable(name)
        return self._tables[name]
