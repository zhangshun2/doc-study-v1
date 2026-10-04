import os
import urllib.parse

def generate_sidebar(root_dir):
    sidebar_content = []
    
    # 定义需要忽略的目录和文件
    ignore_dirs = {'.git', '.trae', 'docsify', 'node_modules', '.idea'}
    ignore_files = {'_sidebar.md', '_coverpage.md', 'index.html', 'README.md', 'README.en.md', 'generate_sidebar.py', '_sidebar.md.bak'}

    # 获取根目录下的所有项，并排序
    items = sorted(os.listdir(root_dir))
    
    # 分离文件夹和文件
    dirs = []
    files = []
    
    for item in items:
        if item in ignore_dirs or item in ignore_files:
            continue
        
        full_path = os.path.join(root_dir, item)
        if os.path.isdir(full_path):
            dirs.append(item)
        elif item.endswith('.md'):
            files.append(item)

    # 处理文件夹（作为一级菜单）
    for d in dirs:
        sidebar_content.append(f"- **{d}**")
        # 递归遍历子目录
        walk_directory(os.path.join(root_dir, d), d, sidebar_content, level=1)
        sidebar_content.append("") # 分隔符

    # 处理根目录下的文件（作为一级菜单项）
    if files:
        sidebar_content.append("- **其他文档**")
        for f in files:
            link = urllib.parse.quote(f)
            name = os.path.splitext(f)[0]
            sidebar_content.append(f"  - [{name}]({link})")

    return "\n".join(sidebar_content)

def walk_directory(current_path, relative_path, content_list, level):
    try:
        items = sorted(os.listdir(current_path))
    except PermissionError:
        return

    # 分离文件夹和文件
    dirs = []
    files = []
    
    for item in items:
        # 忽略以点开头的文件/文件夹
        if item.startswith('.'):
            continue
            
        full_path = os.path.join(current_path, item)
        if os.path.isdir(full_path):
            dirs.append(item)
        elif item.endswith('.md'):
            files.append(item)

    indent = "  " * level
    
    # 先处理文件
    for f in files:
        file_rel_path = os.path.join(relative_path, f).replace("\\", "/")
        link = urllib.parse.quote(file_rel_path)
        name = os.path.splitext(f)[0]
        content_list.append(f"{indent}- [{name}]({link})")
        
    # 再处理子目录
    for d in dirs:
        dir_rel_path = os.path.join(relative_path, d).replace("\\", "/")
        content_list.append(f"{indent}- **{d}**")
        walk_directory(os.path.join(current_path, d), dir_rel_path, content_list, level + 1)

if __name__ == "__main__":
    root_dir = os.getcwd()
    sidebar = generate_sidebar(root_dir)
    
    with open("_sidebar.md", "w", encoding="utf-8") as f:
        f.write(sidebar)
    
    print("Sidebar generated successfully!")
