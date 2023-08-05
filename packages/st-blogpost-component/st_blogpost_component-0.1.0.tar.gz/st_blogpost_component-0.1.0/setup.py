import setuptools

setuptools.setup(
    name="st_blogpost_component",
    version="0.1.0",
    author="YM",
    author_email="",
    description="",
    long_description="custom component to display blog post card for personal blog",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
