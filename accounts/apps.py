from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from django.contrib import admin
        admin.site.site_header  = '🌾 GaonKaam Administration'
        admin.site.site_title   = 'GaonKaam Admin'
        admin.site.index_title  = 'Village Labour Connect – Dashboard'
