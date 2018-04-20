from setuptools import setup, find_packages

setup(
    name="file-system-reader",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1'],
    namespace_packages=['reader'],
    entry_points={
        'data.read':
            ['file_system_reader=reader.file_system_reader:FileSystemReader'],
    },
    zip_safe=True,
)
