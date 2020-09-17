from django.conf import settings


class DatabaseAppRouter:
    def db_for_read(self, model, **hints):
        return settings.DATABASE_APPS_MAPPING.get(model._meta.app_label)
    
    def db_for_write(self, model, **hints):
        db = settings.DATABASE_APPS_MAPPING.get(model._meta.app_label)
        return None if db == 'ultron' else db
    
    def allow_relation(self, obj1, obj2, **hints):
        app_obj1 = settings.DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
        app_obj2 = settings.DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
        return True if app_obj1 == app_obj2 else False
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return False if db == 'ultron' else db
        