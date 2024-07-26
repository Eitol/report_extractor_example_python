from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import pymupdf

from model import Report, ChapadurHardboard, PalletsArlog, MarcosDeMadera
from pdf2matrix import PDF2RowsExtractor, PDFFile, Image


class ReportExtractor:
    def __init__(self, pdf_path: Path):
        self.doc: pymupdf.Document = pymupdf.open(pdf_path)
        self.report_extractor = PDF2RowsExtractor(pdf_path)

    def extract(self) -> Tuple[Report, List[Image]]:
        pdf = self.report_extractor.extract()
        return self._parse_pdf(pdf)

    @staticmethod
    def _parse_date(date_str: str):
        return datetime.strptime(date_str, '%d/%m/%Y')

    @staticmethod
    def _parse_percentage(percentage_str: str):
        return float(percentage_str.replace('%', '').replace(',', '.'))

    @staticmethod
    def _parse_int(value: str):
        return int(value.replace(' ', '').replace(',', ''))

    def _parse_pdf(self, pdf: PDFFile) -> Tuple[Report, List[Image]]:
        parsed_matrix = self._parse_matrix(pdf.matrix)
        return Report.model_validate(parsed_matrix), pdf.images

    def _parse_matrix(self, matrix: List[List[str]]) -> dict:
        report_data = {}
        chapadur_data = {}
        pallets_data = {}
        marcos_data = {}
        observations = []
        for i, row in enumerate(matrix):
            if 'Nº INFORME' in row:
                report_data['num_informe'] = self._parse_int(row[1])
            elif 'CLIENTE' in row:
                report_data['cliente'] = row[1]
            elif 'Nº REMITO' in row:
                report_data['num_remit'] = row[1]
            elif 'FECHA RECEPCIÓN' in row:
                report_data['reception_date'] = self._parse_date(row[1])
            elif 'CHAPADUR HARDBOARD' in row and len(matrix[i + 2]) > 8:
                chapadur_row = matrix[i + 2]
                chapadur_data = self._parse_chapadur_data(chapadur_row)
            elif 'PALLETS ARLOG' in row:
                pallets_row = matrix[i + 2]
                pallets_data = self._parse_pallet_data(pallets_row)
            elif 'MARCOS DE MADERA' in row:
                marcos_row = matrix[i + 2]
                marcos_data = self._parse_marcos_data(marcos_row)
            elif 'FECHA FIN PROCESO' in row:
                self._parse_end_dates(i, matrix, report_data)
            elif 'OBSERVACIONES' in row:
                observations.append(matrix[i + 1][1])
        report_data['chapadur_hardboard'] = ChapadurHardboard(**chapadur_data)
        report_data['pallets_arlog'] = PalletsArlog(**pallets_data)
        report_data['marcos_de_madera'] = MarcosDeMadera(**marcos_data)
        report_data['observaciones'] = observations
        return report_data

    def _parse_chapadur_data(self, chapadur_row):
        return {
            'apto_s_film': self._parse_int(chapadur_row[1]),
            'second': self._parse_int(chapadur_row[2]),
            'third': self._parse_int(chapadur_row[3]),
            'plastificado': self._parse_int(chapadur_row[4]),
            'no_apto': self._parse_int(chapadur_row[5]),
            'total': self._parse_int(chapadur_row[6]),
            'informado': self._parse_int(chapadur_row[7]),
            'diferencia': self._parse_int(chapadur_row[8]),
            'no_apto_percentage': self._parse_percentage(chapadur_row[9]),
            'motivo_descartes': chapadur_row[0].split("\n")[1].split("descarte: ")[1],
        }

    def _parse_end_dates(self, i, matrix, report_data):
        for r in matrix[i:]:
            for cell_idx in range(len(r)):
                try:
                    date = self._parse_date(r[cell_idx])
                    if date is None:
                        continue
                    if 'CHAPADUR HARDBOARD' in r[cell_idx - 1]:
                        report_data['fecha_fin_proceso_chapadur'] = date
                    elif 'PALLET ARLOG' in r[cell_idx - 1]:
                        report_data['fecha_fin_proceso_pallet_marco'] = date
                except:
                    pass

    def _parse_marcos_data(self, marcos_row):
        return {
            'apto': self._parse_int(marcos_row[1]),
            'no_apto_mnpncr': self._parse_int(marcos_row[2]),
            'no_apto': self._parse_int(marcos_row[3]),
            'total': self._parse_int(marcos_row[4]),
            'informado': self._parse_int(marcos_row[5]),
            'diferencia': self._parse_int(marcos_row[6]),
            'no_apto_percentage': self._parse_percentage(marcos_row[7]),
            'motivo_descartes': marcos_row[0].split("\n")[1].split("descarte: ")[1],
        }

    def _parse_pallet_data(self, pallets_row):
        return {
            'oi': self._parse_int(pallets_row[1]),
            'branca': self._parse_int(pallets_row[2]),
            'reparacion': self._parse_int(pallets_row[3]),
            'no_apto': self._parse_int(pallets_row[4]),
            'total': self._parse_int(pallets_row[5]),
            'informado': self._parse_int(pallets_row[6]),
            'diferencia': self._parse_int(pallets_row[7]),
            'no_apto_percentage': self._parse_percentage(pallets_row[8]),
            'motivo_descartes': pallets_row[0].split("\n")[1].split("descarte: ")[1],
        }
