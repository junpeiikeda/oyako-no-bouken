# おやこ の ぼうけん
2体のキャラを同時に動かしゴールを目指す２Dアクションゲームです。
そうさはキーボードのみで行います。

 
# EXPLANATION

![ゲーム開始時](./data/start.png "gamesover")
<br>[ゲーム開始画面]<br>
![ゲームオーバー](./data/gameover.gif "gamesover")
<br>ゲームオーバー：敵のレーザーに当たってしまうと負けてしまう！！<br>
![ゲームクリア](./data/clear.gif "gameclear")
<br>ゲームクリア：全員倒すとゲームクリア！<br>



 

 
# Requirement
 
"未来の射的（SHATEKI of FUTURE）"を動かすのに必要なライブラリなどを列挙する
 
* Python-3.7.19 or than later<br>
* tkinter-8.6.9<br>
* Pillow-8.3.2<br>


# Installation
 
Requirementで列挙したライブラリなどのインストール方法を説明する<br>
Anacondaの仮想環境の作成を推奨します。
```bash
conda create -n sof python=3.7.10 -y
conda activate sof
```
git がインストールされている場合
```bash
git clone https://github.com/Amenbo1219/SHATEKI-of-FUTURE.git
cd SHATEKI-of-FUTURE
```
gitがインストールされていない場合<br>
こちらからソースコードをダウンロードしてください。<br>
github:(https://github.com/Amenbo1219/SHATEKI-of-FUTURE)<br>
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


 
# Usage

* Python3.7.10以上がインストールされているものとする。
* main.py,crab.jpeg,cannon.jpegをフォルダ内部に配置する。
![ファイル配置図](./data/folderlist.svg "folderlist")

* 実行はmain.pyを実行
```bash
python main.py
```
 
# How to use?
敵の発射するレーザーを避けて、敵を攻撃しよう！<br>
<span style="font-size: 200%;color: red; ">たくさん敵を倒して高スコアを目指せ！！</span><br>
![操作方法](./data/rule.png "rule")<br>
移動→マウスドラッグ<br>
球発射→マウス左ボタン<br>
リスタート→ENTER


# Note
プレイ中にドラッグを解除しないでください。<br>
抜け出せないバグに遭遇した場合はENTERキーでリスタートしてください。
 
# Author
 
* 作成者 JP,あほたんけ,あめんぼ
* 所属　えぺ
* E-mail c0b20140d0@edu.teu.ac.jp
 
# SpecialThanks
* 元のコード<br>
作成者 ishikawa08様<br>
配布URL：(https://github.com/ishikawa08/invader_game)
* 画像引用<br>
無料素材サービス　株式会社シーマン様<br>
配布URL：(https://sozai.cman.jp/)
