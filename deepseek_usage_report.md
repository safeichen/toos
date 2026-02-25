
# DeepSeek API 用量监控报告
生成时间: 2026-02-25 19:33:07

## 📊 用量状态
- 状态: 需要登录访问
- 说明: 实际用量信息需要登录DeepSeek平台查看

## 💰 定价信息
### deepseek-chat 模型
- 模型版本: DeepSeek-V3.2 (Non-thinking Mode)
- 上下文长度: 128K
- 最大输出: 4K (default), 8K (maximum)
- 价格:
  - 输入token（缓存命中）: $0.028 / 1M tokens
  - 输入token（缓存未命中）: $0.28 / 1M tokens
  - 输出token: $0.42 / 1M tokens

### deepseek-reasoner 模型
- 模型版本: DeepSeek-V3.2 (Thinking Mode)
- 上下文长度: 128K
- 最大输出: 32K (default), 64K (maximum)
- 价格: 与deepseek-chat相同

## 📈 估算用量
### 每日估算
- 请求数: 100
- 输入token: 50,000
- 输出token: 20,000
- 估算成本: $0.0186

### 每月估算
- 请求数: 3,000
- 输入token: 1,500,000
- 输出token: 600,000
- 估算成本: $0.5586

## ⚡ 速率限制
### 免费层级
- 每分钟请求: 10
- 每日请求: 1000
- 每分钟token: 10,000

### 付费层级
- 每分钟请求: 60
- 每日请求: 10000
- 每分钟token: 100,000

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
