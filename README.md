## このリポジトリについて
ライントレーサーのシミュレーション

## 実行方法

```bash
cd
git clone https://github.com/ku-gcl/gcl-line-tracer.git
```

```bash
cd ~/gcl-line-tracer/python
python mouse_motor_control.py
```




## 各ファイルの説明
| No. | ファイル                                                | 説明                                                            |
| --- | ------------------------------------------------------- | --------------------------------------------------------------- |
| 1   | [lineTracerReadImage.m](matlab/lineTracerReadImage.m) | 画像を読み込んでライントレースする。パワーポイントで白と黒でできたコースマップを用意してその画像の座標を指定してピクセル値を読み取る (センサの代わり)。その値と目標値の差の割合から偏差を求め、次のループで加える入力とする。                        |
| 2   | [lineTracerMouse.m](matlab/lineTracerMouse.m)               | [ライントレースロボットのシミュレーション](https://rikei-tawamure.com/entry/2020/07/24/162236)のPythonコードをMATLABに変換したコード                     |




<!-- **LineTracerReadImage.mの修正するべき事項**
コースマップの修正
様々な諸元値とゲイン値の修正
P制御→PID制御へ拡張 -->
