"""
处理A(B/C)格式列表的函数
生成时间: 2025-02-25 14:45:00
生成工具: OpenClaw编程助手
"""

def process_parentheses_list(input_list):
    """
    处理 A(B/C) 格式的列表，返回两个去重后的数组
    
    参数:
        input_list: 包含 A(B/C) 格式字符串的列表
        
    返回:
        tuple: (list_A, list_BC) 两个去重后的列表
        
    示例:
        >>> input_data = ["苹果(红富士/嘎啦)", "香蕉(进口/本地)", "苹果(红富士/青苹果)"]
        >>> process_parentheses_list(input_data)
        (['苹果', '香蕉'], ['红富士', '嘎啦', '进口', '本地', '青苹果'])
    """
    
    if not input_list:
        return [], []
    
    list_A = []
    list_BC = []
    
    for item in input_list:
        # 检查格式是否正确
        if '(' not in item or ')' not in item:
            print(f"警告: 跳过格式不正确的项: {item}")
            continue
        
        # 分割主项和子项
        try:
            # 找到括号位置
            left_paren = item.index('(')
            right_paren = item.index(')')
            
            # 提取A部分（括号前的内容）
            part_A = item[:left_paren].strip()
            
            # 提取B/C部分（括号内的内容）
            part_BC_str = item[left_paren + 1:right_paren]
            
            # 分割B/C部分
            if '/' in part_BC_str:
                parts_BC = [p.strip() for p in part_BC_str.split('/')]
            else:
                parts_BC = [part_BC_str.strip()]
            
            # 添加到列表
            if part_A:
                list_A.append(part_A)
            
            for bc in parts_BC:
                if bc:
                    list_BC.append(bc)
                    
        except (ValueError, IndexError) as e:
            print(f"错误: 处理项 '{item}' 时出错: {e}")
            continue
    
    # 去重并保持顺序
    # 使用字典保持插入顺序（Python 3.7+ 字典保持插入顺序）
    unique_A = list(dict.fromkeys(list_A))
    unique_BC = list(dict.fromkeys(list_BC))
    
    return unique_A, unique_BC


def process_parentheses_list_advanced(input_list, separator='/', keep_empty=False):
    """
    高级版本：处理 A(B/C) 格式的列表，支持自定义分隔符
    
    参数:
        input_list: 包含 A(B/C) 格式字符串的列表
        separator: 括号内的分隔符，默认为 '/'
        keep_empty: 是否保留空字符串，默认为 False
        
    返回:
        tuple: (list_A, list_BC) 两个去重后的列表
    """
    
    if not input_list:
        return [], []
    
    list_A = []
    list_BC = []
    
    for item in input_list:
        # 检查格式
        if '(' not in item or ')' not in item:
            print(f"警告: 跳过格式不正确的项: {item}")
            continue
        
        try:
            # 使用正则表达式更灵活地匹配
            import re
            
            # 匹配 A(B/C) 格式
            pattern = r'^([^(]+)\(([^)]+)\)$'
            match = re.match(pattern, item)
            
            if not match:
                print(f"警告: 无法解析项: {item}")
                continue
            
            part_A = match.group(1).strip()
            part_BC_str = match.group(2).strip()
            
            # 分割子项
            if separator in part_BC_str:
                parts_BC = [p.strip() for p in part_BC_str.split(separator)]
            else:
                parts_BC = [part_BC_str.strip()]
            
            # 过滤空字符串
            if part_A or keep_empty:
                list_A.append(part_A)
            
            for bc in parts_BC:
                if bc or keep_empty:
                    list_BC.append(bc)
                    
        except Exception as e:
            print(f"错误: 处理项 '{item}' 时出错: {e}")
            continue
    
    # 去重
    unique_A = []
    seen_A = set()
    for a in list_A:
        if a not in seen_A:
            seen_A.add(a)
            unique_A.append(a)
    
    unique_BC = []
    seen_BC = set()
    for bc in list_BC:
        if bc not in seen_BC:
            seen_BC.add(bc)
            unique_BC.append(bc)
    
    return unique_A, unique_BC


