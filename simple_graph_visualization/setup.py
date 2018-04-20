from setuptools import setup, find_packages

setup(
    name="simple-graph-visualization",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1'],
    namespace_packages=['visualizer'],
    entry_points={
        'data.display':
            ['simple_graph_visualization=visualizer.simple_graph_visualization:SimpleGraphVisualization'],
    },
    zip_safe=True,
)
