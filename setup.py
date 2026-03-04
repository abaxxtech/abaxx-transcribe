from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = [l.strip() for l in f if l.strip() and not l.startswith("#")]

setup(
    name="abaxx-transcribe",
    version="0.1.0",
    author="Abaxx Technologies",
    author_email="dev@abaxx.tech",
    description="Local, privacy-first meeting audio transcription with speaker diarization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abaxxtech/abaxx-transcribe",
    packages=find_packages(exclude=["tests*", "docs*", "scripts*"]),
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={"console_scripts": ["transcribe-and-diarize=transcribe_and_diarize.__main__:cli"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
)
