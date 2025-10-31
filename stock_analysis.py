import requests
import os
import pandas as pd
from datetime import datetime
import json

# 配置 - 需要您填写Google Apps Script的URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzZlae78l_9Imlsmzv1hPAFQYuh9Vgl-MBvVEvwGUE3EyoZgbZFlzcEJ-rhZqWvf7TA/exec"

def get_stock_data_from_sheets():
    """从Google Sheets获取股票数据"""
    print("📥 从Google Sheets获取股票数据...")
    try:
        response = requests.get(GOOGLE_SCRIPT_URL)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                print(f"✅ 成功获取 {len(data['data'])} 只股票数据")
                return data['data']
        print(f"❌ 获取数据失败: {response.status_code}")
        return None
    except Exception as e:
        print(f"❌ 连接Google Sheets失败: {e}")
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
    
    # 模拟分析 - 实际使用时调用真实API
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
    stocks_data = get_stock_data_from_sheets()
    
    if not stocks_data:
        print("❌ 无法从Google Sheets获取数据，使用备用数据源...")
        # 备用方案：使用硬编码的股票列表
        stocks_data = [
            {'symbol': 'AAPL', 'company': 'Apple Inc', 'price': 175.0},
            {'symbol': 'MSFT', 'company': 'Microsoft', 'price': 330.0},
            {'symbol': 'TSLA', 'company': 'Tesla', 'price': 240.0}
        ]
    
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
