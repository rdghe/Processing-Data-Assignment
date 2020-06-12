from django.contrib import admin

from.models import SyncBag, SyncItem, CurrentData, HistoryData

admin.site.register(SyncBag)
admin.site.register(SyncItem)
admin.site.register(CurrentData)
admin.site.register(HistoryData)