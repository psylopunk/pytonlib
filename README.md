# 🌐 Introduction

### Introduction

This library allows you to work with the [TON blockchain](https://ton.org) API from Python.

**Features**:

* Creating and importing wallet
* Getting wallets balance
* Getting transactions of any wallet
* Transfer coins
* Executing methods of smart-contracts
* Transfer NFT

[![PyPI version](https://badge.fury.io/py/ton.svg)](https://badge.fury.io/py/ton) ![visitors](https://visitor-badge.glitch.me/badge?page\_id=psylopunk.pytonlib.readme\&left\_color=gray\&right\_color=red) ![](https://pepy.tech/badge/ton) [![](https://img.shields.io/badge/%F0%9F%92%8E-TON-green)](https://ton.org)

### How to install:

```bash
pip install ton
```

If you have an _illegal instruction_ error then you need to build libtonlibjson by yourself:

```bash
git clone https://github.com/psylopunk/ton && cd ton
chmod +x build_tonlib.sh && ./build_tonlib.sh # docker is needed
```

#### Getting started

Examples will give a general look at the library. They describe almost all supported methods, but in addition, below you can see each method in detail. To make a custom request to `libtonlibjson`, check out list of available methods and execute it using `client.execute`

#### [More documentation here](developer-interface.md) <a href="#documentation" id="documentation"></a>

#### Troubleshooting

Found a bug? Or just improvments? -- Read more about this in [Troubleshooting](troubleshooting.md)

**Donate**

* BTC – 192gK2df3izkpaNgcMbfEDrLgoofyjjfeC
* TON – [EQCl1Ug9ZT9ZfGyFH9l4q-bqaUy6kyOzVPmrk7bivmVKJRRZ](ton://transfer/EQCl1Ug9ZT9ZfGyFH9l4q-bqaUy6kyOzVPmrk7bivmVKJRRZ)
