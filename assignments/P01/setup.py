from setuptools import setup

setup (
    name = "maddy",
    version = '0.1',
    py_modules = ["maddy"],
    install_requires = [
        'click',
    ],
    entry_points = '''
        [console_scripts]
        maddy=maddy:cli
    ''',    
)