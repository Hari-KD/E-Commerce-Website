from django.db import models

# Dashboard app doesn't need its own models
# It will use models from store and users apps
def get_image_url(self):
    if self.image:
        return self.image
    elif self.image_file:
        return self.image_file.url
    return 'path/to/default/image.jpg'