from config.config import Config
import logging
from web3 import Web3
from fpdf import FPDF
from datetime import date

logger = logging.getLogger(__name__)

class PDFHandler:
    def generate_contract_pdf(self, product_name, seller_name,  customer_name, quantity, contract_number) -> tuple[str, str]:
        filename = f"{seller_name}-{customer_name}-{product_name}-{quantity}-{contract_number}.pdf"
        basedir = Config.BASE_DIR[:Config.BASE_DIR.rfind("/")]
        basedir = basedir[:basedir.rfind("/"):]
        basedir = basedir[:basedir.rfind("/"):]
        save_location = f"{basedir}/documents/"

        pdf = FPDF()
        pdf.add_page()

        content = (f"This is a purchasing agreement between {seller_name} "
                   f"and {customer_name} for {quantity} of {product_name}.\n\n{date.today()}")

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=content, align='C')

        PDF_URI = save_location + filename
        pdf.output(PDF_URI)

        hash = Web3.solidity_keccak(['string'], [content])

        logger.info(f"contract PDF {contract_number} generated at: {PDF_URI}. Contract hash {hash}")

        return PDF_URI, hash
