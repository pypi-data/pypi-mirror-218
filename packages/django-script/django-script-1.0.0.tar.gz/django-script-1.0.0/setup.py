from setuptools import setup, find_packages

setup(
    name='django-script',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'django = starts.starts:create_folder'
        ]
    },
    install_requires=[
        'django-script','APScheduler'
    ],
    author='Santhosh Parthiban',
    author_email='santhoshparthiban2002@gmail.com',
    description='Django-Genius is a Python package that automates the setup and configuration of Django and React applications. This streamlines the development process, allowing developers to focus on building application features.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
