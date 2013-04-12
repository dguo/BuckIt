from django.contrib import admin
from BuckIt.buckitapp.models import User, Task, Tag, Ownership

admin.site.register(User)
admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(Ownership)