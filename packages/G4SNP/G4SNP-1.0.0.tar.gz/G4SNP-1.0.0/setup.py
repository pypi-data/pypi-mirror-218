import setuptools
with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
 name='G4SNP',
 include_package_data=True,
 version='1.0.0',
 author="Marc Shebaby",
 author_email="marc_shebaby@lau.edu",
 description="This code finds the distances of SNPs relative to the start codon based on their mRNA positions then executes G4Hunter tool and extracts the closest G4 sequences from the SNPs for several genes. ",
 
 packages=setuptools.find_packages(),
 classifiers=[
 "Programming Language :: Python :: 3.9",
 "License :: OSI Approved :: MIT License",
 "Operating System :: OS Independent",
 ],
 install_requires=['numpy','pandas','Bio'],
 url='https://github.com/Marc-shebaby/Capstone-Project.git',
 long_description=long_description,
 long_description_content_type='text/markdown',
)
 
 
