from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Poll)
admin.site.register(Option)
admin.site.register(Submission)