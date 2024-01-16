[English](README_en.md)

# ハウスミュージックの楽曲構成の分析

![image](preview.png)

## 概要

本プロジェクトは、ハウスミュージックにおける楽曲構成の決定要因や法則性を解明することを目的に分析を行うための環境である。本プロジェクトに関する論文は[こちら](https://github.com/Jtwulf/papers)。

## リポジトリの構成

```
.
├── Dockerfile          # Omnizart用
├── docker-compose.yml  # Omnizart用
├── requirements.txt    # Pythonプログラムに必要なライブラリ
├── NATTEN/             # All-In-Oneの利用に必要なモデル
├── data/               # 実験用データ
├── images/             # 実験結果
├── notebook/           # 実験用プログラムのjupyter notebook環境
└── src/                # 実験用プログラム
    └── scripts/        # 各種スクリプト
```

`data/`は著作権の都合で一部のみpublicにしている。

## 準備・前提条件

`src/`のプログラムを実行するには、必要なライブラリをインストールする必要がある。

```
pip install -r requirements.txt
```

もしくは、`src/`と同じ内容のプログラムが`notebook/experiments.ipynb`に存在する。

実験用データは`data/`に適宜配置する必要がある。

本プロジェクトでは、ハウスミュージックの楽曲構成のセクションとして以下の4つを定義している。


| Section | Description                       |
|---------|-----------------------------------|
| Intro   | 曲の導入部分                        |
| Drop    | 曲における盛り上がり部分             |
| Break   | 曲の盛り上がり部分以外の部分          |
| Outro   | 曲の終結部分                        |

## 各プログラムの説明

### [experiment1](src/experiment1.py)

各セクションと周波数特徴量の関連性の分析

#### プログラムの流れ

1. All-In-Oneを用いて楽曲のセグメンテーション情報を取得
2. 楽曲から周波数特徴量(Spectral Centorid)を取得
3. セグメンテーション情報から各セクションの周波数特徴量の平均値を可視化

#### 結果

<p float="left">
  <img src="images/experiment1_bar_prod.png" width="300" />
  <img src="images/experiment1_box_prod.png" width="300" /> 
  <img src="images/experiment1_violin_prod.png" width="300" />
</p>

---

### [experiment2](src/experiment2.py)

各パートにおける各セクションと周波数特徴量の関連性の分析

#### プログラムの流れ

1. All-In-Oneを用いて楽曲のセグメンテーション情報を取得
2. Demucsで楽曲を4パート(drums, bass, other, vocals)に音源分離
3. RMSが閾値を下回る音源区間を除外
4. 楽曲から周波数特徴量(Spectral Centorid)を取得
5. セグメンテーション情報から各パートごとの各セクションの周波数特徴量の平均値を可視化

#### 結果

<p float="left">
  <img src="images/experiment2_combined_bar_prod.png" width="300" />
  <img src="images/experiment2_combined_box_prod.png" width="300" /> 
  <img src="images/experiment2_combined_violin_prod.png" width="300" />
</p>

---

### [experiment2ex](src/experiment2ex.py)

experiment2における各パートの有効時間を調査

#### プログラムの流れ

1. All-In-Oneを用いて楽曲のセグメンテーション情報を取得
2. Demucsで楽曲を4パート(drums, bass, other, vocals)に音源分離
3. RMSが閾値を上回る音源区間の長さ(有効時間)を取得
4. 各パートにおける各セクションごとの有効時間を可視化

#### 結果

<p float="left">
  <img src="images/experiment2ex.png" width="300" />
</p>

---

### [experiment2ex2](src/experiment2ex2.py)

各パートにおける各セクションと音圧特徴量の関連性の調査

#### プログラムの流れ

1. All-In-Oneを用いて楽曲のセグメンテーション情報を取得
2. Demucsで楽曲を4パート(drums, bass, other, vocals)に音源分離
3. 楽曲から音圧特徴量(RMS)を取得
4. セグメンテーション情報から各パートごとの各セクションの音圧特徴量の平均値を可視化

#### 結果

<p float="left">
  <img src="images/experiment2ex2_combined_bar_prod.png" width="300" />
  <img src="images/experiment2ex2_combined_box_prod.png" width="300" /> 
  <img src="images/experiment2ex2_combined_violin_prod.png" width="300" />
</p>

---

### [experiment3](src/experiment3.py)

各セクションにおける各パートの音圧バランスの傾向を分析

#### プログラムの流れ

1. All-In-Oneを用いて楽曲のセグメンテーション情報を取得
2. Demucsで楽曲を3パート(drums, bass, other+vocals)に音源分離
3. 楽曲から音圧特徴量(RMS)を取得
4. 3パートのセクションごとの音圧特徴量のバランスを3次元空間にプロットし可視化

#### 結果

<p float="left">
  <img src="images/experiment3_combined_prod.png" width="300" />
</p>

---

### [experiment4](src/experiment4.py)

各セクションのドラムの要素の傾向を分析

#### プログラムの流れ

1. Omnizartを用いて音源からドラムMIDIを取得
2. 各セクションごとの各種ドラム要素の個数を集計し可視化

#### 結果

<p float="left">
  <img src="images/experiment4_drum_count.png" width="300" />
</p>

---

### [experiment4ex](src/experiment4ex.py)

各ドラム要素の発音時刻の傾向を分析

#### プログラムの流れ

1. Omnizartを用いて音源からドラムMIDIを取得
2. 各セクションごとの各種ドラム要素の個数とその時刻を集計
3. 各ドラム要素の発音時刻を折れ線グラフからなるスパゲッティプロットとして可視化

#### 結果

<p float="left">
  <img src="images/experiment4ex_Acoustic_Bass_drum_prod.png" width="300" />
  <img src="images/experiment4ex_Acoustic_Snare_prod.png" width="300" />
  <img src="images/experiment4ex_Closed_Hi-Hat_prod.png" width="300" />
</p>

---

### [experiment4ex2](src/experiment4ex2.py)

各ドラム要素の発音時刻の傾向を分析

#### プログラムの流れ

1. Omnizartを用いて音源からドラムMIDIを取得
2. All-In-Oneのテンポ推定結果を用いて楽曲の8小節の長さを計算
3. 各セクションごとの各種ドラム要素の8小節ごとの個数を集計
4. 各ドラム要素の8小節ごとの個数を折れ線グラフからなるスパゲッティプロットとして可視化

#### 結果

<p float="left">
  <img src="images/experiment4ex2_Acoustic_Bass_drum_prod.png" width="300" />
  <img src="images/experiment4ex2_Acoustic_Snare_prod.png" width="300" />
  <img src="images/experiment4ex2_Closed_Hi-Hat_prod.png" width="300" />
</p>

---

### [experiment5](src/experiment5.py)

ドラムパターンの変化とセクションの変化の相関性について分析

#### プログラムの流れ

1. Omnizartを用いて音源からドラムMIDIを取得
2. All-In-Oneのセグメンテーション情報からセクションの変化タイミングを取得
3. ドラムMIDIにおける全ドラムイベントの間隔の長さを取得し、その標準偏差を閾値として、閾値を超えるドラムイベントの間隔がある場合をドラムパターンの変化として検出
4. ドラムパターンの変化タイミングとセクションの変化タイミングの一致率をそれぞれが分母である場合について計算
5. 一致率を可視化

#### 結果

ドラムパターンの変化を分母とした確率

<p float="left">
  <img src="images/experiment5_distribution_drum_based_prod.png" width="300" />
  <img src="images/experiment5_timeseries_drum_based_prod.png" width="300" />
</p>

セクションの変化を分母とした確率

<p float="left">
  <img src="images/experiment5_distribution_section_based_prod.png" width="300" />
  <img src="images/experiment5_timeseries_section_based_prod.png" width="300" />
</p>

## 関連 (Webs of Interest)

[All-In-One](https://github.com/mir-aidj/all-in-one)

[Demucs](https://github.com/facebookresearch/demucs)

[Omnizart](https://github.com/Music-and-Culture-Technology-Lab/omnizart)

## 著者 (Authors)

Justin Wulf - wulf@kthrlab.jp
