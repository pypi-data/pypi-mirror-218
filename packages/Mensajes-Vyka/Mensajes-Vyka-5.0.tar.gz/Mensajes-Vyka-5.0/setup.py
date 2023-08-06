from setuptools import setup, find_packages

setup(
    name='Mensajes-Vyka',
    version='5.0',
    description='Un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='David Rojas',
    author_email='rojasdavid9618@gmail.com',
    url='https://www.davidrojas.com',
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip() for paquete in open('requirements.txt').readlines()],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities'
    ]
)
