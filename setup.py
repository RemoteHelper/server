from setuptools import setup, find_packages

version = '0.0.0'

setup(
    name='remote_helper',
    version=version,
    description='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='remote task automation helper event redirect',
    author='',
    author_email='',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        i.strip() for i in open('requirements.txt').readlines()
    ],
    entry_points='''
    # -*- Entry points: -*-
    '''
)
