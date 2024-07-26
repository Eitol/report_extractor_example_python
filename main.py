import io
from pathlib import Path

from PIL import Image
from matplotlib import pyplot as plt

from report_extractor import ReportExtractor

if __name__ == '__main__':
    file = Path("reporte.pdf")
    extractor = ReportExtractor(file)
    report, images = extractor.extract()
    print(report.model_dump_json(indent=4))
    for img in images:
        image_data = img.data
        image = Image.open(io.BytesIO(image_data))
        plt.figure()
        plt.imshow(image)
        plt.axis('off')
    plt.show()
