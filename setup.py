from setuptools import setup, find_packages

setup(
    name="action",
    version="0.1.0",
    license="Apache-2.0",
    author="Giovanni Vigna",
    author_email="vigna@ucsb.edu",
    maintainer="Gabriel Pizarro",
    maintainer_email="gpizarro@ucsb.edu",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "kombu ~= 5.3",
    ],
    url="https://github.com/action-ai-institute/ai-stack",
    project_urls={
        "Homepage": "https://github.com/action-ai-institute/ai-stack",
        "Issues": "https://github.com/action-ai-institute/ai-stack/issues",
    },
    packages=find_packages(),
)