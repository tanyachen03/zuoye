#!/usr/bin/env python3
"""生成可部署到 Cloudflare Pages 的纯静态站点"""
import os
import shutil
import re

# 目录设置
PAGES_DIR = "/workspace/pages"
STATIC_DIR = "/workspace/static"
BUILD_DIR = "/workspace"  # 直接输出到工作目录根

# 课程数据（每门课程有3章）
COURSES = [
    ("course1", "Python编程基础", ["Python环境搭建", "基础语法与数据类型", "控制流程与函数"], [1, 2, 3]),
    ("course2", "NumPy数据分析", ["NumPy基础入门", "数组操作与运算", "高级技巧与实战"], [4, 5, 6]),
    ("course3", "Pandas数据处理", ["Pandas基础入门", "数据清洗与转换", "分组聚合与高级操作"], [7, 8, 9]),
    ("course4", "数据可视化", ["Matplotlib基础", "Seaborn高级图表", "交互式可视化"], [10, 11, 12]),
    ("course5", "统计分析基础", ["描述性统计", "推断统计与假设检验", "回归分析"], [13, 14, 15]),
    ("course6", "机器学习入门", ["机器学习概述", "监督学习算法", "无监督学习与模型评估"], [16, 17, 18]),
    ("course7", "商业数据分析", ["销售数据分析", "客户行为分析", "商业智能与决策"], [19, 20, 21]),
    ("course8", "实战项目演练", ["销售数据分析项目", "客户分群分析项目", "综合项目实战"], [22, 23, 24]),
]

PROJECTS = [
    ("销售数据分析", "分析销售数据趋势，找出业绩增长点", "初级", "10小时", ["Python", "Pandas", "数据可视化"]),
    ("客户分群分析", "使用RFM模型对客户进行分群分析", "中级", "15小时", ["Python", "聚类算法", "RFM分析"]),
    ("市场篮子分析", "商品关联规则挖掘，优化商品摆放", "中级", "12小时", ["Python", "关联规则", "Apriori"]),
    ("用户流失预测", "构建机器学习模型预测客户流失", "高级", "20小时", ["Python", "Scikit-learn", "分类算法"]),
    ("销售预测建模", "使用时间序列分析预测未来销售", "高级", "18小时", ["Python", "时间序列", "回归分析"]),
    ("产品推荐系统", "构建个性化产品推荐引擎", "高级", "22小时", ["Python", "推荐算法", "协同过滤"]),
    ("价格优化分析", "基于数据的产品定价策略分析", "中级", "14小时", ["Python", "回归分析", "定价模型"]),
    ("库存优化分析", "数据驱动的库存管理与补货策略", "中级", "12小时", ["Python", "库存模型", "优化算法"]),
    ("营销效果分析", "评估营销活动ROI与转化分析", "初级", "10小时", ["Python", "A/B测试", "转化率分析"]),
    ("综合商业分析", "端到端商业数据分析完整案例", "高级", "25小时", ["Python", "综合分析", "商业报告"]),
]

