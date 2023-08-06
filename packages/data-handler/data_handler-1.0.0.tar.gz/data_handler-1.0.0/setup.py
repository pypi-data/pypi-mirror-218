import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data_handler",
    version="1.0.0",
    author="Vardan Agarwal",
    author_email="vardanagarwal16@gmail.com",
    description="A package for handling and structuring of data before training.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vardanagarwal/data_handling",
    project_urls={
        "Bug Tracker": "https://github.com/vardanagarwal/data_handling/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['data_handler'],
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=[
        'albumentations',
        'matplotlib',
        'numpy',
        'opencv-python',
        'pandas',
        'Pillow',
        'pycocotools',
        'scikit_learn',
        'seaborn',
        'tqdm',
        'wget',
        ],
    extra_require={
        'all': [
            'lightly',
            ]
        }
)
