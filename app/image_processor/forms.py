from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SelectMultipleField, SubmitField, widgets
from wtforms.validators import DataRequired, ValidationError

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ImageUploadForm(FlaskForm):
    title = StringField('Image Title', validators=[DataRequired()])
    image = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')
    ])
    sizes = MultiCheckboxField('Sizes', choices=[
        ('3840x2160', '16:9 (3840x2160)'),
        ('3200x1800', '16:9 (3200x1800)'),
        ('2560x1440', '16:9 (2560x1440)'),
        ('1920x1080', '16:9 (1920x1080)'),
        ('1280x720', '16:9 (1280x720)'),
        ('960x540', '16:9 (960x540)'),
        ('640x360', '16:9 (640x360)'),
        ('480x270', '16:9 (480x270)'),
        ('320x180', '16:9 (320x180)'),
        ('160x90', '16:9 (160x90)'),
        ('80x45', '16:9 (80x45)'),
        ('2048x2048', '1:1 (2048x2048)'),
        ('1024x1024', '1:1 (1024x1024)'),
        ('512x512', '1:1 (512x512)'),
        ('256x256', '1:1 (256x256)'),
        ('128x128', '1:1 (128x128)'),
        ('64x64', '1:1 (64x64)'),
        ('32x32', '1:1 (32x32)'),
        ('2048x3072', '2:3 (2048x3072)'),
        ('1024x1536', '2:3 (1024x1536)'),
        ('512x768', '2:3 (512x768)'),
        ('256x384', '2:3 (256x384)'),
        ('128x192', '2:3 (128x192)'),
        ('64x96', '2:3 (64x96)'),
        ('32x48', '2:3 (32x48)'),
        ('3072x2048', '3:2 (3072x2048)'),
        ('1536x1024', '3:2 (1536x1024)'),
        ('768x512', '3:2 (768x512)'),
        ('384x256', '3:2 (384x256)'),
        ('192x128', '3:2 (192x128)'),
        ('96x64', '3:2 (96x64)'),
        ('48x32', '3:2 (48x32)'),
        ('1600x2000', '4:5 (1600x2000)'),
        ('1280x1600', '4:5 (1280x1600)'),
        ('1024x1280', '4:5 (1024x1280)'),
        ('800x1000', '4:5 (800x1000)'),
        ('640x800', '4:5 (640x800)'),
        ('512x640', '4:5 (512x640)'),
        ('256x320', '4:5 (256x320)'),
        ('128x160', '4:5 (128x160)'),
        ('2560x2048', '5:4 (2560x2048)'),
        ('1280x1024', '5:4 (1280x1024)'),
        ('640x512', '5:4 (640x512)'),
        ('320x256', '5:4 (320x256)'),
        ('160x128', '5:4 (160x128)'),
        ('80x64', '5:4 (80x64)'),
        ('40x32', '5:4 (40x32)'),
        ('2880x5120', '9:16 (2880x5120)'),
        ('2160x3840', '9:16 (2160x3840)'),
        ('1440x2560', '9:16 (1440x2560)'),
        ('720x1280', '9:16 (720x1280)'),
        ('360x640', '9:16 (360x640)'),
        ('180x320', '9:16 (180x320)'),
        ('90x160', '9:16 (90x160)'),
        ('45x80', '9:16 (45x80)'),
        ('1920x1080', 'Background Image (1920x1080)'),
        ('1280x720', 'Hero Image (1280x720)'),
        ('250x250', 'Website Banner (250x250)'),
        ('1200x630', 'Blog Image (1200x630)'),
        ('250x100', 'Logo Rectangle (250x100)'),
        ('100x100', 'Logo Square (100x100)'),
        ('16x16', 'Favicon (16x16)'),
        ('32x32', 'Social Media Icons (32x32)'),
        ('1600x500', 'Lightbox Images (1600x500)'),
        ('150x150', 'Thumbnail Image (150x150)')
    ])
    submit = SubmitField('Process Image')

    def validate_sizes(self, field):
        if not field.data:
            raise ValidationError('Please select at least one size.')

