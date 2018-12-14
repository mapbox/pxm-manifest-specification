[![Build Status](https://travis-ci.org/mapbox/pxm-manifest-specification.svg?branch=master)](https://travis-ci.org/mapbox/pxm-manifest-specification) 

# pxm-manifest-specification

![pixelmonster](https://cloud.githubusercontent.com/assets/83384/4510319/28472d4a-4b29-11e4-8d02-0efc58ae4e7f.png)

Pixelmonster (PXM) is a service for processing remotely-sensed images and rendering them to raster tiles on the Mapbox platform.

This document describes the **PXM manifest file** - the interchange format for specifying the source images and processing parameters.


## Specification

The Manifest file is a JSON file (typically with a `.json` extension) described in this specification:

https://github.com/mapbox/pxm-manifest-specification/blob/master/pxm-manifest-spec.md

Example:
```json
{
  "sources": [
    "s3://my-bucket/20171101/17RLL630825.tif",
    "s3://my-bucket/20171101/17RLL675930.tif",
    "s3://my-bucket/20171101/17RLL675720.tif",
    "s3://my-bucket/20171101/17RLL705780.tif"
  ],
  "info": {
    "tilesets": [
      "customer1.aerials"
    ],
    "date": "2018",
    "license": "cc by-sa 4.0",
    "account": "customer1",
    "product": "november_aerial_photos",
    "notes": "Aerial photos from November 2017, Northern California",
    "crs": "EPSG:26910"
  }
}
```


## Usage

### 1. Create manifest file

To create a PXM manifest file, read the [specification](https://github.com/mapbox/pxm-manifest-specification/blob/master/pxm-manifest-spec.md) and

* Create the JSON file manually or with tools of your choice.

* Use the included command line script, `manifest.py`.


#### 1.1 Tools

Python 3.6+ is required and it is recommended to use a [venv](https://docs.python.org/3/library/venv.html).

```
pip install -r requirements.txt
python manifest.py --help
```

And example of its usage would be

```bash
# source-list.txt is a line-delimited list of s3 URLs
python manifest.py source-list.txt \
    -t accountname.tileset \
    --license "CC BY-SA" \
    --account accountname \
    --product productname \
    --date 2018 \
    --output render1.json
```

which would generate the following output;

```json
{
    "info": {
        "account": "accountname",
        "date": "2018",
        "license": "CC BY-SA",
        "notes": "",
        "product": "productname",
        "tilesets": [
            "accountname.tileset"
        ]
    },
    "sources": [
        "s3://my-bucket/test.tif"
    ],
    "version": "0.5.1"
}
```

A more advanced usage would be;

```bash
# List files in a AWS S3 bucket and pipe them into the python CLI
aws s3 ls mybucket/mydata/ --recursive | grep -E '.tif$' | awk '{print "s3://mybucket/"$NF}' | python manifest.py \
    -t accountname.tileset \
    --license "CC BY-SA" \
    --account accountname \
    --product productname \
    --date 2018 \
    --output render1.json
```


### 2. Manifest validation

PXM manifest uses [JSON Schemas](http://json-schema.org/) to validate manifest files.

The file `schemas/pxm-manifest-0.5.1.json` is used to validate the PXM manifest file.

An example of using `jsonschema` from the command line is

```
jsonschema -i render1.json schemas/pxm-manifest-0.5.1.json
```

### 3. Use manifest files to initiate a render

Currently, we review the manifest file and run the processing using an internal workflow.
Please [contact the sales team](https://www.mapbox.com/contact/sales/) and mention `PXM cc: team-satellite`.
