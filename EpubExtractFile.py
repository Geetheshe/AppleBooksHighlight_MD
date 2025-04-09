from pathlib import Path
from zipfile import ZipFile


def get_ebook_folder(choice):
    # 电子书绝对地址
    ebook_path = Path(input("--------------------\n"
                            "请输入电子书的地址："))
    # 电子书文件名，不带后缀
    ebook_ohne_suffix = ebook_path.stem
    # 电子书解压缩根目录
    if choice == "1":
        ebook_folder_parent = Path(input("--------------------------------\n"
                                         "请输入将电子书解压至哪个文件夹："))
        ebook_folder = ebook_folder_parent / ebook_ohne_suffix
    elif choice == "2":
        ebook_folder = ebook_path.parent / ebook_ohne_suffix

    ebook_folder.mkdir(exist_ok=True)
    extract_epub(ebook_path, ebook_folder)

    return ebook_folder


def extract_epub(ebook_path, ebook_folder):
    # 将电子书解压至解压缩地址
    with ZipFile(ebook_path, "r") as zip_ref:
        zip_ref.extractall(ebook_folder)