def test_examples():
    """测试函数"""
    
    print("=== 测试基本功能 ===")
    
    # 测试用例1：水果示例
    test_data1 = ["苹果(红富士/嘎啦)", "香蕉(进口/本地)", "苹果(红富士/青苹果)"]
    print(f"输入: {test_data1}")
    result1 = process_parentheses_list(test_data1)
    print(f"输出: {result1}")
    print(f"A列表: {result1[0]}")
    print(f"BC列表: {result1[1]}")
    print()
    
    # 测试用例2：城市示例
    test_data2 = ["中国(北京/上海)", "美国(纽约/洛杉矶)", "中国(北京/广州)"]
    print(f"输入: {test_data2}")
    result2 = process_parentheses_list(test_data2)
    print(f"输出: {result2}")
    print()
    
    # 测试用例3：包含空格的项
    test_data3 = ["红色 (深红/浅红)", "蓝色(深蓝 / 浅蓝)", "红色(深红/正红)"]
    print(f"输入: {test_data3}")
    result3 = process_parentheses_list(test_data3)
    print(f"输出: {result3}")
    print()
    
    # 测试用例4：错误格式
    test_data4 = ["正确(格式)", "错误格式", "另一个(正确/格式)"]
    print(f"输入: {test_data4}")
    result4 = process_parentheses_list(test_data4)
    print(f"输出: {result4}")
    print()
    
    print("=== 测试高级功能 ===")
    
    # 测试自定义分隔符
    test_data5 = ["项目A(选项1|选项2)", "项目B(选项3|选项1)", "项目A(选项1|选项4)"]
    print(f"输入: {test_data5}")
    result5 = process_parentheses_list_advanced(test_data5, separator='|')
    print(f"使用'|'分隔符: {result5}")
    print()
    
    # 测试空字符串处理
    test_data6 = ["A(B/)", "C(/D)", "E(F/G)"]
    print(f"输入: {test_data6}")
    result6_keep = process_parentheses_list_advanced(test_data6, keep_empty=True)
    result6_filter = process_parentheses_list_advanced(test_data6, keep_empty=False)
    print(f"保留空字符串: {result6_keep}")
    print(f"过滤空字符串: {result6_filter}")


def process_file(input_file, output_file=None):
    """
    从文件读取数据并处理
    
    参数:
        input_file: 输入文件路径，每行一个 A(B/C) 格式的字符串
        output_file: 输出文件路径（可选）
        
    返回:
        tuple: (list_A, list_BC)
    """
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        list_A, list_BC = process_parentheses_list(lines)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("=== 处理结果 ===\n\n")
                f.write(f"输入数据 ({len(lines)} 行):\n")
                for line in lines:
                    f.write(f"  {line}\n")
                
                f.write(f"\nA列表 ({len(list_A)} 项):\n")
                for item in list_A:
                    f.write(f"  {item}\n")
                
                f.write(f"\nBC列表 ({len(list_BC)} 项):\n")
                for item in list_BC:
                    f.write(f"  {item}\n")
            
            print(f"结果已保存到: {output_file}")
        
        return list_A, list_BC
        
    except FileNotFoundError:
        print(f"错误: 文件不存在: {input_file}")
        return [], []
    except Exception as e:
        print(f"错误: 处理文件时出错: {e}")
        return [], []


def main():
    """主函数：命令行接口"""
    
    import sys
    
    if len(sys.argv) > 1:
        # 命令行模式
        if sys.argv[1] == "--test":
            test_examples()
        elif sys.argv[1] == "--file" and len(sys.argv) > 2:
            input_file = sys.argv[2]
            output_file = sys.argv[3] if len(sys.argv) > 3 else None
            process_file(input_file, output_file)
        elif sys.argv[1] == "--help":
            print("用法:")
            print("  python script.py                    # 交互模式")
            print("  python script.py --test             # 运行测试")
            print("  python script.py --file <输入文件> [输出文件]  # 处理文件")
            print("  python script.py --help             # 显示帮助")
    else:
        # 交互模式
        print("=== A(B/C) 格式列表处理器 ===")
        print("输入 A(B/C) 格式的字符串，每行一个，空行结束:")
        
        input_lines = []
        while True:
            try:
                line = input("> ").strip()
                if not line:
                    break
                input_lines.append(line)
            except EOFError:
                break
        
        if input_lines:
            list_A, list_BC = process_parentheses_list(input_lines)
            
            print(f"\n=== 处理结果 ===")
            print(f"输入数据: {len(input_lines)} 项")
            print(f"A列表 ({len(list_A)} 项): {list_A}")
            print(f"BC列表 ({len(list_BC)} 项): {list_BC}")
            
            # 询问是否保存到文件
            save = input("\n是否保存结果到文件? (y/N): ").strip().lower()
            if save == 'y':
                filename = input("文件名 (默认: output.txt): ").strip()
                if not filename:
                    filename = "output.txt"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("输入数据:\n")
                    for line in input_lines:
                        f.write(f"  {line}\n")
                    f.write(f"\nA列表:\n")
                    for item in list_A:
                        f.write(f"  {item}\n")
                    f.write(f"\nBC列表:\n")
                    for item in list_BC:
                        f.write(f"  {item}\n")
                
                print(f"结果已保存到: {filename}")
        else:
            print("没有输入数据")


if __name__ == "__main__":
    # 运行测试
    test_examples()