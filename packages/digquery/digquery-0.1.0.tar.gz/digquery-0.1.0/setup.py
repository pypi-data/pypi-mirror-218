from setuptools import setup

setup(
    name='digquery',
    version='0.1.0',
    author='Jay',
    author_email='techdjay@gmail.com',
    description='A Python package for querying DNS information using dig',
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
