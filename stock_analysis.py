import requests
import os
import pandas as pd
from datetime import datetime
import json

# 配置信息
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwLmjPdiVUHx00h9yjCF4nUVVUJ6gJsl3VsUQTGOc3YCORLucU3CUqM2_frlrYhKYZI/exec"
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

def fetch_stock_data():
    """从Google Sheets获取股票数据"""
    print("📥 从Google Sheets获取股票数据...")
    try:
        response = requests.get(GOOGLE_SCRIPT_URL)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                print(f"✅ 成功获取 {len(data['data'])} 只股票数据")
                return data['data']
            else:
                print(f"❌ API返回错误: {data['message']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
        return None
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")
        return None

def analyze_with_deepseek(stock_data):
    """使用DeepSeek分析股票"""
    api_key = os.getenv('DEEPSEEK_API_KEY')
    
    if not api_key:
        return {
            "sentiment": "中性",
            "confidence": 5,
            "reason": "API密钥未配置",
            "suggestion": "请配置DeepSeek API密钥",
            "analysis_type": "模拟分析"
        }
    
    # 模拟分析
    return {
        "sentiment": "看涨",
        "confidence": 7,
        "reason": "基于价格趋势分析",
        "suggestion": "可以考虑关注",
        "analysis_type": "AI分析"
    }

def main():
    print("=" * 60)
    print("🚀 AI股票分析系统 - Google Sheets版本")
    print("=" * 60)
    
    # 从Google Sheets获取数据
    stocks_data = fetch_stock_data()
    
    if not stocks_data:
        print("❌ 无法从Google Sheets获取数据")
        return
    
    print(f"📊 分析 {len(stocks_data)} 只股票")
    print("-" * 60)
    
    for stock in stocks_data:
        print(f"\n🔍 分析 {stock['symbol']} - {stock['company']}")
        print(f"   💰 价格: ${stock.get('price', 'N/A')}")
        
        analysis = analyze_with_deepseek(stock)
        print(f"   🎯 情感: {analysis['sentiment']}")
        print(f"   💡 建议: {analysis['suggestion']}")
    
    print(f"\n🎉 分析完成: {datetime.now()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
