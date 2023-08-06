from setuptools import setup, find_packages

if __name__ == '__main__':
    name = 'taichu-storage'

    requirements = ['boto==2.49.0', 'esdk-obs-python==3.22.2']

    long_description = 'storage sdks aggregation'
    # with open('README.md', 'r') as f:
    #     long_description = f.read()

    setup(
        name=name,
        version='0.0.1',
        description='taichu storage is a tool for storage',
        long_description=long_description,
        author='taichu platform team',
        python_requires=">=3.6.0",
        url='',
        keywords='taichu',
        packages=find_packages(),
        install_requires=requirements,
        include_package_data=True,
        package_data={
            '': ['*.sh'],
        }
    )
