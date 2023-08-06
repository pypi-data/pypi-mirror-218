from setuptools import setup, Extension

module_name = 'display'

module = Extension(
    module_name,
    sources=['display/arch/windows/display.c']
)

setup(
    name='display_package_test',
    version='1.0',
    description='Display Package',
    packages=['display', 'display.arch.windows'],  # Include package directories
    ext_modules=[module],
    package_data={
        'display.arch.windows': ['display.c']  # Include the C file in package data
    },
    include_package_data=True
)