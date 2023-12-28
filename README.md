<h1 align="center">gpx-learning</h1>

<div align="center">

Use TensorFlow to generate similar gpx-format routes.

<a title="hits" target="_blank" href="https://github.com/stack-all/gpx-learning"><img src="https://hits.b3log.org/stack-all/gpx-learning.svg" ></a> ![GitHub contributors](https://img.shields.io/github/contributors/stack-all/gpx-learning) ![GitHub License](https://img.shields.io/github/license/stack-all/gpx-learning)

English &nbsp;&nbsp;|&nbsp;&nbsp; [简体中文](README_ZH.md)

</div>

## ✨ Features

- 🤖 Use Deep-Learning to simulate almost real routes!

## 🔧 Usage

Just install dependencies and put GPX-format samples in `input` folder, run the `python3 main.py` script and follow the interactive guide, to generate the routes in `output` folder.

## 🖥 Command Line Interface

Install dependencies：

```shell
pip3 install -r requirements.txt
```

To generate GPX routes using the script, you can use the following command line options:

- `-ni`, `--no-interaction`: Run the script without interactive input, using default values.
- `-e`, `--epochs`: Specify the number of epochs to train the model (default is 100).
- `-p`, `--num-points`: Set the number of points to generate in each GPX route (default is 100).
- `-n`, `--num-files`: Define the number of GPX files to generate (default is 10).

Example usage:

```shell
python3 main.py --no-interaction --epochs 200 --num-points 150 --num-files 20
```

It means to generate 20 GPX files with 200 epochs, each with 150 points.

## 🙏 Credit

- [`GPT4`](https://chat.openai.com), the powerful AI language model.
- [`Codeium`](https://codeium.com/), free AI code assistant.
- [`TensorFlow`](https://www.tensorflow.org/), an open source machine learning framework.
- [`VSCodium`](https://github.com/VSCodium/vscodium), a community-driven and freely-licensed binary distribution of VS Code.
