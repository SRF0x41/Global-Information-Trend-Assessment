from setuptools import setup, find_packages

setup(
    name="gita",
    version="0.1.0",
    author="Your Name",
    author_email="you@example.com",
    description="Global Information Trend Assessment System",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gita",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "numpy",
        "faiss-cpu",
        "requests",
        "beautifulsoup4",
        "praw",
        "feedparser",
        "sqlite3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
