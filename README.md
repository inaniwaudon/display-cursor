# display-cursor

マルチディスプレイ環境にて，今見ている画面にポインタを移動させる Python スクリプトです（アイデア自体は既に存在するものです[^existing]）．頭部方向（頭の向き）を基に角度を推定します．

[^existing]: https://help.mirametrix.com/hc/ja/articles/360004520211-%E3%82%B9%E3%83%9E%E3%83%BC%E3%83%88%E3%83%9D%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%BC%E3%81%A8%E3%81%AF

## 実行手順

```bash
pip install -r requirements.txt
python main.py

# 動作確認用（カメラ画像を表示します）
python main.py --frame true
```

- スクリプト起動時の顔の向きが基準になります．基準点が検出された段階でコマンドラインに Deletection of reference point is completed と表示されます．
- メインディスプレイの上にサブディスプレイが設置される状況を想定しているため，ピッチ（y 軸の角度）のみで判断しています．閾値は main.py 内の `PITCH_THRESHOLD` を調整してください．
- スクリプトを終了させる場合は Ctrl + C で終了させてください．

## ライセンス

本スクリプトはパブリックドメインとします．

同梱する shape_predictor_68_face_landmarks.dat はパブリックドメインとして公開されていますが，商用利用が制限される可能性がある点に注意してください[^public]．

[^public]: https://github.com/davisking/dlib-models/blob/master/README.md
