# FAIRsoft 

Library for the aggregation of Life Sciences software metadata and FAIR evaluation.


## Installation 
Install using [pip](https://pip.pypa.io/en/stable/):
```
pip install FAIRsoft
``` 

### Requirements 
In order to use the Bioconda, Galaxy Toolshed and repositories (GitHub and Bitbucket) metadata importers, the following tools need to be installed:

- [bioconda-utils](https://github.com/bioconda/bioconda-utils) is required by the bioconda importer. 

    bioconda-utils is a bioconda package and thus requires [Conda](https://docs.conda.io/projects/conda/en/latest/index.html). 

    ❗️ The large size of bioconda-utils package can cause Conda to crash during the installation process. Using [Mamba](https://github.com/mamba-org/mamb) instead of Conda prevents this problem. 

    ❗️ bioconda-utils requires Python 3.7 or lower. Simulating a compatible platform might be necessary. To do so, use the following commands: 
    ```sh 
    # create the environment
    mamba create -n myenv

    # activate the environment
    conda activate myenv
    
    # before installing anything in the environment, set the usage of x86_64 architecture
    conda config --env --set subdir osx-64
    ```

 - [opeb-enrichers/repoEnricher](https://github.com/inab/opeb-enrichers) is required by the Source Code Respositories importer.

 - [AnyStyle](https://github.com/inukshuk/anystyle) is required by the Galaxy Toolshed importer.


## Usage 

Configuration is done through environment variables. Those refering to the database where extracted and/or proccessd software metadata is stored are: 

| Name             | Description | Default | Notes |
|------------------|-------------|---------|-------|
| DBHOST       |  Host of database where output will be pushed |   `localhost`        | |
| DBPORT       |  Port of database where output will be pushed |   `27017`            | |
| DB         |  Name of database where output will be pushed |   `observatory`      | |
| ALAMBIQUE |  Name of collection where importers output will be stored  |   `alambique`        | Needed for importation only |
| PRETOOLS      |  Name of collection where output of transformation step (harmonized version of data in ALAMBIQUE collection) will be pushed. It is also the collection from which the following step, integration, will use as source of input data |   `pretools`    | Needed for transformation and integration |
| TOOLS      |  Name of collection where output of integration  will be stored. This is the final collection os the porccess. Thus, it is the collection that can be use for the evaluation of FAIRness, calculation of statictics, etc |   `tools`        |  Needed for integration  |


### Data extraction

Data extraction is done through the execution of importers. Each importer is responsible for extracting metadata from a specific source. 

All importers require the environment variables DBHOST, DBPORT, DB, ALAMBIQUE and PRETOOLS (previously explained) to be set.

#### Bioconda importer

Configuration: 

| Name             | Description | Default | Notes |
|------------------|-------------|---------|-------|
| RECIPES_PATH | Path to bioconda recipes (from [repository](https://github.com/bioconda/bioconda-recipes/recipes)) | `./bioconda-recipes/recipes` | Only required when running natively AND if the location of bioconda recipes changes|

To run the importer use: 

```sh
FAIRsoft_import_bioconda -e=[env-file] -l=[log-level] -d=[log-directory]
``` 
- `-e`/`--env-file` is optional. It specifies the path to the file containing the environment variables. Default is `.env`.
- `-l`/`--loglevel` is optional. It can be `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`. Default is `INFO`.
- `-d`/`--logdir`/ is optional. It specifies the path to the directory where the logs will be written. Default is `./logs`.

#### Galaxy Toolshed importer

Configuration:

| Name             | Description | Default | Notes |
|------------------|-------------|---------|-------|
| GALAXY_METADATA | Path to metadata extracted from Galaxy Metadata. This JSON file, automatically generated after the extraction of repositories metadata, constains identifiers that are necessary for the download of repositories, which contain the recipes.  | `./data/galaxy_metadata.json` | ||

To run the importer use: 

```sh
FAIRsoft_import_toolshed -e=[env-file] -l=[log-level] -d=[log-directory]
``` 
- `-e`/`--env-file` is optional. It specifies the path to the file containing the environment variables. Default is `.env`.
- `-l`/`--loglevel` is optional. It can be `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`. Default is `INFO`.
- `-d`/`--logdir`/ is optional. It specifies the path to the directory where the logs will be written. Default is `./logs`.

#### Source Code Repositories (GitHub and Bitbucket) importer

This importer is actually and "enricher" of tools in OpenEBench Tools API. It only extracts metadata from the repositories associted to those tools. It requires the following environment variables to be set:

| Name             | Description | Default | Notes |
|------------------|-------------|---------|-------|
| REPOENRICHER_PATH | Path to [*repoEnricher*](https://github.com/inab/opeb-enrichers/repoEnricher) program. | `./opeb-enrichers/repoEnricher/repoEnricher.pl`      |  |

In addition, it requires a file containing the credentials for the GitHub and BitBucket APIs: `config.ini`. This file must be palced in the REPOENRICHER_PATH. Details [here](https://github.com/inab/opeb-enrichers/tree/master/repoEnricher/README.md)

To run the importer use: 
    
```sh
FAIRsoft_import_repositories
``` 

#### OpenEBench Tools importer

Configuration:

| Name             | Description | Default | Notes |
|------------------|-------------|---------|-------|
| URL_OPEB_TOOLS | URL to OpenEBench Tools API | `https://openebench.bsc.es/monitor/tool` | |

To use the importer, run the following command:

```sh
FAIRsoft_import_opeb_tools -e=[env-file] -l=[log-level] -d=[log-directory]
```
- `-e`/`--env-file` is optional. It specifies the path to the file containing the environment variables. Default is `.env`.
- `-l`/`--loglevel` is optional. It can be `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`. Default is `INFO`.
- `-d`/`--logdir`/ is optional. It specifies the path to the directory where the logs will be written. Default is `./logs`.


#### OpenEBench Metrics importer

Configuration:

| Name             | Description | Default | Notes |
|------------------|-------------|---------|-------|
| URL_OPEB_METRICS | URL to OpenEBench Metrics API | `https://openebench.bsc.es/monitor/metrics/` | |

To use the importer run:
    
```sh
FAIRsoft_import_opeb_metrics -e=[env-file] -l=[log-level] -d=[log-directory]
```
- `-e`/`--env-file` is optional. It specifies the path to the file containing the environment variables. Default is `.env`.
- `-l`/`--loglevel` is optional. It can be `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`. Default is `INFO`.
- `-d`/`--logdir`/ is optional. It specifies the path to the directory where the logs will be written. Default is `./logs`.


#### Bioconductor importer

Configuration: 

| Name             | Description | Default | Notes |
|------------------|-------------|---------|-------|
| URL_BIOCONDUCTOR | Path to file containing the URLs of the bioconductor packages to be scraped. | `./data/bioconductor_opeb.txt` |  |

To run the importer use: 

```sh
FAIRsoft_import_bioconductor -e=[env-file] -l=[log-level] -d=[log-directory]
```
- `-e`/`--env-file` is optional. It specifies the path to the file containing the environment variables. Default is `.env`.
- `-l`/`--loglevel` is optional. It can be `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`. Default is `INFO`.
- `-d`/`--logdir`/ is optional. It specifies the path to the directory where the logs will be written. Default is `./logs`.

#### SourceForge importer

Configuration:

| Name             | Description | Default | Notes |
|------------------|-------------|---------|-------|
| URL_SOURCEFORGE_PACKAGES | URL to SourceForge packages of our interest | `https://sourceforge.net/directory/science-engineering/bioinformatics/` | |

To run the importer use: 

```sh
FAIRsoft_import_sourceforge -e=[env-file] -l=[log-level] -d=[log-directory]
```
- `-e`/`--env-file` is optional. It specifies the path to the file containing the environment variables. Default is `.env`.
- `-l`/`--loglevel` is optional. It can be `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`. Default is `INFO`.
- `-d`/`--logdir`/ is optional. It specifies the path to the directory where the logs will be written. Default is `./logs`.

## Data transformation 

Data transformation requires the environment variables DBHOST, DBPORT, DB, ALAMBIQUE and PRETOOLS (previously explained) to be set.

Execute the following command to transform data: 

```sh
FAIRsoft_transform --env-file=[env-file] -l=[log-level]
``` 
- `-e`/`--env-file` is optional. It specifies the path to the file containing the environment variables. Default is `.env`.
- `-l`/`--loglevel` is optional. It can be `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`. Default is `INFO`.

## Data integration
Data integration requires the environment variables DBHOST, DBPORT, DB, PRETOOLS and TOOLS (previously explained) to be set.

Execute the following command to integrate data: 

```sh
FAIRsoft_integrate --env-file=[env-file] -l=[log-level]
```
- `-e`/`--env-file` is optional. It specifies the path to the file containing the environment variables. Default is `.env`.
- `-l`/`--loglevel` is optional. It can be `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`. Default is `INFO`.

### FAIRsoft indicators evaluation 
FAIRness indicators evaluation requires the environment variables DBHOST, DBPORT, DB and TOOLS (previously explained) to be set. 
Additionally, FAIR is required: 
| Name             | Description | Default | Notes |
|------------------|-------------|---------|-------|
| FAIR | Name of collection where FAIRness indicators will be stored | `fair` | | 

To run the evaluation use: 

```sh
FAIRsoft_indicators_evaluation --env-file=[env-file] -l=[log-level]
```