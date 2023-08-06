# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gecs', 'gecs.utils']

package_data = \
{'': ['*']}

install_requires = \
['lightgbm==3.3.5',
 'matplotlib==3.7.1',
 'numpy==1.23.5',
 'pandas==1.5.2',
 'poetry==1.3.2',
 'pytest==7.2.1',
 'scikit-learn==1.2.2',
 'scipy==1.10.1',
 'tqdm==4.65.0',
 'typer==0.9.0']

setup_kwargs = {
    'name': 'gecs',
    'version': '0.29.0',
    'description': 'LightGBM Classifier with integrated bayesian hyperparameter optimization',
    'long_description': "![a gecko looking at the camera with bayesian math in white on a pink and green background](documentation/assets/header.png)\n\n\n# (100)gecs\n\nBayesian hyperparameter tuning for LGBMClassifier with a scikit-learn API\n\n## Table of Contents\n\n- [Project Overview](#project-overview)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Contributing](#contributing)\n- [License](#license)\n\n## Project Overview\n\nThe package `gecs` provides the class `GEC`, which is a child class of the class `LGBMClassifier` from the package `lightgbm`. It can be imported from `gecs.gec` and then used in place of `LGBMClassifier`, with the same API. The difference to `LGBMClassifier` lies in the fact that `GEC`automatically does bayesian hyperparameter optimization of the parameters `learning_rate`, `reg_alpha`, `reg_lambda`, `min_child_samples`, `min_child_weight`, `colsample_bytree` and optionally also of `num_leaves` and `n_estimators`.\n\nThe fit method has two new parameters: `n_iter`, which sets the number of hyperparameter combinations that will be tried (the higher `n_iter` the higher the expected accuracy, but at a cost of compute) and `fixed_hyperparameters`, which determines which hyperparameters of the LGBM classifier won't get optimized. By default, these are `n_estimators` and `num_leaves`, as the highest possible value for these hyperparameters is almost always optimal. The idea then is to set these as high as makes sense in a specific context and then optimize the other hyperparameters.\n\n\n## Installation\n\n    pip install gecs\n\n## Usage\n\n    from gecs.gec import GEC\n\n    gec.fit(X, y)\n\n    gec.serialize(path) # stores gec data and settings, but not underlying LGBMClassifier attributes\n\n    gec2 = GEC.deserialize(path, X, y) # X and y are necessary to fit the underlying LGBMClassifier\n\n    yhat = gec.predict(X)\n\n    gec.freeze() # freeze GEC so that it behaves like a LGBMClassifier\n    gec.unfreeze() # unfreeze to enable GEC hyperparameter optimisation\n\n\n    \n\n\n\n## Contributing\n\nIf you want to contribute, please reach out and I'll design a process around it.\n\n## License\n\nMIT\n\n## Contact Information\n\nYou can find my contact information on my website: [https://leonluithlen.eu](https://leonluithlen.eu)",
    'author': 'Leon Luithlen',
    'author_email': 'leontimnaluithlen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/0xideas/sequifier',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<3.11.0',
}


setup(**setup_kwargs)
