from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='digquery',
    version='0.1.1',
    author='Jay',
    author_email='techdjay@gmail.com',
    description='A Python package for querying DNS information using dig',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['digquery'],
    	entry_points={
		'console_scripts': [
			'digquery = digquery.dig_query_types:main',
			'pydig = digquery.dig_query_types:main',
			'mydig = digquery.dig_query_types:main',
		]
	},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
