# New Gallery

### 项目说明

本项目内容与gallery项目类似，用于展示新一代模型生成的内容。

本项目已部署到Streamlit Cloud，域名为https://william7004-new-gallery.streamlit.app/

### 使用python部署
1.安装依赖
```
pip install -r requirements.txt
```
2.运行应用
```
streamlit run streamlit_app.py
```

### 使用docker部署
1.创建docker
```
docker build . -t new-gallery
```
2.运行docker
```
docker run -p 8501:8501 new-gallery
```
