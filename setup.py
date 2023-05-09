from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

packages = [
    "aiomk_api",
    "aiomk_api.utils",
    "aiomk_api.types"
]

if __name__ == "__main__":
    setup(
        name="aiomk_api",
        author="Yumax-panda",
        url="https://github.com/Yumax-panda/aiomk_api",
        use_scm_version=True,
        setup_requires=["setuptools_scm"],
        packages=packages,
        license="MIT",
        description="An asynchronous API wrapper for the MK8DX 150cc Lounge.",
        install_requires=requirements,
        long_description=long_description,
        long_description_content_type="text/markdown",
    )