<p align="center">
    <img src="docs/assets/logo.svg" alt="MQPy Logo" width="200" height="200">
</p>

<p align="center">
    <img src="https://img.shields.io/pypi/dm/mqpy" alt="PyPI - Downloads">
    <img src="https://img.shields.io/pypi/v/mqpy" alt="PyPI">
    <img src="https://img.shields.io/pypi/wheel/mqpy" alt="PyPI - Wheel">
    <img src="https://img.shields.io/pypi/l/mqpy" alt="PyPI - License">
</p>

<h1 align="center">Mql5-Python-Integration (MQPy)</h1>

<p align="center"><strong>Current Version: v0.6.9</strong></p>

Welcome to the Mql5-Python-Integration project! This project facilitates the integration between MetaTrader 5 (Mql5) and Python, allowing for efficient algorithmic trading strategies.

## ⚠️ TRADING RISK WARNING

**IMPORTANT: Trading involves substantial risk of loss and is not suitable for all investors.**

- Always use a **demo account** with fake money when testing strategies
- MQPy is provided for **educational purposes only**
- Past performance is not indicative of future results
- Never trade with money you cannot afford to lose
- The developers are not responsible for any financial losses incurred from using this software

## Table of Contents

- [⚠️ TRADING RISK WARNING](#️-trading-risk-warning)
- [Table of Contents](#table-of-contents)
- [Project Update: Changes in Progress](#project-update-changes-in-progress)
- [Installation](#installation)
- [Usage](#usage)
  - [Generate the File](#generate-the-file)
- [Missing Features/Good Practice](#missing-featuresgood-practice)
  - [Delicate Metatrader5 Environment](#delicate-metatrader5-environment)
  - [Alternative Libraries](#alternative-libraries)

## Project Update: Changes in Progress

🚧 **Work in Progress: v0.6.9**
This project is currently undergoing significant changes and improvements. The latest version is v0.6.0, and various enhancements are being made to provide a more robust and user-friendly experience.

📌 **Previous Version: v0.5.0**
To access the code for the previous version, you can check it out at [v0.5.0](https://github.com/Joaopeuko/Mql5-Python-Integration/releases/tag/v0.5.0).

## Installation

**Note: In order to use this package, you need to have MetaTrader 5 installed on a Windows system with Python 3.8 or later.**

To install the package, you can use the following command:

```bash
pip install mqpy
```

Make sure to fulfill the prerequisites mentioned above before attempting to use the Mql5-Python-Integration (MQPy) package.

## Usage

Basic Usage

Once installed, you can use the mqpy command to generate the boilerplate code.

### Generate the File

To create a template file for a trading strategy, use the following command:

```bash
mqpy --symbol <Symbol> --file_name <File Name>
```

Please change `<Symbol>` and `<File Name>` to the desired values. For example:

```bash
mqpy --symbol EURUSD --file_name demo
```

## Missing Features/Good Practice

This library has been in existence for several years and was designed to be simple and straightforward. While there are plans to enhance it with features such as logging and other components to improve its overall quality, there are considerations specific to the nature of the Metatrader5 library.

### Delicate Metatrader5 Environment

Metatrader5 operates within a highly restrictive environment, and certain practices that may be considered best practices in other contexts might cause trouble for newcomers in software development, which is the main focus of this library. For the sake of simplicity and ease of use, the library currently retains some practices that may not align with conventional best practices.

### Alternative Libraries

For users seeking a more advanced library with a similar concept, consider exploring the following alternative:

[metatrader5EasyT](https://github.com/Joaopeuko/metatrader5EasyT): A more advanced library that aligns with best practices while providing a similar user-friendly approach. It is also available on PyPI.
