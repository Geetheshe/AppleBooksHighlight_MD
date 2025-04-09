from pathlib import Path


def transform_md(matched_result, book_title):
    md_folder = Path(input("---------------------------------\n"
                           "请输入 Markdown 文件存放的文件夹："))

    i = 0
    while i < len(matched_result):
        index = str(i + 1)
        md_file = md_folder / index

        with open(f"{md_file}.md", "w", encoding="UTF-8") as create_md:
            create_md.write(f"书籍：[[{book_title}]]\n\n")

            if len(matched_result[i]["备注"]) == 1:
                create_md.write(f"笔记：{matched_result[i]["备注"][0]}\n\n")
            elif len(matched_result[i]["备注"]) > 1:
                for j in matched_result[i]["备注"]:
                    create_md.write("笔记：" + j + "\n\n")

            create_md.write(f"> {matched_result[i]["所属章目"]}\n")
            create_md.write("> \n")
            create_md.write(f"> {matched_result[i]["原文段落"]}\n")

        i += 1
