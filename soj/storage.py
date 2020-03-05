from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
 
class AvatarStorage(FileSystemStorage):
    from django.conf import settings
 
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(AvatarStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        import os, time
        ext = os.path.splitext(name)[1]
        d = os.path.dirname(name)
        fn = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        name = os.path.join(d, fn + ext)
        return super(AvatarStorage, self)._save(name, content)