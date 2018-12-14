PXM JSON Schemas
================

pxm-manifest-0.5.1.json
-----------------------

This schema can be used to validate a PXM manifest file (version 0.5.1).

The example below uses the Python jsonschema package.

```
$ python -m jsonschema -i manifest.json pxm-manifest-0.5.1.json
```

pxm-source-gdal-1.0.0.json
--------------------------

This schema can be used to validate a PXM source dataset by checking the JSON
output of gdalinfo.

The example below uses the Python jsonschema package.

```
$ gdalinfo example.tif -json > example.json
$ python -m jsonschema -i example.json pxm-source-gdal-1.0.0.json
```

pxm-source-rasterio-1.0.0.json
------------------------------

This schema can be used to validate a PXM source dataset by checking the JSON
output of rio-info.

The example below uses the Python jsonschema package.

```
$ rio info example.tif > example.json
$ python -m jsonschema -i example.json pxm-source-rasterio-1.0.0.json
```

