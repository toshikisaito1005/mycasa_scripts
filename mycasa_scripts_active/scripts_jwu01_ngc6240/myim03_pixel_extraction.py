import math
import numpy as np

imageco10 = "n6240_co10_moment8_Kelvin.image"
imageco21 = "n6240_co21_moment8_Kelvin.image"

### 中心からの距離を計算する関数を作る。
def distance(x, y):
    ra_cnt = 253.245   # degree unit, ngc6240の中心のR.A.
    dec_cnt = 2.40111  # degree unit, ngc6240の中心のDeclination
    scale = 0.48       # 1 arcsec = 0.48 kpc
    x_new = x - ra_cnt
    y_new = y - dec_cnt
    r = np.sqrt(x_new**2 + y_new**2) * 3600 * scale
    return r

### imageの縦横のピクセル数を知る。
length_x = imhead(imageco10,mode="list")["shape"][0] - 1
length_y = imhead(imageco10,mode="list")["shape"][1] - 1

### ピクセルの値を取ってくる領域をボックスで指定する。今回は全ピクセルです。
box = "0,0,"+str(length_x)+","+str(length_y)

### CASA task imvalでピクセル毎の値を取ってくる。
valueco10_tmp = imval(imageco10,box=box)["data"]
valueco10 = valueco10_tmp.flatten()

### CO(2-1)も同様。
valueco21_tmp = imval(imageco21,box=box)["data"]
valueco21 = valueco21_tmp.flatten()

### CO(1-0) and/or CO(2-1)の値が0のpixelを省く。
cut_zero = np.where((valueco10 > 0) & (valueco21 > 0))
valueco10_cut = valueco10[cut_zero]
valueco21_cut = valueco21[cut_zero]

### 座標を中心からの距離に変換する。
# まずR.A.を読み込む。
valuera_tmp = imval(imageco10,box=box)["coords"][:,:,0] * 180 / np.pi
valuera_tmp2 = valuera_tmp.flatten()
valuera_cut = valuera_tmp2[cut_zero]

# そしてDeclinationを読み込む。
valuedec_tmp = imval(imageco10,box=box)["coords"][:,:,1] * 180 / np.pi
valuedec_tmp2 = valuedec_tmp.flatten()
valuedec_cut = valuedec_tmp2[cut_zero]

# 距離を計算する関数で距離を各ピクセルの中心からの距離を算出する。
valuedist_cut = distance(valuera_cut, valuedec_cut)

# txtに保存する。
datatable = np.c_[valuedist_cut,valueco10_cut,valueco21_cut]
np.savetxt("n6240_mom8_data.txt",datatable)
