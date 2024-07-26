Ejemplo de extracción de data para el reporte de una cristaleria

Primero extraemos la data del pdf como una matrix (Ver PDF2RowsExtractor)

Luego, extraemos la data de la matrix como un diccionario (Ver Rows2DictExtractor)

Finalmente, creamos el reporte (Ver Reporte)

Ejemplo de uso:

```python
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
```

### Instalación

```bash
pip install -r requirements.txt
```

### Ejecución

```bash
python main.py
```

Recuerda que debes pegar el fichero "reporte.pdf" en este path