#!/usr/bin/env python3
import os
import re

PROJECTS_DIR = "/workspace/data-analytics-platform/projects"

# 参考答案数据
ANSWERS = {
    "project1.html": '''import pandas as pd

data = [
    {"订单ID": "ORD001", "日期": "2024-01-15", "商品名": "无线耳机", "数量": 2, "单价": 299, "地区": "北京"},
    {"订单ID": "ORD002", "日期": "01/16/2024", "商品名": "机械键盘", "数量": 1, "单价": 499, "地区": "上海"},
    {"订单ID": "ORD003", "日期": "2024-01-17", "商品名": None, "数量": 3, "单价": 199, "地区": "广州"},
    {"订单ID": "ORD004", "日期": "01/18/2024", "商品名": "智能手表", "数量": -1, "单价": 1299, "地区": "深圳"},
    {"订单ID": "ORD005", "日期": "2024-01-19", "商品名": "蓝牙音箱", "数量": 1, "单价": None, "地区": "杭州"},
    {"订单ID": "ORD006", "日期": "01/20/2024", "商品名": "笔记本电脑", "数量": 1, "单价": 5999, "地区": "北京"},
    {"订单ID": "ORD007", "日期": "2024-01-21", "商品名": "平板电脑", "数量": -2, "单价": 2999, "地区": "上海"},
    {"订单ID": "ORD008", "日期": "01/22/2024", "商品名": "移动电源", "数量": 5, "单价": 99, "地区": None},
    {"订单ID": "ORD009", "日期": "2024-01-23", "商品名": "数据线", "数量": 10, "单价": 19, "地区": "成都"},
    {"订单ID": "ORD010", "日期": "01/24/2024", "商品名": "充电器", "数量": 2, "单价": 59, "地区": "武汉"},
]

df = pd.DataFrame(data)
print("【原始数据】")
print(df.to_string(index=False))

df = df[df['数量'] >= 0]
print("\\n【删除异常行后】")
print(df.to_string(index=False))

df['日期'] = pd.to_datetime(df['日期'], errors='coerce').dt.strftime('%Y-%m-%d')
print("\\n【统一日期格式后】")
print(df.to_string(index=False))''',
    "project2.html": '''import pandas as pd

data = [
    {"区域": "华东", "月份": "1月", "销售额": 1850},
    {"区域": "华东", "月份": "2月", "销售额": 1680},
    {"区域": "华东", "月份": "3月", "销售额": 1920},
    {"区域": "华东", "月份": "4月", "销售额": 2100},
    {"区域": "华东", "月份": "5月", "销售额": 2250},
    {"区域": "华东", "月份": "6月", "销售额": 2380},
    {"区域": "华南", "月份": "1月", "销售额": 1520},
    {"区域": "华南", "月份": "2月", "销售额": 1380},
    {"区域": "华南", "月份": "3月", "销售额": 1650},
    {"区域": "华南", "月份": "4月", "销售额": 1780},
    {"区域": "华南", "月份": "5月", "销售额": 1920},
    {"区域": "华南", "月份": "6月", "销售额": 2050},
    {"区域": "华北", "月份": "1月", "销售额": 1380},
    {"区域": "华北", "月份": "2月", "销售额": 1250},
    {"区域": "华北", "月份": "3月", "销售额": 1520},
    {"区域": "华北", "月份": "4月", "销售额": 1650},
    {"区域": "华北", "月份": "5月", "销售额": 1780},
    {"区域": "华北", "月份": "6月", "销售额": 1850},
    {"区域": "西南", "月份": "1月", "销售额": 980},
    {"区域": "西南", "月份": "2月", "销售额": 850},
    {"区域": "西南", "月份": "3月", "销售额": 1050},
    {"区域": "西南", "月份": "4月", "销售额": 1180},
    {"区域": "西南", "月份": "5月", "销售额": 1320},
    {"区域": "西南", "月份": "6月", "销售额": 1450},
    {"区域": "西北", "月份": "1月", "销售额": 720},
    {"区域": "西北", "月份": "2月", "销售额": 650},
    {"区域": "西北", "月份": "3月", "销售额": 820},
    {"区域": "西北", "月份": "4月", "销售额": 950},
    {"区域": "西北", "月份": "5月", "销售额": 1080},
    {"区域": "西北", "月份": "6月", "销售额": 1150},
    {"区域": "东北", "月份": "1月", "销售额": 1120},
    {"区域": "东北", "月份": "2月", "销售额": 980},
    {"区域": "东北", "月份": "3月", "销售额": 1250},
    {"区域": "东北", "月份": "4月", "销售额": 1380},
    {"区域": "东北", "月份": "5月", "销售额": 1520},
    {"区域": "东北", "月份": "6月", "销售额": 1650},
]

df = pd.DataFrame(data)

region_sales = df.groupby('区域')['销售额'].sum().reset_index()
top3 = region_sales.sort_values('销售额', ascending=False).head(3)

print("【销售额最高的3个区域】")
print(top3.to_string(index=False))''',
}

