from pathlib import Path
import EpubExtractFile
import EpubToList
import HighlightWash
import HighlightMatch
import ResultToMD

if __name__ == '__main__':
    choice = input("---------------------------------------------\n"
                   "选择「1」自行决定将电子书解压缩至哪个文件夹\n"
                   "选择「2」将自动解压缩至电子书所在的文件夹\n"
                   "选择「3」自行指定已解压缩电子书的文件夹地址：")

    if choice == "1":
        ebook_folder = EpubExtractFile.get_ebook_folder(choice)
    elif choice == "2":
        ebook_folder = EpubExtractFile.get_ebook_folder(choice)
    elif choice == "3":
        # 跳过解压缩环节，指定已解压缩的文件夹地址
        ebook_folder = Path(input("----------------------------------\n"
                                  "请输入已解压缩电子书的文件夹地址："))
    else:
        print("------------------------------------------\n"
              "你输入了其他不存在的选项，请重新运行程序。")
        exit()

    # 将解压缩文件夹地址传入，执行读取电子书任务，返回电子书字典
    book_title, book_content = EpubToList.epub_list(ebook_folder)

    highlight_washed = HighlightWash.wash(input("------------------------------\n"
                                                "请输入苹果图书高亮文件的地址："))

    iforder = input("-----------------------------------------------------\n"
                    "如果你的图书笔记顺序是正序，即从前到后，请选择「1」\n"
                    "如果你的图书笔记顺序是乱序，请选择「2」：")

    if iforder == "1":
        matched_result = HighlightMatch.ordered_stateful(
            highlight_washed, book_content)
    elif iforder == "2":
        matched_result = HighlightMatch.unordered_stateless(
            highlight_washed, book_content)

    ResultToMD.transform_md(matched_result, book_title)
