from django.core.exceptions import ValidationError
import os

def allow_only_image_validators(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extensions. Allowed extensions '+str(valid_extensions))
