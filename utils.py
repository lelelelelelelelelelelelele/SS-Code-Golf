import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
import json
import io
from PIL import Image
FIXED_WIDTH_INCH =5.0 # substitute by attr inch          # 你想要的固定宽度（英寸）
base_path = "./dataset"
# PIL concat
def fig_to_pil(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    return Image.open(buf).convert("RGB")
def merge_image(img1, img2, mode='horizontal'):
    img1 = fig_to_pil(img1)
    img2 = fig_to_pil(img2)
    if mode == 'horizontal':
        if img1.height != img2.height:
            new_width = int(img2.width * img1.height / img2.height)
            img2 = img2.resize((new_width, img1.height))
        new_img = Image.new("RGB", (img1.width + img2.width, img1.height))
        new_img.paste(img1, (0, 0))
        new_img.paste(img2, (img1.width, 0))
    else:
        if img1.width != img2.width:
            new_height = int(img2.height * img1.width / img2.width)
            img2 = img2.resize((img1.width, new_height))
        new_img = Image.new("RGB", (img1.width, img1.height + img2.height))
        new_img.paste(img1, (0, 0))
        new_img.paste(img2, (0, img1.height))
    return new_img

# matplot -> numpy -> concat
def array_to_fig(arr):
    # 按像素设置 figure 尺寸
    dpi = 100  # 每英寸像素密度
    h, w = arr.shape[:2]
    fig = plt.figure(figsize=(w / dpi, h / dpi), dpi=dpi)

    # 添加全屏坐标轴
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(arr)
    ax.axis("off")  # 关闭坐标轴
    return fig
def fig_to_array(fig):
    """把 matplotlib Figure 转成 numpy 数组 (H, W, 3)"""
    fig.canvas.draw()  # 绘制到缓冲区
    buf = np.asarray(fig.canvas.buffer_rgba())  # 得到 RGBA
    return buf[:, :, :3]

def merge_image1(fig1, fig2, mode='horizontal'):
    """拼接两个 matplotlib Figure（numpy方式）"""
    arr1 = fig_to_array(fig1)
    arr2 = fig_to_array(fig2)

    if mode == 'horizontal':
        # 高度对齐
        if arr1.shape[0] != arr2.shape[0]:
            raise ValueError("Figures have different heights, please resize before concat.")
        arr = np.hstack((arr1, arr2))
    else:
        # 宽度对齐
        if arr1.shape[1] != arr2.shape[1]:
            raise ValueError("Figures have different widths, please resize before concat.")
        arr = np.vstack((arr1, arr2))
    return array_to_fig(arr)



def visualize_grid(grid, title: str = "Grid Visualization", task: str = "", idx: int = 0, inch = None):
    """
    用 matplotlib 画出二维网格。
    0-9 映射到 tab10 颜色表。
    """
    arr = np.array(grid)
    h, w = arr.shape
    # 高度按原始比例缩放
    height_inch = inch * h / max(w, 1)
    # inch = None
    if inch is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = plt.subplots(figsize=(inch, height_inch))
    atitle = f'{title}-{task}-{idx}'
    # tab10 只有 10 种颜色，刚好对应 0-9
    cmap = plt.cm.get_cmap("tab10", 10)
    im = ax.imshow(arr, cmap=cmap, vmin=0, vmax=9)
    
    # 在每个格子里标数字，并根据 subplot 尺寸动态调整字体大小
    cell_height = height_inch / max(h, 1)
    cell_width = inch / max(w, 1) if inch is not None else 1.0
    base_fontsize = min(cell_height, cell_width) * 30  # 10 是经验缩放因子，可调整
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            ax.text(j, i, str(arr[i, j]),
                    ha="center", va="center", color="white", fontsize=base_fontsize)
    
    ax.set_xticks(range(arr.shape[1]))
    ax.set_yticks(range(arr.shape[0]))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title(atitle)
    return fig

def load_images(task: str, idx: int, dataset, inch = None):
    """返回该任务该索引的两张图（PIL.Image 或 matplotlib figure 均可）"""
    # 这里用随机图占位
    fig1 = visualize_grid(dataset[idx]['input'], title = 'input', task=task, idx=idx, inch=inch)
    fig2 = visualize_grid(dataset[idx]['output'], title = 'output', task=task, idx=idx, inch=inch)
    return fig1, fig2

def load_data(task: str):
    path = os.path.join(base_path, f'{task}.json')
    # print(path)
    st.text(f"path: {path} opening...")
    with open(path, "r") as f:
        data = json.load(f)
    return data, sum(len(v) for v in data.values())
    # train_set_data = data["train"]
    # # st.text(f"train_set_data has {len(train_set_data)} samples")
    # max_idx = len(train_set_data) - 1
    # return train_set_data, max_idx