# 每章数据: (title, sections, exercises, practices)
# sections: [(标题, 内容), ...]
# exercises: [(题目, A, B, C, D, 正确答案, 解析), ...]
# practices: [(标题, 难度, [步骤,...]), ...]
CHAPTERS_DATA = {
    1: (
        "Python环境搭建",
        [("Python语言介绍", "Python是一门简洁易学的高级编程语言，广泛应用于数据分析、人工智能、Web开发等领域。它拥有丰富的第三方库，是数据分析师必备的工具。"),
         ("安装Python环境", "从Python官网下载安装包，选择3.x最新版本。Windows用户安装时请勾选\"Add Python to PATH\"选项。安装完成后在终端输入 python --version 验证。"),
         ("配置开发工具", "推荐使用VS Code或PyCharm作为Python开发工具。安装后配置Python解释器路径，安装Python扩展插件以获得代码补全、语法高亮等功能。"),
         ("第一个Python程序", "打开文本编辑器，输入 print(\"Hello, Python!\")，保存为 hello.py。在终端运行 python hello.py，你将看到输出信息。"),
         ("包管理器pip", "pip是Python的包管理工具。使用 pip install package_name 安装第三方库，如 pip install pandas。使用 pip list 查看已安装的包。")],
        [("以下哪个命令用于检查Python版本？", "python --check", "python --version", "python -v", "python --info", "B", "python --version 或 python -V 是查看Python版本的标准命令。"),
         ("pip install numpy 命令的作用是？", "卸载numpy", "更新numpy", "安装numpy", "查看numpy", "C", "pip install 命令用于安装第三方Python包。"),
         ("Python代码文件的扩展名是？", ".pt", ".py", ".python", ".txt", "B", "Python代码文件使用 .py 作为标准扩展名。"),
         ("推荐用于Python开发的工具不包括？", "VS Code", "PyCharm", "记事本", "Jupyter", "C", "记事本没有代码高亮和调试功能，不适合专业开发。推荐使用VS Code、PyCharm或Jupyter。"),
         ("执行Python脚本的命令是？", "python script.py", "run script.py", "execute script.py", "./script.py run", "A", "python filename.py 是执行Python脚本的标准方式。")],
        [("安装并验证Python环境", "初级", ["在你的电脑上安装Python 3.x最新版本", "打开终端/命令行，输入 python --version 和 pip --version", "确认两者都能正常显示版本信息", "将输出结果记录下来"]),
         ("编写并运行Hello World程序", "初级", ["创建一个名为 hello.py 的文件", "写入打印\"Hello, 数析学院！\"的代码", "通过命令行运行该脚本，确认输出正确", "尝试修改打印的内容并重新运行"]),
         ("使用pip安装一个数据分析包", "中级", ["使用 pip install pandas 安装Pandas库", "安装完成后运行 pip list 确认安装成功", "启动Python交互模式（输入 python）", "输入 import pandas as pd 测试是否能正常导入"])],
    ),
    2: (
        "基础语法与数据类型",
        [("变量与赋值", "变量是存储数据的容器。在Python中，变量不需要声明类型，直接赋值即可。例如：name = \"张三\"，age = 25，price = 99.9。"),
         ("数字类型与运算", "Python支持整数(int)、浮点数(float)、复数(complex)。运算符包括 + 加、- 减、* 乘、/ 除、// 整除、% 取余、** 幂运算。"),
         ("字符串操作", "字符串用单引号或双引号包裹。常用操作：拼接 +、重复 *、索引 []、切片 [:]、len() 长度、.upper() 大写、.lower() 小写。"),
         ("列表与元组", "列表 list 用 [] 创建，可修改、可混合类型。元组 tuple 用 () 创建，不可修改。常用方法：append() 添加、pop() 删除、len() 长度。"),
         ("字典与集合", "字典 dict 用 {} 创建，键值对存储。person = {\"name\": \"张三\", \"age\": 25}。集合 set 用 set() 创建，自动去重，支持交并差运算。")],
        [("以下哪个是合法的Python变量名？", "2name", "my-name", "my_name", "my name", "C", "变量名必须以字母或下划线开头，不能有空格和特殊字符（除下划线）。"),
         ("执行 print(10 // 3) 的结果是？", "3.333", "3", "4", "1", "B", "// 是整除运算符，返回商的整数部分。10除以3商为3。"),
         ("list1 = [1,2,3], print(list1[-1]) 输出？", "1", "2", "3", "报错", "C", "-1 表示最后一个元素。列表索引支持负数，从末尾向前数。"),
         ("dict1 = {\"a\": 1, \"b\": 2}, 如何获取值2？", "dict1[\"b\"]", "dict1.b", "dict1(2)", "dict1->b", "A", "字典通过 字典名[\"键名\"] 访问值。也可用 dict1.get(\"b\")。"),
         ("s = \"Hello\", 哪个方法转为大写？", "s.upper()", "s.up()", "upper(s)", "s.toUpper()", "A", "字符串对象的 .upper() 方法将字符串转为大写。")],
        [("数字计算器练习", "初级", ["定义两个数字变量 a = 15，b = 4", "分别计算并打印它们的和、差、积、商、整除结果、余数", "计算 a 的 b 次方", "观察每种运算的结果类型"]),
         ("字符串处理练习", "初级", ["创建字符串 s = \"Python数据分析很有趣\"", "打印字符串长度", "打印前6个字符", "将字符串全部转为大写", "用\"很\"字分割字符串"]),
         ("学生信息管理", "中级", ["创建一个字典 student 包含 name、age、major、scores四个键", "scores 是一个列表，包含3个成绩数值", "打印学生姓名和各科成绩", "修改 age 的值为一个新数值", "计算 scores 的平均分并打印"])],
    ),
    3: (
        "控制流程与函数",
        [("条件语句 if-elif-else", "if 条件: 语句块用于分支判断。条件为 True 时执行缩进的代码块。elif 可以添加多个条件分支，else 处理所有其他情况。"),
         ("for循环与while循环", "for item in iterable: 遍历可迭代对象。配合 range() 可以生成数字序列。while 条件: 循环直到条件为False。循环中可用 break 跳出、continue 跳过。"),
         ("函数定义与参数", "def 函数名(参数): 定义函数。函数可以有位置参数、默认参数、可变参数 *args、关键字参数 **kwargs。调用函数时根据定义传入参数。"),
         ("函数返回值与作用域", "return 语句从函数返回值。不写 return 默认返回 None。作用域：函数内定义的变量是局部变量，函数外是全局变量。用 global 声明全局变量。"),
         ("模块导入与包管理", "import module 导入模块；from module import func 导入指定函数。Python标准库有丰富模块如 math、random、datetime。第三方包需先用 pip 安装再导入。")],
        [("for i in range(1, 4): print(i) 输出？", "1 2 3 4", "1 2 3", "0 1 2 3", "0 1 2", "B", "range(1, 4) 生成 1, 2, 3，不含结束值。Python的 range 是左闭右开区间。"),
         ("函数中不写return语句，默认返回？", "0", "空字符串", "None", "报错", "C", "Python函数如果没有return语句，或return后没有值，默认返回 None。"),
         ("以下哪种写法可以无限循环？", "for i in range(inf):", "while True:", "for True:", "loop:", "B", "while True: 创建无限循环。需要在循环内使用 break 语句来退出。"),
         ("如何从模块导入特定函数？", "import func from module", "from module import func", "include module.func", "use module.func", "B", "Python使用 from 模块 import 函数 的语法从指定模块导入函数。"),
         ("执行 3 > 2 and 1 < 0 的结果？", "True", "False", "报错", "None", "B", "3>2为True，但1<0为False。and 需要两边都为True，结果为False。")],
        [("成绩等级判断器", "初级", ["编写一个函数 get_grade(score)，接收分数(0-100)", "使用 if-elif-else 判断并返回等级", "90以上\"A\"，80-89\"B\"，70-79\"C\"，60-69\"D\"，60以下\"E\"", "测试多个分数，验证返回结果是否正确"]),
         ("数字列表统计分析", "初级", ["创建一个包含20个随机整数的列表（1到100之间）", "打印所有元素", "统计并打印最大值、最小值、总和、平均值", "筛选并打印所有大于平均值的数", "将列表按降序排序并打印"]),
         ("自定义模块与函数", "中级", ["创建一个名为 math_utils.py 的文件", "在其中编写 is_prime(n) 判断是否为素数的函数", "再编写 factorial(n) 计算阶乘的函数", "创建另一个Python文件测试这两个函数"])],
    ),
    4: (
        "NumPy基础入门",
        [("NumPy介绍", "NumPy是Python科学计算的基础包。它提供高性能的多维数组对象ndarray以及广播功能函数。相比Python列表，NumPy数组运算更快、内存更省。"),
         ("创建数组", "使用 np.array(list) 从列表创建数组。np.zeros(shape) 创建全零数组，np.ones(shape) 创建全一数组，np.arange(start, stop, step) 创建序列数组。"),
         ("数组属性", "ndarray.shape 返回数组维度元组，.ndim 返回维度数，.size 返回元素总数，.dtype 返回数据类型（int32、float64等）。可以用 reshape() 改变数组形状。"),
         ("基本运算", "NumPy数组支持逐元素运算。两个数组的 + - * / 都是对应位置运算。与标量的运算会广播到所有元素。矩阵乘法用 @ 或 np.dot()。"),
         ("索引与切片", "一维数组索引与Python列表类似：arr[0]，arr[-1]，arr[1:4]。二维数组：arr[0, 1] 第0行第1列，arr[:, 1] 第1列全部，arr[1:3, :] 第1-2行。")],
        [("np.zeros((3, 4)) 创建的数组形状是？", "(4, 3)", "(3, 4)", "12个元素的一维数组", "(3, 3)", "B", "参数 (3, 4) 表示3行4列。shape返回的元组中行数在前，列数在后。"),
         ("arr = np.array([1,2,3]), arr.dtype 是？", "float64", "int32或int64", "string", "object", "B", "整数列表创建的NumPy数组默认是整型，具体为int32或int64（取决于系统）。"),
         ("arr = np.array([[1,2],[3,4]]), arr[1,0] 值为？", "1", "2", "3", "4", "C", "索引 [1, 0] 表示第1行第0列。NumPy索引从0开始，结果为3。"),
         ("np.arange(0, 10, 2) 包含几个元素？", "4", "5", "6", "10", "B", "从0开始，步长为2：0, 2, 4, 6, 8，共5个元素。不包含10，因为arange是左闭右开区间。"),
         ("两个形状相同的数组 * 运算结果是？", "矩阵乘法", "对应元素相乘", "报错", "数组拼接", "B", "* 在NumPy中是逐元素相乘。真正的矩阵乘法使用 @ 运算符或 np.dot() 函数。")],
        [("NumPy数组基础操作", "初级", ["创建一个形状为 (4, 5) 的二维数组，元素为1到20的连续整数", "打印数组的shape、ndim、size、dtype属性", "提取第2行元素并打印", "提取第3列元素并打印", "将数组转为一维后打印"]),
         ("数组运算与统计", "初级", ["生成一个包含50个0到100之间随机整数的一维数组", "使用NumPy计算数组的总和、平均值、标准差、方差", "找出最大值和最小值及其位置索引", "将所有大于平均值的元素替换为1，其余替换为0"]),
         ("矩阵运算练习", "中级", ["创建两个 3×3 的矩阵 A 和 B（元素自定义）", "计算 A + B、A - B", "计算 A * B（逐元素相乘）和 A @ B（矩阵乘法），观察区别", "计算 A 的转置 A.T 和逆矩阵 np.linalg.inv(A)", "计算 A 的行列式值和对角线元素之和"])],
    ),
    5: (
        "数组操作与运算",
        [("数组变形 reshape", "reshape() 改变数组形状但保持元素总数不变。arr.reshape(3, 4) 将数组变为3行4列。参数 -1 可以自动计算维度，如 arr.reshape(2, -1) 自动计算列数。"),
         ("数组拼接与分割", "np.concatenate([a, b], axis=0) 沿轴拼接数组。np.vstack([a, b]) 垂直堆叠（行方向），np.hstack([a, b]) 水平堆叠（列方向）。np.split() 可将数组分割为多个子数组。"),
         ("广播机制", "当不同形状的数组进行运算时，NumPy会自动扩展维度较小的数组使其匹配维度较大的数组。例如形状为 (3, 4) 的数组与标量运算，标量被广播到每个元素。"),
         ("统计函数", "NumPy提供丰富的统计函数：np.sum() 求和，np.mean() 均值，np.std() 标准差，np.var() 方差，np.max()/np.min() 最值，np.argmax()/np.argmin() 最值索引，np.median() 中位数。"),
         ("条件索引与筛选", "布尔索引：arr[arr > 5] 返回所有大于5的元素。np.where(cond, x, y) 根据条件选择值。np.any() 检查是否有True，np.all() 检查是否全为True。")],
        [("arr = np.arange(12).reshape(3, -1), shape是？", "(3, 3)", "(3, 4)", "(4, 3)", "(3, 12)", "B", "12个元素重塑为3行，-1自动计算列数：12/3=4列。所以shape为(3, 4)。"),
         ("形状 (3,1) 和 (1,4) 的数组相加结果形状？", "(3, 4)", "(1, 1)", "报错", "(3, 1)", "A", "这是广播机制：(3,1)扩展为(3,4)，(1,4)扩展为(3,4)，结果形状(3,4)。"),
         ("np.argmax([3, 1, 4, 1, 5, 9, 2]) 返回？", "9", "5", "[9]", "\"max\"", "B", "argmax 返回最大值所在的索引。最大值9在索引5处（从0开始）。"),
         ("np.concatenate([a, b], axis=1) 效果是？", "行方向拼接", "列方向拼接", "报错", "合并成一维", "B", "axis=1 表示沿第1轴（列方向）拼接。axis=0沿行方向，axis=1沿列方向。"),
         ("arr[[False, True, True]] 返回？假设arr=[1,2,3]", "[1, 2, 3]", "[2, 3]", "[1]", "[True, True]", "B", "布尔索引只保留对应位置为True的元素。索引1和2为True，返回[2, 3]。")],
        [("二维数组的变形与转置", "初级", ["创建一个 2×6 的二维数组，元素为1到12的连续整数", "使用 reshape 转为 3×4 并打印", "使用 reshape(-1, 3) 自动计算行数并打印结果", "将原数组转置（行变列）并打印", "将数组展平为一维后打印"]),
         ("多个数组的拼接与分割", "中级", ["创建两个 2×3 的数组A和B", "沿行方向（垂直）拼接并打印", "沿列方向（水平）拼接并打印", "创建一个 6×6 的随机数组", "将数组沿行方向平均分割为3个数组并打印第一个"]),
         ("条件筛选与统计分析", "中级", ["生成一个 5×10 的随机整数数组（范围0-100）", "找出所有大于50的元素及数量", "将大于70的元素替换为70，小于30的替换为30", "计算每行的平均值", "找出每列最大值所在的行号"])],
    ),
    6: (
        "NumPy高级技巧",
        [("条件索引高级", "组合多个条件：arr[(arr > 3) & (arr < 10)] 同时满足两个条件（注意用 & 而不是 and，| 代替 or）。np.select() 根据条件列表选择值列表。"),
         ("文件读写", "np.save(\"file.npy\", arr) 将数组保存为二进制文件，np.load(\"file.npy\") 加载。np.savetxt(\"data.csv\", arr, delimiter=\",\") 保存为文本CSV格式，np.loadtxt() 读取。"),
         ("性能优化技巧", "尽量避免Python循环，使用NumPy向量化运算。使用内置函数（如np.sum而非自己写循环）。了解 .copy() 与视图的区别避免意外修改。合理设置 dtype 节省内存。"),
         ("随机数生成", "np.random 模块提供丰富的随机数函数。np.random.rand(n) 均匀分布[0,1)，np.random.randn(n) 标准正态分布，np.random.randint(low, high, size) 随机整数。"),
         ("综合实战案例", "使用NumPy进行数据分析的完整流程：加载数据 → 数据探查（形状、统计量）→ 数据清洗（缺失值、异常值处理）→ 统计分析 → 结果输出。通过真实数据集应用所学知识。")],
        [("保存NumPy数组为二进制文件用哪个函数？", "np.write()", "np.save()", "np.store()", "np.dump()", "B", "np.save() 将数组保存为 .npy 二进制格式，对应 np.load() 加载。"),
         ("切片产生的是视图还是副本？", "视图，修改会影响原数组", "副本，互不影响", "两者都是", "随机", "A", "切片产生的是视图（view）而非副本，修改视图会影响原数组。需要副本时用 .copy()。"),
         ("生成3个标准正态分布随机数用？", "np.random.rand(3)", "np.random.randn(3)", "np.random.normal(3)", "np.random(3)", "B", "np.random.randn() 生成标准正态分布(均值0方差1)。np.random.rand()是均匀分布[0,1)。"),
         ("arr[arr > 3] 使用了哪种索引方式？", "位置索引", "切片索引", "布尔索引", "花式索引", "C", "传入布尔数组作为索引的方式叫布尔索引，用于根据条件筛选元素。"),
         ("为什么NumPy比Python列表运算快？", "使用了GPU", "向量化运算+C实现", "用了多线程", "不消耗内存", "B", "NumPy运算在连续内存块上执行，用C实现，避免了Python循环的解释器开销，称为向量化运算。")],
        [("数据分析完整流程", "中级", ["生成一个包含100个样本的数据集，每个样本包含3个特征（模拟学生成绩）", "创建形状为(100, 3)的随机整数数组", "计算每个学生的三科平均分", "找出平均分最高和最低的学生索引", "统计每科成绩的平均分和标准差", "将数据保存为CSV文件"]),
         ("随机数模拟实验", "中级", ["编写一个模拟投硬币的程序", "使用np.random.randint(0, 2, size=1000)模拟投1000次硬币（0反面1正面）", "计算正面出现的比例并与0.5比较", "模拟10000次和100000次，观察比例变化", "用柱状图或文字展示各结果"]),
         ("矩阵图像处理模拟", "高级", ["创建一个100×100的随机矩阵模拟图像像素值", "对矩阵应用简单的平滑操作：每个像素替换为其与相邻8个像素的平均值", "将大于平均值的像素设为255（白），其余设为0（黑）实现二值化", "统计两种像素的数量比例", "尝试对不同大小的矩阵执行相同操作"])],
    ),
}

