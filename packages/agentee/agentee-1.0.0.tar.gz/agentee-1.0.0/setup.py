from setuptools import setup, find_packages

setup(
    name='agentee',
    version='1.0.0',
    author='w12231',
    description='LLM + knowledge graph',
    url='https://github.com/your-username/your-package-repo',
    packages=find_packages(),
    install_requires=[
        "tiktoken",
        "openai",
        "colorama",
        "jwt",
        "colorlog",
        "python-dotenv"
    ],

)
