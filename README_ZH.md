<h1 align="center">gpx-learning</h1>

<div align="center">

使用 TensorFlow 来学习生成相似的 GPX 格式路线！

<a title="点击量" target="_blank" href="https://github.com/stack-all/gpx-learning"><img src="https://hits.b3log.org/stack-all/gpx-learning.svg" ></a> ![GitHub 贡献者](https://img.shields.io/github/contributors/stack-all/gpx-learning) ![GitHub 许可证](https://img.shields.io/github/license/stack-all/gpx-learning)

[English](README.md) &nbsp;&nbsp;|&nbsp;&nbsp; 简体中文

</div>

## ✨ 特点

- 🤖 使用深度学习模拟近乎真实的路线！

## 🔧 使用方法

只需安装依赖项后将 GPX 格式样本放入 `input` 文件夹中，运行 `python3 main.py` 并按照交互式输入相应值，即可在 `output` 文件夹中找到生成路线。

## 🖥 命令行参数

安装依赖项：

```shell
pip3 install -r requirements.txt
```

要使用命令行生成 GPX 路线，您可以使用以下命令行选项：

- `-ni`, `--no-interaction`：不使用交互式运行并使用默认值。
- `-e`, `--epochs`：指定训练模型的迭代次数（默认是 100）。
- `-p`, `--num-points`：设置生成的每个 GPX 文件中包含的点数（默认是 100）。
- `-n`, `--num-files`：定义要生成的 GPX 文件数量（默认是 10）。

示例用法：

```shell
python3 main.py --no-interaction --epochs 200 --num-points 150 --num-files 20
```

它表示生成20个GPX文件，迭代次数 200 次，每个文件中包含 150 个点。

## 🙏 致谢

- [`GPT4`](https://chat.openai.com)，强大的 AI 大模型。
- [`Codeium`](https://codeium.com/)，免费的 AI 编程助手
- [`TensorFlow`](https://www.tensorflow.org/)，开源的机器学习框架。
- [`VSCodium`](https://github.com/VSCodium/vscodium)，由社区驱动的 VSCode 自由分发版。
