from distutils.core import setup

description="""
HTML5 Server-Side Events for Django 1.3+
"""

setup(
    name="django-sse",
    version='0.4.1',
    url='https://github.com/niwibe/django-sse',
    license='BSD',
    platforms=['OS Independent'],
    description = description.strip(),
    author = 'Andrei Antoukh',
    author_email = 'niwi@niwi.be',
    maintainer = 'Andrei Antoukh',
    maintainer_email = 'niwi@niwi.be',
    packages = [
        'django_sse',
    ],
    requires = [
        'sse',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
