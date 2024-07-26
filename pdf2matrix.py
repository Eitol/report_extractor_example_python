from dataclasses import dataclass
from pathlib import Path
import pymupdf
from pymupdf.table import TableFinder
from typing import List


@dataclass
class Image:
    width: int
    height: int
    data: bytes


@dataclass
class PDFFile:
    matrix: List[List[str]]
    images: List[Image]


class PDF2RowsExtractor:

    def __init__(self, pdf_path: Path):
        self.doc: pymupdf.Document = pymupdf.open(pdf_path)

    def extract(self) -> PDFFile:
        images: List[Image] = []
        pages_gen = self.doc.pages()  # this is the first page
        clean_rows: List[List[str]] = []
        for page in pages_gen:
            table_finder: TableFinder = page.find_tables()
            for table in table_finder:
                dirty_rows = table.extract()
                for row in dirty_rows:
                    row = self.remove_nulls(row)
                    if len(row) > 0:
                        clean_rows.append(row)
            raw_images = page.get_images(full=True)
            for img_index, img in enumerate(raw_images):
                xref = img[0]
                base_image = self.doc.extract_image(xref)
                images.append(
                    Image(
                        width=base_image['width'],
                        height=base_image['height'],
                        data=base_image['image']
                    )
                )

        return PDFFile(matrix=clean_rows, images=images)

    @staticmethod
    def remove_nulls(df: List[str]) -> List[str]:
        return list(filter(lambda x: x not in ['', None], df))
