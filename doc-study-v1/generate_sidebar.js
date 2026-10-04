const fs = require('fs');
const path = require('path');

// 配置
const rootDir = __dirname;
const outputFile = path.join(rootDir, '_sidebar.md');
const ignoreDirs = new Set(['.git', '.trae', 'docsify', 'node_modules', '.idea']);
const ignoreFiles = new Set(['_sidebar.md', '_coverpage.md', 'index.html', 'README.md', 'README.en.md', 'generate_sidebar.js', '_sidebar.md.bak', 'package.json', 'package-lock.json']);

// 特殊排序：确保某些文件夹排在前面或后面
const folderOrder = {
    '二叉树专题': 1,
    '动态规划专题': 2,
    '搜索和回溯': 3,
    '单调栈': 4,
    '字符串专题': 5,
    '题': 99 // 放在最后
};

function generateSidebar() {
    let sidebarContent = [];

    // 获取根目录下的所有项
    const items = fs.readdirSync(rootDir);
    
    // 分离文件夹和文件
    let dirs = [];
    let files = [];

    items.forEach(item => {
        if (ignoreDirs.has(item) || ignoreFiles.has(item) || item.startsWith('.')) return;
        
        const fullPath = path.join(rootDir, item);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
            dirs.push(item);
        } else if (item.endsWith('.md')) {
            files.push(item);
        }
    });

    // 排序文件夹
    dirs.sort((a, b) => {
        const orderA = folderOrder[a] || 50;
        const orderB = folderOrder[b] || 50;
        if (orderA !== orderB) return orderA - orderB;
        return a.localeCompare(b);
    });
    
    // 排序文件
    files.sort((a, b) => a.localeCompare(b));

    // 处理文件夹
    dirs.forEach(d => {
        // 如果是"题"文件夹，特殊处理
        if (d === '题') {
            sidebarContent.push(`- **LeetCode 热题 100**`);
            processLeetCodeFolder(path.join(rootDir, d), d, sidebarContent, 1);
        } else {
            sidebarContent.push(`- **${d}**`);
            walkDirectory(path.join(rootDir, d), d, sidebarContent, 1);
        }
        sidebarContent.push(''); // 分隔符
    });

    // 处理根目录下的文件
    if (files.length > 0) {
        sidebarContent.push('- **其他文档**');
        files.forEach(f => {
            const name = path.basename(f, '.md');
            const link = f;
            sidebarContent.push(`  - [${name}](${link})`);
        });
    }

    // 写入文件
    fs.writeFileSync(outputFile, sidebarContent.join('\n'), 'utf8');
    console.log('Sidebar generated successfully at ' + outputFile);
}

// 辅助函数：生成不带编码的路径（Docsify 内部会自动处理编码）
function encodePath(pathStr) {
    // Docsify 通常不需要 encodeURI，除非文件名包含特殊字符导致解析失败
    // 但为了兼容性，我们只对空格进行转义，或者保留原样
    // 在 Windows 环境下，Docsify 读取本地文件可能需要 URI 编码，
    // 但如果编码过度（如中文字符被编码），会导致视觉上链接不可读，且有时会引起 404
    // 最佳实践：使用 encodeURI 编码整个路径，但保留 / 符号
    
    // 尝试方案：不进行 encodeURI，直接使用原始字符串（Docsify 会处理中文）
    return pathStr; 
}

