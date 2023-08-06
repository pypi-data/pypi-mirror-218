# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['powertools_oas_validator',
 'powertools_oas_validator.overrides',
 'powertools_oas_validator.services']

package_data = \
{'': ['*']}

install_requires = \
['aws-lambda-powertools>=2.18.0,<3.0.0',
 'fastjsonschema>=2.17.1,<3.0.0',
 'jmespath>=1.0.1,<2.0.0',
 'openapi-core>=0.17.2,<0.18.0']

setup_kwargs = {
    'name': 'powertools-oas-validator',
    'version': '6.0.0',
    'description': '',
    'long_description': '# powertools-oas-validator\n<br><a href="https://badge.fury.io/py/powertools-oas-validator"><img src="https://badge.fury.io/py/powertools-oas-validator.svg" alt="PyPI version"></a>  ![CI](https://github.com/RasmusFangel/powertools-oas-validator/workflows/CI/badge.svg) <img src="https://coveralls.io/repos/RasmusFangel/powertools-oas-validator/badge.svg?branch=main" alt="Coveralls"></a>\n\n## Introduction\n\n[Powertools for AWS Lambda (Python)](https://github.com/aws-powertools/powertools-lambda-python) is an awesome set of tools for supercharging your lambdas. Powertools supports validating incoming requests (or event in PT lingo) against [JSONSchema](https://json-schema.org/) which is not ideal if you are using OpenAPI schemas to define your API contracts.\n\nThe *Powertools OAS Validator* adds a decorator that you can use with your lambda handlers and have the events validated against an OpenAPI schema instead.\n\n\n## Installation\nPoetry:\n`poetry add powertools-oas-validator`\n\nPip:\n`pip install powertools-oas-validator`\n\n\n## Usage\nDecorate your functions with `@validate_request(oas_path="openapi.yaml")` and your request/event (and schema) will be validated on a request.\n\n\n### Minimal Example\n\n```python\nfrom typing import Dict\nfrom aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response\nfrom aws_lambda_powertools.utilities.typing import LambdaContext\nfrom powertools_oas_validator.middleware import validate_request\n\n\napp = APIGatewayRestResolver()\n\n@app.post("/example")\ndef example() -> Response:\n  ...\n\n@validate_request(oas_path="openapi.yaml")\ndef lambda_handler(event: Dict, context: LambdaContext) -> Dict:\n    response = app.resolve(event, context)\n\n    return response\n```\n\n## Error Handling\nIf the validation fails, the decorator throws a `SchemaValidatonError` with relevant information about the failed validation.\n\n\nExample of a `SchemaValidatonError`:\n```python\nfrom aws_lambda_powertools.utilities.validation import SchemaValidationError\n\nSchemaValidatonError(\n  name="test-path.test-endpoint.requestBody[param_1]",\n  path=["test-path", "test-endpoint", "requestBody", "param_1"],\n  validation_message="\'not an integer\' is not of type \'integer\'.",\n  message="\'not an integer\' is not of type \'integer\'",\n  rule="int",\n  rule_definition="type",\n  value="\'not an integer\'"\n)\n```\n\n## Know Issues\nWhile all validation errors are caught, there is only limited information about the various errors. The decorator will try its best to throw a `SchemaValidatonError`\n(same as the Powertools validator would), with as much of the optional attributes as possible.\n\nIn summary, it is possible that not all `SchemaValidationErrors`\'s will have the correct name and path attributes.\n\n\n## Contributions\nPlease make a pull request and I will review it ASAP.\n',
    'author': 'Rasmus Hansen',
    'author_email': 'R.FangelHansen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/RasmusFangel/powertools-oas-validator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
