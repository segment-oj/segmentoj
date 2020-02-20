from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
 
class AvatarStorage(FileSystemStorage):
    from django.conf import settings
    uid = 0
 
    def __init__(self, uid, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        self.uid = uid
        super(AvatarStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        import os
        ext = os.path.splitext(name)[1]
        d = os.path.dirname(name)
        fn = str(self.uid)
        name = os.path.join(d, fn + ext)
        return super(AvatarStorage, self)._save(name, content)