# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概览

这是一个使用 Microsoft GraphRAG 框架对《左传》古籍文本进行知识图谱构建和智能问答的项目。

## 常用命令

### 环境设置
```bash
# 激活虚拟环境
source graphrag_env/bin/activate

# 安装可视化依赖
python install_visualization_deps.py
```

### GraphRAG 索引和查询
```bash
# 构建知识图谱索引（处理输入文本）
python -m graphrag.index --config settings.yaml

# 运行查询示例
python query_examples.py

# 快速启动脚本（交互式菜单）
python quick_start.py
```

### 可视化工具
```bash
# 统一仪表板（推荐入口）
python dashboard.py

# 主要可视化工具
python visualize_graphrag.py

# 网络图可视化
python network_visualizer.py

# 社区报告可视化
python community_visualizer.py
```

### 调试
```bash
# 测试 DeepSeek API 连接
python debug_deepseek.py
```

## 代码架构

### 核心工作流程
```
input/zuozhuan_full.txt
    ↓ (GraphRAG 索引)
output/*.parquet (实体、关系、社区等)
    ↓ (查询/可视化)
答案 / 可视化图表
```

### 关键目录和文件

**输入/输出：**
- `input/` - 存放《左传》全文（zuozhuan_full.txt）
- `output/` - GraphRAG 处理后的 parquet 数据文件：
  - `entities.parquet` - 提取的实体（人物、地点、组织、事件）
  - `relationships.parquet` - 实体间的关系
  - `communities.parquet` - 实体社区
  - `community_reports.parquet` - 社区报告
  - `documents.parquet` - 处理后的文档
  - `text_units.parquet` - 文本单元
  - `lancedb/` - 向量数据库
- `cache/` - GraphRAG 缓存
- `logs/` - 日志文件

**配置：**
- `settings.yaml` - GraphRAG 主配置文件
  - 模型：DeepSeek-V3（聊天）+ text-embedding-3-small（嵌入）
  - 分块：size=1200, overlap=100
  - 实体类型：organization, person, geo, event
- `.env` - API 密钥（GRAPHRAG_API_KEY, OPENAI_API_KEY）
- `prompts/` - GraphRAG 提示词模板

**核心脚本：**
- `quick_start.py` - 交互式启动脚本（环境检查、索引、查询）
- `query_examples.py` - 查询示例（包含 local/global/basic 三种搜索）

**可视化脚本：**
- `dashboard.py` - 统一仪表板（项目状态、统计、一键生成所有可视化）
- `visualize_graphrag.py` - 主要可视化（实体分布、关系网络、社区分布）
- `network_visualizer.py` - 网络图可视化（完整网络、按类型分类、社区网络）
- `community_visualizer.py` - 社区分析（大小分布、词云、关键词分析）

### GraphRAG 查询类型

1. **Local Search（本地搜索）**
   - 用途：具体事实、人物关系、事件细节
   - 方法：基于向量相似度检索相关文档片段

2. **Global Search（全局搜索）**
   - 用途：复杂分析、趋势总结、宏观问题
   - 方法：Map-Reduce 模式，综合多个社区信息

3. **Basic Search（基础搜索）**
   - 用途：简单问答、定义查询
   - 方法：直接检索，快速响应

4. **Drift Search（漂移搜索）**
   - 用途：探索性查询、开放性问题
   - 方法：允许查询偏离原始问题

### 可视化输出文件

**静态图表（PNG）：**
- `entity_types_distribution.png` - 实体类型分布
- `relationship_network.png` - 关系网络图
- `communities_distribution.png` - 社区分布
- `full_network.png` - 完整网络图
- `community_sizes_distribution.png` - 社区大小分布
- `wordcloud_community_*.png` - 词云

**交互式图表（HTML）：**
- `graphrag_dashboard.html` - GraphRAG 仪表板
- `community_dashboard.html` - 社区仪表板
- `full_network.html` - 交互式网络图

**报告文档（MD）：**
- `graphrag_summary_report.md` - 摘要报告
- `community_detailed_report.md` - 详细社区报告

## 配置调优

### settings.yaml 关键参数
- `chunks.size` / `chunks.overlap` - 调整文本分块大小和重叠
- `extract_graph.entity_types` - 定义要提取的实体类型
- `community_reports.max_length` - 社区报告最大长度
- `concurrent_requests` - 并发 API 请求数（影响速度）
- `tokens_per_minute` / `requests_per_minute` - API 速率限制

### 提示词定制
修改 `prompts/` 目录中的 .txt 文件：
- `extract_graph.txt` - 实体和关系提取
- `community_report_*.txt` - 社区报告生成
- `*_search_system_prompt.txt` - 各类查询系统提示词
- `summarize_descriptions.txt` - 实体描述摘要

## 重要注意事项

1. **环境依赖**：所有操作需要先激活虚拟环境 `graphrag_env`
2. **API 密钥**：确保 `.env` 文件包含有效的 API 密钥
3. **索引顺序**：必须先运行索引才能进行查询或可视化
4. **中文支持**：可视化工具已配置中文字体支持（jieba 分词）
5. **数据格式**：GraphRAG 输出使用 parquet 格式，需要 pandas/pyarrow 读取
