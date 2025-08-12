import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
import json
# 假装你有 400 个任务
base_path = "./dataset"
TASKS = [f"task{i:03d}" for i in range(1, 401)]

def visualize_grid(grid, title: str = "Grid Visualization"):
    """
    用 matplotlib 画出二维网格。
    0-9 映射到 tab10 颜色表。
    """
    arr = np.array(grid)
    fig, ax = plt.subplots()
    
    # tab10 只有 10 种颜色，刚好对应 0-9
    cmap = plt.cm.get_cmap("tab10", 10)
    im = ax.imshow(arr, cmap=cmap, vmin=0, vmax=9)
    
    # 在每个格子里标数字
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            ax.text(j, i, str(arr[i, j]),
                    ha="center", va="center", color="white", fontsize=12)
    
    ax.set_xticks(range(arr.shape[1]))
    ax.set_yticks(range(arr.shape[0]))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title(title)
    return fig
# 每个任务有多少条数据（示例都设为 100，你可以做成字典）
TASK_LENGTH = {t: 100 for t in TASKS}
def __load_images(task: str, idx: int, dataset):
    """返回该任务该索引的两张图（PIL.Image 或 matplotlib figure 均可）"""
    st.text(f'num: {idx}\n, input: {dataset[idx]["input"]}\n, output: {dataset[idx]["output"]}')
    # 这里用随机图占位
    fig1 = visualize_grid(dataset[idx]['input'], title = 'input')
    fig2 = visualize_grid(dataset[idx]['output'], title = 'output')
    return fig1, fig2
def _load_images(task: str, idx: int):
    """返回该任务该索引的两张图（PIL.Image 或 matplotlib figure 均可）"""
    # if num is None:
    #     num = 0
    path = os.path.join(base_path, f'{task}.json')
    # print(path)
    st.text(f"path: {path} opening...")
    with open(path, "r") as f:
        data = json.load(f)
    train_set_data = data["train"]
    st.text(f"train_set_data has {len(train_set_data)} samples")
    max_idx = len(train_set_data) - 1
    st.text(train_set_data[idx])
    # 这里用随机图占位
    fig1, ax1 = plt.subplots()
    ax1.plot(np.random.randn(100))
    ax1.set_title(f"{task} — 样本 {idx} — 图1")

    fig2, ax2 = plt.subplots()
    ax2.imshow(np.random.rand(10, 10), cmap='Blues')
    ax2.set_title(f"{task} — 样本 {idx} — 图2")
    return fig1, fig2
# —— 把这两张图换成你自己的真实数据 ——
def load_images(task: str, idx: int):
    """返回该任务该索引的两张图（PIL.Image 或 matplotlib figure 均可）"""
    # 这里用随机图占位
    fig1, ax1 = plt.subplots()
    ax1.plot(np.random.randn(100))
    ax1.set_title(f"{task} — 样本 {idx} — 图1")

    fig2, ax2 = plt.subplots()
    ax2.imshow(np.random.rand(10, 10), cmap='Blues')
    ax2.set_title(f"{task} — 样本 {idx} — 图2")
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
    if task != st.session_state.task:
        st.session_state.idx = 0  # Reset index when task changes
        st.session_state.task = task
        st.session_state.dataset, st.session_state.max_idx = load_data(task)

    # 3. 取出来用
    dataset = st.session_state.dataset
    max_idx = st.session_state.max_idx

    col1, col2 = st.columns(2)
    if col1.button("◀ 前一个", use_container_width=True):
        st.session_state.idx = max(st.session_state.idx - 1, 0)
    if col2.button("后一个 ▶", use_container_width=True):
        st.session_state.idx = min(st.session_state.idx + 1, max_idx)

    # 4. 直接跳指定编号（可选）
    jump = st.number_input("直接跳转", 0, max_idx, st.session_state.idx, key="jump")
    if jump != st.session_state.idx:
        st.session_state.idx = jump
    st.metric("当前样本编号", st.session_state.idx)


# ------------------ 主区域 ------------------
st.text(f"train_set_data has {max_idx} samples")

fig1, fig2 = __load_images(st.session_state.task, st.session_state.idx, dataset=dataset)
st.pyplot(fig1)
st.pyplot(fig2)
