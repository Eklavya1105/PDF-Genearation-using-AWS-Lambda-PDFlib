import json
import boto3
import logging
import os
import sys
import traceback
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), 'PDFlib'))
from PDFlib.PDFlib import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        json_data = json.loads(event['body']) if 'body' in event else event
        if 'pdf_data' not in json_data:
            return {'statusCode': 400, 'body': json.dumps({"error": "Missing required field: pdf_data"})}

        if 'output_bucket' not in json_data or not json_data['output_bucket']:
            return {'statusCode': 400, 'body': json.dumps({"error": "Missing required field: output_bucket"})}

        pdf_path = generate_pdf(json_data)

        output_bucket = json_data['output_bucket']
        output_key = json_data.get('output_key', "output.pdf")
        s3_client.upload_file(pdf_path, output_bucket, output_key, ExtraArgs={'ContentType': 'application/pdf'})

        return {
            'statusCode': 200,
            'body': json.dumps({"message": "PDF generated successfully", "s3_location": f"s3://{output_bucket}/{output_key}"})
        }

    except Exception as e:
        logger.error(f"Lambda execution error: {str(e)}")
        logger.error(traceback.format_exc())
        return {'statusCode': 500, 'body': json.dumps({"error": str(e)})}

def generate_pdf(json_data):
    try:
        logger.info(f"Generating PDF with data: {json_data}")
        pdf = PDFlib()
        font_path = "/tmp/font.ttf"
        image_path = "/tmp/image.jpg"
        font_loaded = False

        
        if "font_key" in json_data and "input_bucket" in json_data:
            try:
                s3_client.download_file(json_data["input_bucket"], json_data["font_key"], font_path)
                logger.info(f"Downloaded font from S3: {font_path}")
            except Exception as e:
                logger.warning(f"Failed to download font from S3: {str(e)}")

        elif "font_url" in json_data:
            try:
                response = requests.get(json_data["font_url"])
                if response.status_code == 200:
                    with open(font_path, "wb") as f:
                        f.write(response.content)
                    logger.info(f"Downloaded font from pre-signed URL: {font_path}")
                else:
                    logger.warning(f"Failed to download font: {response.status_code}")
            except Exception as e:
                logger.warning(f"Error fetching font from URL: {str(e)}")

        
        if "image_key" in json_data and "input_bucket" in json_data:
            try:
                s3_client.download_file(json_data["input_bucket"], json_data["image_key"], image_path)
                logger.info(f"Downloaded image from S3: {image_path}")
            except Exception as e:
                logger.warning(f"Failed to download image from S3: {str(e)}")

        elif "image_url" in json_data:
            try:
                response = requests.get(json_data["image_url"])
                if response.status_code == 200:
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                    logger.info(f"Downloaded image from URL: {image_path}")
                else:
                    logger.warning(f"Failed to download image: {response.status_code}")
            except Exception as e:
                logger.warning(f"Error fetching image from URL: {str(e)}")

        pdf.set_option("errorpolicy=return")
        pdf.set_option("searchpath={/tmp}")
        pdf.begin_document("/tmp/output.pdf", "")
        pdf.begin_page_ext(595, 842, "")

        
        font = -1
        if os.path.exists(font_path):
            try:
                font = pdf.load_font("font", "unicode", "embedding")
                if font != -1:
                    logger.info(f"Successfully loaded font: {font_path}")
                    font_loaded = True
                else:
                    logger.error(f"Failed to load font: {font_path}")
            except Exception as e:
                logger.error(f"Error loading font: {str(e)}")

        
        if not font_loaded:
            font = pdf.load_font("Helvetica", "unicode", "")
            if font == -1:
                logger.critical("Both custom and default font loading failed. Cannot generate PDF.")
                raise Exception("Font loading failed.")

        pdf.setfont(font, 16)

        
        pdf.fit_textline(json_data['pdf_data'].get('title', 'Default Title'), 100, 750, "")

        
        if os.path.exists(image_path):
            image = pdf.load_image("auto", image_path, "")
            if image != -1:
                pdf.fit_image(image, 50, 400, "scale=2.5 position=center")
                pdf.close_image(image)
                logger.info("Successfully embedded image.")
            else:
                logger.error(f"Failed to load image: {image_path}")
        else:
            logger.warning(f"Image file not found: {image_path}")

        pdf.end_page_ext("")
        pdf.end_document("")

        return "/tmp/output.pdf"

    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        logger.error(traceback.format_exc())
        raise
