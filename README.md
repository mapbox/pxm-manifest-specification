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
    "license": "cc by-sa 4.0",
    "account": "customer1",
    "product": "november_aerial_photos",
    "notes": "Aerial photos from November 2017, Northern California",
    "srs": "EPSG:26910"
  }
}
```


## Usage

### 1. Create manifest file

To create a PXM manifest file, read the [specification](https://github.com/mapbox/pxm-manifest-specification/blob/master/pxm-manifest-spec.md) and

* Create the JSON file manually or with tools of your choice.

* Use the included command line script, `create-manifest.py`.

```
Usage: create-manifest.py [OPTIONS] [SOURCES]

  Create a PXM manifest file

Inputs:
  sources            Line-delimited list of s3 URLs

Options:
  -t, --tileset STR  Mapbox tileset id ({username}.{map})  [required]
  --license TEXT     License and usage restrictions  [required]
  --account STR      Valid mapbox account name  [required]
  --product TEXT     Product name  [required]
  --date STR         Images date  [required]
  --notes TEXT       Additional notes
  --bidx STR         Band index array
  --crs STR          Coordinate Reference System, EPSG:NNNN
  --color TEXT       rio color formula
  --ndv STR          nodata value array
  -o, --output PATH  Output file name
  ```

**Simple**

```bash
# source-list.txt is a line-delimited list of s3 URLs
python create-manifest.py source-list.txt \
    -t accountname.tileset \
    --license "CC BY-SA" \
    --account accountname \
    --product productname \
    --date 2018 \
    --output render1.json
```

**Advanced**

```bash
# List files in a AWS S3 bucket and pipe them into the python CLI
aws s3 ls mybucket/mydata/ --recursive | grep -E '*.tif$' | awk '{print "s3://mybucket/"$NF}' | python create-manifest.py \
    -t accountname.tileset \
    --license "CC BY-SA" \
    --account accountname \
    --product productname \
    --date 2018 \
    --output render1.json
```

### 2. Use manifest files to initiate a render

Currently, we review the manifest file and run the processing using an internal workflow.
Please [contact the sales team](https://www.mapbox.com/contact/sales/) and mention `PXM cc: team-satellite`.
