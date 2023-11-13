import pathlib

from setuptools import find_packages, setup

with open('requirements.txt') as f:
    runtime_requirements = f.read().splitlines()

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

if __name__ == '__main__':
    setup(
        install_requires=runtime_requirements,
        python_requires='~=3.11',
        author='Dominik Haid',
        author_email='info@dominikhaid.de',
        long_description=README,
        long_description_content_type="text/markdown",
        url='https://github.com/dominikhaid/infratasks',
        version='0.0.1',
        name='infratasks',
        description='Install & bootstrap Linux and Windows Environments for development.',
        packages=find_packages('src'),
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'deploy = infratasks.main:main',
            ]
        },
        package_dir={"": "src"}
    )
