#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 GraphRAG 数据导出为 Sigma.js 可用的 JSON 格式
"""

import pandas as pd
import json
from pathlib import Path


def export_graph_data():
    """导出图数据为 JSON"""
    print("📊 读取 GraphRAG 数据...")

    # 读取实体数据
    entities_df = pd.read_parquet('output/entities.parquet')
    print(f"✓ 实体: {len(entities_df)}")

    # 读取关系数据
    relationships_df = pd.read_parquet('output/relationships.parquet')
    print(f"✓ 关系: {len(relationships_df)}")

    # 创建节点列表
    nodes = []
    for _, row in entities_df.iterrows():
        node = {
            'key': str(row['id']),
            'label': str(row['title']),
            'tag': str(row.get('type', 'UNKNOWN')),
            'description': str(row.get('description', ''))[:500],
            'degree': int(row.get('degree', 0)) if pd.notna(row.get('degree')) else 1,
        }
        nodes.append(node)

    # 创建边列表
    edges = []
    edge_count = 0
    for _, row in relationships_df.iterrows():
        source = str(row['source'])
        target = str(row['target'])

        # 映射 title 到 id
        source_entity = entities_df[entities_df['title'] == source]
        target_entity = entities_df[entities_df['title'] == target]

        if not source_entity.empty and not target_entity.empty:
            edge = {
                'key': f"edge_{edge_count}",
                'source': str(source_entity.iloc[0]['id']),
                'target': str(target_entity.iloc[0]['id']),
                'label': str(row.get('description', ''))[:100],
                'weight': float(row.get('weight', 1.0)) if pd.notna(row.get('weight')) else 1.0
            }
            edges.append(edge)
            edge_count += 1

    # 创建图数据结构
    graph_data = {
        'nodes': nodes,
        'edges': edges
    }

    # 保存 JSON
    output_dir = Path('viz_data')
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / 'graph.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 数据导出成功！")
    print(f"📁 文件: {output_file}")
    print(f"📊 节点: {len(nodes)}, 边: {len(edges)}")

    return graph_data


if __name__ == '__main__':
    export_graph_data()