def update_project_file(filepath, answer_code):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加复制按钮样式
    if '.btn-answer {' in content and '.btn-copy {' not in content:
        content = content.replace(
            '.btn-answer:hover {\n            background: #d97706;\n        }',
            '.btn-answer:hover {\n            background: #d97706;\n        }\n        \n        .btn-copy {\n            background: #3b82f6;\n            color: white;\n        }\n        \n        .btn-copy:hover {\n            background: #2563eb;\n        }'
        )
    
    # 添加复制按钮到工具栏
    if '<button class="btn-fullscreen"' in content and '<button class="btn-copy"' not in content:
        content = content.replace(
            '<button class="btn-answer" onclick="toggleAnswer()">\n                            <i class="fas fa-lightbulb"></i> 参考答案\n                        </button>\n                        <button class="btn-fullscreen"',
            '<button class="btn-answer" onclick="toggleAnswer()">\n                            <i class="fas fa-lightbulb"></i> 参考答案\n                        </button>\n                        <button class="btn-copy" onclick="copyAnswer()">\n                            <i class="fas fa-clipboard"></i> 复制\n                        </button>\n                        <button class="btn-fullscreen"'
        )
    
    # 转义参考答案代码
    answer_code_escaped = answer_code.replace("\\", "\\\\").replace("`", "\\`")
    
    # 更新answerCode变量
    if 'const defaultCode =' in content:
        content = re.sub(
            r'(const defaultCode = `[^`]*`;\n)\s*(const answerCode = `[^`]*`;)?',
            f'\\1        const answerCode = `{answer_code_escaped}`;',
            content
        )
    else:
        # 直接在defaultCode后面添加
        content = content.replace(
            'const defaultCode =',
            f'const defaultCode = `{answer_code_escaped}`;\n        const answerCode = `{answer_code_escaped}`;'
        )
    
    # 添加copyAnswer函数
    if 'function toggleAnswer() {' in content and 'function copyAnswer() {' not in content:
        content = content.replace(
            'function toggleAnswer() {\n            const answerSection = document.getElementById(\'answer-section\');\n            if (answerSection.style.display === \'none\') {\n                answerSection.style.display = \'block\';\n            } else {\n                answerSection.style.display = \'none\';\n            }\n        }',
            'function toggleAnswer() {\n            const answerSection = document.getElementById(\'answer-section\');\n            if (answerSection.style.display === \'none\') {\n                answerSection.style.display = \'block\';\n            } else {\n                answerSection.style.display = \'none\';\n            }\n        }\n        \n        function copyAnswer() {\n            editor.setValue(answerCode);\n            const btn = event.target.closest(\'button\');\n            const originalHTML = btn.innerHTML;\n            btn.innerHTML = \'<i class="fas fa-check"></i> 已复制\';\n            setTimeout(() => {\n                btn.innerHTML = originalHTML;\n            }, 1500);\n        }'
        )
    
    # 更新answer-section中的显示内容
    answer_code_display = answer_code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    content = re.sub(
        r'<pre style="background:#e0f2fe; padding:12px; border-radius:6px; margin:0;">.*?</pre>',
        f'<pre style="background:#e0f2fe; padding:12px; border-radius:6px; margin:0;">{answer_code_display}</pre>',
        content,
        flags=re.DOTALL
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ 已更新 {os.path.basename(filepath)}")

def main():
    for filename, answer_code in ANSWERS.items():
        filepath = os.path.join(PROJECTS_DIR, filename)
        if os.path.exists(filepath):
            update_project_file(filepath, answer_code)
    
    print("\n所有项目文件已更新！")

if __name__ == "__main__":
    main()