CHAPTERS_PART2 = {
    7: (
        "Pandas基础入门",
        [("Pandas介绍", "Pandas是基于NumPy构建的数据分析库，提供两种核心数据结构：Series（一维带标签数组）和DataFrame（二维表格）。它简化了数据加载、清洗、转换、聚合等操作。"),
         ("创建和访问 Series", "pd.Series(data, index=labels) 创建Series，数据可以是列表、字典或数组。访问方式：s[\"index_label\"] 按标签索引，s[0] 按位置索引，s.iloc[0] 整数位置，s.loc[\"label\"] 标签索引。"),
         ("创建和访问 DataFrame", "pd.DataFrame(dict_of_lists) 或 pd.DataFrame(array, columns=col_names) 创建DataFrame。df[\"col_name\"] 或 df.col_name 访问列，df.loc[row_label, col_name] 按标签访问单元格。"),
         ("读取和写入数据", "pd.read_csv(\"file.csv\") 读取CSV文件，pd.read_excel(\"file.xlsx\") 读取Excel。df.to_csv(\"out.csv\", index=False) 保存为CSV。其他支持格式：JSON、SQL、Parquet等。"),
         ("基本数据探索", "df.head(n) 查看前n行，df.tail(n) 查看后n行。df.shape 返回形状，df.columns 查看列名，df.info() 查看数据结构。df.describe() 生成描述性统计（数值列的均值、分位数等）。")],
        [("Pandas的两个主要数据结构是？", "List和Dict", "Series和DataFrame", "Array和Matrix", "Table和Row", "B", "Series是一维带标签的数据结构，DataFrame是二维表格结构。两者是Pandas的核心。"),
         ("读取CSV文件的函数是？", "pd.load_csv()", "pd.read_csv()", "pd.open_csv()", "pd.csv()", "B", "pd.read_csv() 是读取CSV文件的标准函数，类似的还有 read_excel、read_json 等。"),
         ("df.loc 是根据什么选择数据？", "整数位置", "标签/索引名", "条件表达式", "列号", "B", "loc 使用标签索引（行名/列名）。iloc 使用整数位置索引。两者不要混淆！"),
         ("df.describe() 对什么列生成统计？", "所有列", "仅数值列", "仅文本列", "仅日期列", "B", "describe() 默认只对数值列生成描述性统计（计数、均值、标准差、分位数等）。"),
         ("如何获取DataFrame的行数？", "df.length", "df.size", "len(df)", "df.rows", "C", "len(df) 返回行数。df.shape 返回(行数, 列数)元组，df.size 返回总元素数（行×列）。")],
        [("Series创建与操作", "初级", ["创建一个Series，包含5种水果名称及其价格（索引为水果名，值为价格）", "打印Series查看数据", "通过索引访问一种水果的价格", "筛选出价格大于某个阈值的水果", "计算所有水果的平均价格"]),
         ("学生成绩DataFrame分析", "初级", ["创建一个DataFrame模拟10个学生的3科成绩（语文、数学、英语）", "打印前5行数据", "查看数据的shape、columns、dtypes", "查看数学成绩列", "查看第3名学生的所有成绩", "生成描述性统计信息（平均分、标准差等）"]),
         ("CSV数据读写实战", "中级", ["创建一个DataFrame，包含日期、产品、销量、金额四列，至少10行数据", "将数据保存为 sales.csv 文件（使用to_csv，不保存索引）", "用read_csv重新加载数据并打印确认", "对金额列求和计算总销售额", "按销量排序并打印Top 5"])],
    ),
    8: (
        "数据清洗与转换",
        [("处理缺失值", "df.isnull() 或 df.isna() 返回布尔掩码标记缺失值。df.dropna() 删除含缺失值的行或列，df.fillna(value) 用指定值填充，df.fillna(method=\"ffill\") 用前一个值填充（前向填充）。"),
         ("数据类型转换", "df[\"col\"].astype(new_type) 转换数据类型，如将字符串转为数字 int/float。pd.to_numeric(df[\"col\"], errors=\"coerce\") 安全转换（无法转换的设为NaN）。pd.to_datetime() 将字符串解析为日期时间类型。"),
         ("数据筛选", "布尔筛选：df[df[\"age\"] > 18]。多条件组合：df[(df[\"age\"] > 18) & (df[\"score\"] < 90)]（每个条件必须加括号）。df.query(\"age > 18\") 使用字符串表达式筛选。"),
         ("数据排序", "df.sort_values(\"col_name\") 按列值排序，ascending=False 降序。df.sort_values([\"col1\", \"col2\"], ascending=[True, False]) 多列排序。df.sort_index() 按索引排序。排名函数 df[\"col\"].rank()。"),
         ("数据合并与连接", "pd.concat([df1, df2]) 简单拼接（按行或按列）。pd.merge(left, right, on=\"key\") 类似SQL的JOIN操作，支持inner/left/right/outer四种连接方式。")],
        [("删除含缺失值的行用哪个方法？", "df.nan_drop()", "df.dropna()", "df.clean()", "df.remove_na()", "B", "df.dropna() 删除包含NA/NaN的行或列。可用 axis 参数控制是删除行(0，默认)还是列(1)。"),
         ("df[\"a\"].fillna(0) 的作用是？", "将0替换为NaN", "将NaN替换为0", "查找0值", "删除0值", "B", "fillna(value) 将缺失值 NaN 用给定的 value 填充。也可以用字典为不同列指定不同填充值。"),
         ("筛选 age > 20 且 score < 80 的写法？", "df[age > 20 and score < 80]", "df[df[\"age\"]>20 and df[\"score\"]<80]", "df[(df[\"age\"]>20) & (df[\"score\"]<80)]", "df.where(age>20, score<80)", "C", "多条件筛选要用 & 代替 and，| 代替 or，且每个条件必须用括号！这是最常见的Pandas错误之一。"),
         ("df.sort_values(\"price\", ascending=False) 效果？", "按价格升序排序", "按价格降序排序", "按索引排序", "随机排序", "B", "ascending=False 指定降序排序（从大到小）。默认值True为升序。可以传入列表对多列排序。"),
         ("pd.merge(df1, df2, on=\"id\") 默认是？", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "FULL JOIN", "C", "merge 默认使用 inner 连接，即只保留两个表中id匹配的行。通过 how 参数可以指定 \"left\"、\"right\"、\"outer\" 等连接方式。")],
        [("缺失值处理练习", "初级", ["创建一个包含故意缺失值的DataFrame（如某些分数缺失）", "检查每列有多少个缺失值（df.isnull().sum()）", "用每列的平均值填充数值列的缺失值", "用前向填充方法填充其他列的缺失值", "删除任一包含缺失值的行，查看剩余行数"]),
         ("数据筛选与条件更新", "中级", ["模拟销售数据：创建含日期、产品、数量、单价、销售额（=数量×单价）的DataFrame（20行以上）", "筛选出销售额大于某个值的记录", "筛选某产品在特定日期范围的数据", "将单价小于某个值的记录标记为\"低价\"，其他标记为\"高价\"，新增一列", "按销售额降序排序并取前10行"]),
         ("多表连接实战", "中级", ["创建两个DataFrame：学生表 student(id, name, class_id) 包含10名学生", "班级表 class_info(class_id, class_name, teacher) 包含3个班级", "用merge将两表按 class_id 连接", "使用 left join 确保所有学生都保留", "使用 concat 垂直拼接两个班级的学生子表"])],
    ),
}

