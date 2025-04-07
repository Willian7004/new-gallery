'''
使用Streamlit写一个程序，实现以下功能：
1.当前文件夹中的files/video页面有多个mp4格式的视频文件
2.把第一行分为三列，左侧为复选框，文字为“显示提示词”。中间为下拉菜单，文字为“选择模式”，选项为“顺序”、“随机”和“搜索”
3.在页面上显示5个视频文件并设为自动播放、循环播放，每两个视频之间添加st.divider，选中复选框时在每个视频下方显示对应视频的文件名（不含扩展名）
4.“选择模式”下拉菜单选中“顺序”时，根据文件名排列视频并在第一行右侧创建下拉菜单用于选择页数。“选择模式”下拉菜单选中“随机”时，随机显示视频并在第一行右侧创建刷新按钮。“选择模式”下拉菜单选中“搜索”时，在第一行右侧创建输入框，在文件名中匹配输入框中的文字并显示对应视频
'''
import streamlit as st
st.sidebar.title("AI视频")
st.sidebar.write("本页面展示了使用Wan2.1 14b生成的视频（720p 33帧 teacache rel_l1_treash=0.1）。生成策略上更注重生成效果，每个提示词只生成一个视频，页面布局也有调整。提示词方面，由于umt5实现了多语言，全面改用中文提示词。")
import os
from pathlib import Path
import random

# 设置视频目录和初始化参数
video_dir = Path("files/video")
video_files = list(video_dir.glob("*.mp4"))
videos_per_page = 5

# 处理文件名和排序
sorted_files = sorted(video_files, key=lambda x: x.name)
all_names = [f.stem for f in video_files]

# 页面布局
col1, col2, col3 = st.columns([1, 3, 3],vertical_alignment="bottom")

with col1:
    show_caption = st.checkbox("显示提示词")

with col2:
    mode = st.selectbox("选择模式", ["顺序", "随机", "搜索"])

# 根据模式处理右侧控件和视频选择
selected_videos = []
selected_names = []

if mode == "顺序":
    total_pages = (len(sorted_files) + videos_per_page - 1) // videos_per_page
    with col3:
        page = st.selectbox("选择页数", range(1, total_pages+1))
    start = (page-1)*videos_per_page
    selected_videos = sorted_files[start:start+videos_per_page]
    selected_names = [f.stem for f in selected_videos]

elif mode == "随机":
    with col3:
        if st.button("刷新"):
            st.session_state.random_seed = random.randint(0, 10000)
    random.seed(st.session_state.get("random_seed", 42))
    selected_videos = random.sample(video_files, min(len(video_files), videos_per_page))
    selected_names = [f.stem for f in selected_videos]

elif mode == "搜索":
    with col3:
        search_term = st.text_input("输入搜索关键词")
    if search_term:
        matched = [i for i, name in enumerate(all_names) if search_term.lower() in name.lower()]
        selected_videos = [video_files[i] for i in matched[:videos_per_page]]
        selected_names = [all_names[i] for i in matched[:videos_per_page]]

# 显示视频内容
if selected_videos:
    for idx, (video, name) in enumerate(zip(selected_videos, selected_names)):
        st.video(str(video), format="video/mp4", autoplay=True, loop=True)
        if show_caption:
            st.write(name)
        if idx < len(selected_videos)-1:
            st.divider()
else:
    st.warning("没有找到符合条件的视频")