import os, sys

paths = os.listdir(os.path.dirname(os.path.abspath((__file__))))
for path in paths:
    if path.endswith('.docx'):
        new_path = path.replace(' ', '_')
        os.system('mv "%s" "%s"' % (path, new_path))
