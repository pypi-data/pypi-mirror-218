import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=['pytest'],
    name='linlangleyprime', # a unique name for PyPI
    version='0.8',
    author='Lin Chen, Yanhua Feng',
    author_email='lin.chen@ieee.org, yf@vims.edu',
    description='Demo for building a Python project',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='http://lin-chen-langley.github.io',
    project_urls = {
        'PyPI': 'https://pypi.org/manage/project/linlangleyprime/releases/',
        },
    classifiers=[
      'Development Status :: 1 - Planning',
      'Environment :: X11 Applications :: GTK',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Apache Software License',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python',
      'Topic :: Desktop Environment',
      'Topic :: Text Processing :: Fonts'
      ],
    install_requires=requirements,
    package_dir={'':'src'}, # location to find the packages
    packages=setuptools.find_packages(where="src"),
    #packages=['primepackage', ], # packages and subpackages containing .py files
    python_requires=">=3.11",
    scripts=['src/generator',], # the executable files will be installed for user
    license='Apache License 2.0',
)
