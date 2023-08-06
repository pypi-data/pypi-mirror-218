import os
import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path: str, pdfs_path: str, company_name: str,
             image_path: str, product_id: str, product_name: str,
             amount_purchased: str, price_per_unit: str, total_price: str):
    """
    This function converts the invoice Excel files into PDF invoicing.
    :param invoices_path: The path to the folder containing the invoices.
    :param pdfs_path: The path of the folder where the inovices will be stored as PDF.
    :param company_name: The name of the company to be printed on the PDF.
    :param image_path: The logo of the company to be printed on the PDF.
    :param product_id: The name of the column representing the product id.
    :param product_name: The name of the column representing the product name.
    :param amount_purchased: The name of the column representing the number of units sold.
    :param price_per_unit: The name of the column representing the price per unit.
    :param total_price: The name of the column representing the total price earned.
    :return: Returns a folder containing the PDFs.
    """

    # To extract a list of the filepaths of the files
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        # To extract the date and invoice nr.
        filename = Path(filepath).stem
        invoice_nr, date = filename.split("-")

        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1, align="L")

        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1, align="L")

        # To add the header
        df = pd.read_excel(filepath, sheet_name="Sheet 1")
        columns = df.columns
        columns = [column.replace("_", " ").title() for column in columns]

        pdf.set_font(family="Times", style="B", size=12)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=10, txt=columns[0], border=1)
        pdf.cell(w=65, h=10, txt=columns[1], border=1)
        pdf.cell(w=40, h=10, txt=columns[2], border=1)
        pdf.cell(w=30, h=10, txt=columns[3], border=1)
        pdf.cell(w=30, h=10, txt=columns[4], border=1, ln=1)

        # To add the table
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=10, txt=str(row[product_id]), border=1)
            pdf.cell(w=65, h=10, txt=str(row[product_name]), border=1)
            pdf.cell(w=40, h=10, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=10, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=10, txt=str(row[total_price]), border=1, ln=1)

        # To add the total price
        total = df[total_price].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=10, border=1)
        pdf.cell(w=65, h=10, border=1)
        pdf.cell(w=40, h=10, border=1)
        pdf.cell(w=30, h=10, border=1)
        pdf.cell(w=30, h=10, txt=str(total), border=1, ln=1)

        # To add the total amount, company name and logo
        pdf.ln(20)
        pdf.set_font(family="Times", size=12, style="B")
        pdf.set_text_color(0, 0, 0)
        pdf.cell(w=0, h=10, txt=f"The total due amount is Rs. {total}.", ln=1)
        pdf.cell(w=26, h=10, txt=company_name)
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")
