
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


# https://github.com/pypa/setuptools_scm
setup(
    use_scm_version={
        "write_to": "napari_mclabel/_version.py",
        "local_scheme": "no-local-version",
    }
)
