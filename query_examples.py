#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GraphRAG 查詢示例腳本
展示如何使用 GraphRAG 對《左傳》進行各種類型的查詢
"""

import os
import sys
from pathlib import Path

# 添加 GraphRAG 到 Python 路徑
sys.path.append(str(Path(__file__).parent))

try:
    from graphrag.query import QueryEngine
    print("✓ GraphRAG 模組導入成功")
except ImportError as e:
    print(f"✗ GraphRAG 模組導入失敗: {e}")
    print("請確保已安裝 GraphRAG: pip install graphrag")
    sys.exit(1)

def test_query_engine():
    """測試查詢引擎初始化"""
    try:
        config_path = "settings.yaml"
        if not os.path.exists(config_path):
            print(f"✗ 配置文件不存在: {config_path}")
            return None
            
        query_engine = QueryEngine(config_path=config_path)
        print("✓ 查詢引擎初始化成功")
        return query_engine
    except Exception as e:
        print(f"✗ 查詢引擎初始化失敗: {e}")
        return None

def run_queries(query_engine):
    """運行各種類型的查詢示例"""
    
    # 查詢示例列表
    queries = [
        {
            "question": "鄭莊公和共叔段之間發生了什麼？",
            "search_type": "local",
            "description": "本地搜索 - 具體人物關係"
        },
        {
            "question": "春秋時期各國之間的盟約關係如何？",
            "search_type": "global", 
            "description": "全局搜索 - 宏觀分析"
        },
        {
            "question": "左傳中提到了哪些國家？",
            "search_type": "basic",
            "description": "基礎搜索 - 簡單列舉"
        },
        {
            "question": "春秋時期的政治格局有什麼特點？",
            "search_type": "global",
            "description": "全局搜索 - 歷史分析"
        },
        {
            "question": "穎考叔這個人物做了什麼？",
            "search_type": "local",
            "description": "本地搜索 - 具體人物"
        }
    ]
    
    print("\n" + "="*60)
    print("開始運行查詢示例")
    print("="*60)
    
    for i, query_info in enumerate(queries, 1):
        print(f"\n【查詢 {i}】{query_info['description']}")
        print(f"問題: {query_info['question']}")
        print(f"搜索類型: {query_info['search_type']}")
        print("-" * 40)
        
        try:
            result = query_engine.query(
                query_info['question'],
                search_type=query_info['search_type']
            )
            
            if result and hasattr(result, 'answer'):
                print(f"答案: {result.answer}")
                
                # 顯示相關文檔片段
                if hasattr(result, 'context') and result.context:
                    print(f"\n相關文檔片段:")
                    for j, context in enumerate(result.context[:3], 1):  # 只顯示前3個
                        print(f"  {j}. {context[:200]}...")
                
                # 顯示相關實體
                if hasattr(result, 'entities') and result.entities:
                    print(f"\n相關實體: {', '.join(result.entities[:5])}")
                    
            else:
                print("未找到相關答案")
                
        except Exception as e:
            print(f"✗ 查詢失敗: {e}")
        
        print("-" * 40)

def interactive_query(query_engine):
    """互動式查詢模式"""
    print("\n" + "="*60)
    print("進入互動式查詢模式")
    print("輸入 'quit' 或 'exit' 退出")
    print("="*60)
    
    while True:
        try:
            question = input("\n請輸入您的問題: ").strip()
            
            if question.lower() in ['quit', 'exit', '退出']:
                print("再見！")
                break
                
            if not question:
                continue
                
            # 讓用戶選擇搜索類型
            print("\n請選擇搜索類型:")
            print("1. local - 本地搜索（具體事實）")
            print("2. global - 全局搜索（宏觀分析）")
            print("3. basic - 基礎搜索（簡單問答）")
            
            choice = input("請輸入選擇 (1-3, 默認 1): ").strip()
            
            search_type_map = {
                '1': 'local',
                '2': 'global', 
                '3': 'basic',
                '': 'local'  # 默認
            }
            
            search_type = search_type_map.get(choice, 'local')
            
            print(f"\n正在搜索... (類型: {search_type})")
            
            result = query_engine.query(question, search_type=search_type)
            
            if result and hasattr(result, 'answer'):
                print(f"\n答案: {result.answer}")
                
                if hasattr(result, 'context') and result.context:
                    print(f"\n相關文檔片段:")
                    for i, context in enumerate(result.context[:2], 1):
                        print(f"  {i}. {context[:300]}...")
            else:
                print("未找到相關答案")
                
        except KeyboardInterrupt:
            print("\n\n再見！")
            break
        except Exception as e:
            print(f"✗ 查詢失敗: {e}")

def main():
    """主函數"""
    print("GraphRAG 查詢示例")
    print("="*60)
    
    # 檢查環境
    if not os.path.exists("output/entities.parquet"):
        print("✗ 未找到索引文件，請先運行索引:")
        print("   python -m graphrag.index --config settings.yaml")
        return
    
    # 初始化查詢引擎
    query_engine = test_query_engine()
    if not query_engine:
        return
    
    # 運行示例查詢
    run_queries(query_engine)
    
    # 詢問是否進入互動模式
    try:
        choice = input("\n是否進入互動式查詢模式？(y/n): ").strip().lower()
        if choice in ['y', 'yes', '是']:
            interactive_query(query_engine)
    except KeyboardInterrupt:
        print("\n再見！")

if __name__ == "__main__":
    main()