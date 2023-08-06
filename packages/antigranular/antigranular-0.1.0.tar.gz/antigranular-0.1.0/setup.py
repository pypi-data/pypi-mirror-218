# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['antigranular',
 'antigranular.config',
 'antigranular.enclave_client',
 'antigranular.magics',
 'antigranular.models',
 'antigranular.utils']

package_data = \
{'': ['*']}

install_requires = \
['diffprivlib>=0.6.2,<0.7.0',
 'ipython>=8.12.0,<9.0.0',
 'oblv-client>=0.1.11,<0.2.0',
 'pandas>=2.0.1,<3.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'antigranular',
    'version': '0.1.0',
    'description': 'Antigranular is a community-driven, open-source platform that merges confidential computing and differential privacy. This creates a secure environment for handling and unlocking the full potential of unseen data..',
    'long_description': '# Unlock privacy: Getting along with Antigranular\nAntigranular is a community-driven, open-source platform that merges confidential computing and differential privacy. This creates a secure environment for handling and unlocking the full potential of unseen data.\n### Connect to Antigranular \nAntigranular works with just 4 characters `%%ag` , like magic!\nAny code written after the magic cell `%%ag` is run in our remote server \nwhich is a restricted environment allowing methods which guarantees\ndifferential privacy.\n\nInstall the Antigranular package using `pip`:\n```python\n!pip install antigranular\n```\nImport the `Antigranular` library:\n```python\nimport antigranular as ag\n```\nUse your client credentials and dataset or competition ID to connect to the AG Enclave Server:\n```python\nag.login("client id": "<client_secret_id>": competition="<competition_id>")\n```\nA succesful login will register the cell magic `%%ag`. \n\n### Loading Private Datasets \nPrivate dataset objects can be loaded in the form of `PrivateDataFrames` and `PrivateSeries`\nusing the `ag_utils` library. `ag_utils` is a package locally intalled in the remote server.\nThis eliminated the hassle of having to install anything other than \nantigranular package.\n\nYou can learn more about `PrivateSeries` and `PrivateDataFrames` on our quick \non [Private Pandas](./QS_pandas).\n\nWe use `load_dataset()` method to obtain a collection of private objects in the form of a dictionary.\nThe structure of the response dictionary, \ndataset path and private object names will be mentioned during the competition.\n```python\n%%ag\nfrom op_pandas import PrivateDataFrame , PrivateSeries\nfrom ag_utils import load_dataset \n"""\nSample response structure\n{\n    train_x : priv_train_x,\n    train_y : priv_train_y,\n    test_x : priv_test_x\n}\n"""\n# Obtaining the dictionary containing private objects\nresponse = load_dataset("<path_to_dataset>")\n\n# Unpacking the response dictionary\ntrain_x = response["train_x"]\ntrain_y = response["train_y"]\ntest_x = response["test_x"]\n```\n### Exporting Objects\nSince `%%ag` runs code in a very restricted environment, you need to export the differentially private \nobjects to the local environment in order to do further analysis.\nThe data objects can be exported using the `export` method in `ag_utils`.\n##### **API info**: `export(obj, variable_name:str)`\nThe remote object gets exported to the local environment and gets \nassigned to the stated variable name. It is important to note that`PrivateSeries` and `PrivateDataFrame`\nobjects cannot be exported and will raise an error if tried to \nbe exported in any manner.\n```python \n%%ag\nfrom ag_utils import export\ntrain_info = train_x.describe(eps=1)\nexport(train_info , \'variable_name\')\n```\nOnce exported, you can apply any form of data anlysis on the \ndifferentially private object.\n\n```python\n# Local code block\nprint(variable_name)\n--------------------------------------\n                    Age         Salary\n    count  99987.000000   99987.000000\n    mean      38.435953  120009.334336\n    std       12.167379   46255.486093\n    min       18.257448   40048.259037\n    25%       27.185189   80057.639960\n    50%       38.210860  120380.291216\n    75%       49.147724  159835.637091\n    max       59.282932  199920.664706\n```\n\n## Libraries Supported\n\n\n- **`pandas`**: A versatile data manipulation library that offers efficient data structures and tools for data analysis and manipulation.\n\n- **`op_pandas`**: A wrapped library specifically designed for differentially private data manipulation within the Pandas framework. It enhances privacy-preserving techniques and enables privacy-aware data processing.\n\n- **`op_diffprivlib`**: A differentially private library that provides various privacy-preserving algorithms and mechanisms for machine learning and data analysis tasks.\n\n- **`op_smartnoise`**: A library focused on privacy-preserving analysis using the SmartNoise framework. It provides tools for differential privacy and secure computation.\n\n- **`op_opendp`**: A library that offers differentially private data analysis and algorithms based on the OpenDP project. It provides privacy-preserving methods and tools for statistical analysis.',
    'author': 'Oblivious Software',
    'author_email': 'support@oblivious.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
