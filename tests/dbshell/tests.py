from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import OperationalError
from django.test import TestCase


class DBShellCommandTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='jon', password='snow')

    def test_using_valid_sql_statement_should_be_ok(self):
        """Using valid SQL statement on existing table should work"""
        u = User.objects.get(pk=1)
        out = StringIO()
        call_command('dbshell', command='select username from auth_user', stdout=out)
        self.assertIn(u.username, out.getvalue())

    def test_using_invalid_sql_statement_should_raise_exception(self):
        """Using invalid SQL statement should raise OperationalError"""
        with self.assertRaises(OperationalError):
            call_command('dbshell', command='invalid clause from auth_user')
