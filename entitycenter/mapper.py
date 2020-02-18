class SwaggerMapper:
    def __init__(self):
        self._entity_map = dict()

    def add_mapping(self, name, entity):
        self._entity_map[name] = entity

    def query_schema(self, name):
        return self._entity_map[name]

    def query_schema_or_else_get(self, name, default):
        return self._entity_map.get(name, default)

    def remove_mapping(self, name):
        self._entity_map.pop(name)

    def __str__(self):
        return "\n".join(["{}".format(v) for v in self._entity_map.values()])
