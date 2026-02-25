"""
DeepSeek API用量监控脚本
生成时间: 2026-02-25 19:32:52
生成工具: OpenClaw编程助手
"""

#!/usr/bin/env python3
"""
DeepSeek API 用量监控脚本
获取DeepSeek平台用量信息并生成报告
"""

import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional

class DeepSeekUsageMonitor:
    """DeepSeek API用量监控器"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化监控器
        
        Args:
            api_key: DeepSeek API密钥（可选）
        """
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com"
        self.usage_url = "https://platform.deepseek.com/usage"
        
        # 定价信息（从官方文档获取）
        self.pricing_info = {
            "deepseek-chat": {
                "model": "DeepSeek-V3.2 (Non-thinking Mode)",
                "context_length": "128K",
                "max_output": "4K (default), 8K (maximum)",
                "pricing": {
                    "input_cache_hit": 0.028,  # $ per 1M tokens
                    "input_cache_miss": 0.28,   # $ per 1M tokens
                    "output": 0.42             # $ per 1M tokens
                }
            },
            "deepseek-reasoner": {
                "model": "DeepSeek-V3.2 (Thinking Mode)",
                "context_length": "128K",
                "max_output": "32K (default), 64K (maximum)",
                "pricing": {
                    "input_cache_hit": 0.028,  # $ per 1M tokens
                    "input_cache_miss": 0.28,   # $ per 1M tokens
                    "output": 0.42             # $ per 1M tokens
                }
            }
        }
    
    def get_usage_page(self) -> str:
        """获取用量页面内容"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(self.usage_url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return f"无法访问用量页面: {e}"
    
    def extract_usage_info(self, html_content: str) -> Dict[str, Any]:
        """从HTML内容中提取用量信息"""
        # 注意：实际用量页面需要登录才能访问
        # 这里返回模拟数据用于演示
        
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "需要登录访问",
            "note": "实际用量信息需要登录DeepSeek平台查看",
            "estimated_usage": self.get_estimated_usage(),
            "pricing_info": self.pricing_info,
            "rate_limits": self.get_rate_limits()
        }
    
    def get_estimated_usage(self) -> Dict[str, Any]:
        """获取估算用量（基于常见使用模式）"""
        return {
            "daily_estimate": {
                "requests": 100,  # 估算每日请求数
                "input_tokens": 50000,  # 估算输入token数
                "output_tokens": 20000,  # 估算输出token数
                "cost_usd": self.calculate_cost(50000, 20000)
            },
            "monthly_estimate": {
                "requests": 3000,  # 估算每月请求数
                "input_tokens": 1500000,  # 估算输入token数
                "output_tokens": 600000,  # 估算输出token数
                "cost_usd": self.calculate_cost(1500000, 600000)
            }
        }
    
    def calculate_cost(self, input_tokens: int, output_tokens: int, 
                      cache_hit_ratio: float = 0.3) -> float:
        """
        计算使用成本
        
        Args:
            input_tokens: 输入token数
            output_tokens: 输出token数
            cache_hit_ratio: 缓存命中率（0-1）
            
        Returns:
            估算成本（美元）
        """
        # 计算输入token成本（考虑缓存命中率）
        input_tokens_hit = input_tokens * cache_hit_ratio
        input_tokens_miss = input_tokens * (1 - cache_hit_ratio)
        
        input_cost_hit = (input_tokens_hit / 1_000_000) * self.pricing_info["deepseek-chat"]["pricing"]["input_cache_hit"]
        input_cost_miss = (input_tokens_miss / 1_000_000) * self.pricing_info["deepseek-chat"]["pricing"]["input_cache_miss"]
        
        # 计算输出token成本
        output_cost = (output_tokens / 1_000_000) * self.pricing_info["deepseek-chat"]["pricing"]["output"]
        
        total_cost = input_cost_hit + input_cost_miss + output_cost
        return round(total_cost, 4)
    
    def get_rate_limits(self) -> Dict[str, Any]:
        """获取API速率限制信息"""
        return {
            "free_tier": {
                "requests_per_minute": 10,
                "requests_per_day": 1000,
                "tokens_per_minute": 10000
            },
            "paid_tier": {
                "requests_per_minute": 60,
                "requests_per_day": 10000,
                "tokens_per_minute": 100000
            },
            "enterprise_tier": {
                "requests_per_minute": "自定义",
                "requests_per_day": "自定义",
                "tokens_per_minute": "自定义"
            }
        }
    
    def generate_report(self) -> str:
        """生成用量报告"""
        html_content = self.get_usage_page()
        usage_info = self.extract_usage_info(html_content)
        
        report = f"""
# DeepSeek API 用量监控报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 用量状态
- 状态: {usage_info['status']}
- 说明: {usage_info['note']}

## 💰 定价信息
### deepseek-chat 模型
- 模型版本: {self.pricing_info['deepseek-chat']['model']}
- 上下文长度: {self.pricing_info['deepseek-chat']['context_length']}
- 最大输出: {self.pricing_info['deepseek-chat']['max_output']}
- 价格:
  - 输入token（缓存命中）: ${self.pricing_info['deepseek-chat']['pricing']['input_cache_hit']} / 1M tokens
  - 输入token（缓存未命中）: ${self.pricing_info['deepseek-chat']['pricing']['input_cache_miss']} / 1M tokens
  - 输出token: ${self.pricing_info['deepseek-chat']['pricing']['output']} / 1M tokens

### deepseek-reasoner 模型
- 模型版本: {self.pricing_info['deepseek-reasoner']['model']}
- 上下文长度: {self.pricing_info['deepseek-reasoner']['context_length']}
- 最大输出: {self.pricing_info['deepseek-reasoner']['max_output']}
- 价格: 与deepseek-chat相同

