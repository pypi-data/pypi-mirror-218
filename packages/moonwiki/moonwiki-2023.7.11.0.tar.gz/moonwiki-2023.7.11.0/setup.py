import setuptools

setuptools.setup(
	name="moonwiki",
	version="2023.7.11.0",
	author="RixTheTyrunt",
	author_email="rixthetyrunt@gmail.com",
	description="moonwiki is a wiki application made with Python",
	packages=["moonwiki"],
	url="https://github.com/RixTheTyrunt/moonwiki",
	python_requires=">=3.0.0",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown"
)