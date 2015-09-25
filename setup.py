from setuptools import setup

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'deform>=0.9,<1.0',
    'lingua',
    'babel',
]

setup(
    name='tutorial',
    install_requires=requires,
    entry_points="""\
    [paste.app_factory]
    main = tutorial:main
    """,
)
