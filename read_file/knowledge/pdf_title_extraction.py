import os
from typing import List
import tempfile


## pip install pymupdf
## pip install frontend
## pip install paddleocr
# pip install unstructured
# python -m pip install paddlepaddle-gpu==2.4.2 -f https://www.paddlepaddle.org.cn/whl/windows/mkl/avx/stable.html
#python3 -m pip install paddlepaddle-gpu==2.6.0.post120 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
# sudo apt-get update
# sudo apt-get upgrade
# sudo apt-get install libstdc++6
# pip install paddlepaddle==2.6.0

# strings /usr/lib/x86_64-linux-gnu/libstdc++.so.6 | grep GLIBCXX
import fitz
from langchain.document_loaders.unstructured import UnstructuredFileLoader
from paddleocr import PaddleOCR


class UnstructuredPaddlePDFLoader(UnstructuredFileLoader):
    """Loader that uses unstructured to load image files, such as PNGs and JPGs."""

    def _get_elements(self) -> List:
        def pdf_ocr_txt(filepath, dir_path="tmp_files"):
            full_dir_path = os.path.join(os.path.dirname(filepath), dir_path)
            if not os.path.exists(full_dir_path):
                os.makedirs(full_dir_path)
            filename = os.path.split(filepath)[-1]
            ocr = PaddleOCR(lang="ch", use_gpu=False, show_log=False)
            doc = fitz.open(filepath)
            txt_file_path = os.path.join(full_dir_path, "%s.txt" % (filename))
            img_name = os.path.join(full_dir_path, ".tmp.png")
            with open(txt_file_path, "w", encoding="utf-8") as fout:
                for i in range(doc.page_count):
                    page = doc[i]
                    text = page.get_text("")
                    fout.write(text)
                    fout.write("\n")

                    img_list = page.get_images()
                    for img in img_list:
                        pix = fitz.Pixmap(doc, img[0])

                        pix.save(img_name)

                        result = ocr.ocr(img_name)
                        print(result)
                        ocr_result = [i[1][0] for lines in result for line in lines for i in line]
                        fout.write("\n".join(ocr_result))
            os.remove(img_name)
            return txt_file_path

        txt_file_path = pdf_ocr_txt(self.file_path)
        from unstructured.partition.text import partition_text

        return partition_text(filename=txt_file_path, **self.unstructured_kwargs)

pdfloader = UnstructuredPaddlePDFLoader('/root/yovole/LLM_Survey_Chinese.pdf')
print(pdfloader.load())


import fitz
import time
import os
from paddleocr import PaddleOCR

ocr = PaddleOCR(det=False, use_gpu=True, enable_mkldnn=True, use_tensorrt=True, use_angle_cls=True, lang='ch')


def pdf_to_jpg(name):
    pdfdoc = fitz.open(name)
    temp = 0
    for pg in range(pdfdoc.page_count):
        page = pdfdoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
        zoom_x = 2.0
        zoom_y = 2.0
        trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        pm._writeIMG('temp.jpg', 1)

        # ocr识别
        result = ocr.ocr('temp.jpg', cls=True)

        # 提取文件名
        xx = os.path.splitext(name)
        filename = xx[0].split('\\')[-1] + '.txt'
        # 存储结果
        with open(filename, mode='a') as f:
            for lines in result:
                for line in lines:
                    if line[1][1] > 0.5:
                        f.write(line[1][0] + '\n')
        print(pg)


pdf_to_jpg('/root/yovole/LLM_Survey_Chinese.pdf')