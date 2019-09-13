import pandas as pd
import pandas_schema
from pandas_schema import Column
from pandas_schema.validation import CustomElementValidation
import numpy as np


def check_int(num):
    try:
        int(num)
    except ValueError:
        return False
    return True

# read the data
data = pd.read_csv('noon.csv')
data.dtypes
# define validation elements
int_validation = [CustomElementValidation(lambda i: check_int(i), 'is not integer')]
null_validation = [CustomElementValidation(lambda d: d is not np.nan, 'this field cannot be null')]
#d is not np.nan
# define validation schema
schema = pandas_schema.Schema([
            Column('Name', null_validation),
            Column('SKU', null_validation),
            Column('Price', int_validation + null_validation),
            Column('Special price', int_validation + null_validation),
            Column('Qty', int_validation + null_validation)])

# apply validation
errors = schema.validate(data)

for error in errors:
        print('"{}" failed!'.format(error.value))

errors_index_rows = [e.row for e in errors]

data_clean = data.drop(index = errors_index_rows)

# save data
pd.DataFrame({'col':errors}).to_csv('errors.csv')