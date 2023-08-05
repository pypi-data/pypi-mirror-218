# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kor', 'kor.documents', 'kor.encoders', 'kor.extraction']

package_data = \
{'': ['*']}

install_requires = \
['langchain>=0.0.110', 'openai>=0.27,<0.28', 'pandas>=1.5.3,<2.0.0']

extras_require = \
{'html': ['markdownify>=0.11.6,<0.12.0']}

setup_kwargs = {
    'name': 'kor',
    'version': '0.12.0',
    'description': 'Extract information with LLMs from text',
    'long_description': '**⚠ WARNING: Prototype with unstable API. 🚧**  \n\n[![Unit Tests](https://github.com/eyurtsev/kor/actions/workflows/test.yml/badge.svg?branch=main&event=push)](https://github.com/eyurtsev/kor/actions/workflows/test.yml)\n[![Test Docs](https://github.com/eyurtsev/kor/actions/workflows/doc_test.yaml/badge.svg?branch=main&event=push)](https://github.com/eyurtsev/kor/actions/workflows/doc_test.yaml)\n\n# Kor\n\nThis is a half-baked prototype that "helps" you extract structured data from text using LLMs 🧩.\n\nSpecify the schema of what should be extracted and provide some examples.\n\nKor will generate a prompt, send it to the specified LLM and parse out the\noutput.\n\nYou might even get results back.\n\nSo yes – it’s just another wrapper on top of LLMs with its own flavor of abstractions. 😸\n\nSee [documentation](https://eyurtsev.github.io/kor/).\n\nIntegrated with the [LangChain framework 😽💗 🦜🔗](https://python.langchain.com/en/latest/index.html).\n\n## Kor style schema\n\n```python\nfrom langchain.chat_models import ChatOpenAI\nfrom kor import create_extraction_chain, Object, Text\n\nllm = ChatOpenAI(\n    model_name="gpt-3.5-turbo",\n    temperature=0,\n    max_tokens=2000,\n    frequency_penalty=0,\n    presence_penalty=0,\n    top_p=1.0,\n)\n\nschema = Object(\n    id="player",\n    description=(\n        "User is controlling a music player to select songs, pause or start them or play"\n        " music by a particular artist."\n    ),\n    attributes=[\n        Text(\n            id="song",\n            description="User wants to play this song",\n            examples=[],\n            many=True,\n        ),\n        Text(\n            id="album",\n            description="User wants to play this album",\n            examples=[],\n            many=True,\n        ),\n        Text(\n            id="artist",\n            description="Music by the given artist",\n            examples=[("Songs by paul simon", "paul simon")],\n            many=True,\n        ),\n        Text(\n            id="action",\n            description="Action to take one of: `play`, `stop`, `next`, `previous`.",\n            examples=[\n                ("Please stop the music", "stop"),\n                ("play something", "play"),\n                ("play a song", "play"),\n                ("next song", "next"),\n            ],\n        ),\n    ],\n    many=False,\n)\n\nchain = create_extraction_chain(llm, schema, encoder_or_encoder_class=\'json\')\nchain.predict_and_parse(text="play songs by paul simon and led zeppelin and the doors")[\'data\']\n```\n\n```python\n{\'player\': {\'artist\': [\'paul simon\', \'led zeppelin\', \'the doors\']}}\n```\n\n## Pydantic style schema\n\n* See documentation here [pydantic](https://eyurtsev.github.io/kor/validation.html).\n\n```python \nclass Action(enum.Enum):\n    play = "play"\n    stop = "stop"\n    previous = "previous"\n    next_ = "next"\n\n\nclass MusicRequest(BaseModel):\n    song: Optional[List[str]] = Field(\n        description="The song(s) that the user would like to be played."\n    )\n    album: Optional[List[str]] = Field(\n        description="The album(s) that the user would like to be played."\n    )\n    artist: Optional[List[str]] = Field(\n        description="The artist(s) whose music the user would like to hear.",\n        examples=[("Songs by paul simon", "paul simon")],\n    )\n    action: Optional[Action] = Field(\n        description="The action that should be taken; one of `play`, `stop`, `next`, `previous`",\n        examples=[\n            ("Please stop the music", "stop"),\n            ("play something", "play"),\n            ("play a song", "play"),\n            ("next song", "next"),\n        ],\n    )\n    \nschema, validator = from_pydantic(MusicRequest)   \nchain = create_extraction_chain(\n    llm, schema, encoder_or_encoder_class="json", validator=validator\n)\nchain.predict_and_parse(text="stop the music now")["validated_data"]\n```\n\n```python\nMusicRequest(song=None, album=None, artist=None, action=<Action.stop: \'stop\'>)\n```\n\n\n\n## Compatibility\n\n`Kor` is tested against python 3.8, 3.9, 3.10, 3.11.\n\n## Installation\n\n```sh\npip install kor\n```\n\n## 💡 Ideas\n\nIdeas of some things that could be done with Kor.\n\n* Extract data from text that matches an extraction schema.\n* Power an AI assistant with skills by precisely understanding a user request.\n* Provide natural language access to an existing API.\n\n## 🚧 Prototype\n\nPrototype! So the API is not expected to be stable!\n\n##  ✨ What does Kor excel at?  🌟\n\n* Making mistakes! Plenty of them!\n* Slow! It uses large prompts with examples, and works best with the larger slower LLMs.\n* Crashing for long enough pieces of text! Context length window could become\n  limiting when working with large forms or long text inputs.\n\nThe expectation is that as LLMs improve some of these issues will be mitigated.\n\n## Limitations\n\nKor has no limitations. (Just kidding.)\n\nTake a look at the section above and at the compatibility section.\n\n## Got Ideas?\n\nOpen an issue, and let\'s discuss!\n\n## 🎶 Why the name?\n\nFast to type and sufficiently unique.\n\n## Contributing\n\nIf you have any ideas or feature requests, please open an issue and share!\n\nSee [CONTRIBUTING.md](https://github.com/eyurtsev/kor/blob/main/CONTRIBUTING.md) for more information.\n\n## Other packages\n\nProbabilistically speaking this package is unlikely to work for your use case.\n\nSo here are some great alternatives:\n\n* [Promptify](https://github.com/promptslab/Promptify)\n* [MiniChain](https://srush.github.io/MiniChain/examples/stats/)\n',
    'author': 'Eugene Yurtsev',
    'author_email': 'eyurtsev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.github.com/eyurtsev/kor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
