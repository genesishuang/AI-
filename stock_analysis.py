import requests
import os
import pandas as pd
import yfinance as yf
from datetime import datetime

def get_stock_data(symbol):
    """获取股票数据"""
    try:
        print(f"📡 正在获取 {symbol} 的数据...")
        ticker = yf.Ticker(symbol)
        
        # 获取基本信息
        info = ticker.info
        company_name = info.get('longName', symbol)
        
        # 获取最近5天股价
        history = ticker.history(period="5d")
        
        if history.empty:
            print(f"❌ 无法获取 {symbol} 的历史数据")
            return None
        
        current_price = history['Close'].iloc[-1]
        previous_price = history['Close'].iloc[-2] if len(history) > 1 else current_price
        
        # 计算涨跌幅
        if previous_price and previous_price != 0:
            change_percent = ((current_price - previous_price) / previous_price) * 100
        else:
            change_percent = 0
            
        return {
            'symbol': symbol,
            'company': company_name,
            'price': round(current_price, 2),
            'previous_price': round(previous_price, 2),
            'change_percent': round(change_percent, 2),
            'currency': info.get('currency', 'USD'),
            'update_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        print(f"❌ 获取 {symbol} 数据失败: {e}")
        return None

def analyze_with_deepseek(stock_data):
    """使用DeepSeek分析股票（模拟版本）"""
    api_key = os.getenv('DEEPSEEK_API_KEY')
    
    # 检查API密钥
    if not api_key:
        print("   🔑 DeepSeek API密钥: 未设置（使用模拟分析）")
        return {
            "sentiment": "中性",
            "confidence": 5,
            "reason": "API密钥未配置，使用模拟分析",
            "suggestion": "配置API密钥后获取真实分析",
            "analysis_type": "模拟分析"
        }
    else:
        print(f"   🔑 DeepSeek API密钥: 已检测到（前8位: {api_key[:8]}...）")
        # 这里可以添加真实的API调用代码
        return {
            "sentiment": "看涨",
            "confidence": 7,
            "reason": "价格趋势积极，市场情绪良好",
            "suggestion": "可以考虑关注",
            "analysis_type": "模拟分析（API已就绪）"
        }

def main():
    print("=" * 70)
    print("🚀 AI股票分析系统启动")
    print("📊 数据源: yfinance | 🤖 AI引擎: DeepSeek")
    print("=" * 70)
    
    # 要分析的股票列表
    symbols = ['AAPL', 'MSFT', 'TSLA', 'GOOGL', 'AMZN']
    
    print(f"🎯 分析目标: {', '.join(symbols)}")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 70)
    
    analysis_results = []
    successful_analysis = 0
    
    # 分析每只股票
    for symbol in symbols:
        print(f"\n🔍 正在分析 {symbol}...")
        
        # 1. 获取股票数据
        stock_data = get_stock_data(symbol)
        if not stock_data:
            continue
            
        # 显示基本信息
        print(f"   🏢 公司: {stock_data['company']}")
        print(f"   💰 当前价格: ${stock_data['price']} {stock_data['currency']}")
        print(f"   📈 今日涨跌幅: {stock_data['change_percent']}%")
        
        # 2. AI分析
        print("   🤖 正在进行AI分析...")
        analysis = analyze_with_deepseek(stock_data)
        
        # 显示分析结果
        if isinstance(analysis, dict):
            sentiment_emoji = "🟢" if "看涨" in analysis["sentiment"] else "🔴" if "看跌" in analysis["sentiment"] else "🟡"
            print(f"   {sentiment_emoji} 情感: {analysis['sentiment']}")
            print(f"   ⭐ 置信度: {analysis['confidence']}/10")
            print(f"   📝 理由: {analysis['reason']}")
            print(f"   💡 建议: {analysis['suggestion']}")
            print(f"   🔧 模式: {analysis['analysis_type']}")
            
            # 保存结果
            analysis_results.append({
                'symbol': stock_data['symbol'],
                'company': stock_data['company'],
                'price': stock_data['price'],
                'change_percent': f"{stock_data['change_percent']}%",
                'sentiment': analysis['sentiment'],
                'confidence': analysis['confidence'],
                'suggestion': analysis['suggestion']
            })
            successful_analysis += 1
        else:
            print(f"   ❌ 分析失败: {analysis}")
    
    # 总结报告
    print("\n" + "=" * 70)
    print("📋 分析总结报告")
    print("=" * 70)
    
    if successful_analysis > 0:
        print(f"✅ 成功分析 {successful_analysis}/{len(symbols)} 只股票")
        print("\n详细结果:")
        print("-" * 50)
        
        for result in analysis_results:
            emoji = "🟢" if "看涨" in result["sentiment"] else "🔴" if "看跌" in result["sentiment"] else "🟡"
            print(f"{emoji} {result['symbol']:6} | ${result['price']:8} | {result['change_percent']:8} | {result['sentiment']:6} | {result['suggestion']}")
    else:
        print("❌ 未能成功分析任何股票")
    
    print(f"\n🎉 分析完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

# 程序入口
if __name__ == "__main__":
    main()
