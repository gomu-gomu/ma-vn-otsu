# Thresholding
### Otsu's Algorithm

Sample images are in the [assets](./assets) folder.
Source code is under the [src](./src/) folder

## Installation

Before running make sure you set up your environment:

```sh
python3 -m venv venv
source venv/bin/activate
```

Then install the dependencies:

```sh
pip3 install -r requirements.txt
```

## Usage

Web demo can be run with:

```sh
streamlit run src/__main__.py
```

Cli demo can be run with:

```sh
python3 src/cli.py assets/finger_print.jpg
```

## Docker

This demo comes in with a docker image that can be run with:

```sh
./scripts/run.sh
```

## Credits

- ESSAMADI Oussama
- ZOUIR Amine
- LOULID zakaria