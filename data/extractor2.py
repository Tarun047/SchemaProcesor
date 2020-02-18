import yaml
from collections import defaultdict


def process_schema(schema):
    if '$ref' in schema:
        resource = schema['$ref']
        resource = process_schema(swagger['definitions'][resource[resource.rindex("/") + 1:]])
        return resource
    else:
        if 'type' in schema and schema['type'] != 'object':
            return schema['type']
        elif 'properties' in schema:
            answer = []
            for sub_schema in schema.get('properties', []):
                answer.append({sub_schema: process_schema(schema['properties'][sub_schema])})
            return answer
        elif 'additionalProperties' in schema:
            return process_schema(schema['additionalProperties'])


def resolve_to_str(data):
    if isinstance(data, dict) or isinstance(data, list):
        ans = ""
        for attr in x:
            ans += " " + resolve_to_str(attr)
    else:
        return ans

def process_request_inputs(working_data):
    input_variables = defaultdict(dict)
    for parameter in working_data:
        if 'type' in parameter:
            input_variables[parameter['in']][parameter['name']] = parameter['type']
        if 'schema' in parameter:
            input_variables[parameter['in']][parameter['name']] = []
            for data in parameter['schema'].get('allOf', []):
                input_variables[parameter['in']][parameter['name']].append(process_schema(data))
            if len(input_variables[parameter['in']][parameter['name']]) == 0:
                input_variables[parameter['in']][parameter['name']] = process_schema(parameter['schema'])
    return resolve_to_str(input_variables)


def extractor(swagger, out):
    working_data = swagger['paths']
    for endpoint in working_data:
        for operation in working_data[endpoint]:
            if 'parameters' in working_data[endpoint][operation]:
                out.write('{}\t{}\t{}\t{}\n'.format(operation, endpoint, str(
                    process_request_inputs(working_data[endpoint][operation]['parameters'])),
                                                    working_data[endpoint][operation]['summary']))
            else:
                print(endpoint, operation)


with open("output.tsv", "w") as out:
    with open("swagger.yaml") as inp:
        swagger = yaml.safe_load(inp.read())
        extractor(swagger, out)
