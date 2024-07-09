import os
from flask import render_template, flash, redirect, url_for, current_app, request
from werkzeug.utils import secure_filename
from . import image_processor
from .forms import ImageUploadForm
from PIL import Image
import slugify

def process_image(image, sizes, title):
    results = []
    output_directory = os.path.join(current_app.root_path, 'static', 'output')
    os.makedirs(output_directory, exist_ok=True)

    for size in sizes:
        width, height = map(int, size.split('x'))
        img = Image.open(image)
        img = img.resize((width, height), Image.LANCZOS)

        # Create slugified filename
        filename = f"{slugify.slugify(title)}_{width}x{height}.webp"

        # Save the image
        output_path = os.path.join(output_directory, filename)
        img.save(output_path, 'WEBP')
        results.append(f"Saved {filename} to {output_path}")

    return results

@image_processor.route('/', methods=['GET', 'POST'])
def upload_image():
    form = ImageUploadForm()
    if form.validate_on_submit():
        f = form.image.data
        filename = secure_filename(f.filename)

        # Process the image only for selected sizes
        results = process_image(f, form.sizes.data, form.title.data)

        flash('Image processed successfully!', 'success')
        return render_template('image_processor/result.html', results=results)

    return render_template('image_processor/upload.html', form=form)