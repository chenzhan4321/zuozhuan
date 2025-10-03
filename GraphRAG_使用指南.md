# GraphRAG 使用指南

## 什麼是 GraphRAG？

GraphRAG 是微軟開發的一個開源框架，用於構建基於圖的檢索增強生成（RAG）系統。它能夠從文檔中提取實體和關係，構建知識圖譜，並提供更智能的問答功能。

## 你的項目現狀

根據你的項目結構，你已經有一個完整的 GraphRAG 設置：

- ✅ **配置文件**: `settings.yaml` - 已配置 DeepSeek-V3 模型
- ✅ **輸入數據**: `input/zuozhuan_full.txt` - 《左傳》全文
- ✅ **輸出結果**: `output/` 目錄包含處理後的圖譜數據
- ✅ **虛擬環境**: `graphrag_env/` - Python 環境已設置

## 基本使用流程

### 1. 環境設置

```bash
# 激活虛擬環境
source graphrag_env/bin/activate

# 設置環境變量（需要創建 .env 文件）
echo "GRAPHRAG_API_KEY=你的_DeepSeek_API_密鑰" > .env
echo "OPENAI_API_KEY=你的_OpenAI_API_密鑰" >> .env
```

### 2. 運行索引（Indexing）

```bash
# 對文檔進行索引，構建知識圖譜
python -m graphrag.index --config settings.yaml
```

這個命令會：
- 讀取 `input/` 目錄中的文檔
- 提取實體和關係
- 構建知識圖譜
- 生成社區報告
- 創建向量嵌入
- 將結果保存到 `output/` 目錄

### 3. 進行查詢

```python
from graphrag.query import QueryEngine

# 初始化查詢引擎
query_engine = QueryEngine(config_path="settings.yaml")

# 本地搜索 - 適合具體事實查詢
result = query_engine.query(
    "鄭莊公和共叔段之間發生了什麼？",
    search_type="local"
)

# 全局搜索 - 適合複雜分析
result = query_engine.query(
    "春秋時期的政治格局如何？",
    search_type="global"
)

# 基礎搜索 - 簡單問答
result = query_engine.query(
    "左傳中提到了哪些國家？",
    search_type="basic"
)
```

## 配置說明

### 模型配置
你的 `settings.yaml` 中配置了：
- **聊天模型**: DeepSeek-V3 (用於圖譜提取和查詢)
- **嵌入模型**: text-embedding-3-small (用於向量化)

### 關鍵參數
- `chunks.size: 1200` - 文檔分塊大小
- `chunks.overlap: 100` - 分塊重疊
- `extract_graph.entity_types` - 提取的實體類型
- `community_reports.max_length: 2000` - 社區報告最大長度

## 輸出文件說明

### 核心數據文件
- `entities.parquet` - 提取的實體
- `relationships.parquet` - 實體間的關係
- `communities.parquet` - 實體社區
- `community_reports.parquet` - 社區報告
- `documents.parquet` - 處理後的文檔
- `text_units.parquet` - 文本單元

### 向量存儲
- `lancedb/` - LanceDB 向量數據庫

## 查詢類型

### 1. Local Search（本地搜索）
- 適合：具體事實、人物關係、事件細節
- 特點：基於向量相似度，返回相關文檔片段

### 2. Global Search（全局搜索）
- 適合：複雜分析、趨勢總結、宏觀問題
- 特點：使用 Map-Reduce 模式，綜合多個社區信息

### 3. Basic Search（基礎搜索）
- 適合：簡單問答、定義查詢
- 特點：直接檢索，快速響應

### 4. Drift Search（漂移搜索）
- 適合：探索性查詢、開放性問題
- 特點：允許查詢偏離原始問題

## 實際使用示例

### 示例 1: 人物關係查詢
```python
# 查詢特定人物的關係
result = query_engine.query(
    "鄭莊公與哪些人物有關係？他們之間發生了什麼？",
    search_type="local"
)
```

### 示例 2: 歷史事件分析
```python
# 分析歷史事件
result = query_engine.query(
    "春秋時期各國之間的盟約關係如何？",
    search_type="global"
)
```

### 示例 3: 地理信息查詢
```python
# 查詢地理信息
result = query_engine.query(
    "左傳中提到了哪些城市和國家？",
    search_type="basic"
)
```

## 最佳實踐

### 1. 查詢優化
- 使用具體的實體名稱
- 避免過於寬泛的問題
- 根據問題類型選擇合適的搜索模式

### 2. 性能調優
- 調整 `concurrent_requests` 參數
- 根據 API 限制設置 `tokens_per_minute`
- 適當調整 `chunks.size` 和 `chunks.overlap`

### 3. 結果處理
- 檢查返回的相關性分數
- 結合多種搜索類型獲得更全面的結果
- 利用社區報告獲取背景信息

## 故障排除

### 常見問題
1. **API 密鑰錯誤**: 檢查 `.env` 文件中的 API 密鑰
2. **模型不支持**: 確認 DeepSeek-V3 支持 JSON 格式
3. **內存不足**: 減少 `concurrent_requests` 或 `chunks.size`
4. **網絡超時**: 增加 `timeout` 設置

### 調試工具
你的項目中有 `debug_deepseek.py` 可以用來測試 API 連接。

## 下一步

1. **嘗試不同查詢**: 測試各種類型的問題
2. **調整配置**: 根據結果質量調整參數
3. **擴展數據**: 添加更多文檔到 `input/` 目錄
4. **自定義提示**: 修改 `prompts/` 目錄中的提示模板

## 相關資源

- [GraphRAG 官方文檔](https://microsoft.github.io/graphrag/)
- [GitHub 倉庫](https://github.com/microsoft/graphrag)
- [配置參考](https://microsoft.github.io/graphrag/config/yaml/)

---

*這個指南基於你現有的項目設置。如果你需要針對特定用例的幫助，請告訴我！*