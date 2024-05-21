from django.contrib.admin import AdminSite
from . import views


class CustomAdminSite(AdminSite):
    site_header = 'My Custom Admin'
    site_title = 'My Custom Admin'
    index_title = 'Dashboard'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        urls += [
            path('statistics/', self.admin_view(views.statistics), name='statistics'),
        ]
        return urls

custom_admin_site = CustomAdminSite()

