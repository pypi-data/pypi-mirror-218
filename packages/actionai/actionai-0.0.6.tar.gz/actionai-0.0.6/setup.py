# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['actionai']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.8,<0.28.0', 'pydantic>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'actionai',
    'version': '0.0.6',
    'description': 'A small library to call local functions using openai function calling',
    'long_description': '# ActionAI\n\nA small library to run local functions using openai function calling\n\n## Install\n\n```shell\npip install actionai\n```\n\n## Usage\n\n> **Note**\n> A function must be fully typed and must have a docstring(one liner explanation of the function would be enough)\n\n```python\n# define a new function\ndef get_current_weather(location: str, unit: str = "fahrenheit"):\n    """Function to get current weather for the given location"""\n    weather_info = {\n        "location": location,\n        "temperature": "72",\n        "unit": unit,\n        "forecast": ["sunny", "windy"],\n    }\n    return weather_info\n\n\nimport actionai\n\naction = actionai.ActionAI()\naction.register(get_current_weather)\n\nresponse = action.prompt("What is the current weather in the north pole?")\n\nprint(response["choices"][0]["message"]["content"])\n# The current weather at the North Pole is 72°F. It is sunny and windy.\n```\n\nThe openai api key will be read automatically from the `OPENAI_API_KEY` environment variable. You can pass it manually as,\n\n```python\nimport actionai\n\naction = actionai.ActionAI(openai_api_key="YOUR_KEY")\n```\n\n### Adding context\n\nSometimes your function will have variables that needs to be set by the program.\n\n```python\ndef list_todos(user: str):\n    """Function to list all todos"""\n    return todos[user]\n\naction = actionai.ActionAI(context={"user": "jason"})\n```\n\nThe context keys are skipped when creating json schema. The values are directly passed at the time of function calling.\n\n### Choosing a model\n\nBy default, the completion run on the `gpt-3.5-turbo-0613` model. You can change the model using the `model` argument.\n\n```python\nimport actionai\n\naction = actionai.ActionAI(model="gpt-4")\n```\n\nYou can see the complete list of supported chat completion models [here](https://platform.openai.com/docs/models/model-endpoint-compatibility)\n\n## Demo\n\nRunning [todo example](https://github.com/amalshaji/actionai/blob/main/examples/todo.py) 👇🏻\n\n![todo demo](https://raw.githubusercontent.com/amalshaji/actionai/main/examples/demo.svg)\n\nFor more examples, checkout the [examples](https://github.com/amalshaji/actionai/tree/main/examples) directory.\n',
    'author': 'Amal Shaji',
    'author_email': 'amalshajid@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