# 将PART2合并到主CHAPTERS_DATA
CHAPTERS_DATA.update(CHAPTERS_PART2)

# 简化的剩余章节数据（保持格式一致）
CHAPTERS_PART3 = {
    9: (
        "分组聚合与透视表",
        [("分组操作 groupby", "df.groupby(\"col\") 将数据按指定列分组，生成GroupBy对象。后续可以链式调用聚合函数。df.groupby([\"col1\", \"col2\"]) 多列分组。分组后默认分组键变为索引，可用 as_index=False 保持为列。"),
         ("聚合函数", "分组后常用聚合：.sum() 求和，.mean() 均值，.count() 计数，.max()/.min() 最值，.std() 标准差。.agg({\"col1\": \"sum\", \"col2\": [\"mean\", \"max\"]}) 对不同列应用不同聚合。"),
         ("透视表 pivot_table", "pd.pivot_table(df, values=\"val\", index=\"row_col\", columns=\"col_col\", aggfunc=\"mean\") 创建透视表。行由index列决定，列由columns列决定，values列进行聚合计算。类似Excel的数据透视表。"),
         ("时间序列处理", "pd.to_datetime(df[\"date_col\"]) 转换为日期时间类型后，可访问 .dt.year、.dt.month、.dt.day 等属性。df.resample(\"M\").mean() 按月重采样聚合。df.rolling(window=7).mean() 计算7日移动平均。"),
         ("综合案例：销售分析", "典型销售分析流程：加载数据 → 清洗（缺失值/类型转换）→ 日期字段解析 → 按时间/产品/地区多维度分组聚合 → 生成透视表看交叉分析 → 识别Top N产品/客户 → 时间序列看趋势。")],
        [("groupby 后默认分组列会成为？", "普通列", "索引", "被删除", "新列名加后缀", "B", "groupby 后分组键默认成为结果的索引。可以用 as_index=False 参数让分组键保持为普通列。"),
         ("df.groupby(\"dept\")[\"salary\"].mean() 计算？", "所有员工平均工资", "每个部门的平均工资", "工资的中位数", "部门数", "B", "先按部门分组，再对每组的工资列求平均值。结果是每个部门的平均工资。"),
         ("透视表 pivot_table 中 aggfunc 参数？", "分组列", "要聚合的值列", "聚合函数", "输出文件名", "C", "aggfunc 指定聚合函数，如 \"mean\"、\"sum\"、\"count\" 或自定义函数。可以传入列表同时应用多种函数。"),
         ("df[\"date\"].dt.year 提取什么？", "月份", "年份", "日期", "星期几", "B", ".dt 是Pandas日期时间列的访问器。dt.year 年份、dt.month 月份、dt.day 日期、dt.dayofweek 星期几（0=周一）。"),
         ("df.rolling(window=30).mean() 计算？", "30个数据的均值", "30天滚动均值", "前30行均值", "每月均值", "B", "rolling(window=30) 创建30期滚动窗口，.mean()计算每期窗口的均值。常用于计算移动平均线平滑时间序列波动。")],
        [("分组聚合分析销售数据", "中级", ["模拟一份完整的销售数据（DataFrame，至少30行）", "包含：日期、产品名（5种产品）、销售区域（3个区域）、数量、单价、销售额", "按产品分组，计算每种产品的总销量和总销售额", "按区域分组，计算每区域的平均单笔销售额", "按产品+区域双维度分组，计算每个组合的销售统计", "使用 agg 同时计算总和、均值、最大值"]),
         ("创建销售数据透视表", "中级", ["使用上面的销售数据", "创建以产品为行、区域为列的销量透视表", "创建以月份为行、产品为列的销售额透视表（先从日期提取月份）", "创建行多层级（区域+产品）、列为月份的多维度透视表", "添加 margins=True 查看汇总行列"]),
         ("时间序列数据分析", "高级", ["使用 pd.date_range 生成过去一年（365天）的日期索引", "创建每天销售额的时间序列数据（可用随机数模拟）", "按月份（\"M\"）重采样计算每月总销售额", "计算7日移动平均，观察趋势", "找出销售额最高/最低的10天", "按季度汇总销售额并分析季节性"])],
    ),
    10: (
        "Matplotlib基础绘图",
        [("Matplotlib介绍与设置", "Matplotlib是Python的基础绘图库，pyplot是其常用接口。import matplotlib.pyplot as plt 导入。支持折线图、柱状图、散点图、饼图、热力图等多种图形。使用 plt.style.use() 或 plt.rcParams 配置样式。"),
         ("折线图 plot", "plt.plot(x, y, marker=\"o\", label=\"标签\") 绘制折线图。marker 设置数据点样式，linewidth 线宽，color 颜色。plt.title() 标题，plt.xlabel()/plt.ylabel() 轴标签，plt.legend() 图例，plt.grid() 网格线。"),
         ("柱状图 bar", "plt.bar(x_pos, heights, width=0.6) 柱状图，plt.barh() 水平柱状图。用于展示分类数据的数值对比。设置 x_pos = range(len(categories))，再用 plt.xticks(x_pos, categories) 设置x轴标签。"),
         ("散点图 scatter", "plt.scatter(x, y, s=size, c=color, alpha=0.6) 散点图。s控制点大小，c控制点颜色（可以是数值数组），alpha控制透明度。用于观察两个变量之间的关系/聚类模式。"),
         ("饼图与组合图", "plt.pie(values, labels=labels, autopct=\"%1.1f%%\") 饼图。plt.subplots(rows, cols, figsize=(w, h)) 创建多子图布局。可以在同一图中组合多种图形类型，更丰富地展示数据。")],
        [("绘制折线图的函数是？", "plt.line()", "plt.plot()", "plt.linechart()", "plt.graph()", "B", "plt.plot() 是Matplotlib绘制折线图的核心函数。可以传入多组y值同时画多条线。"),
         ("plt.bar 主要用于？", "展示趋势变化", "展示分类数据对比", "展示变量关系", "展示分布", "B", "柱状图最适合比较不同类别间的数值大小。折线图展示趋势，散点图展示关系，直方图展示分布。"),
         ("散点图的 alpha 参数控制？", "点的大小", "点的形状", "透明度", "颜色", "C", "alpha 取值0-1，控制透明度。1为不透明，接近0为几乎透明。点很多时降低alpha可看清点的密度分布。"),
         ("添加图例的函数是？", "plt.label()", "plt.legend()", "plt.key()", "plt.title()", "B", "plt.legend() 添加图例。需要在绘图时为每条线/图形指定 label 参数，legend 会自动收集并显示。"),
         ("创建2行3列子图用哪个？", "plt.subplot(2, 3)", "plt.subplots(2, 3)", "plt.figure(2, 3)", "plt.grid(2, 3)", "B", "plt.subplots(rows, cols) 返回 (fig, axes) 元组。axes 是子图数组，可以用 axes[i,j] 或 axes.flat[i] 访问具体子图。")],
        [("月度销售趋势折线图", "初级", ["创建模拟的12个月销售数据（月份、销售额列表）", "使用 plt.plot 绘制折线图", "添加标题、x轴/ y轴标签", "在每个数据点处用 marker=\"o\" 显示圆点", "添加网格线", "在图上标注最高/最低点的数值"]),
         ("多产品销售对比柱状图", "初级", ["模拟5种产品的季度销售数据", "绘制各产品的总销售额柱状图", "将柱子设为不同颜色并添加图例", "在每个柱子上方显示具体数值", "尝试水平柱状图 plt.barh 展示", "绘制分组柱状图（每季度一组展示不同产品对比）"]),
         ("相关性分析热力图", "中级", ["创建一个包含多个数值列的DataFrame（模拟产品各项指标数据：价格、评分、销量、库存量等，100行样本）", "使用 df.corr() 计算各列的相关系数矩阵", "绘制相关性热力图（用matplotlib或seaborn）", "设置合适的配色方案，并在格子中显示相关系数值", "分析哪些变量之间存在强正/负相关"])],
    ),
}

