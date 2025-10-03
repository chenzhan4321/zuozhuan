#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GraphRAG 快速開始腳本
提供簡單的命令行界面來運行 GraphRAG 的主要功能
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """檢查環境設置"""
    print("🔍 檢查環境設置...")
    
    # 檢查虛擬環境
    if os.path.exists("graphrag_env"):
        print("✓ 虛擬環境存在")
    else:
        print("✗ 虛擬環境不存在")
        return False
    
    # 檢查配置文件
    if os.path.exists("settings.yaml"):
        print("✓ 配置文件存在")
    else:
        print("✗ 配置文件不存在")
        return False
    
    # 檢查 .env 文件
    if os.path.exists(".env"):
        print("✓ 環境變量文件存在")
    else:
        print("⚠ 環境變量文件不存在，請創建 .env 文件")
        print("  內容應包含:")
        print("  GRAPHRAG_API_KEY=你的_DeepSeek_API_密鑰")
        print("  OPENAI_API_KEY=你的_OpenAI_API_密鑰")
    
    # 檢查輸入文件
    if os.path.exists("input/zuozhuan_full.txt"):
        print("✓ 輸入文件存在")
    else:
        print("⚠ 輸入文件不存在")
    
    return True

def run_indexing():
    """運行索引"""
    print("\n📚 開始運行 GraphRAG 索引...")
    print("這可能需要幾分鐘時間，請耐心等待...")
    
    try:
        # 激活虛擬環境並運行索引
        cmd = [
            "python", "-m", "graphrag.index", 
            "--config", "settings.yaml"
        ]
        
        print(f"執行命令: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1800  # 30分鐘超時
        )
        
        if result.returncode == 0:
            print("✓ 索引完成！")
            print("輸出文件已保存到 output/ 目錄")
            return True
        else:
            print("✗ 索引失敗:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ 索引超時（30分鐘）")
        return False
    except Exception as e:
        print(f"✗ 索引過程出錯: {e}")
        return False

def run_query():
    """運行查詢"""
    print("\n🔍 運行查詢示例...")
    
    try:
        # 運行查詢示例腳本
        result = subprocess.run(
            ["python", "query_examples.py"],
            capture_output=True,
            text=True,
            timeout=300  # 5分鐘超時
        )
        
        if result.returncode == 0:
            print("✓ 查詢示例運行完成")
            print(result.stdout)
            return True
        else:
            print("✗ 查詢失敗:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ 查詢過程出錯: {e}")
        return False

def show_status():
    """顯示項目狀態"""
    print("\n📊 項目狀態:")
    
    # 檢查輸出文件
    output_files = [
        "entities.parquet",
        "relationships.parquet", 
        "communities.parquet",
        "community_reports.parquet",
        "documents.parquet",
        "text_units.parquet"
    ]
    
    for file in output_files:
        path = f"output/{file}"
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✓ {file} ({size:,} bytes)")
        else:
            print(f"✗ {file} (不存在)")
    
    # 檢查統計信息
    if os.path.exists("output/stats.json"):
        print("✓ 統計信息文件存在")
    else:
        print("✗ 統計信息文件不存在")

def main():
    """主函數"""
    print("🚀 GraphRAG 快速開始")
    print("="*50)
    
    while True:
        print("\n請選擇操作:")
        print("1. 檢查環境設置")
        print("2. 運行索引 (構建知識圖譜)")
        print("3. 運行查詢示例")
        print("4. 顯示項目狀態")
        print("5. 退出")
        
        try:
            choice = input("\n請輸入選擇 (1-5): ").strip()
            
            if choice == "1":
                check_environment()
                
            elif choice == "2":
                if check_environment():
                    run_indexing()
                else:
                    print("請先解決環境問題")
                    
            elif choice == "3":
                if os.path.exists("output/entities.parquet"):
                    run_query()
                else:
                    print("請先運行索引 (選項 2)")
                    
            elif choice == "4":
                show_status()
                
            elif choice == "5":
                print("再見！")
                break
                
            else:
                print("無效選擇，請重新輸入")
                
        except KeyboardInterrupt:
            print("\n\n再見！")
            break
        except Exception as e:
            print(f"出錯: {e}")

if __name__ == "__main__":
    main()