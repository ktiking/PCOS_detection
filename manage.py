#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
# get the tools we need
import os
import sys


def main():
    """Run administrative tasks."""
    # tell Django where to find our settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcos_detection.settings')
    try:
        # get Django's command line tools
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # if Django isn't installed, tell the user what to do
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # run whatever command the user typed
    execute_from_command_line(sys.argv)


# if someone runs this file directly (not importing it)
if __name__ == '__main__':
    main()
