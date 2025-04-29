'''
使用streamlit写一个程序，实现以下功能：
1.当前目录下的files/vace文件夹中包含多个文件夹，每个文件夹包含一个mp4文件，一个或多个jpg文件和一个txt文件。
2.根据文件夹的名称在侧边栏创建单选按钮，用于选择对应的文件夹。
3.选中文件夹后，在页面上显示文件夹中的mp4文件，并在下方分两列分别显示txt和jpg文件的内容。
'''
import streamlit as st
st.title("Wan2.1 1.3b VACE")
st.write("Wan2.1 1.3b VACE能实现主体参考等功能，也是首次在主流开源视频模型中实现这一功能。在实际生成时会偏向还原参考图中的主体角度，导致部分片段生成异常，总体运动表现比原版差。生成时使用了1088x608分辨率以缩小与Fast Hunyuan的速度差距，实际单帧用时还是要2倍左右。本页面在侧边栏选择视频主题，每个主题包含5个分镜，页面包含生成的视频、提示词和参考图。视频进行了超分辨率和补帧，规格提升到1080p 60帧 6mbps。")
import os
parent_dir = os.path.join("files", "vace")

# 检查根目录是否存在
if not os.path.exists(parent_dir):
    st.error(f"未找到目录 '{parent_dir}'，请确保文件结构正确！")

# 获取所有子目录
with os.scandir(parent_dir) as entries:
    folders = [entry.name for entry in entries if entry.is_dir() and not entry.name.startswith('.')]

if not folders:
    st.warning("在文件夹 'vace' 下没有发现任何有效子文件夹！")

# 侧边栏文件夹选择
selected_folder = st.sidebar.radio("请选择文件夹：", sorted(folders))
subfolder_path = os.path.join(parent_dir, selected_folder)

# 显示视频部分
video_path = None
video_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith('.mp4')]
if video_files:
    video_path = os.path.join(subfolder_path, video_files[0])
    st.video(video_path, autoplay=True, loop=True)
else:
    st.warning("该文件夹内未找到有效MP4视频文件！")

# 布局分左右两列
col1, col2 = st.columns([1, 1])

# 文本展示列
with col1:
    st.subheader("提示词")
    txt_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith('.txt')]
    if txt_files:
        try:
            with open(os.path.join(subfolder_path, txt_files[0]), 'r', encoding='utf-8') as f:
                content = f.read()
            st.text(content)
        except Exception as e:
            st.error(f"文本文件读取失败：{str(e)}")
    else:
        st.write("该文件夹中没有TXT文件")

# 图片展示列
with col2:
    st.subheader("参考图")
    image_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith(('.jpg', '.jpeg'))]
    if image_files:
        for img in image_files:
            img_path = os.path.join(subfolder_path, img)
            try:
                st.image(img_path)
            except Exception as e:
                st.error(f"图片 '{img}' 加载失败：{str(e)}")
    else:
        st.write("该文件夹中没有JPG/JPEG图片文件")
