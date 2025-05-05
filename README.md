# 随手记个人精选知识库 v1.0

## 项目简介
随手记个人精选知识库是一个基于飞书多维表格的知识管理系统，帮助用户高效管理和展示个人收藏的文章和知识内容。通过简洁的界面和强大的搜索功能，用户可以轻松访问和分享自己的知识收藏。

## 功能特点
- 文章列表展示：支持分页浏览所有收藏的文章
- 文章搜索：支持按内容简介和核心看点进行搜索
- 分类筛选：支持按文章分类进行内容筛选
- 文章封面：自动处理和展示文章封面图片
- 文章链接：支持直接跳转到原文阅读

## 技术栈
- 后端：Python Flask框架
- 前端：HTML、CSS、JavaScript
- 数据存储：飞书多维表格
- API集成：飞书开放平台API

## 项目结构
```
mylink-manager/
├── README.md           # 项目说明文档
├── requirements.txt    # Python依赖包列表
├── .env               # 环境变量配置文件
├── app.py             # Flask应用主文件
├── static/            # 静态资源文件
│   └── default-cover.jpg  # 默认文章封面
└── templates/         # HTML模板文件
    ├── base.html      # 基础模板
    └── index.html     # 首页模板
```

## 部署说明

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置飞书应用
- 在飞书开放平台创建应用
- 获取应用凭证（App ID和App Secret）
- 开启多维表格权限

3. 配置环境变量
- 复制.env文件中的配置项
- 填入您的飞书应用信息：
  - FEISHU_APP_ID
  - FEISHU_APP_SECRET
  - BASE_ID（多维表格ID）
  - TABLE_ID（表格ID）

4. 运行应用
```bash
python app.py
```

5. 访问网站
打开浏览器访问 http://localhost:5000

## 版本历史

### v1.0 (2024-01)
- 初始版本发布
- 实现基本的文章列表展示功能
- 支持文章搜索和分类筛选
- 集成飞书多维表格作为数据源
- 支持文章封面和链接展示