CHAPTERS_DATA.update(CHAPTERS_PART3)

# 为章节11-24使用简化模板数据（保持页面一致可用）
CHAPTERS_SIMPLE = {}
for ch_num in range(11, 25):
    course_names = {
        (10,11,12): "数据可视化",
        (13,14,15): "统计分析基础",
        (16,17,18): "机器学习入门",
        (19,20,21): "商业数据分析",
        (22,23,24): "实战项目演练",
    }
    cname = ""
    for k, v in course_names.items():
        if ch_num in k:
            cname = v
            break

    titles = {
        11: "Seaborn高级图表", 12: "交互式可视化",
        13: "描述性统计", 14: "推断统计与假设检验", 15: "回归分析",
        16: "机器学习概述", 17: "监督学习算法", 18: "无监督学习与评估",
        19: "销售数据分析", 20: "客户行为分析", 21: "商业智能与决策",
        22: "销售数据项目", 23: "客户分群项目", 24: "综合项目实战",
    }
    sections = [
        ("核心概念" + str(i+1), f"本节介绍{titles[ch_num]}的核心知识要点{i+1}。通过实际案例讲解关键方法和应用场景，帮助你建立完整的知识体系。")
        for i in range(5)
    ]
    exercises = [
        (f"以下哪个概念与{titles[ch_num]}最相关？", "选项A内容示例", "选项B内容示例", "选项C内容示例", "选项D内容示例", "B",
         f"这是关于{titles[ch_num]}的核心知识点。B选项正确描述了本章学习内容的关键特征。"),
        (f"在实际分析中，{titles[ch_num]}常用于？", "数据存储", "数据展示和分析", "网络请求", "文件压缩", "B",
         f"{titles[ch_num]}是数据分析的重要环节，主要用于数据展示、模式发现和决策支持。"),
        (f"学习{titles[ch_num]}最重要的是？", "记住所有函数名", "理解原理并多练习", "等待他人指导", "通过考试", "B",
         "数据分析是实践性很强的技能，理解基本原理后通过大量练习才能真正掌握。"),
    ]
    practices = [
        (f"{titles[ch_num]}练习一", "初级",
         ["阅读本章相关理论内容", "查找并阅读2-3个实际案例", "尝试用简单例子验证概念", "记录学习笔记"]),
        (f"{titles[ch_num]}练习二", "中级",
         ["使用模拟数据集进行实操", "应用本章学到的核心方法", "对比不同参数的效果差异", "总结最佳实践"]),
        (f"{titles[ch_num]}综合练习", "高级",
         ["设计一个完整的分析流程", "收集或生成合适的测试数据", "应用本章技术完成分析", "撰写分析报告"]),
    ]
    CHAPTERS_SIMPLE[ch_num] = (titles[ch_num], sections, exercises, practices)

