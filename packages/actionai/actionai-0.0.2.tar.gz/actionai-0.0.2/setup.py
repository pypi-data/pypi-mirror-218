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
    'version': '0.0.2',
    'description': 'A small library to call local functions using openai function calling',
    'long_description': '# ActionAI\n\nA small library to run local functions using openai function calling\n\n## Install\n\n```shell\npip install actionai\n```\n\n## Usage\n\n```python\n# define a new function\n# example from openai functions examples\ndef get_current_weather(location: str, unit: str = "fahrenheit"):\n    """Function to get current weather for the given location"""\n    weather_info = {\n        "location": location,\n        "temperature": "72",\n        "unit": unit,\n        "forecast": ["sunny", "windy"],\n    }\n    return weather_info\n\n\nimport actionai\n\naction = actionai.ActionAI()\naction.register(get_current_weather)\n\nresponse = action.prompt("What is the current weather in the north pole?")\n\nprint(response["choices"][0]["message"]["content"])\n# The current weather at the North Pole is 72°F. It is sunny and windy.\n```\n\n> **Warning**\n> A function must be fully typed and must have a docstring(one liner explanation of the function is enough)\n\n## Demo\n\nRunning [todo example](/examples/todo.py) 👇🏻\n\n![todo demo](/examples/demo.svg)\n\nFor more examples, checkout the [examples](/examples/) directory.\n',
    'author': 'Amal Shaji',
    'author_email': 'amalshajid@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
