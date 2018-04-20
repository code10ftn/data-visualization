from setuptools import setup, find_packages

setup(
    name="json-reader",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1'],
    namespace_packages=['reader'],
    entry_points={
        'data.read':
            ['json_reader=reader.json_reader:JsonReader'],
    },
    zip_safe=True,
)
