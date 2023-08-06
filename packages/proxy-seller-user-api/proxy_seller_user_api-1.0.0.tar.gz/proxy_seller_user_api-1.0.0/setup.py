from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='proxy_seller_user_api',
    version='1.0.0',
    author='proxy-seller',
    author_email='support@proxy-seller.com',
    description='Interaction with user api',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/proxy-seller/user-api-python',
    packages=find_packages(),
    install_requires=['requests>=2.25.1','json'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='api client',
    project_urls={
        'Documentation': 'https://proxy-seller.com/personal/api/'
    },
    python_requires='>=3.7'
)
