import setuptools

with open("README.md", "r") as fh:
	description = fh.read()

setuptools.setup(
	name="datapeach-wrapper",
	version="0.0.1",
	author="datapeach",
	author_email="datapeach@gigarion.com",
	packages=["wrapper"],
	description="datapeach wrapper",
	long_description=description,
	long_description_content_type="text/markdown",
	url="",
	license='MIT',
	python_requires='>=3.8',
	install_requires=[]
)
