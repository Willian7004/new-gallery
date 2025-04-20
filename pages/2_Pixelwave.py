'''
使用streamlit写一个程序，实现以下功能：
1.当前目录下files/pixelwave中有horizontal和vertical两个文件夹，每个文件夹中有多个包含图片的文件夹。
2.在侧边栏创建st.segmented_control，选项为16：9和9：16，分别用于选择horizonal和vertical文件夹。
3.在页面上根据选中的文件夹中的文件夹名称创建st.pills并设为单选模式，选中时随机显示对应文件夹中的3张图片。创建刷新按钮用于重新随机选择图片。
4.如果在st.segmented_control选中16：9，不分列显示图片；如果在st.segmented_control选中9：16，分两列显示图片。
5.在侧边栏创建复选框，文字为“显示下载按钮”，选中时在每张图片下方显示下载按钮用于下载对应图片。
'''
import os
import random
import streamlit as st
from PIL import Image

st.sidebar.title("Pixelwave")
st.sidebar.write("由于Pixelwave的短提示词表现较好，本页面尝试了新的形式，使用不超过两个单词的提示词各生成横竖屏图片各20张并筛选。选择提示词查看相应图片，按刷新按钮随机选择图片。生成分辨率为1080p，因此添加了下载按钮以便获取原始分辨率版本。")

# 定义文件路径
BASE_DIR = "files/pixelwave"
HORIZONTAL_DIR = os.path.join(BASE_DIR, "horizontal")
VERTICAL_DIR = os.path.join(BASE_DIR, "vertical")

# 初始化session_state
if 'selected_images' not in st.session_state:
    st.session_state.selected_images = {}
if 'refresh' not in st.session_state:
    st.session_state.refresh = False

# 侧边栏控件
with st.sidebar:
    # 选择比例
    ratio = st.segmented_control("选择比例", options=["16:9", "9:16"],default="16:9")
    # 下载按钮开关
    show_download = st.checkbox("显示下载按钮")

# 根据比例选择目录
main_dir = HORIZONTAL_DIR if ratio == "16:9" else VERTICAL_DIR

# 获取所有子文件夹
sub_folders = [f for f in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, f))]

if not sub_folders:
    st.warning("当前目录下没有子文件夹")
    st.stop()

# 创建pills选择器
selected_folder = st.pills("选择提示词", sub_folders, selection_mode="single",default="city")

# 刷新按钮
if st.button("刷新图片"):
    st.session_state.refresh = not st.session_state.refresh

# 获取选中文件夹的图片
folder_path = os.path.join(main_dir, selected_folder)
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

if not image_files:
    st.warning("选中文件夹中没有图片")
    st.stop()

# 随机选择3张图片
selected_images = random.sample(image_files, min(3, len(image_files)))

# 根据比例设置布局
if ratio == "9:16":
    col1, col2, col3 = st.columns(3)   
    columns = [col1, col2, col3]
else:
    pass

# 显示图片
for idx, img_name in enumerate(selected_images):
    img_path = os.path.join(folder_path, img_name)
    
    try:
        img = Image.open(img_path)
        if ratio == "9:16":
            with columns[idx%3 if ratio == "9:16" else 0]:  # 两列布局时交替显示
                st.image(img)
        else:        
            st.image(img)
            if show_download:
                with open(img_path, "rb") as f:
                    img_bytes = f.read()
                st.download_button(
                    label=f"下载",
                    data=img_bytes,
                    file_name=img_name,
                    mime="image/jpeg",
                    key=f"dl_{idx}"
                )
    except Exception as e:
        st.error(f"无法加载图片 {img_name}: {str(e)}")

# 刷新按钮（底部）
if st.button("刷新图片"):
    st.session_state.refresh = not st.session_state.refresh