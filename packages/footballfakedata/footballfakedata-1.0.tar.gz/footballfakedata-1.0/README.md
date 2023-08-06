# Fake Footballer

[![PyPI Version](https://img.shields.io/pypi/v/fake-footballer.svg)](https://pypi.org/project/fake-footballer/)
[![License](https://img.shields.io/pypi/l/fake-footballer.svg)](https://github.com/your-username/fake-footballer/blob/main/LICENSE)

Generate fake footballer data with this Python package.

## Installation

You can install the package using pip:

```shell
pip install fake-footballer
```
## Usage

Import the FootballerGenerator class and other necessary modules to generate fake footballer data:

```
from fake_footballer import FootballerGenerator, position
from fake_footballer.data import ENG, ITA, SPA, BRA
```

Initialize the FootballerGenerator object with the desired data for a specific country:
```
country = 'ENG'
footballer_generator = FootballerGenerator(ENG['first_names'], ENG['last_names'], ENG['cities'], ENG['club'], position)
```
Generate fake footballer data:
```
num_footballers = 10
fake_footballers = [footballer_generator.generate_fake_footballer(country) for _ in range(num_footballers)]
```
Create a pandas DataFrame from the generated data:
```
import pandas as pd
df = pd.DataFrame(fake_footballers)
```
Save the DataFrame to an Excel file:
```
filename = f'fake_{country}_footballers.xlsx'
df.to_excel(filename, index=False)
```
For more usage examples and customization options, please refer to the documentation.

## Documentation
For detailed documentation, refer to the official documentation.

## Contributing
Contributions are welcome! If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes and commit them.
4. Open a pull request on the main branch.
5. Please review the contribution guidelines for more details.

## License
This project is licensed under the MIT License.
