# geekshop

dumpdata:
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > dump.json

не удается загрузить dump базы данных, получаю ошибку
python manage.py loaddata dump.json 
Traceback (most recent call last):
  File "/home/django/env/lib/python3.8/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "authapp_userprofile_user_id_key"
DETAIL:  Key (user_id)=(23) already exists.


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "manage.py", line 22, in <module>
    main()
  File "manage.py", line 18, in main
    execute_from_command_line(sys.argv)
  File "/home/django/env/lib/python3.8/site-packages/django/core/management/__init__.py", line 419, in execute_from_command_line
    utility.execute()
  File "/home/django/env/lib/python3.8/site-packages/django/core/management/__init__.py", line 413, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/home/django/env/lib/python3.8/site-packages/django/core/management/base.py", line 354, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/home/django/env/lib/python3.8/site-packages/django/core/management/base.py", line 398, in execute
    output = self.handle(*args, **options)
  File "/home/django/env/lib/python3.8/site-packages/django/core/management/commands/loaddata.py", line 78, in handle
    self.loaddata(fixture_labels)
  File "/home/django/env/lib/python3.8/site-packages/django/core/management/commands/loaddata.py", line 123, in loaddata
    self.load_label(fixture_label)
  File "/home/django/env/lib/python3.8/site-packages/django/core/management/commands/loaddata.py", line 190, in load_label
    obj.save(using=self.using)
  File "/home/django/env/lib/python3.8/site-packages/django/core/serializers/base.py", line 223, in save
    models.Model.save_base(self.object, using=using, raw=True, **kwargs)
  File "/home/django/env/lib/python3.8/site-packages/django/db/models/base.py", line 763, in save_base
    updated = self._save_table(
  File "/home/django/env/lib/python3.8/site-packages/django/db/models/base.py", line 868, in _save_table
    results = self._do_insert(cls._base_manager, using, fields, returning_fields, raw)
  File "/home/django/env/lib/python3.8/site-packages/django/db/models/base.py", line 906, in _do_insert
    return manager._insert(
  File "/home/django/env/lib/python3.8/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/home/django/env/lib/python3.8/site-packages/django/db/models/query.py", line 1270, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
  File "/home/django/env/lib/python3.8/site-packages/django/db/models/sql/compiler.py", line 1410, in execute_sql
    cursor.execute(sql, params)
  File "/home/django/env/lib/python3.8/site-packages/django/db/backends/utils.py", line 98, in execute
    return super().execute(sql, params)
  File "/home/django/env/lib/python3.8/site-packages/django/db/backends/utils.py", line 66, in execute
    return self._execute_with_wrappers(sql, params, many=False, executor=self._execute)
  File "/home/django/env/lib/python3.8/site-packages/django/db/backends/utils.py", line 75, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/django/env/lib/python3.8/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
  File "/home/django/env/lib/python3.8/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/django/env/lib/python3.8/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
django.db.utils.IntegrityError: Problem installing fixture '/home/django/geekshop/dump.json': Could not load authapp.UserProfile(pk=22): duplicate key value violates unique constraint "authapp_userprofile_user_id_key"
DETAIL:  Key (user_id)=(23) already exists.