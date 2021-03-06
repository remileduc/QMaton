# QMaton
[![GitHub Super-Linter](https://github.com/remileduc/QMaton/actions/workflows/ci.yaml/badge.svg)](https://github.com/marketplace/actions/super-linter)

Cellular automaton easily customizable, with a fully functional UI interface (based on Qt)

## Dev

### Install requirements
The development has been done on Pyzo with MiniConda installed. In order to get the dependencies, you need to run the following:

```bash
conda install --file requirements.txt
```

### Setup Pyzo
To be able to run QMaton from Pyzo, you need to setup your Python shell in Pyzo, so it knows where are located the files we want to import.

To do so, you need to edit your shell configurations and put the following values:
- pythonPath: add the path to the `src` folder of QMaton (e.g. `D:\documents\projet\QMaton\src`
- startDir: this is the folder where you can select the files you want to write . load. This should point to the root folder of QMaton (e.g. `D:\documents\projet\QMaton`)
