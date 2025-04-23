'''
写一个streamlit程序，实现以下功能：
1.当前目录下files/FastHunyuan文件夹中有 主体.txt 场景.txt 和多个包含视频的文件夹
2.在文件夹名称中匹配 主体.txt 中每一行的内容（匹配完整字符串），对于匹配到的所有行，在页面上创建第一个st.segmented_control，以对应的文字作为选项，默认选中第一项。在包含视频的文件夹中匹配文件夹名称包含选中项的文字的文件夹。
3.在匹配到的文件夹名称中匹配 场景.txt 中每一行的内容（匹配完整字符串），把匹配到的行的文字作为选项创建第二个st.segmented_control，用于选择具体的文件夹（不考虑存在多个有同一组关键词的文件夹的情况），默认选中第一项。
4.在页面上显示选中的文件夹名称，根据名称对选中的文件夹中的视频进行排序，把序号作为选项创建第三个st.segmented_control，用于选择具体的视频，默认选中第一项。
5.在页面上显示选中的视频，开启自动播放、循环播放。
'''
import streamlit as st
import os
st.sidebar.title("Fast Hunyuan")
st.sidebar.write("Fast Hunyuan是Hunyuan Video的步数蒸馏版本，在3070m上生成1136x640分辨率视频单帧耗时8.3秒。由于速度提高，本项目增加了提示词数量，使用场景+主体形式快速组合提示词，共规划118个提示词，每个提示词生成8个视频并筛选。另外使用了对应的方法选择视频，复杂度高于之前的streamlit程序。")
def read_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
            return [line for line in lines if line]
    except FileNotFoundError:
        return []

# 基础路径配置
base_dir = os.path.join('files', 'FastHunyuan')
subject_file = os.path.join(base_dir, '主体.txt')
scene_file = os.path.join(base_dir, '场景.txt')

# 读取配置内容
subjects = read_lines(subject_file)
scenes = read_lines(scene_file)

# 获取所有视频文件夹（排除txt文件）
video_folders = []
for item in os.listdir(base_dir):
    item_path = os.path.join(base_dir, item)
    if os.path.isdir(item_path) and item not in ['主体.txt', '场景.txt']:
        video_folders.append(item)

# 初始化session_state
if 'selected_subject' not in st.session_state:
    st.session_state.selected_subject = subjects[0] if subjects else ''
if 'selected_scene' not in st.session_state:
    st.session_state.selected_scene = scenes[0] if scenes else ''
if 'selected_video_index' not in st.session_state:
    st.session_state.selected_video_index = 0

# 主体选择
if not subjects:
    st.error("主体文件内容为空，请检查主体.txt")
    st.stop()

st.session_state.selected_subject = st.segmented_control(
    "选择主体",
    subjects,
    default="offroad car"
)

# 根据主体筛选文件夹
matched_subject_folders = [f for f in video_folders if st.session_state.selected_subject in f]

# 场景选择逻辑
scene_folder_map = {}
available_scenes = []

for scene in scenes:
    for folder in matched_subject_folders:
        if scene in folder:
            scene_folder_map[scene] = folder
            available_scenes.append(scene)
            break  # 每个场景只匹配第一个找到的文件夹

if not available_scenes:
    st.error("视频未上传")
    st.stop()

try:
    st.session_state.selected_scene = st.segmented_control(
        "选择场景",
        available_scenes,
        default="grassland"   
    )
except:
     st.session_state.selected_scene = st.segmented_control(
        "选择场景",
        available_scenes,
        default="village"    
    )

# 获取目标文件夹
target_folder = scene_folder_map[st.session_state.selected_scene]
st.write(f"提示词: {target_folder}")

# 视频选择逻辑
video_dir = os.path.join(base_dir, target_folder)
video_files = sorted([f for f in os.listdir(video_dir) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))])

if not video_files:
    st.error("文件夹中没有视频文件")
    st.stop()

video_options = [f"视频 {i+1}" for i in range(len(video_files))]
st.session_state.selected_video_index = st.segmented_control(
    "选择视频",
    range(len(video_files)),
    format_func=lambda x: f"{x+1}",
    default=0
)

# 显示视频
video_path = os.path.join(video_dir, video_files[st.session_state.selected_video_index])
st.video(video_path, format="video/mp4", start_time=0, autoplay=True, loop=True)