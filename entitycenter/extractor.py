from .models import Entity
from .mapper import SwaggerMapper


class SwaggerExtractor:
    def __init__(self):
        self.swagger_mapper = SwaggerMapper()
        self.swagger_spec = None

    def swagger_entity_extractor(self, swagger):
        self.swagger_spec = swagger
        for entity_name, schema in swagger['definitions'].items():
            entity = Entity()
            entity.name = entity_name
            entity.type = self.__resolve_entities__(schema)
            self.swagger_mapper.add_mapping(entity_name, entity)

    def __resolve_entities__(self, schema):
        if 'type' in schema and schema['type'] != 'object':
            return schema['type']
        elif 'properties' in schema:
            all_props = set()
            for property in schema['properties']:
                sub_entity = Entity()
                sub_entity.name = property
                sub_entity.type = self.__resolve_entities__(schema['properties'][property])
                all_props.add(sub_entity)
            return all_props
        elif 'allOf' in schema:
            all_props = dict()
            for sub_schema in schema['allOf']:
                resolved_schema = self.__resolve_entities__(sub_schema)
                all_props.update(resolved_schema)
            return all_props
        elif '$ref' in schema:
            resource = schema['$ref'][schema['$ref'].rindex('/') + 1:]
            return self.swagger_mapper.query_schema_or_else_get(resource, {resource: "Yet to be found"})