function walkDirectory(currentPath, relativePath, contentList, level) {
    let items;
    try {
        items = fs.readdirSync(currentPath);
    } catch (e) {
        return;
    }

    let dirs = [];
    let files = [];

    items.forEach(item => {
        if (item.startsWith('.')) return;
        
        const fullPath = path.join(currentPath, item);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
            dirs.push(item);
        } else if (item.endsWith('.md') && item !== 'README.md' && item !== '_sidebar.md') {
            files.push(item);
        }
    });

    // 排序
    dirs.sort((a, b) => a.localeCompare(b));
    files.sort((a, b) => a.localeCompare(b));

    const indent = '  '.repeat(level);

    // 先处理子目录（为了保持层级感，文件夹优先）
    dirs.forEach(d => {
        const dirRelPath = path.join(relativePath, d).replace(/\\/g, '/');
        contentList.push(`${indent}- **${d}**`);
        walkDirectory(path.join(currentPath, d), dirRelPath, contentList, level + 1);
    });

    // 再处理文件
    files.forEach(f => {
        const fileRelPath = path.join(relativePath, f).replace(/\\/g, '/');
        const name = path.basename(f, '.md');
        // 修改：不再使用 encodeURI
        const link = fileRelPath; 
        contentList.push(`${indent}- [${name}](${link})`);
    });
}

// 特殊处理"题"文件夹，根据"4. LeetCode热题100专题分组.md"进行分组
function processLeetCodeFolder(currentPath, relativePath, contentList, level) {
    // 读取分组文件
    const groupFilePath = path.join(currentPath, '4. LeetCode热题100专题分组.md');
    let groupContent = '';
    try {
        groupContent = fs.readFileSync(groupFilePath, 'utf8');
    } catch (e) {
        // 如果读取失败，回退到普通遍历
        walkDirectory(currentPath, relativePath, contentList, level);
        return;
    }

    // 简单的正则匹配提取分组标题和题目
    const lines = groupContent.split('\n');
    let currentGroup = null;
    const indent = '  '.repeat(level);
    
    // 获取"题"目录下所有文件，用于查找
    const allFiles = fs.readdirSync(currentPath).filter(f => f.endsWith('.md'));
    const fileMap = {}; // 题目ID/名称 -> 文件名
    
    allFiles.forEach(f => {
        // 尝试匹配 LeetCode-123-题目名.md
        const match = f.match(/LeetCode-(\d+)-(.+)\.md/);
        if (match) {
            fileMap[match[1]] = f; // 用题号做key
            fileMap[match[2]] = f; // 用题目名做key
        }
        fileMap[f] = f; // 全名也做key
    });

    // 解析Markdown表格逻辑略显复杂，这里简化处理：
    // 1. 识别 "## 分组名"
    // 2. 识别表格行中的题号和题目
    
    lines.forEach(line => {
        // 匹配二级标题作为分组
        const headerMatch = line.match(/^##\s+(.+)/);
        if (headerMatch) {
            currentGroup = headerMatch[1].trim();
            // 去掉可能的图标和括号注释，让标题更干净
            // currentGroup = currentGroup.replace(/^[^\u4e00-\u9fa5a-zA-Z]+/, ''); 
            contentList.push(`${indent}- **${currentGroup}**`);
        }
        
        // 匹配表格行: | 1 | 两数之和 | ...
        // 只有在有分组的情况下才处理表格
        if (currentGroup && line.trim().startsWith('|')) {
            const parts = line.split('|').map(p => p.trim());
            if (parts.length > 3) {
                const id = parts[1];
                const title = parts[2];
                
                // 排除表头分隔行
                if (id.includes('---')) return;
                
                // 尝试找到对应的文件
                let targetFile = fileMap[id] || fileMap[title];
                
                // 如果找不到，尝试模糊匹配
                if (!targetFile) {
                     targetFile = allFiles.find(f => f.includes(title));
                }

                if (targetFile) {
                    const fileRelPath = path.join(relativePath, targetFile).replace(/\\/g, '/');
                    // 修改：不再使用 encodeURI
                    const link = fileRelPath;
                    // 使用两级缩进
                    contentList.push(`${indent}  - [${id}. ${title}](${link})`);
                }
            }
        }
    });
    
    // 添加"未分类/索引"链接
    contentList.push(`${indent}- **索引与归档**`);
    contentList.push(`${indent}  - [分组说明](题/4. LeetCode热题100专题分组.md)`);
    contentList.push(`${indent}  - [总索引](题/LeetCode热题100-总索引.md)`);
}

generateSidebar();
