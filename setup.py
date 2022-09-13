from setuptools import setup, find_packages

requirements = [
    'aiofiles==22.1.0',
    'anyio==3.6.1',
    'beautifulsoup4==4.11.1',
    'certifi==2022.6.15.1',
    'cffi==1.15.1',
    'cryptography==38.0.1',
    'h11==0.12.0',
    'h2==4.1.0',
    'hpack==4.0.0',
    'httpcore==0.15.0',
    'httpx==0.23.0',
    'hyperframe==6.0.1',
    'idna==3.3',
    'jaraco.classes==3.2.2',
    'jeepney==0.8.0',
    'keyring==23.9.1',
    'more-itertools==8.14.0',
    'prompt-toolkit==3.0.31',
    'pycparser==2.21',
    'rfc3986==1.5.0',
    'SecretStorage==3.3.3',
    'sniffio==1.3.0',
    'soupsieve==2.3.2.post1',
    'wcwidth==0.2.5',
]

setup(
    name='canopto',
    version='1.0.2',
    author='Atticus T',
    author_email='theresurgence2@proton.me',
    url="https://github.com/theresurgence/canopto",
    description="canopto is a tool to sync course files and videos from the Canvas LMS hosted by the National University of Singapore(NUS).",
    license='GPLv3',
    packages=find_packages(),
    entry_points={
            'console_scripts': [
                'canopto=canopto.__main__:cli'
            ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    keywords='canopoto canvas panopto nus',
    install_requires=requirements,
    zip_safe=False
)
