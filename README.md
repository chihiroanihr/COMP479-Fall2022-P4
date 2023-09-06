# COMP479-Fall2022-P4

**Information Retrieval and Web Search** course project at Concordia University - assigned by Dr. _Sabine Bergler_.

## Overview

COMP479 Project (P4) which experiments with **web crawling**, **web scraping**, and **indexing** a collection of web documents. Subsequently, the indexed data is clustered using the **k-means** algorithm. Each resulting cluster is then assigned a sentiment score using **AFINN** - a script used for sentiment analysis.

For the original project outline (assigned by Dr. _Sabine Bergler_), click [here](/p4.pdf).

### Resources

- [Outline](/p4.pdf)
- [Demo](/deliverables/demo.pdf)
- [Report](/deliverables/report.pdf)

## Programming Language

### Built with Python

**Python>=3.8** is used as a programming language for this project due to its compatibility with natural language processing tasks, facilitated by the NLTK package.

## Dependencies

- beautifulsoup4
- scipy
- afinn
- scikit-learn
- TfidfVectorizer
- KMeans
- reppy
- urllib3

### Crawling Tool

- [**Spidy**](https://github.com/rivermont/spidy) (Refer to its documentation [here](/project/spider-docs))
