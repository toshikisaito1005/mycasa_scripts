import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
plt.ioff()


### データを読み込む。
data = np.loadtxt("n6240_mom8_data.txt")
dist = data[:,0]
co10 = data[:,1]
co21 = data[:,2]


### 輝度温度のヒストグラム
# plotに向けての下準備です。
fig = plt.figure(figsize=(10,5))             # 図の大きさの設定
ax1 = fig.add_subplot(111)                   # これはおまじないです
ax1.grid(axis="x",linestyle='--')            # 図にグリッドを表示させます
plt.rcParams["font.size"] = 22               # 図中の文字サイズの設定
plt.subplots_adjust(bottom=0.15, left=0.12, right=0.95, top=0.9)  # 図の余白設定


# ヒストグラムの準備
bins = 100
historange = [0.001,25.]
hist_co10 = np.histogram(co10, bins = bins, range = historange)
hist_co21 = np.histogram(co21, bins = bins, range = historange)


ax1.step(np.delete(hist_co10[1],-1),
	      hist_co10[0]/float(sum(hist_co10[0])),
	      alpha=0.4,
	      lw = 4,
	      color = "blue",
	      label = "CO(1-0)")

ax1.step(np.delete(hist_co21[1],-1),
	      hist_co21[0]/float(sum(hist_co21[0])),
	      alpha=0.4,
	      lw = 4,
	      color = "red",
	      label = "CO(2-1)")

ax1.set_xlim(historange)                      # xの範囲の指定
ax1.set_ylim([0,0.2])                         # yの範囲の指定

ax1.set_ylabel("Normlized Count")
ax1.set_xlabel("Brightness Temperature (K)")

plt.legend()
plt.savefig("/Users/saito/Desktop/figure_histo_temp.png",dpi=300)


### 比のヒストグラム
# plotに向けての下準備です。
fig = plt.figure(figsize=(10,5))             # 図の大きさの設定
ax1 = fig.add_subplot(111)                   # これはおまじないです
ax1.grid(axis="x",linestyle='--')            # 図にグリッドを表示させます
plt.rcParams["font.size"] = 22               # 図中の文字サイズの設定
plt.subplots_adjust(bottom=0.15, left=0.12, right=0.95, top=0.9)  # 図の余白設定


# ヒストグラムの準備
bins = 100
historange = [0.001,4.]
hist_r21 = np.histogram(co21/co10, bins = bins, range = historange)


ax1.step(np.delete(hist_r21[1],-1),
	      hist_r21[0]/float(sum(hist_r21[0])),
	      alpha=0.4,
	      lw = 4,
	      color = "blue")

ax1.set_xlim(historange)                      # xの範囲の指定
ax1.set_ylim([0,0.1])                         # yの範囲の指定

ax1.set_ylabel("Normlized Count")
ax1.set_xlabel("Brightness Temperature Ratio")

plt.savefig("/Users/saito/Desktop/figure_histo_ratio.png",dpi=300)
