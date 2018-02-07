# pxm-manifest-specification

**Note: This repo will eventually be public. Do not add any details or links to private projects!**

Pixelmonster (PXM) is a service for processing remotely-sensed images and rendering them to map tiles on the Mapbox platform. This document describes the **manifest file** - the interchange format for PXM which specifies the source images and the processing parameters.


## Specification

See https://github.com/mapbox/pxm-manifest-specification/blob/master/pxm-manifest-spec.md

## Usage

### 1. Create Manifest Files

Authoring a manifest file manually is certainly possible given a good understanding of the spec.
However, to improve usability, we provide a command line utility, `create-manifest.py`, to help manifest authors.

Starting with a line-delimited text file with s3 URLs, you can create a Manifest file using:

```
cat source-list.txt | python create-manifest.py \
    -t perrygeo.trymanifest1 \
    --license WTFPL \
    --account perrygeo \
    --product trymanifest \
    --date 2018 \
    > my-manifest.json
```


### 2. Using Manifest Files

Please contact the Mapbox Satellite team. Currently,
we review each Manifest file and manually run the processing using an internal workflow.


