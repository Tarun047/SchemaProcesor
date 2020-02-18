import yaml
from entitycenter.extractor import SwaggerExtractor

with open('data/swagger.yaml') as f:
    swagger = yaml.safe_load(f)
    extractor = SwaggerExtractor()
    extractor.swagger_entity_extractor(swagger)
    print(extractor.swagger_mapper)
