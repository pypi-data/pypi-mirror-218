import os
from PIL import Image, ImageDraw, ImageFont

from readyocr.entities import EntityList, PageEntity, BoundingBox

present_path = os.path.abspath(os.path.dirname(__file__))


def draw_bbox(image: Image, 
              bbox: BoundingBox, 
              fill_color: tuple=(0, 0, 255),
              outline_color: tuple=(0, 255, 0),
              outline_thickness: int=1, 
              opacity: float=0.3) -> Image:
    """
    Draws a box on the image with the specified parameters.

    :param image: The input image.
    :type image: Image
    :param bbox: The bounding box coordinates (x, y, width, height - normalized).
    :type bbox: BoundingBox
    :param fill_color: The color of the box, defaults to [0, 0, 255] (blue).
    :type fill_color: list, optional
    :param outline_color: The color of the outline, defaults to [0, 255, 0] (green).
    :type outline_color: list, optional
    :param outline_thickness: The thickness of the outline, defaults to 1.
    :type outline_thickness: int, optional
    :param opacity: The opacity of the box, defaults to 0.5.
    :type opacity: float, optional
    :return: The image with the drawn box.
    :rtype: Image
    """

    x, y, width, height = bbox.x, bbox.y, bbox.width, bbox.height
    left = int(x * image.width)
    top = int(y * image.height)
    right = int((x + width) * image.width)
    bottom = int((y + height) * image.height)
    
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
    drw = ImageDraw.Draw(overlay, "RGBA")

    # # Draw the box
    drw.rectangle([(left, top), (right, bottom)], fill=(*fill_color, int(255 * opacity)),
                  outline=(*outline_color, 255), width=outline_thickness)

    # Combine the overlay with the original image
    image = Image.alpha_composite(image, overlay)

    return image
 