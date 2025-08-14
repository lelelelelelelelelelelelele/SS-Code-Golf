import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
import json
from utils import *

base_path = "./dataset"
TASKS = [f"task{i:03d}" for i in range(1, 401)]

TASK_LENGTH = {t: 100 for t in TASKS}

# ---------- 状态 ----------
if "task" not in st.session_state:
    st.session_state.task = TASKS[0]
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "select_dataset" not in st.session_state:
    st.session_state.select_dataset = "train"
if "merge_display" not in st.session_state:
    st.session_state.merge_display = False

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
    if task != st.session_state.task or "data" not in st.session_state:
        st.session_state.idx = 0  # Reset index when task changes
        st.session_state.task = task
        st.session_state.data, st.session_state.max_idx = load_data(task)
    st.text(f'task: {st.session_state.task} has {st.session_state.max_idx + 1} samples in total')
    # 3. 取出来用
    data = st.session_state.data
    max_idx = st.session_state.max_idx
    # 只用 idx 作为唯一数据源，避免 key 冲突    
    # if col1.button("◀ 前一个", use_container_width=True):
    #     st.session_state.idx = max(st.session_state.idx - 1, 0)
    # elif col2.button("后一个 ▶", use_container_width=True):
    #     st.session_state.idx = min(st.session_state.idx + 1, max_idx)
    # st.session_state.idx = idx  # 更新 idx

    show_advanced = st.checkbox("显示高级功能")
    # additional function
    if show_advanced:
        st.subheader("高级功能")
        st.checkbox("合并显示", value=False, key="merge_display")
        selected_key = st.selectbox("选择数据集", list(data.keys()), key="select_dataset")
    else:
        selected_key = "train"
    dataset = data[selected_key]
    max_lim = len(dataset)
    idx = st.number_input("当前样本编号（可直接跳转）", min_value=0, max_value=max_lim-1, value=st.session_state.idx, key="idx")

    # st.text(f"当前{selected_key}数据集 有 {max_idx} 个样本")
    st.text(f"{selected_key}_set_data has {max_lim} samples")
    st.text(f'num: {idx} / {max_lim - 1}')

    show_status = st.checkbox("显示状态栏", value=True, key="show_status")
    if show_status:
        st.text(f"task: {st.session_state.task}")
        st.text(f"selected_dataset: {selected_key}")
        st.text(f"idx / max: {st.session_state.idx} / {max_lim - 1}")
        st.text(f"merge_display: {st.session_state.merge_display}")
# ------------------ 主区域 ------------------
left, right = st.columns([1, 1])   # 左侧占约 3/4，右侧占约 1/4，可再调
fig1, fig2 = load_images(st.session_state.task, st.session_state.idx, dataset=dataset, inch = FIXED_WIDTH_INCH)

def display_seperately():
    with left:
        st.text(f'input image:')
        st.pyplot(fig1, use_container_width=False, clear_figure=True)
        st.text(f'input: {dataset[idx]["input"]}')
    with right:
        st.text(f'output image:')
        st.pyplot(fig2, use_container_width=False, clear_figure=True)
        st.text(f'output: {dataset[idx]["output"]}')
def display_combined():
    combined_fig = merge_image(fig1, fig2)
    # st.pyplot(combined_fig, use_container_width=False, clear_figure=True)
    st.image(combined_fig, use_container_width=False)
    # st.text(f'input: {dataset[idx]["input"]}')
    # st.text(f'output: {dataset[idx]["output"]}')

if st.session_state.merge_display:
    display_combined()
else:
    display_seperately()