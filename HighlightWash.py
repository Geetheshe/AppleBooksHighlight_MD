import re


def wash(highlight_content):
    # 清理苹果图书导出后的固定格式
    with open(highlight_content, "r", encoding="UTF-8") as h:
        lines = h.readlines()

    for i in range(len(lines) - 1, -1, -1):  # 逆序遍历
        if lines[i] == "摘录来自：\n":
            del lines[i:i+4]
        elif lines[i] == "\n":
            del lines[i]
        else:
            lines[i] = normalize(lines[i])

    return lines


def normalize(text):
    # 提取前后空白
    match = re.match(r'^(\s*)(.*?)(\s*)$', text, re.DOTALL)
    if not match:
        return text
    prefix, core, suffix = match.groups()

    # 将中间的连续空白（如换行、tab、多空格）替换成一个空格（仅限 core 部分）
    # 空白字符两边是任意“可视字符”的情况，才会被替换
    core = re.sub(r'(?<=\S)\s+(?=\S)', ' ', core)

    return prefix + core + suffix
