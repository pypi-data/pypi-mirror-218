# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ciare_world_creator',
 'ciare_world_creator.collections',
 'ciare_world_creator.commands',
 'ciare_world_creator.contexts_prompts',
 'ciare_world_creator.llm',
 'ciare_world_creator.model_databases',
 'ciare_world_creator.utils',
 'ciare_world_creator.xml']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'chromadb>=0.3.26,<0.4.0',
 'click>=8.1.3,<9.0.0',
 'langchain>=0.0.222,<0.0.223',
 'lark>=1.1.5,<2.0.0',
 'lxml>=4.9.2,<5.0.0',
 'openai>=0.27.8,<0.28.0',
 'pandas>=2.0.3,<3.0.0',
 'pre-commit>=3.3.3,<4.0.0',
 'questionary>=1.10.0,<2.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'tinydb>=4.8.0,<5.0.0',
 'tqdm>=4.65.0,<5.0.0']

entry_points = \
{'console_scripts': ['ciare_world_creator = ciare_world_creator.cli:cli']}

setup_kwargs = {
    'name': 'ciare-world-creator',
    'version': '0.1.2',
    'description': '',
    'long_description': '\n[![Ciare World Creator](/docs/media/logo.png)](https://ciare.dev)\n\n[![GitHub open issues](https://img.shields.io/github/issues-raw/ciare-robotics/world-creator.svg)](https://github.com/ciare/world-creator/issues)\n[![GitHub open pull requests](https://img.shields.io/github/issues-pr-raw/ciare-robotics/world-creator.svg)](https://github.com/ciare/world-creator/pulls)\n[![Hex.pm](https://img.shields.io/hexpm/l/plug.svg)](https://www.apache.org/licenses/LICENSE-2.0)\n\nCiare World Creator is a CLI tool that reimagines the creation of simulation worlds for robotics. We have a vision that in the future you will not be obliged to painstakingly craft detailed SDF files. With Ciare, you will be able to effortlessly generate dynamic and realistic simulation environments by simply providing input text. Whether you\'re testing robot navigation or experimenting with new solutions, Ciare intelligently spawns models, freeing you from the complexities of precise object placement. By harnessing the power of Language Models (LLMs), Ciare empowers developers to rapidly prototype and explore their ideas, simplifying the simulation process and unlocking a world of possibilities for innovation.\n\nImagine a scenario where you want to test the navigation capabilities of a robot. With Ciare World Creator, you no longer have to spend hours meticulously positioning every object in the simulation. Instead, you simply provide input text to the Ciare pipeline, and it takes care of the rest. Ciare intelligently spawns models in a reasonable manner, allowing you to focus on testing your solution in a simulated environment that closely resembles real-world scenarios.\n\n<p align="center">\n  <img width="800" src="https://cdn.jsdelivr.net/gh/ciare-robotics/world-creator@latest/docs/media/demo.svg">\n</p>\n\n# Features\n\n## Models\n\nCurrently it uses gpt-3.5-16k by default, but if you have access to gpt-4, you will be prompted with a selection. Note that gpt-4 performs much better, but not everyone has the invitation from OpenAI to use it.\n\n## Current limitations\n\nCurrently it\'s Proof Of Concept solution. There will be a lot of future development. Right now it really does often hallucinate and it\'s spatial notion is not that great, but sometimes it generates something cool.\n\nAlso complex models(like robots) currently is impossible to include. Work will be done on that in the future. Also complex textures of the models are not properly loading too.\n\n## Integration with other simulators\nGenerate simulation worlds on the fly with LLMs.\n\nSupports selected simulators, with plans to expand support to all major simulators.\nSimulator | Supported\n-- | --\nGazebo | ![Static Badge](https://img.shields.io/badge/Yes-green)\nNvidia Isaac Sim | ![Static Badge](https://img.shields.io/badge/Planned-yellow) \nUnity   | ![Static Badge](https://img.shields.io/badge/Planned-yellow)\n\n## Model Database\nIn the future we want to collect a vast model database from which you can freely choose any model to incorporate into your simulations. It aims to become the largest robotics model database available.\n\nCurrently, we use https://app.gazebosim.org/dashboard as database of the models.\n\n# Examples\n\n| Prompt  | Generated world |\n| ------------- | ------------- |\n| Healthcare worker and couple of medical items around them  | ![alt text](./docs/examples/medical.png)  |\n| Pile of fruits and other food in empty world | ![alt text](./docs/examples/pile.png)  |\n| Surgical room | ![alt text](./docs/examples/surgical_room.png) |\n| Warehouse shelves | ![alt text](./docs/examples/warehouse_shelves.png) |\n| Usual persons living room| ![alt text](./docs/examples/living_room.png) |\n\n\n# Getting Started\n\n## Installation\n\n### From source using poetry\n```\ngit clone https://github.com/ciare-robotics/world-creator.git\ncd world-creator\npoetry install\n```\n\n### Using pip\n```\npip3 install ciare-world-creator\n```\n\n\n## Token configuration\n\nOnce you installed ciare, you need to save your OpenAI token by launching `ciare_world_creator create` command first time.\n\n## OpenAI API usage\n\nI estimate that creating single world is only a matter of a few cents.\n\n# How to use\n\nCiare has couple of commands\n\n```console\nUsage: ciare ciare_world_creator [OPTIONS] COMMAND [ARGS]...\n\n  World creator by Ciare\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  create            Create new simulation world\n  list              Lists all worlds created by you\n  purge             Delete database and all of the worlds you\'ve created\n  fix               Sometimes, world downloaded can be malformed, so we will\n                   take all objects from that world and respawn them in empty\n                     world\n\n```\n\n## Create simulation world\n\nYou can crate simulation worlds by using command `ciare_world_creator create`. You will need to prompt any query that will describe your simulation world as precise as possible. Model hallucinate pretty often.\n\n```console\nsim@sim:world-creator$ ±|main ✗|→ ciare_world_creator create\n? Enter query for world generation(E.g Two cars and person next to it) Multiple cars spawned 5 meters from each other in empty world. One bicycle besides them\n\nUsing embedded DuckDB with persistence: data will be stored in: /var/tmp/ciare/chromadb\n\nGenerating world... 🌎\nWorld is Test, downloading it\nFile downloaded successfully.\n\nSpawning models in the world... 🫖\n\nPlacing models in the world... 📍\n\nFinished! Output available at /var/tmp/ciare/worlds/world_multiple_cars_spawned_5_meters_from_each_other_in_empty_world_one_bicycle_besides_them.sdf 🦄\n```\n\n## List created worlds\nYou can run `ciare_world_creator list` to view already created worlds. We save every prompt from create command, so later you won\'t query LLM again.\n\n## Purge database\n\nWith `ciare_world_creator purge` you can delete created worlds from local storage and start from scratch.\n\n## Fix malformed world\nWe take database of worlds from https://app.gazebosim.org/, but sometimes someone puts a world there that doesn\'t work at all and breaks because of the missing tag or any other error...\n\nTo overcome this, you can fix already created world by running `ciare_world_creator fix` command and later typing the name of your world. All models will be spawned in the empty world after that.\n\n# Feedback and contributions\nWe welcome feedback and contributions from the community to make Ciare World Creator even better. If you encounter any issues, have ideas for improvements, or would like to contribute to the project, please visit the GitHub repository and open an issue or submit a pull request.\n\nLet\'s create stunning simulation worlds together!\n\n',
    'author': 'Alex Karavaev',
    'author_email': 'alexkaravaev@alexkaravaev.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
