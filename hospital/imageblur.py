import cv2


def is_image_blurry(image_path, threshold):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    print("variance" + str(variance))
    if variance < threshold:
        return True  # Image is blurry
    else:
        return False  # Image is not blurry


from django.conf import settings
import os


def handle_uploaded_file(file):
    # Generate a unique file name
    file_name = file.name
    file_path = os.path.join(settings.MEDIA_ROOT, "infectedarea", file_name)

    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path
