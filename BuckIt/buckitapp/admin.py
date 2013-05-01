from django.contrib import admin
from BuckIt.buckitapp.models import UserProfile, Task, Tag, Ownership

admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(Ownership)