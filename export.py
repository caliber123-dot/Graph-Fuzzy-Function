from openpyxl import Workbook
from openpyxl.drawing.image import Image
import os
from PIL import Image as PILImage  # For resizing
import tempfile  # This was missing in your original code

def export_images_to_excel(img1, img2, output_excel="output.xlsx", max_width=500, max_height=300):
    """
    Export two resized PNG images to an Excel file with proper temp file handling.
    """
    temp_files = []  # To keep track of temporary files
    
    try:
        # Validate input images
        for img_path in [img1, img2]:
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"Image file not found: {img_path}")

        # Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Images"

        # Function to resize image and return temp path
        def resize_image(img_path):
            img = PILImage.open(img_path)
            img.thumbnail((max_width, max_height))            
            # Create temp file in system's temp directory
            fd, temp_path = tempfile.mkstemp(suffix='.png')
            os.close(fd)  # We only need the path
            img.save(temp_path)
            temp_files.append(temp_path)  # Track for cleanup
            return temp_path

        # Process images
        resized_img1 = resize_image(img1)
        resized_img2 = resize_image(img2)

        # Add images to worksheet
        ws.add_image(Image(resized_img1), "A1")
        ws.add_image(Image(resized_img2), "A16")

        # Adjust row heights to accommodate images
        # ws.row_dimensions[1].height = max_height * 0.75
        # ws.row_dimensions[20].height = max_height * 0.75

        # Save workbook
        wb.save(output_excel)
        print(f"Successfully created: {os.path.abspath(output_excel)}")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Clean up temp files
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"Warning: Could not delete temp file {temp_file}: {str(e)}")

# Example Usage
# export_images_to_excel(
#     img1="static/img/Alpha_Table.png",
#     img2="static/img/Bar_alpha_dashMF.png",
#     output_excel="images_exported.xlsx",
#     max_width=600,  # Custom max width
#     max_height=400  # Custom max height
# )