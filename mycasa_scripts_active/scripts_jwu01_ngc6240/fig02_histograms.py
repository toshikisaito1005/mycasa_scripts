import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
plt.ioff()


### 重みつけm中央値を計算する関数。
def weighted_median(data, weights):
    """
    Args:
        data (list or numpy.array): data
        weights (list or numpy.array): weights
    """
    data, weights = np.array(data).squeeze(), np.array(weights).squeeze()
    s_data, s_weights = map(np.array, zip(*sorted(zip(data, weights))))
    midpoint = 0.5 * sum(s_weights)
    if any(weights > midpoint):
        w_median = (data[weights == np.max(weights)])[0]
    else:
        cs_weights = np.cumsum(s_weights)
        idx = np.where(cs_weights <= midpoint)[0][-1]
        if cs_weights[idx] == midpoint:
            w_median = np.mean(s_data[idx:idx+2])
        else:
            w_median = s_data[idx+1]

    return w_median


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
plt.rcParams["font.size"] = 20               # 図中の文字サイズの設定
plt.subplots_adjust(bottom=0.15, left=0.12, right=0.95, top=0.9)  # 図の余白設定


# ヒストグラムの準備
bins = 80
historange = [0.001,25.]
hist_co10 = np.histogram(co10, bins = bins, range = historange)
hist_co21 = np.histogram(co21, bins = bins, range = historange)


ax1.step(np.delete(hist_co10[1],-1),
	      hist_co10[0]/float(sum(hist_co10[0])),
	      alpha=0.4,
	      lw = 2,
	      color = "blue",
	      label = "CO(1-0)")

ax1.step(np.delete(hist_co21[1],-1),
	      hist_co21[0]/float(sum(hist_co21[0])),
	      alpha=0.4,
	      lw = 2,
	      color = "red",
	      label = "CO(2-1)")

ax1.set_xlim(historange)                     # xの範囲の指定
ax1.set_ylim([0,0.25])                       # yの範囲の指定

ax1.set_ylabel("Normlized Count")
ax1.set_xlabel("Brightness Temperature (K)")

plt.legend()
plt.savefig("/Users/saito/Desktop/figure_histo_temp.png",dpi=300)


### 比のヒストグラム
# plotに向けての下準備です。
fig = plt.figure(figsize=(10,5))             # 図の大きさの設定
ax1 = fig.add_subplot(111)                   # これはおまじないです
ax1.grid(axis="x",linestyle='--')            # 図にグリッドを表示させます
plt.rcParams["font.size"] = 20               # 図中の文字サイズの設定
plt.subplots_adjust(bottom=0.15, left=0.12, right=0.95, top=0.9)  # 図の余白設定


# ヒストグラムの準備
bins = 80
historange = [0.001,4.]

hist_r21 = np.histogram(co21/co10, bins = bins, range = historange)
hist_r21_wco10 = np.histogram(co21/co10, bins = bins, range = historange, weights = co10)
hist_r21_wco21 = np.histogram(co21/co10, bins = bins, range = historange, weights = co21)

median_r21 = np.median(co21/co10)
median_r21_wco10 = weighted_median(co21/co10,co10)
median_r21_wco21 = weighted_median(co21/co10,co21)

ax1.plot([median_r21,median_r21],[14,0.14],"o",markersize=5)


ax1.step(np.delete(hist_r21[1],-1),
	      hist_r21[0]/float(sum(hist_r21[0])),
	      alpha=0.4,
	      lw = 2,
	      color = "blue")

ax1.step(np.delete(hist_r21_wco10[1],-1),
	      hist_r21_wco10[0]/float(sum(hist_r21_wco10[0])),
	      alpha=0.4,
	      lw = 2,
	      color = "green")

ax1.step(np.delete(hist_r21_wco21[1],-1),
	      hist_r21_wco21[0]/float(sum(hist_r21_wco21[0])),
	      alpha=0.4,
	      lw = 2,
	      color = "red")

ax1.set_xlim(historange)                      # xの範囲の指定
ax1.set_ylim([0,0.15])                        # yの範囲の指定

ax1.set_ylabel("Normlized Count")
ax1.set_xlabel("Brightness Temperature Ratio")

plt.savefig("/Users/saito/Desktop/figure_histo_ratio.png",dpi=300)
