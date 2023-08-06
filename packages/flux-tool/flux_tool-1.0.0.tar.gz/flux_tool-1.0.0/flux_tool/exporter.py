import logging

import subprocess
from pathlib import Path

import uproot
from pandas import DataFrame
from ROOT import TFile

from flux_tool.flux_systematic_analysis import FluxSystematicsAnalysis
from flux_tool.config import AnalysisConfig


class Exporter:
    __slots__ = ("nominal_samples", "products", "products_file")

    def __init__(self, cfg: AnalysisConfig, ana: FluxSystematicsAnalysis) -> None:
        self.nominal_samples = cfg.nominal_samples
        self.products_file = Path(cfg.products_file)
        self.products = ana.get_products()
        self.init_products_file()

    def init_products_file(self) -> None:
        logging.info(f"Initializing output file:\n  {self.products_file}")

        self.products_file.unlink(missing_ok=True)

        cmd1 = f"rootmkdir -p {self.products_file}:ppfx_output/fhc".split()
        cmd2 = f"rootmkdir -p {self.products_file}:ppfx_output/rhc".split()

        subprocess.run(cmd1)
        subprocess.run(cmd2)

    def export_ppfx_output(self) -> None:

        fhc_file = self.nominal_samples["fhc"]
        rhc_file = self.nominal_samples["rhc"]
        if fhc_file is None and rhc_file is None:
            print("Please provide at least one of FHC/RHC file path!")
            return
        if fhc_file is not None:
            logging.info(f"Copying PPFX output from {fhc_file.name} to {self.products_file.name}")
            cmd1 = f"rootcp -r {fhc_file} {self.products_file}:ppfx_output/fhc/".split()
            subprocess.run(cmd1)
        if rhc_file is not None:
            logging.info(f"Copying PPFX output from {rhc_file.name} to {self.products_file.name}")
            cmd2 = f"rootcp -r {rhc_file} {self.products_file}:ppfx_output/rhc/".split()
            subprocess.run(cmd2)

    def export_product(self, product, key: str) -> None:
        with uproot.update(self.products_file) as products:
            products[key] = product

    def export_products(self) -> None:
        logging.info(f"Writing analysis products to {self.products_file.name}")
        product_file = TFile(str(self.products_file), "update")
        for key, product in self.products.items():
            logging.info(f"\t{key}")
            if isinstance(product, DataFrame):
                continue
                # product_file.Close()
                # with uproot.update(self.products_file) as f:
                #     f[key] = product
                # product_file = TFile(str(self.products_file), "update")
                # continue
            dirs = key.split("/")

            if len(dirs) == 1:
                product_file.WriteObject(product, key)
            else:
                subdirs = "/".join(dirs[:-1])

                if not product_file.Get(subdirs):
                    product_file.mkdir(subdirs)
                d = product_file.Get(subdirs)

                d.WriteObject(product, dirs[-1])

        product_file.Close()
