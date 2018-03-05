# pxm-manifest-specification

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
    "vendor": "customer1",
    "product": "november_aerial_photos",
    "notes": "Aerial photos from November 2017, Northern California",
    "srs": "EPSG:26910"
  }
}
```


## Usage

### 1. Create manifest file

To create a PXM manifest file, you can read the [specification](https://github.com/mapbox/pxm-manifest-specification/blob/master/pxm-manifest-spec.md) and 

* Create the JSON file manually or with tools of your choice.
* Use the included command line script, `create-manifest.py`.

Send a line-delimited list of s3 URLs and specify the options as shown in this example:

```bash
# source-list.txt is a line-delimited list of s3 URLs
cat source-list.txt | \
python create-manifest.py \
    -t accountname.tileset \
    --license "CC BY-SA" \
    --account accountname \
    --product productname \
    --date 2018 \
    > render1.json
```


### 2. Use manifest files to initiate a render

Please contact the Mapbox Satellite team. Currently,
we review the manifest file and run the processing using an internal workflow.


