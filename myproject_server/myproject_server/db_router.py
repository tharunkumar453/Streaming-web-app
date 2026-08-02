class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        return 'replica'  # Use the replica database for read operations

    def db_for_write(self, model, **hints):
        return 'default'  # Use the default database for write operations   
    def allow_relation(self, obj1, obj2, **hints):
        # Allow any relation if both models are in the same database
        db_list = ('default', 'replica')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Allow migrations only on the default database
        if db == 'default':
            return True
        return False