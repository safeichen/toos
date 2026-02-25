"""
DeepSeek快速用量检查
生成时间: 2026-02-25 19:48:46
生成工具: OpenClaw编程助手
"""

#!/usr/bin/env python3
"""
快速检查当前DeepSeek用量
基于OpenClaw配置和会话信息
"""

import os
import json
from datetime import datetime

def get_openclaw_config():
    """获取OpenClaw配置"""
    config_path = "/root/.openclaw/openclaw.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def get_current_session_info():
    """获取当前会话信息"""
    info = {
        "model": "deepseek/deepseek-chat",
        "timestamp": datetime.now().isoformat(),
        "estimated_usage": estimate_current_usage()
    }
    return info

def estimate_current_usage():
    """估算当前用量"""
    # 基于典型对话模式估算
    # 假设每次对话平均：
    # - 用户输入: 200 tokens
    # - AI回复: 400 tokens
    # - 系统提示: 50 tokens
    
    # 估算今天的对话次数（基于时间）
    hour = datetime.now().hour
    if 9 <= hour <= 18:  # 工作时间
        estimated_conversations = 20
    else:  # 非工作时间
        estimated_conversations = 10
    
    total_input = estimated_conversations * 250  # 用户+系统
    total_output = estimated_conversations * 400
    
    return {
        "estimated_conversations_today": estimated_conversations,
        "estimated_input_tokens": total_input,
        "estimated_output_tokens": total_output,
        "estimated_cost_usd": calculate_cost(total_input, total_output)
    }

def calculate_cost(input_tokens, output_tokens, cache_hit_ratio=0.3):
    """计算成本"""
    # DeepSeek定价
    input_cache_hit = 0.028  # $ per 1M tokens
    input_cache_miss = 0.28   # $ per 1M tokens
    output_cost = 0.42        # $ per 1M tokens
    
    input_hit = input_tokens * cache_hit_ratio
    input_miss = input_tokens * (1 - cache_hit_ratio)
    
    cost = (input_hit / 1_000_000 * input_cache_hit +
            input_miss / 1_000_000 * input_cache_miss +
            output_tokens / 1_000_000 * output_cost)
    
    return round(cost, 6)

def main():
    """主函数"""
    print("🔍 DeepSeek 当前用量检查")
    print("=" * 50)
    
    # 获取配置
    config = get_openclaw_config()
    print(f"📋 配置模型: {config.get('agents', {}).get('defaults', {}).get('model', 'deepseek/deepseek-chat')}")
    
    # 获取会话信息
    session_info = get_current_session_info()
    print(f"🤖 当前模型: {session_info['model']}")
    print(f"🕒 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 显示估算用量
    usage = session_info['estimated_usage']
    print("\n📊 今日用量估算:")
    print(f"   对话次数: {usage['estimated_conversations_today']}")
    print(f"   输入Token: {usage['estimated_input_tokens']:,}")
    print(f"   输出Token: {usage['estimated_output_tokens']:,}")
    print(f"   估算成本: ${usage['estimated_cost_usd']:.6f}")
    
    # 计算扩展估算
    print("\n📈 扩展估算:")
    
    # 每日估算（基于当前时间比例）
    hour = datetime.now().hour
    day_progress = hour / 24
    daily_input = int(usage['estimated_input_tokens'] / day_progress) if day_progress > 0 else 0
    daily_output = int(usage['estimated_output_tokens'] / day_progress) if day_progress > 0 else 0
    daily_cost = calculate_cost(daily_input, daily_output)
    
    print(f"   全天输入Token: {daily_input:,}")
    print(f"   全天输出Token: {daily_output:,}")
    print(f"   全天估算成本: ${daily_cost:.4f}")
    
    # 每月估算（30天）
    monthly_input = daily_input * 30
    monthly_output = daily_output * 30
    monthly_cost = calculate_cost(monthly_input, monthly_output)
    
    print(f"\n📅 月度估算 (30天):")
    print(f"   总输入Token: {monthly_input:,}")
    print(f"   总输出Token: {monthly_output:,}")
    print(f"   总估算成本: ${monthly_cost:.2f}")
    
    # 定价参考
    print("\n💰 DeepSeek定价参考:")
    print("   输入Token (缓存命中): $0.028 / 1M")
    print("   输入Token (缓存未命中): $0.28 / 1M")
    print("   输出Token: $0.42 / 1M")
    print(f"   缓存命中率假设: 30%")
    
    # 建议
    print("\n🎯 建议:")
    print("   1. 登录 https://platform.deepseek.com/usage 查看实际用量")
    print("   2. 获取API密钥进行精确监控")
    print("   3. 使用生成的监控脚本定期检查")
    print("   4. 设置余额告警阈值")
    
    print("\n" + "=" * 50)
    print("💡 注意: 这是基于典型使用模式的估算")
    print("      实际用量可能有所不同")

if __name__ == "__main__":
    main()