from django.test import TestCase
from datetime import datetime
from views import time_now
from child_app.my_calendar import another_method
from zoneinfo import ZoneInfo
from unittest.mock import DEFAULT, MagicMock, patch
import contextlib
import importlib
import pkgutil
import functools


def patch_in_app(app, *, attribute, wraps):
    module = importlib.import_module(app)
    targets = [
        f"{name}.{attribute}"
        for _, name, _ in pkgutil.walk_packages(module.__path__, prefix=f"{app}.")
        if hasattr(importlib.import_module(name), attribute)
    ]

    def decorator(func):
        @functools.wraps(func)
        def _func(*args):
            with patch_all(*targets, new=MagicMock(wraps=wraps)) as mock:
                return func(*args, mock)
        return _func

    return decorator


@contextlib.contextmanager
def patch_all(target, *targets, new=DEFAULT):
    with patch(target, new=new) as mock:
        if targets:
            with patch_all(*targets, new=mock):
                yield mock
        else:
            yield mock


class TestApp(TestCase):
    @patch_in_app("app", attribute="datetime", wraps=datetime)
    def test_datetime_now(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2022, 9, 10, 14, tzinfo=ZoneInfo("Asia/Tehran"))
        self.assertEqual(time_now(), "2022-09-10 14")
        self.assertEqual(another_method(), "2022-09-10 14")
