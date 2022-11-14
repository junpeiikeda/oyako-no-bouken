# おやこ の ぼうけん
2体のキャラを同時に動かしゴールを目指す２Dアクションゲームです。
操作はキーボードのみで行います。
<br>
 
# EXPLANATION

![ゲーム開始時](./data/start.png "gamesover")
<br>[ゲーム開始画面]<br>
<br>
プレーヤーは親となり子供とともにゴールを目指します。<br>
こどもは親であるプレーヤーと同じ動きをしますが、移動速度やジャンプ力などが異なるため常にこどもに気を配りながら進みましょう。<br>
親子のどちらかが穴に落ちるか、画面上からランダムに落ちてくるやりに触たらゲームオーバーです。<br>
プレーヤーとこどもの両方が画面右上にあるゴールにたどり通ことができればゲームクリアとなります。<br>
<br>
<br>
スタート画面では、プレー難易度を選択することができます。キーボード数字ボタンで難易度選択を行ってください。
難易度によってランダム生成される槍の頻度と数が増減します。<br>
ボタンが押された時点でゲーム開始となります。
<br>
 
# Requirement
 
ゲームをプレイするにあたって必要なライブラリなどを列挙する
 
* Python-3.7.19 or than later<br>
* tkinter-8.6.9<br>
* Pillow-8.3.2<br>
<br>

# Installation
 
Requirementで列挙したライブラリなどのインストール方法を説明する<br>
Anacondaの仮想環境の作成を推奨します。
```bash
conda create -n sof python=3.7.10 -y
conda activate sof
```
git がインストールされている場合
```bash
git clone https://github.com/junpeiikeda/oyako-no-bouken.git
cd oyako-no-bouken
```
gitがインストールされていない場合<br>
こちらからソースコードをダウンロードしてください。<br>
github:(https://github.com/junpeiikeda/oyako-no-bouken)<br>
利用プラグインのインストール
```bash
cd Instration
pip install -r requirements.txt
cd ..
``` 
or
```bash
pip install Pillow
```
<br>
 
# Usage

* Python3.7.10以上がインストールされているものとする。

* 実行はgame.pyを実行
```bash
python game.py
```
 <br>
 
# How to use?
移動...キーボードカーソルキー　→↓←<br>
ジャンプ...キーボードカーソルキー↑
 <br>
 
# Author
 
* 作成者 池田純平
* E-mail c0b20010c8@edu.teu.ac.jp
