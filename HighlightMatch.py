def unordered_stateless(highlight_data, epub_list):
    result = []

    i = 0

    while i < len(highlight_data):

        item = highlight_data[i].strip()
        if item.startswith("“") and item.endswith("”"):
            highlight = item[1:-1].strip()  # 去掉双引号

            belongs_to_chapter, belongs_to_content = ffcc(highlight, epub_list)

            note = []
            while i + 1 < len(highlight_data):
                if not highlight_data[i + 1].startswith("“"):
                    note.append(highlight_data[i + 1].strip())
                    i += 1
                else:
                    break

            highlight_in_content = belongs_to_content.replace(
                highlight, f'**{highlight}** ', 1)

            result.append({
                "所属章目": belongs_to_chapter,
                "原文段落": highlight_in_content,
                "备注": note
            })

        elif item.startswith("“") and not item.endswith("”"):
            highlight_part = []
            highlight_part.append(item[1:].strip())

            belongs_to_content_part = []
            belongs_to_chapter, belongs_to_content = ffcc(
                item[1:].strip(), epub_list)
            belongs_to_content_part.append(belongs_to_content)

            while i + 1 < len(highlight_data):
                if highlight_data[i + 1].startswith("\t"):
                    if highlight_data[i + 1].strip().endswith("”"):
                        if highlight_data[i + 1].strip()[:-1] != "":
                            highlight_part.append(
                                highlight_data[i + 1].strip()[:-1])
                            belongs_to_chapter_part, belongs_to_content = ffcc(
                                highlight_data[i + 1].strip()[:-1], epub_list)
                            belongs_to_content_part.append(
                                belongs_to_content)
                            i += 1
                            break
                        else:
                            i += 1
                            break
                    else:
                        highlight_part.append(highlight_data[i + 1].strip())
                        belongs_to_chapter_part, belongs_to_content = ffcc(
                            highlight_data[i + 1].strip(), epub_list)
                        belongs_to_content_part.append(
                            belongs_to_content.strip())
                        i += 1
                else:
                    break

            note = []
            while i + 1 < len(highlight_data):
                if not highlight_data[i + 1].startswith("“"):
                    note.append(highlight_data[i + 1].strip())
                    i += 1
                else:
                    break

            highlight = "".join(highlight_part)
            content = "".join(belongs_to_content_part)

            highlight_in_content = content.replace(
                highlight, f'**{highlight}** ', 1)

            result.append({
                "所属章目": belongs_to_chapter,
                "原文段落": highlight_in_content,
                "备注": note
            })

        i += 1

    return result


def ordered_stateful(highlight_data, epub_list):
    result = []

    i = 0
    j = 0
    k = 0

    while i < len(highlight_data):
        item = highlight_data[i].strip()
        if item.startswith("“") and item.endswith("”"):
            highlight = item[1:-1].strip()  # 去掉双引号

            belongs_to_chapter, belongs_to_content, j, k = wfcc(
                highlight, epub_list, j, k)

            note = []
            while i + 1 < len(highlight_data):
                if not highlight_data[i + 1].startswith("“"):
                    note.append(highlight_data[i + 1].strip())
                    i += 1
                else:
                    break

            highlight_in_content = belongs_to_content.replace(
                highlight, f'**{highlight}** ', 1)

            result.append({
                "所属章目": belongs_to_chapter,
                "原文段落": highlight_in_content,
                "备注": note
            })

        elif item.startswith("“") and not item.endswith("”"):
            highlight_part = []
            highlight_part.append(item[1:].strip())

            belongs_to_content_part = []
            belongs_to_chapter, belongs_to_content, j, k = wfcc(
                item[1:].strip(), epub_list, j, k)
            belongs_to_content_part.append(belongs_to_content)

            while i + 1 < len(highlight_data):
                if highlight_data[i + 1].startswith("\t"):
                    if highlight_data[i + 1].strip().endswith("”"):
                        if highlight_data[i + 1].strip()[:-1] != "":
                            highlight_part.append(
                                highlight_data[i + 1].strip()[:-1])
                            belongs_to_chapter_part, belongs_to_content, j, k = wfcc(
                                highlight_data[i + 1].strip()[:-1], epub_list, j, k)
                            belongs_to_content_part.append(belongs_to_content)
                            i += 1
                            break
                        else:
                            i += 1
                            break
                    else:
                        highlight_part.append(highlight_data[i + 1].strip())
                        belongs_to_chapter_part, belongs_to_content, j, k = wfcc(
                            highlight_data[i + 1].strip(), epub_list, j, k)
                        belongs_to_content_part.append(belongs_to_content)
                        i += 1
                else:
                    break

            note = []
            while i + 1 < len(highlight_data):
                if not highlight_data[i + 1].startswith("“"):
                    note.append(highlight_data[i + 1].strip())
                    i += 1
                else:
                    break

            highlight = "".join(highlight_part)
            content = "".join(belongs_to_content_part)

            highlight_in_content = content.replace(
                highlight, f'**{highlight}** ', 1)

            result.append({
                "所属章目": belongs_to_chapter,
                "原文段落": highlight_in_content,
                "备注": note
            })

        i += 1

    return result


def ffcc(highlight, epub_list):
    for chapters in epub_list:
        chapter = chapters["章节名"]
        contents = chapters["章节内容"]
        for content in contents:
            if highlight in content:
                return chapter, content
        else:
            continue


def wfcc(highlight, epub_list, j, k):
    while j < len(epub_list):
        chapter = epub_list[j]["章节名"]
        contents = epub_list[j]["章节内容"]
        while k < len(contents):
            if highlight in contents[k]:
                belongs_to_chapter = chapter
                belongs_to_content = contents[k]
                return belongs_to_chapter, belongs_to_content, j, k
            k += 1
        else:
            j += 1
            k = 0
            continue
