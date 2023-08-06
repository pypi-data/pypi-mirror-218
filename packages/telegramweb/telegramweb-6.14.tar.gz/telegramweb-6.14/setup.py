from setuptools import setup, find_packages

requires = [
    'requests',
    'SQLAlchemy',
    'beautifulsoup4',
    'psycopg2-binary',
    'lxml',
    'xmltodict'
]

DESCRIPTION = 'Python package for automatically fetching and pushing news by Telegram.'
LONG_DESCRIPTION = open("README.md").read()

setup(
    name='telegramweb',
    version='6.14',
    author='craziks',
    author_email='chandrashekharpanday07@gmail.com',
    url='https://github.com/craziks-creator/telegram-web',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    python_requires='>=3.8',
    install_requires=requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
