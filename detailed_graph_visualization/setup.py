from setuptools import setup, find_packages

setup(
    name="detailed-graph-visualization",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1'],
    namespace_packages=['visualizer'],
    entry_points={
        'data.display':
            ['detailed_graph_visualization=visualizer.detailed_graph_visualization:DetailedGraphVisualization'],
    },
    zip_safe=True,
)
