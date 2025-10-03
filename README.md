# 左传知识图谱

基于 Microsoft GraphRAG 构建的《左传》古籍知识图谱项目，提供交互式可视化界面。

## 🌟 特性

- 📚 **知识图谱构建** - 使用 GraphRAG 自动提取实体和关系
- 🔍 **智能查询** - 支持 Local/Global/Basic 三种查询模式
- 🎨 **可视化** - Sigma.js 交互式网络图谱展示
- 🤖 **AI 驱动** - DeepSeek-V3 + OpenAI Embeddings

## 📋 前置要求

- Python 3.10+
- Node.js 16+
- DeepSeek API Key
- OpenAI API Key

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone <repository-url>
cd zuozhuan
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥
```

### 3. 安装 Python 依赖

```bash
python -m venv graphrag_env
source graphrag_env/bin/activate  # Windows: graphrag_env\Scripts\activate
pip install graphrag pandas pyarrow
```

### 4. 构建知识图谱

```bash
python -m graphrag.index --config settings.yaml
```

### 5. 启动可视化

```bash
# 转换数据
python export_graph_data.py

# 安装 Node.js 依赖
npm install

# 启动服务器
npm start
```

访问 http://localhost:3000 查看可视化效果。

## 📖 使用指南

### GraphRAG 查询

```bash
# 本地查询（具体问题）
python -m graphrag query --method local --query "鲁隐公是谁？" --config settings.yaml

# 全局查询（宏观问题）
python -m graphrag query --method global --query "春秋时期主要事件" --config settings.yaml
```

### 可视化功能

- 🔍 **搜索** - 搜索框输入节点名称
- 🎯 **筛选** - 点击分类标签过滤节点
- 👆 **交互** - 点击节点查看详情和关联
- 🔄 **缩放** - 鼠标滚轮缩放，拖拽平移

## 📁 项目结构

```
zuozhuan/
├── input/              # 输入文本
├── output/             # GraphRAG 输出
├── prompts/            # 提示词模板
├── public/             # 前端文件
├── viz_data/           # 可视化数据
├── settings.yaml       # GraphRAG 配置
├── export_graph_data.py # 数据转换脚本
└── server.js           # Web 服务器
```

## ⚙️ 配置

在 `settings.yaml` 中可以调整：

- **模型设置** - LLM 和 Embedding 模型
- **分块参数** - 文本分块大小和重叠
- **实体类型** - 要提取的实体类别
- **并发控制** - API 请求速率限制

## 🎨 可视化自定义

编辑 `public/app.js` 中的配置：

```javascript
this.typeColors = {
    'PERSON': '#e91e63',        // 人物
    'ORGANIZATION': '#9c27b0',  // 组织
    'GEO': '#4caf50',           // 地理
    'EVENT': '#ff9800',         // 事件
};
```

## 📝 许可证

MIT

## 🙏 致谢

- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [Sigma.js](https://www.sigmajs.org/)
- [Graphology](https://graphology.github.io/)
