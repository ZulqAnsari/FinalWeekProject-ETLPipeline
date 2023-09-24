# ETL Pipeline using “Data Science Job Salaries” Dataset

## Overview

This project implements an ETL (Extract, Transform, Load) pipeline using “Data Science Job Salaries” dataset. The pipeline extracts salaries data, related job titles, and salaries trends data, transforms them into a single dataframe, and loads the transformed data into a database. Additionally, the project includes steps for various data visualisation using graphs.

## Dependencies

The following packages have to be installed:
1.	pandas
2.	os
3.	chardet from sqlalchemy 
4.	create_engine
5.	matplotlib.pyplot as plt

## Getting Started

To run the project, follow these steps:

1. Clone the repository to your local machine.
2. Open the project in any python environment.
3. Before running the code, make sure to delete the `your_database.db` if it exists in the project directory. This step helps avoid any potential writing permission errors.
4. Run the notebook cells to execute the ETL pipeline, save the data in DB and visualise the data with your tool of choice.

## Data Sources

The following data sources were utilised for this project:

- The `ds_salaries.csv` file was downloaded from [Kaggle]( https://www.kaggle.com/datasets/saurabhshahane/data-science-jobs-salaries ).

## Acknowledgements

I want to express my sincere gratitude to Xander Talent for their unwavering kindness and exceptional support during my time at the academy. Their guidance, mentorship, and encouragement have been invaluable assets that not only helped me achieve my immediate objectives but also instilled in me the confidence and skills to pursue even higher aspirations in the future.

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute the code for your own purposes.

## Conclusion

This ETL pipeline provides a comprehensive solution for extracting, transforming, and loading salaries data. It combines salaries data, job titles, and location trends data into a single dataframe, enabling further analysis and visualisation. The project demonstrates how to import data from CSV, perform data cleaning and transformation, and leverage visualisation for deeper insights.

Please feel encouraged to personalise and improve the pipeline to align with your unique needs and scenarios. Enjoy your journey of data analysis!
