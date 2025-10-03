# 左傳知識圖譜

基於 Microsoft GraphRAG 構建的《左傳》古籍知識圖譜專案，提供交互式可視化介面。

## 🌟 特性

- 📚 **知識圖譜構建** - 使用 GraphRAG 自動提取實體和關係
- 🔍 **智能查詢** - 支援 Local/Global/Basic 三種查詢模式
- 🎨 **可視化** - Sigma.js 交互式網路圖譜展示
- 🤖 **AI 驅動** - DeepSeek-V3 + OpenAI Embeddings

## 📋 前置要求

- Python 3.10+
- Node.js 16+
- DeepSeek API Key
- OpenAI API Key

## 🚀 快速開始

### 1. 克隆倉庫

```bash
git clone https://github.com/chenzhan4321/zuozhuan
cd zuozhuan
```

### 2. 配置環境變量

```bash
cp .env.example .env
# 編輯 .env 文件，填入你的 API 密鑰
```

### 3. 安裝 Python 依賴

```bash
python -m venv graphrag_env
source graphrag_env/bin/activate  # Windows: graphrag_env\Scripts\activate
pip install graphrag pandas pyarrow
```

### 4. 構建知識圖譜

```bash
python -m graphrag.index --config settings.yaml
```

### 5. 啟動可視化

```bash
# 轉換數據
python export_graph_data.py

# 安裝 Node.js 依賴
npm install

# 啟動服務器
npm start
```

訪問 http://localhost:3000 查看可視化效果。

## 📖 使用指南

### GraphRAG 查詢

```bash
# 本地查詢（具體問題）
python -m graphrag query --method local --query "魯隱公是誰？" --config settings.yaml

# 全局查詢（宏觀問題）
python -m graphrag query --method global --query "春秋時期主要事件" --config settings.yaml
```

### 可視化功能

- 🔍 **搜尋** - 搜尋框輸入節點名稱
- 🎯 **篩選** - 點擊分類標籤過濾節點
- 👆 **交互** - 點擊節點查看詳情和關聯
- 🔄 **縮放** - 滑鼠滾輪縮放，拖拽平移

## 📁 專案結構

```
zuozhuan/
├── input/              # 輸入文本
├── output/             # GraphRAG 輸出
├── prompts/            # 提示詞模板
├── public/             # 前端文件
├── viz_data/           # 可視化數據
├── settings.yaml       # GraphRAG 配置
├── export_graph_data.py # 數據轉換腳本
└── server.js           # Web 服務器
```

## 💡 常用命令

### 環境設置
```bash
# 激活虛擬環境
source graphrag_env/bin/activate

# 安裝可視化依賴
python install_visualization_deps.py
```

### GraphRAG 索引和查詢
```bash
# 構建知識圖譜索引（處理輸入文本）
python -m graphrag.index --config settings.yaml

# 運行查詢示例
python query_examples.py

# 快速啟動腳本（交互式選單）
python quick_start.py
```

### 可視化工具
```bash
# 統一儀表板（推薦入口）
python dashboard.py

# 主要可視化工具
python visualize_graphrag.py

# 網路圖可視化
python network_visualizer.py

# 社群報告可視化
python community_visualizer.py
```

### 調試
```bash
# 測試 DeepSeek API 連接
python debug_deepseek.py
```

## 🏗️ 代碼架構

### 核心工作流程
```
input/zuozhuan_full.txt
    ↓ (GraphRAG 索引)
output/*.parquet (實體、關係、社群等)
    ↓ (查詢/可視化)
答案 / 可視化圖表
```

### 關鍵目錄和文件

**輸入/輸出：**
- `input/` - 存放《左傳》全文（zuozhuan_full.txt）
- `output/` - GraphRAG 處理後的 parquet 數據文件：
  - `entities.parquet` - 提取的實體（人物、地點、組織、事件）
  - `relationships.parquet` - 實體間的關係
  - `communities.parquet` - 實體社群
  - `community_reports.parquet` - 社群報告
  - `documents.parquet` - 處理後的文檔
  - `text_units.parquet` - 文本單元
  - `lancedb/` - 向量數據庫
- `cache/` - GraphRAG 緩存
- `logs/` - 日誌文件

