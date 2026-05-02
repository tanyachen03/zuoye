import os
import shutil

PROJECTS_DIR = "/workspace/data-analytics-platform/projects"

# 使用project1.html作为模板
TEMPLATE_PATH = os.path.join(PROJECTS_DIR, "project1.html")

# 复制并更新其他项目文件
for i in range(2, 11):
    src = TEMPLATE_PATH
    dst = os.path.join(PROJECTS_DIR, f"project{i}.html")
    shutil.copy(src, dst)
    print(f"已更新: project{i}.html")

print("\n所有项目文件更新完成！")