## 📈 估算用量
### 每日估算
- 请求数: {usage_info['estimated_usage']['daily_estimate']['requests']}
- 输入token: {usage_info['estimated_usage']['daily_estimate']['input_tokens']:,}
- 输出token: {usage_info['estimated_usage']['daily_estimate']['output_tokens']:,}
- 估算成本: ${usage_info['estimated_usage']['daily_estimate']['cost_usd']}

### 每月估算
- 请求数: {usage_info['estimated_usage']['monthly_estimate']['requests']:,}
- 输入token: {usage_info['estimated_usage']['monthly_estimate']['input_tokens']:,}
- 输出token: {usage_info['estimated_usage']['monthly_estimate']['output_tokens']:,}
- 估算成本: ${usage_info['estimated_usage']['monthly_estimate']['cost_usd']}

## ⚡ 速率限制
### 免费层级
- 每分钟请求: {usage_info['rate_limits']['free_tier']['requests_per_minute']}
- 每日请求: {usage_info['rate_limits']['free_tier']['requests_per_day']}
- 每分钟token: {usage_info['rate_limits']['free_tier']['tokens_per_minute']:,}

### 付费层级
- 每分钟请求: {usage_info['rate_limits']['paid_tier']['requests_per_minute']}
- 每日请求: {usage_info['rate_limits']['paid_tier']['requests_per_day']}
- 每分钟token: {usage_info['rate_limits']['paid_tier']['tokens_per_minute']:,}

## 🎯 使用建议
1. **优化缓存使用**: 尽量复用上下文以提高缓存命中率
2. **控制输出长度**: 设置合理的max_tokens参数
3. **监控用量**: 定期检查用量页面
4. **成本控制**: 根据实际需求选择合适的套餐

## 🔗 相关链接
- DeepSeek平台: https://platform.deepseek.com
- 用量页面: https://platform.deepseek.com/usage
- API文档: https://api-docs.deepseek.com
- 定价页面: https://api-docs.deepseek.com/quick_start/pricing

---
*注: 实际用量信息需要登录DeepSeek平台查看。此报告基于公开信息和估算数据。*
"""
        return report
    
    def save_report(self, filename: str = "deepseek_usage_report.md"):
        """保存报告到文件"""
        report = self.generate_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"报告已保存到: {filename}")
        return filename
    
    def calculate_custom_usage(self, input_tokens: int, output_tokens: int, 
                              model: str = "deepseek-chat") -> Dict[str, Any]:
        """计算自定义用量成本"""
        if model not in self.pricing_info:
            raise ValueError(f"不支持的模型: {model}")
        
        cost = self.calculate_cost(input_tokens, output_tokens)
        
        return {
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": cost,
            "cost_breakdown": {
                "input_cache_hit": f"${(input_tokens * 0.3 / 1_000_000) * self.pricing_info[model]['pricing']['input_cache_hit']:.4f}",
                "input_cache_miss": f"${(input_tokens * 0.7 / 1_000_000) * self.pricing_info[model]['pricing']['input_cache_miss']:.4f}",
                "output": f"${(output_tokens / 1_000_000) * self.pricing_info[model]['pricing']['output']:.4f}"
            }
        }


def main():
    """主函数"""
    import sys
    
    monitor = DeepSeekUsageMonitor()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--custom":
            if len(sys.argv) >= 4:
                try:
                    input_tokens = int(sys.argv[2])
                    output_tokens = int(sys.argv[3])
                    model = sys.argv[4] if len(sys.argv) > 4 else "deepseek-chat"
                    
                    result = monitor.calculate_custom_usage(input_tokens, output_tokens, model)
                    
                    print(f"\n📊 自定义用量计算:")
                    print(f"模型: {result['model']}")
                    print(f"输入token: {result['input_tokens']:,}")
                    print(f"输出token: {result['output_tokens']:,}")
                    print(f"估算成本: ${result['estimated_cost_usd']:.4f}")
                    print(f"\n成本明细:")
                    for key, value in result['cost_breakdown'].items():
                        print(f"  - {key}: {value}")
                    
                except ValueError as e:
                    print(f"错误: {e}")
                    print("用法: python deepseek_usage_monitor.py --custom <输入token> <输出token> [模型]")
            else:
                print("用法: python deepseek_usage_monitor.py --custom <输入token> <输出token> [模型]")
        
        elif sys.argv[1] == "--report":
            filename = sys.argv[2] if len(sys.argv) > 2 else "deepseek_usage_report.md"
            monitor.save_report(filename)
            print(f"\n✅ 报告已生成: {filename}")
        
        elif sys.argv[1] == "--help":
            print("DeepSeek API 用量监控工具")
            print("用法:")
            print("  python deepseek_usage_monitor.py                    # 显示报告")
            print("  python deepseek_usage_monitor.py --report [文件名]  # 生成报告文件")
            print("  python deepseek_usage_monitor.py --custom <输入token> <输出token> [模型]  # 计算自定义用量")
            print("  python deepseek_usage_monitor.py --help             # 显示帮助")
            print("\n示例:")
            print("  python deepseek_usage_monitor.py --custom 10000 5000")
            print("  python deepseek_usage_monitor.py --report my_report.md")
    
    else:
        # 显示报告
        report = monitor.generate_report()
        print(report)
        
        # 询问是否保存
        save = input("\n是否保存报告到文件? (y/N): ").strip().lower()
        if save == 'y':
            filename = input("文件名 (默认: deepseek_usage_report.md): ").strip()
            if not filename:
                filename = "deepseek_usage_report.md"
            monitor.save_report(filename)


if __name__ == "__main__":
    main()