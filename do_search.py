from google.cloud import vision
from google.cloud.vision import types

from typing import NamedTuple
import io
import logging


class ImageInfo(NamedTuple):
    adult_code: int
    adult_name: str
    medical_code: int
    medical_name: str
    spoof_code: int
    spoof_name: str
    violence_code: int
    violence_name: str


def do_safe_search(path):
    client = vision.ImageAnnotatorClient()

    if path.startswith("http") or path.startswith("gs:"):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, "rb") as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    # safe search checker
    logging.info("Do the safe search.....")

    safe_client = client.safe_search_detection(image=image)
    safe = safe_client.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )

    adult = likelihood_name[safe.adult]
    violence = likelihood_name[safe.violence]

    # Create namedtuple with results from the vision api analysis
    print("        Safe Search Results:")
    print("            Adult: {0}, Violence: {1}".format(safe.adult, safe.violence))

    picture_info = ImageInfo(
        safe.adult,
        likelihood_name[safe.adult],
        safe.medical,
        likelihood_name[safe.medical],
        safe.spoof,
        likelihood_name[safe.spoof],
        safe.violence,
        likelihood_name[safe.violence],
    )

    return picture_info, adult, violence

# Label Detection

def do_label_detection(path):
    client = vision.ImageAnnotatorClient()

    if path.startswith("http") or path.startswith("gs:"):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, "rb") as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    labels_client = client.label_detection(image=image)
    labels = labels_client.label_annotations

    return labels
