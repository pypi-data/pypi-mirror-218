from setuptools import setup, find_packages

for name in ['dynamic-sh', 'dynamic-llm', 'dynamic-api']:
    setup(
        name=name,
        version='0.0.2',
        description='',
        author='',
        author_email='',
        packages=find_packages(),
        install_requires=[
            # List of package dependencies
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
        ],
)