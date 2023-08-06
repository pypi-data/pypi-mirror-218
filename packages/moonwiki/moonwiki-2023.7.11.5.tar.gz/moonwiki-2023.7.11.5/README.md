# moonwiki
![](https://img.shields.io/pypi/v/moonwiki?logo=python&logoColor=ffffff)

moonwiki is a wiki application made with Python that doesn't require:
- A database
- External modules
- Too much configuration
## Install
You can install moonwiki by using `pip`
```sh
pip install moonwiki
```
You can configure the above command to fit your needs for installing moonwiki
## Usage
Here are some usage examples:
```py
import moonwiki

print(moonwiki.__package__) # "moonwiki"
```
```py
from moonwiki import moonwiki
wiki = moonwiki("testWiki")

wiki.run("0.0.0.0", 8080)
```