CHAPTERS_DATA.update(CHAPTERS_SIMPLE)

NAV_TEMPLATE = """<nav class="navbar">
            <div class="logo">数析学院</div>
            <div class="nav-links">
                <a href="index.html"{active_index}>首页</a>
                <a href="courses.html"{active_courses}>课程体系</a>
                <a href="projects.html"{active_projects}>项目实战</a>
            </div>
        </nav>"""

def generate_index():
    courses_html = ""
    for i, (cid, title, chapters, chapter_nums) in enumerate(COURSES, 1):
        icons = ["💻", "📊", "📈", "🎨", "📐", "🤖", "💼", "🎯"]
        levels = ["入门", "初级", "初级", "初级", "中级", "中级", "高级", "高级"]
        durations = ["8小时", "10小时", "12小时", "8小时", "10小时", "12小时", "15小时", "20小时"]
        icon = icons[i-1]
        level = levels[i-1]
        duration = durations[i-1]
        desc = {
            1: "从零开始学习Python编程语言，掌握数据分析必备的编程基础",
            2: "学习使用NumPy进行高效的数值计算和数组操作",
            3: "掌握Pandas库进行数据读取、清洗、筛选和聚合分析",
            4: "使用Matplotlib、Seaborn等工具创建专业的数据可视化图表",
            5: "学习统计学基础，掌握数据描述、假设检验和回归分析",
            6: "了解机器学习基本概念，掌握常用监督和无监督学习算法",
            7: "将数据分析技术应用于实际商业场景，提升商业决策能力",
            8: "通过完整项目案例，综合运用所学知识解决实际问题",
        }[i]
        courses_html += f"""            <a href="{cid}.html" class="course-card">
                <div class="course-icon">{icon}</div>
                <h3 class="course-title">{title}</h3>
                <p class="course-desc">{desc}</p>
                <div class="course-meta">
                    <span class="tag">{level}</span>
                    <span class="duration">{duration}</span>
                </div>
            </a>
"""

    projects_html = ""
    for title, desc, level, duration, skills in PROJECTS:
        skills_html = " ".join(f'<span class="tag">{s}</span>' for s in skills)
        projects_html += f"""            <div class="project-card">
                <h3 class="project-title">{title}</h3>
                <p class="project-desc">{desc}</p>
                <div class="project-meta">
                    <span class="tag">{level}</span>
                    <span class="duration">{duration}</span>
                </div>
                <div class="project-skills">{skills_html}</div>
            </div>
"""

    nav = NAV_TEMPLATE.format(active_index=' class="active"', active_courses='', active_projects='')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数析学院 - 商务数据分析在线教育平台</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="page-container">
        {nav}

        <h1 class="page-title">数析学院 - 商务数据分析在线教育平台</h1>
        <p class="page-subtitle">掌握商务数据分析技能，开启数据驱动决策之旅</p>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">8</div>
                <div class="stat-label">门课程</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">24</div>
                <div class="stat-label">个章节</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">10</div>
                <div class="stat-label">个项目</div>
            </div>
        </div>

        <h2 class="section-title">📚 课程体系</h2>
        <div class="courses-grid">
{courses_html}        </div>

        <h2 class="section-title">🎯 项目实战</h2>
        <div class="projects-grid">
{projects_html}        </div>
    </div>
