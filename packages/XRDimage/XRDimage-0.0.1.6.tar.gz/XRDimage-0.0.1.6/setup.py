import setuptools 

setuptools.setup(
      name='XRDimage',
      version='0.0.1.6',
      description='XRDImage is a Python 3 package developed by the SDLE Research Center at Case Western Reserve University in Cleveland, OH.',
      long_description="""
                  XRDImage is a Python3 package developed by the SDLE Research Center at Case Western Reserve University in Cleveland, OH. 
                  X-Ray Diffraction (XRD) is a technique used to identify and quantify crystalline phases in a material. By obtaining diffraction patterns, 
                  XRD enables the identification of crystalline phases and orientation, determination of various structural properties such as lattice parameters, 
                  stain, grain size, epitaxy, phase composition, and preferred orientation. The analysis of diffraction patterns also allows for 
                  the identification of internal stress and defects in crystals, providing valuable insights into material performance in different environments.

                  Due to the nature of XRD Imaging techniques, most XRD images may not turn out perfect out of the lab. In XRDImage, 
                  we have created an image processing pipeline with multitudes of functions to pre-process XRD Images.
                   """,
      url='http://engineering.case.edu/centers/sdle/',
      author='Weiqi Yue, Ethan Fang, Gabriel Ponon, Zhuldyz Ualikhankyzy, Nathaniel K. Tomczak, Pawan K. Tripathi, Roger H. French',
      author_email='wxy215@case.edu, pkt19@case.edu, roger.french@case.edu',
      license='MIT License',
      packages=setuptools.find_packages(),
      #package_dir={'XRDimage': './XRDimage'},
#      package_data={'XRDimage': ['data','files/data/FullSizeModules/*','files/tutorials/*','files/data/out','README.rst']},
      python_requires='>=3.8',
      install_requires=['numpy', 'Pillow', 'opencv-python', 'matplotlib', 'imageio', 'scikit-learn'],
#      include_package_data=True,
      project_urls={"Documentation":"https://xrdimage-doc.readthedocs.io/en/latest/","Bugtracker": "https://bitbucket.org/cwrusdle/xrd-image/src/main/"},
)

