from django.contrib import admin
from BuckIt.buckitapp.models import Badge, UserProfile, Task, Tag, Ownership

admin.site.register(Badge)
admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(Ownership)