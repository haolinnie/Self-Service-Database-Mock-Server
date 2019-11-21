from setuptools import find_packages, setup

setup(
    name='ssd_api',
    version='1.0.0',
    author='Tiger Nie',
    author_email='nhl0819@gmail.com',
    packages=['ssd_api'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'coverage>=4.5.4',
        'Flask==1.1.1',
        'Flask-RESTful==0.3.7',
        'gunicorn==19.9.0',
        'itsdangerous==1.1.0',
        'Jinja2==2.10.3',
        'MarkupSafe==1.1.1',
        'PyMySQL==0.9.3',
        'pytest==5.2.1',
        'python-dateutil==2.8.0',
        'pytz==2019.3',
        'six==1.12.0',
        'Werkzeug==0.16.0',
        'xlrd==1.2.0',
    ],
)
