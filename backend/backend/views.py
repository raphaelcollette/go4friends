import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str

@login_required
def protected_media(request, path):
    full_path = os.path.join(settings.MEDIA_ROOT, path)

    if not os.path.exists(full_path):
        raise Http404

    response = FileResponse(open(full_path, 'rb'))
    response['Content-Disposition'] = 'inline; filename=' + smart_str(os.path.basename(full_path))
    return response