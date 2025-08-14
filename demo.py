import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
import json
# 假装你有 400 个任务
base_path = "./dataset"
TASKS = [f"task{i:03d}" for i in range(1, 401)]
FIXED_WIDTH_INCH =5.0 # substitute by attr inch          # 你想要的固定宽度（英寸）

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
# 每个任务有多少条数据（示例都设为 100，你可以做成字典）
TASK_LENGTH = {t: 100 for t in TASKS}
def load_images(task: str, idx: int, dataset, inch = None):
    """返回该任务该索引的两张图（PIL.Image 或 matplotlib figure 均可）"""
    # 这里用随机图占位
    fig1 = visualize_grid(dataset[idx]['input'], title = 'input', task=task, idx=idx, inch=inch)
    fig2 = visualize_grid(dataset[idx]['output'], title = 'output', task=task, idx=idx, inch=inch)
    return fig1, fig2

# ---------- 状态 ----------
if "task" not in st.session_state:
    st.session_state.task = TASKS[0]
if "idx" not in st.session_state:
    st.session_state.idx = 0

def load_data(task: str):
    path = os.path.join(base_path, f'{task}.json')
    # print(path)
    st.text(f"path: {path} opening...")
    with open(path, "r") as f:
        data = json.load(f)
    train_set_data = data["train"]
    # st.text(f"train_set_data has {len(train_set_data)} samples")
    max_idx = len(train_set_data) - 1
    return train_set_data, max_idx
with st.sidebar:
    # 1) 选任务
    def on_task_change():
        st.session_state.idx = 0              # 换任务回到 0 号样本

    task = st.selectbox(
        "选择任务",
        TASKS,
        index=TASKS.index(st.session_state.task),
        on_change=on_task_change,
        key="task_select"
    )
    if task != st.session_state.task or "dataset" not in st.session_state:
        st.session_state.idx = 0  # Reset index when task changes
        st.session_state.task = task
        st.session_state.dataset, st.session_state.max_idx = load_data(task)

    # 3. 取出来用
    dataset = st.session_state.dataset
    max_idx = st.session_state.max_idx
    # 只用 idx 作为唯一数据源，避免 key 冲突    
    # if col1.button("◀ 前一个", use_container_width=True):
    #     st.session_state.idx = max(st.session_state.idx - 1, 0)
    # elif col2.button("后一个 ▶", use_container_width=True):
    #     st.session_state.idx = min(st.session_state.idx + 1, max_idx)
    idx = st.number_input("当前样本编号（可直接跳转）", 0, max_idx, value=st.session_state.idx, key="idx")
    # st.session_state.idx = idx  # 更新 idx
    st.text(f"train_set_data has {max_idx+1} samples")
    st.text(f'num: {idx}')
    show_status = st.checkbox("显示状态栏", value=True, key="show_status")
    if show_status:
        st.text(f"task: {st.session_state.task}")
        st.text(f"idx: {st.session_state.idx}")

# ------------------ 主区域 ------------------
left, right = st.columns([1, 1])   # 左侧占约 3/4，右侧占约 1/4，可再调
fig1, fig2 = load_images(st.session_state.task, st.session_state.idx, dataset=dataset, inch = FIXED_WIDTH_INCH)

with left:
    st.text(f'input image:')
    st.pyplot(fig1, use_container_width=False, clear_figure=True)
    st.text(f'input: {dataset[idx]["input"]}')
with right:
    st.text(f'output image:')
    st.pyplot(fig2, use_container_width=False, clear_figure=True)
    st.text(f'output: {dataset[idx]["output"]}')
