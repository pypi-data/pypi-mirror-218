[![PyPI version](https://badge.fury.io/py/node-distance.svg)](https://badge.fury.io/py/node-distance)
[![PyPi downloads](https://img.shields.io/pypi/dm/node-distance)](https://img.shields.io/pypi/dm/node-distance)
[![DOI](https://zenodo.org/badge/433801845.svg)](https://zenodo.org/badge/latestdoi/433801845)


# node-distance: Tree node distances as features
Compute distance between all nodes of a tree, and estimate an histogram that can be used as features for other models.

### Toy Text Corpus

```py
corpus = "Als Ada Lovelace auf einem Ball den Mathematiker Charles Babbage traf, der sie einlud, die von ihm erfundene „Differenzmaschine“ anzusehen, war sie hellauf begeistert. Die Maschine konnte selbstständig addieren und subtrahieren, doch Ada war klar, dass die Möglichkeiten damit noch lange nicht erschöpft waren. Sie träumte davon, dass eine solche Maschine eines Tages sogar Musik abspielen könnte, und ersann so die Idee eines modernen Computers. 1845 legte sie den ersten Algorithmus zur maschinellen Berechnung der Bernoulli-Zahlen vor und wird daher von vielen als erste Computerprogrammiererin der Welt gefeiert."
```
(Source: DWDS, Wort des Tages, "Algorithmus, der", 27.11.2021, URL: https://www.dwds.de/adt )


### Extract the graph edges from a dependency tree with SpaCy/Stanza/Trankit
- We assume that NodeIDs are numbers `[1,2,3,...]` starting with 1. 
  The NodeIDs are equivalent to the TokenIDs in Conll-U.
- An graph edge is a tuple `(ParentID, NodeID)`


Example, SpaCy:
```py
# load the SpaCy model
import de_dep_news_trf
model = de_dep_news_trf.load()
# extract the edges for each sentence
import node_distance as nd
all_edges, num_nodes = nd.extract_edges_from_spacy(corpus, model)
```

Example, stanza:
```py
# load the stanza model
import stanza
model = stanza.Pipeline(
    lang='de', processors='tokenize,mwt,pos,lemma,depparse',
    tokenize_pretokenized=False)
# extract the edges for each sentence
import node_distance as nd
all_edges, num_nodes = nd.extract_edges_from_stanza(corpus, model)
```

Example, trankit:
```py
# load the trankit model
import trankit
model = trankit.Pipeline(lang='german', gpu=False, cache_dir='./cache')
# extract the edges for each sentence
import node_distance as nd
all_edges, num_nodes = nd.extract_edges_from_trankit(corpus, model)
```

`num_nodes` with the number of tokens/nodes in each sentence.
`all_edges` contains lists of edges for each sentence, e.g.
```py
# Edges of the 3rd sentence
edges = all_edges[2]
# Edge between the 6th token/node and its parent node
edge = edges[6]
parent_id, node_id = edge
```

### Compute Shortest Paths between Nodes
Compute node distances and the corresponding token distances

```py
import node_distance as nd
nodedist, tokendist, indicies = nd.node_token_distances(all_edges, num_nodes, cutoff=25)
```

### Histograms as Features

The Distribution of node distances:
```py
import node_distance as nd
xobs, pdf, _ = nd.nodedist_distribution(nodedist, xmin=1, xmax=12)

import matplotlib.pyplot as plt
plt.bar(xobs, pdf);
plt.title("distribution of node distances");
plt.xlabel("node distance");
plt.ylabel("PDF");
plt.show();
```

Distribution of token distance vs node distance:
```py
import node_distance as nd
xobs, pdf, _ = nd.tokenvsnode_distribution(tokendist, nodedist, xmin=-5, xmax=15)

import matplotlib.pyplot as plt
plt.bar(xobs, pdf);
plt.title("Distribution of token distance vs node distance");
plt.xlabel("token distance minus node distance");
plt.ylabel("PDF");
plt.show();
```


## Appendix

### Installation
The `node-distance` [git repo](http://github.com/ulf1/node-distance) is available as [PyPi package](https://pypi.org/project/node-distance)

```sh
pip install node-distance
pip install git+ssh://git@github.com/ulf1/node-distance.git
```

### Install a virtual environment
It is recommended to install python packages into a seperate virtual environement. (If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
pip install -r requirements-demo.txt --no-cache-dir
```

The usage example and demo notebooks might require spacy, stanza and trankit to be installed. You should download the pretrained models beforehand, e.g. pretrained models for German:

```sh
python -m spacy download de_dep_news_trf
python -c "import stanza; stanza.download(lang='de')"
python -c "import trankit; trankit.Pipeline(lang='german', gpu=False, cache_dir='./cache')"
```

### Python commands

* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `PYTHONPATH=. pytest`

Publish

```sh
python setup.py sdist 
twine upload -r pypi dist/*
```

### Clean up 

```sh
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```

### Support
Please [open an issue](https://github.com/ulf1/node-distance/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/node-distance/compare/).

### Acknowledgements
The "Evidence" project was funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - [433249742](https://gepris.dfg.de/gepris/projekt/433249742) (GU 798/27-1; GE 1119/11-1).

### Maintenance
- till 31.Aug.2023 (v0.1.0) the code repository was maintained within the DFG project [433249742](https://gepris.dfg.de/gepris/projekt/433249742)
- since 01.Sep.2023 (v0.2.0) the code repository is maintained by Ulf Hamster.

### Citation
You can cite the following paper if you want to use this repository in your research work.

```
@inproceedings{hamster-2022-everybody,
    title = "Everybody likes short sentences - A Data Analysis for the Text Complexity {DE} Challenge 2022",
    author = "Hamster, Ulf A.",
    booktitle = "Proceedings of the GermEval 2022 Workshop on Text Complexity Assessment of German Text",
    month = sep,
    year = "2022",
    address = "Potsdam, Germany",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.germeval-1.2",
    pages = "10--14",
}
```
