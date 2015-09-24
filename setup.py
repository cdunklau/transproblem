from setuptools import setup

requires = [
    'pyramid',
    'deform',
    'colander',
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
