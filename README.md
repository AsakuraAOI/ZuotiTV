# 做题蛆度量表

输入文本，AI 将分析其中的"做题蛆"特征并给出 0-100+ 评分。

**做题蛆** 是网络用语，指深度信奉"做题万能"、以成绩作为唯一价值标准的人群，核心意识形态为"穷人原罪论 + 做题万能论 + 社会达尔文主义"三位一体。

## 评分等级

| 分数 | 等级 |
|------|------|
| 0-15 | 正常 |
| 16-35 | 做题倾向 |
| 36-60 | 做题家 |
| 61-80 | 做题蛆（轻度） |
| 81-100 | 做题蛆（重度） |
| 101+ | 间桐樱 |

## 分析维度

基于 11 个维度综合评估：穷人原罪论、做题万能论、社会达尔文主义、做题行为模式、炫耀/凡尔赛、权威崇拜、权力滥用、心理/情绪、价值观、经典话术、性/亲密关系扭曲。

## 快速开始

```bash
pip install -r requirements.txt
# 编辑 config.json 填入 API Key
python server.py
```

打开浏览器访问 `http://localhost:7860`

## 技术栈

- **后端**: Flask
- **前端**: 纯 HTML/CSS/JS，Chart.js 雷达图
- **AI 模型**: SiliconFlow（DeepSeek V3.2）

## 文件说明

```
dist/
├── index.html       # 前端界面
├── server.py        # Flask 后端（API 中转，保护 Key 不暴露）
├── config.json      # API 配置
├── requirements.txt # Python 依赖
└── README.md        # 本文件
```
