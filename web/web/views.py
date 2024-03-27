from django.shortcuts import render
from django.http import HttpResponse
import torch
import os
from django.core.files.storage import FileSystemStorage
from subprocess import run
from django.conf import settings
import subprocess

from django.templatetags.static import static



def index(request):
    return render(request, 'index.html')

def predict(request):
    if request.method == 'POST':
        uploaded_image = request.FILES['image_input']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)

        # Ensure temporary file path construction:
        image_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Execute the python code using subprocess:
        try:
            result = subprocess.run([
                "python",
                "C:\\Users\\shash\\Downloads\\Indian-Sign-Language-Detection\\yolov5\\detect.py",
                "--weights", "C:\\Users\\shash\\Downloads\\Indian-Sign-Language-Detection\\best.pt",
                "--source", image_path,
                "--img", "416"
            ], capture_output=True, text=True)                  
            if result.returncode == 0:
                results = result.stdout  # Access captured output
            else:
                print(f"Error running detect2.py: {result.stderr}")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Remove the temporary file after processing:
        os.remove(image_path)

        # Get the latest saved image path in the static folder
        latest_image_path = os.path.join(settings.STATIC_URL, filename)

        # Render results (replace with appropriate logic based on the detect2.py output)
        params = {'inference': results, 'img_pth': latest_image_path}
        return render(request, 'result.html', params)


def delete(request):
    return render(request, 'index.html')