</body>
</html>
"""

def generate_courses_page():
    courses_html = ""
    for i, (cid, title, chapters, chapter_nums) in enumerate(COURSES, 1):
        icons = ["💻", "📊", "📈", "🎨", "📐", "🤖", "💼", "🎯"]
        levels = ["入门", "初级", "初级", "初级", "中级", "中级", "高级", "高级"]
        durations = ["8小时", "10小时", "12小时", "8小时", "10小时", "12小时", "15小时", "20小时"]
        icon = icons[i-1]
        level = levels[i-1]
        duration = durations[i-1]
        desc = {
            1: "从零开始学习Python编程语言",
            2: "学习使用NumPy进行高效的数值计算",
            3: "掌握Pandas库进行数据处理",
            4: "创建专业的数据可视化图表",
            5: "学习统计学基础和假设检验",
            6: "掌握常用机器学习算法",
            7: "将数据分析应用于商业场景",
            8: "综合项目案例实战演练",
        }[i]
        courses_html += f"""            <a href="{cid}.html" class="course-card">
                <div class="course-icon">{icon}</div>
                <h3 class="course-title">{title}</h3>
                <p class="course-desc">{desc}</p>
                <div class="course-meta">
                    <span class="tag">{level}</span>
                    <span class="duration">{duration}</span>
                    <span class="chapter-count">{len(chapters)}个章节</span>
                </div>
            </a>
"""
    nav = NAV_TEMPLATE.format(active_index='', active_courses=' class="active"', active_projects='')
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>课程体系 - 数析学院</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="page-container">
        {nav}

        <h1 class="page-title">📚 课程体系</h1>
        <p class="page-subtitle">系统化的学习路径，从入门到精通</p>

        <div class="courses-grid">
{courses_html}        </div>
    </div>
</body>
</html>
"""

def generate_projects_page():
    projects_html = ""
    for title, desc, level, duration, skills in PROJECTS:
        skills_html = " ".join(f'<span class="tag">{s}</span>' for s in skills)
        projects_html += f"""            <div class="project-card">
                <h3 class="project-title">{title}</h3>
                <p class="project-desc">{desc}</p>
                <div class="project-meta">
                    <span class="tag">{level}</span>
                    <span class="duration">{duration}</span>
                </div>
                <div class="project-skills">{skills_html}</div>
            </div>
"""
    nav = NAV_TEMPLATE.format(active_index='', active_courses='', active_projects=' class="active"')
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>项目实战 - 数析学院</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="page-container">
        {nav}

        <h1 class="page-title">🎯 项目实战</h1>
        <p class="page-subtitle">通过真实项目案例，积累实战经验</p>

        <div class="projects-grid">
{projects_html}        </div>
    </div>
</body>
</html>
"""

def generate_course_page(course_idx):
    cid, title, chapter_titles, chapter_nums = COURSES[course_idx]
    icons = ["💻", "📊", "📈", "🎨", "📐", "🤖", "💼", "🎯"]
    levels = ["入门", "初级", "初级", "初级", "中级", "中级", "高级", "高级"]
    durations = ["8小时", "10小时", "12小时", "8小时", "10小时", "12小时", "15小时", "20小时"]
    icon = icons[course_idx]
    level = levels[course_idx]
    duration = durations[course_idx]

    sidebar_html = ""
    for ci, (chapter_title, chapter_num) in enumerate(zip(chapter_titles, chapter_nums)):
        sidebar_html += f'<li><a href="chapter{chapter_num}.html"><span class="chapter-number">{ci+1:02d}</span> {chapter_title}</a></li>\n'

    nav = NAV_TEMPLATE.format(active_index='', active_courses=' class="active"', active_projects='')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 数析学院</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="page-container">
        {nav}

        <div class="course-header">
            <div class="course-icon-large">{icon}</div>
            <h1 class="course-title-large">{title}</h1>
            <p class="course-desc-large">系统学习{title}，掌握数据分析核心技能</p>
            <div class="course-meta-large">
                <span class="tag">{level}</span>
                <span class="duration">{duration}</span>
                <span class="chapter-count">{len(chapter_titles)}个章节</span>
            </div>
            <a href="courses.html" class="back-btn">← 返回课程体系</a>
        </div>

        <h2 class="section-title">📖 课程章节</h2>
        <div class="chapter-list-container">
            <ul class="chapter-list-large">
{sidebar_html}            </ul>
        </div>
    </div>
</body>
</html>
"""

