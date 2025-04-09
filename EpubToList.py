from bs4 import BeautifulSoup
import FileFindFolder
import re


def epub_list(ebook_folder):
    # 读取电子书解压文件夹内的 ncx 文件
    toc_files = [file for file in ebook_folder.glob("**/*.ncx")]

    # 读取 toc.ncx 文件，并读取各个章节的标题与起始页，放入字典 chapters = { "章节名": "起始页" }
    for toc_file in toc_files:
        chapters_start = {}
        with open(toc_file, "r", encoding="UTF-8") as tf:
            soup = BeautifulSoup(tf, "lxml-xml")

        for navPoint in soup.find_all("navPoint"):
            text = navPoint.find("text").get_text()
            src = navPoint.find("content")["src"]
            chapters_start[text] = src

    # 读取电子书解压文件夹内的 opf 文件
    opf_files = [file for file in ebook_folder.glob("**/*.opf")]

    # 读取 .opf 文件，读取书籍所有页数 html，并存入列表 all_htmls = [ "页数" ]
    for opf_file in opf_files:
        with open(opf_file, "r", encoding="UTF-8") as of:
            soup = BeautifulSoup(of, "lxml-xml")

        book_title = soup.find("dc:title").get_text()

        all_htmls = []

        # all_files 罗列出书本中的所有文件地址，.opf 文件将这些地址存放在<manifest><item>里，包括每一页、图片等
        all_files = {item["id"]: item["href"]
                     for item in soup.find_all("item")}

        # <spine><itemref> 罗列出书本中的每一页，但没有地址，所以要通过 idref 在 all_files 中找到地址，若不存在于 idref 中则认为是无关紧要的文件
        for itemref in soup.find_all("itemref"):
            item_id = itemref["idref"]
            if item_id in all_files:
                all_htmls.append(all_files[item_id])

    chapter_belong = {}
    start_titles = list(chapters_start.keys())
    start_pages = list(chapters_start.values())

    for every_html in all_htmls:
        for start_page in start_pages:
            if start_page.startswith(every_html):
                chapter_title = start_titles[
                    start_pages.index(start_page)]
                chapter_belong.setdefault(chapter_title, [])
                break

        if len(chapter_belong) > 0:
            current_chapter = list(chapter_belong.keys())[-1]
            chapter_belong[current_chapter].append(every_html)

    belong_titles = list(chapter_belong.keys())
    belong_pages = list(chapter_belong.values())
    book_content = []

    for pages in belong_pages:
        for page in pages:
            with open(FileFindFolder.find_file(ebook_folder, page), "r", encoding="UTF-8") as html:
                soup = BeautifulSoup(html.read(), "lxml-xml")

            book_content.append(
                {"章节名": belong_titles[belong_pages.index(pages)], "章节内容": []})
            contents = soup.find_all(
                ["p", "h1", "h2", "h3", "h4", "h5", "h6"])
            for content in contents:
                book_content[-1]["章节内容"].append(
                    normalize(content.get_text()))

    return book_title, book_content


def normalize(text):
    # 去掉多余空白字符、tab、换行，并统一多个空格为一个空格
    return re.sub(r'\s+', ' ', text).strip()
