# simplify data retrieving on citybrain.org

### retrieve **raw data** from **odps data source** on citybrain.org 
```python
from citybrain_official import client

data = client.retrieve_df(dataAddress='', sql='')
print(data)
```

### retrieve data as **pandas dataframe** from **odps data source** on citybrain.org 
```python
from citybrain_official import client

data = client.retrieve_df(dataAddress='', sql='')
print(data)
```

### retrieve **raw data** from **file data source** on citybrain.org 
```python
from citybrain_official import client

data = client.retrieve_df(dataAddress='')
print(data)
```

### retrieve data as **pandas dataframe** from **csv data source** on citybrain.org 
```python
from citybrain_official import client

data = client.retrieve_df(dataAddress='')
print(data)
```