def generate_chapter_page(chapter_num):
    chapter_data = CHAPTERS_DATA[chapter_num]
    title = chapter_data[0]
    sections = chapter_data[1]
    exercises = chapter_data[2] if len(chapter_data) > 2 else []
    practices = chapter_data[3] if len(chapter_data) > 3 else []

    # 找到所属课程
    course_idx = None
    chapter_in_course_idx = None
    for ci, (cid, ctitle, cchapters, cnums) in enumerate(COURSES):
        if chapter_num in cnums:
            course_idx = ci
            chapter_in_course_idx = cnums.index(chapter_num)
            break

    cid, course_title, course_chapters, course_chapter_nums = COURSES[course_idx]

    # 侧边栏
    sidebar_html = ""
    for ci, (ct, cn) in enumerate(zip(course_chapters, course_chapter_nums)):
        is_active = ' class="active"' if cn == chapter_num else ''
        sidebar_html += f'<li><a href="chapter{cn}.html"{is_active}"><span class="chapter-number">{ci+1:02d}</span> {ct}</a></li>\n'

    # 下一章
    next_chapter = None
    if chapter_in_course_idx < len(course_chapter_nums) - 1:
        next_num = course_chapter_nums[chapter_in_course_idx + 1]
        next_title = course_chapters[chapter_in_course_idx + 1]
        next_chapter = f'<a href="chapter{next_num}.html" class="next-chapter-btn">下一章：{next_title} →</a>'

    # 上一章
    prev_chapter = None
    if chapter_in_course_idx > 0:
        prev_num = course_chapter_nums[chapter_in_course_idx - 1]
        prev_title = course_chapters[chapter_in_course_idx - 1]
        prev_chapter = f'<a href="chapter{prev_num}.html" class="prev-chapter-btn">← 上一章：{prev_title}</a>'

    # sections HTML (新格式: (标题, 内容) 元组)
    sections_html = ""
    for s in sections:
        if isinstance(s, tuple) and len(s) == 2:
            s_title, s_content = s
        else:
            s_title = s
            s_content = f"本节介绍{s}的核心概念和应用方法。通过理论讲解和实例演示，帮助你理解并掌握相关知识。"
        sections_html += f"""                <div class="section-block">
                    <h3 class="section-title">{s_title}</h3>
                    <p class="section-content">{s_content}</p>
                </div>
"""

    # exercises HTML
    exercises_html = ""
    if exercises:
        ex_cards = ""
        for ei, ex in enumerate(exercises, 1):
            question, optA, optB, optC, optD, correct, explain = ex
            letters = ['A', 'B', 'C', 'D']
            correct_letter_zh = {
                'A': '甲', 'B': '乙', 'C': '丙', 'D': '丁',
                'a': '甲', 'b': '乙', 'c': '丙', 'd': '丁'
            }.get(correct, correct)

            # 构建选项列表，正确答案特殊标记
            opts_html = ""
            for letter, opt in zip(letters, [optA, optB, optC, optD]):
                is_correct = (letter == correct.upper())
                highlight = ' class="correct-option"' if is_correct else ''
                opts_html += f'                    <li{highlight}>{letter}. {opt}</li>\n'

            ex_cards += f"""                <div class="exercise-card">
                    <div class="exercise-number">习题 {ei}</div>
                    <div class="exercise-question">{question}</div>
                    <ul class="exercise-options">
{opts_html}                    </ul>
                    <div class="explanation-box">
                        <strong>正确答案：</strong><span class="correct-ans">{correct}</span>
                        <br><strong>解析：</strong>{explain}
                    </div>
                </div>
"""
        exercises_html = f"""                <div class="exercise-section">
                    <h2 class="exercise-section-title">📝 课后习题</h2>
{ex_cards}                </div>
"""

    # practices HTML
    practices_html = ""
    if practices:
        p_cards = ""
        for pi, p in enumerate(practices, 1):
            p_title = p[0]
            p_difficulty = p[1] if len(p) > 1 else "初级"
            p_steps = p[2] if len(p) > 2 else []
            steps_html = ""
            if p_steps:
                steps_html = "<ol>" + "".join(f"<li>{step}</li>" for step in p_steps) + "</ol>"
            p_cards += f"""                <div class="practice-card">
                    <div class="practice-number">实践 {pi}</div>
                    <div class="practice-title">{p_title} <span class="practice-difficulty">[{p_difficulty}]</span></div>
                    <div class="practice-content">
                        {steps_html}
                    </div>
                </div>
"""
        practices_html = f"""                <div class="practice-section">
                    <h2 class="practice-section-title">💻 动手实践</h2>
{p_cards}                </div>
"""

    # 要点总结（从第一小节提取关键词）
    first_section_title = sections[0][0] if isinstance(sections[0], tuple) else sections[0]
    second_section_title = sections[1][0] if isinstance(sections[1], tuple) else sections[1]

    nav = NAV_TEMPLATE.format(active_index='', active_courses=' class="active"', active_projects='')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 数析学院</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="page-container">
        {nav}

        <div class="chapter-layout">
            <div class="sidebar">
                <div class="sidebar-title">章节目录</div>
                <ul class="chapter-list">
{sidebar_html}                </ul>
                <a href="{cid}.html" class="back-btn">← 返回课程</a>
                <a href="courses.html" class="back-btn">← 课程体系</a>
            </div>

            <div class="chapter-content">
                <h1 class="chapter-title">{title}</h1>
                <p class="chapter-subtitle">课程：{course_title}</p>

{sections_html}
                <div class="key-point">
                    <h4>💡 要点总结</h4>
                    <p>本章介绍了{title}的核心知识点，包括{first_section_title}、{second_section_title}等关键内容。通过系统学习，你将掌握相关概念和方法。</p>
                </div>

                <div class="tip-box">
                    <h4>✏️ 学习小贴士</h4>
                    <p>建议在学习时结合实际代码练习，理论结合实践是掌握数据分析技能的最佳方式。遇到问题时多查文档、多动手实验，培养独立解决问题的能力。</p>
                </div>

                <div class="warn-box">
                    <h4>⚠️ 注意事项</h4>
                    <p>学习过程中遇到问题不要气馁，数据分析是实践性很强的技能，需要持续练习和积累。从错误中学习是成长的重要途径。</p>
                </div>

{exercises_html}
{practices_html}
                <div class="chapter-nav-bottom">
                    {prev_chapter if prev_chapter else ''}
                    <a href="index.html" class="home-btn">🏠 回到首页</a>
                    {next_chapter if next_chapter else ''}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

def main():
    print("=" * 50)
    print("生成静态站点...")
    print("=" * 50)

    # 清理旧文件（保留 static 目录）
    html_files = [f for f in os.listdir(BUILD_DIR) if f.endswith('.html') and f not in ['111.html', 'deepseek_html_20260524_0487e5.html', 'index.html.old']]
    for f in html_files:
        os.remove(os.path.join(BUILD_DIR, f))
        print(f"  清理旧文件: {f}")

    # 生成页面
    files_generated = []

    # 首页
    index_html = generate_index()
    with open(os.path.join(BUILD_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    files_generated.append("index.html")

    # 课程体系页
    courses_html = generate_courses_page()
    with open(os.path.join(BUILD_DIR, "courses.html"), "w", encoding="utf-8") as f:
        f.write(courses_html)
    files_generated.append("courses.html")

    # 项目实战页
    projects_html = generate_projects_page()
    with open(os.path.join(BUILD_DIR, "projects.html"), "w", encoding="utf-8") as f:
        f.write(projects_html)
    files_generated.append("projects.html")

    # 课程详情页
    for i in range(8):
        html = generate_course_page(i)
        fname = f"course{i+1}.html"
        with open(os.path.join(BUILD_DIR, fname), "w", encoding="utf-8") as f:
            f.write(html)
        files_generated.append(fname)

    # 章节详情页
    for ch_num in range(1, 25):
        html = generate_chapter_page(ch_num)
        fname = f"chapter{ch_num}.html"
        with open(os.path.join(BUILD_DIR, fname), "w", encoding="utf-8") as f:
            f.write(html)
        files_generated.append(fname)

    print(f"\n✅ 生成完成！共 {len(files_generated)} 个页面")
    print(f"   - 首页: 1 个")
    print(f"   - 课程列表: 1 个")
    print(f"   - 项目列表: 1 个")
    print(f"   - 课程详情: 8 个")
    print(f"   - 章节详情: 24 个")
    print(f"\n   static/ 目录: CSS 样式文件")
    print(f"\n📂 站点根目录: {BUILD_DIR}")
    print(f"   入口文件: index.html")
    print(f"\n🌐 Cloudflare Pages 部署:")
    print(f"   Build command: (留空)")
    print(f"   Build output directory: / (或当前目录)")

    # 验证文件
    print(f"\n🔍 验证生成的文件:")
    for fname in sorted(files_generated)[:10]:
        size = os.path.getsize(os.path.join(BUILD_DIR, fname))
        print(f"   - {fname} ({size} bytes)")
    if len(files_generated) > 10:
        print(f"   ... 以及 {len(files_generated) - 10} 个其他文件")

if __name__ == "__main__":
    main()