**配置：**
- `settings.yaml` - GraphRAG 主配置文件
  - 模型：DeepSeek-V3（聊天）+ text-embedding-3-small（嵌入）
  - 分塊：size=1200, overlap=100
  - 實體類型：organization, person, geo, event
- `.env` - API 密鑰（GRAPHRAG_API_KEY, OPENAI_API_KEY）
- `prompts/` - GraphRAG 提示詞模板

**核心腳本：**
- `quick_start.py` - 交互式啟動腳本（環境檢查、索引、查詢）
- `query_examples.py` - 查詢示例（包含 local/global/basic 三種搜尋）

**可視化腳本：**
- `dashboard.py` - 統一儀表板（專案狀態、統計、一鍵生成所有可視化）
- `visualize_graphrag.py` - 主要可視化（實體分布、關係網路、社群分布）
- `network_visualizer.py` - 網路圖可視化（完整網路、按類型分類、社群網路）
- `community_visualizer.py` - 社群分析（大小分布、詞雲、關鍵詞分析）

### GraphRAG 查詢類型

1. **Local Search（本地搜尋）**
   - 用途：具體事實、人物關係、事件細節
   - 方法：基於向量相似度檢索相關文檔片段

2. **Global Search（全局搜尋）**
   - 用途：複雜分析、趨勢總結、宏觀問題
   - 方法：Map-Reduce 模式，綜合多個社群資訊

3. **Basic Search（基礎搜尋）**
   - 用途：簡單問答、定義查詢
   - 方法：直接檢索，快速響應

4. **Drift Search（漂移搜尋）**
   - 用途：探索性查詢、開放性問題
   - 方法：允許查詢偏離原始問題

### 可視化輸出文件

**靜態圖表（PNG）：**
- `entity_types_distribution.png` - 實體類型分布
- `relationship_network.png` - 關係網路圖
- `communities_distribution.png` - 社群分布
- `full_network.png` - 完整網路圖
- `community_sizes_distribution.png` - 社群大小分布
- `wordcloud_community_*.png` - 詞雲

**交互式圖表（HTML）：**
- `graphrag_dashboard.html` - GraphRAG 儀表板
- `community_dashboard.html` - 社群儀表板
- `full_network.html` - 交互式網路圖

**報告文檔（MD）：**
- `graphrag_summary_report.md` - 摘要報告
- `community_detailed_report.md` - 詳細社群報告

## ⚙️ 配置

在 `settings.yaml` 中可以調整：

- **模型設置** - LLM 和 Embedding 模型
- **分塊參數** - 文本分塊大小和重疊
- **實體類型** - 要提取的實體類別
- **併發控制** - API 請求速率限制

### settings.yaml 關鍵參數
- `chunks.size` / `chunks.overlap` - 調整文本分塊大小和重疊
- `extract_graph.entity_types` - 定義要提取的實體類型
- `community_reports.max_length` - 社群報告最大長度
- `concurrent_requests` - 併發 API 請求數（影響速度）
- `tokens_per_minute` / `requests_per_minute` - API 速率限制

### 提示詞定製
修改 `prompts/` 目錄中的 .txt 文件：
- `extract_graph.txt` - 實體和關係提取
- `community_report_*.txt` - 社群報告生成
- `*_search_system_prompt.txt` - 各類查詢系統提示詞
- `summarize_descriptions.txt` - 實體描述摘要

## 🎨 可視化自定義

編輯 `public/app.js` 中的配置：

```javascript
this.typeColors = {
    'PERSON': '#e91e63',        // 人物
    'ORGANIZATION': '#9c27b0',  // 組織
    'GEO': '#4caf50',           // 地理
    'EVENT': '#ff9800',         // 事件
};
```

## ⚠️ 重要注意事項

1. **環境依賴**：所有操作需要先激活虛擬環境 `graphrag_env`
2. **API 密鑰**：確保 `.env` 文件包含有效的 API 密鑰
3. **索引順序**：必須先運行索引才能進行查詢或可視化
4. **中文支援**：可視化工具已配置中文字體支援（jieba 分詞）
5. **數據格式**：GraphRAG 輸出使用 parquet 格式，需要 pandas/pyarrow 讀取

## 📝 許可證

MIT

## 🙏 致謝

- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [Sigma.js](https://www.sigmajs.org/)
- [Graphology](https://graphology.github.io/)
