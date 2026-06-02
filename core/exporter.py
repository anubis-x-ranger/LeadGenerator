
import os
import json
import pandas as pd
from datetime import datetime
from typing import List

from core.models import BusinessLead
from config import config


class Exporter:

    @staticmethod
    def export_all(
        leads: List[BusinessLead],
        base_filename: str
    ):

        Exporter.ensure_output_directory()

        Exporter.export_csv(
            leads,
            f"{base_filename}.csv"
        )

        Exporter.export_excel(
            leads,
            f"{base_filename}.xlsx"
        )

        Exporter.export_json(
            leads,
            f"{base_filename}.json"
        )

    # =====================================================
    # CSV EXPORT
    # =====================================================

    @staticmethod
    def export_csv(
        leads: List[BusinessLead],
        filename: str
    ):

        rows = [
            
            lead.to_dict()
            if hasattr(lead, "to_dict")
            else lead


            for lead in leads
        ]

        df = pd.DataFrame(rows)

        df.to_csv(filename, index=False)

        print(f"[✓] CSV exported: {filename}")

    # =====================================================
    # EXCEL EXPORT
    # =====================================================

    @staticmethod
    def export_excel(
        leads: List[BusinessLead],
        filename: str
    ):

        rows = [
            
            lead.to_dict()
            if hasattr(lead, "to_dict")
            else lead


            for lead in leads
        ]

        df = pd.DataFrame(rows)

        df.to_excel(filename, index=False)

        print(f"[✓] Excel exported: {filename}")

    # =====================================================
    # JSON EXPORT
    # =====================================================

    @staticmethod
    def export_json(
        leads: List[BusinessLead],
        filename: str
    ):

        rows = [
            
            lead.to_dict()
            if hasattr(lead, "to_dict")
            else lead


            for lead in leads
        ]

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                rows,
                f,
                indent=2,
                ensure_ascii=False
            )

        print(f"[✓] JSON exported: {filename}")

    # =====================================================
    # OUTPUT DIRECTORY
    # =====================================================

    @staticmethod
    def ensure_output_directory():

        output_dir = config.export.output_directory

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    # =====================================================
    # TIMESTAMPED FILENAMES
    # =====================================================

    @staticmethod
    def generate_filename(
        prefix: str,
        extension: str
    ) -> str:

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        output_dir = config.export.output_directory

        return (
            f"{output_dir}/"
            f"{prefix}_{timestamp}.{extension}"
        )

