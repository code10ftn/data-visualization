from setuptools import setup, find_packages

setup(
    name="html-reader",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1'],
    namespace_packages=['reader'],
    entry_points={
        'data.read':
            ['html_reader=reader.html_reader:HtmlReader'],
    },
    zip_safe=True,
)
