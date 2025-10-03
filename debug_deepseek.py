#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""调试 DeepSeek API 连接"""

import requests
import json

API_KEY = "sk-caaa6d9b2c2b43e6a5cccca712c73fc9"
BASE_URL = "https://api.deepseek.com"

# 测试 1: 直接 HTTP 请求测试
print("=== 测试 1: 直接 HTTP 请求测试 ===")
try:
    url = f"{BASE_URL}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "你好"}],
        "max_tokens": 10
    }

    print(f"请求 URL: {url}")
    print(f"请求头: {headers}")

    response = requests.post(url, headers=headers, json=data, timeout=30)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text[:500]}")

    if response.status_code == 200:
        result = response.json()
        print(f"✓ 成功! 回复: {result['choices'][0]['message']['content']}")
    else:
        print(f"✗ 请求失败: {response.text}")

except requests.exceptions.Timeout:
    print("✗ 请求超时")
except requests.exceptions.ConnectionError as e:
    print(f"✗ 连接错误: {e}")
except Exception as e:
    print(f"✗ 错误: {type(e).__name__}: {e}")

# 测试 2: 使用 OpenAI SDK
print("\n=== 测试 2: 使用 OpenAI SDK ===")
try:
    from openai import OpenAI

    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL,
        timeout=30.0
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "你好"}],
        max_tokens=10
    )

    print(f"✓ 成功! 回复: {response.choices[0].message.content}")

except Exception as e:
    print(f"✗ 错误: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# 测试 3: 检查网络连通性
print("\n=== 测试 3: 网络连通性检查 ===")
try:
    response = requests.get("https://api.deepseek.com", timeout=10)
    print(f"✓ 可以访问 api.deepseek.com (状态码: {response.status_code})")
except Exception as e:
    print(f"✗ 无法访问 api.deepseek.com: {e}")

# 测试 4: 尝试不同的 base_url
print("\n=== 测试 4: 尝试不同的 API endpoint ===")
endpoints = [
    "https://api.deepseek.com",
    "https://api.deepseek.com/v1",
]

for endpoint in endpoints:
    try:
        url = f"{endpoint}/chat/completions" if not endpoint.endswith("/v1") else f"{endpoint}/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "测试"}],
            "max_tokens": 5
        }

        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"{endpoint}: 状态码 {response.status_code}")
        if response.status_code == 200:
            print(f"  ✓ 成功!")
        else:
            print(f"  ✗ 失败: {response.text[:200]}")
    except Exception as e:
        print(f"{endpoint}: ✗ {type(e).__name__}: {e}")
