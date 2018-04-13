# PXM manifest specification

* Status: DRAFT, not for production use
* Authors: Mapbox Satellite team
* Date: April 13, 2018
* Version: 0.4

## 1. Summary

Pixelmonster (PXM) is a service for processing remotely-sensed images and rendering them to map tiles on the Mapbox platform. This document describes a **manifest file** - the interchange format for PXM which specifies the source images and the processing parameters.

## 2. File Format

The PXM manifest files uses JavaScript Object Notation (JSON) open-standard format. The JSON format is a language-independent, human-readable, structured format.

## 3. Structure

The manifest file MUST contain a single valid JSON object with the following required members:

- `sources` : a list of source images to process
- `info` : the parameters for the render

We will discuss each below:

### 3.1.  sources

The `sources` object MUST be a list of source images to be rendered. Each element must be an S3 URI to a valid raster dataset, one of the following:

- GeoTiff (with a .tif extension)
- JPEG2000 image (.jp2)
- Others?? (ECW)

Image must be georeferenced and use 8-bit color depth with Red, Green and Blue bands.

The basename of the s3 paths must contain only ascii letters, numbers and `_`. Importantly dashes `-` are not allowed in the basename. For example:


    s3://my-bucket/image1.tif  # valid
    s3://my-bucket/image-1.tif # NOT a valid source path

Each source file MUST have a deterministic nodata mask, either:

- A non-lossy alpha band or internal mask
- Non-lossy R, G and B bands with internal `ndv` metadata
- Lossy R, G and B where the entire image is valid pixels.

### 3.2. info

The `info` object MUST contain the following keys:

- `tilesets`
- `license`
- `notes`
- `account`
- `product`
- `date`


And MAY contain the following OPTIONAL keys which are only required for special cases. Note that there may be additional costs associated with

- `bidx`
- `crs`
- `color`
- `ndv`

#### 3.2.1. tilesets

An array of at least one Mapbox tileset id defining the destination layer(s) to render to.

 Each tileset id must be of the form `{username}.{mapname}` and the username MUST be associated with your Mapbox account.

 Example:

    "tilesets": ["customer1.map1", "customer1.map2"]

#### 3.2.2. license

Licensing information, and any other usage restrictions we should be aware of.

Example:

    "license": "License: Commercial license from Customer1 Inc."

#### 3.2.3. notes

String describing the source data in human-readable terms.

Example:

    "notes": "Novemember 2017 Aerial Photos from Santa Rosa, CA"

#### 3.2.4. account

String; the Mapbox account name under which PXM will render the map. MUST not contain spaces and have max 32 chars.

Example:

    "account": "customer1"

#### 3.2.5. product

String identifying the unique product line distributed by a vendor. MUST not contain any spaces.

Example:

    "product": "us_aerial_2017"

#### 3.2.6. date

String; Images date (SHOULD be either in `YYYY` or `YYYY-MM-DD` format).

Example:

    "date": "2017"
    or
    "date": "2017-01-01"

#### 3.2.7. crs

Optional. Describes the source coordinate reference system. The crs is a string representing an `EPSG:NNNN` code. Do not include the crs key if your data already has properly defined spatial referencing.


    "crs": "EPSG:3948"

#### 3.2.8. color

Optional. A JSON object defining a [rio color](https://github.com/mapbox/rio-color) formula which will be applied to the rendered imagery.

The key(s) are used as a regex pattern to match the image file name. The value(s) MUST be valid `rio color` formulas. Do not include the `color` key if no color enhancement is required.

When a single color formulae is required for all source files

      "color": {
          ".": "sigmoidal RGB 3 0.6"
      }

If there are multiple color formula's that need to be applied, use a string unique to the subset of imagery as the key and the color formula as the value.

       "color": {
          "west_aerial_photos_2011": "sigmoidal RGB 4 0.5",
          "east_aerial_photos_2011": "sigmoidal RGB 3 0.4 gamma B 1.1 saturation 1.25",
      }


#### 3.2.9. ndv

Optional. String containing a 3-element array of integers defining the the `nodata` value of the red, green and blue bands respectively.  Often, this value will be either `[255, 255, 255]` or `[0, 0, 0]` (with "" quotes). Do not specify `ndv` if your source data already contains the correct nodata value in the raster’s metadata.

For example,

    "ndv": "[0, 0, 0]"
    or
    "ndv": "[255, 255, 255]"

#### 3.2.10. bidx

Optional. The band indexes used to form an RGB image from source data. The source data may have superflous bands, different band ordering, or some other band configuration that prevents from pxm from using it directly.

The optional `bidx` describes which bands to use. The value should be a string of comma-separated integers representing the band indexes for red, green and blue respectively. All other bands will be dropped (useful for dropping the near-infrared band for example)

The value is passed directly to the [rio stack](https://github.com/mapbox/rasterio/blob/master/docs/cli.rst#stack) `--bidx` option.


    "bidx": "1,2,3"


## 4. Examples

The following is a minimal PXM manifest in JSON format


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
      }
    }



The following is a complete PXM manifest in JSON format


    {
      "sources": [
        "s3://my-bucket/20171101/17RLL630825.tif",
        "s3://my-bucket/20171101/17RLL675930.tif",
        "s3://my-bucket/20171101/17RLL675720.tif",
        "s3://my-bucket/20171101/17RLL705780.tif"
      ],
      "info": {
        "tilesets": [
          "customer1.aerials",
          "customer1.aerials-2018"
        ],
        "color": {
            ".": "sigmoidal RGB 4 0.5",
            "7RLL675": "sigmoidal RGB 3 0.4 gamma B 1.1 saturation 1.25",
        },
        "bidx": "1,2,3",
        "ndv": "[255, 255, 255]",
        "date": "2018-02-20",
        "license": "cc by-sa 4.0",
        "account": "customer1",
        "product": "november_aerial_photos",
        "notes": "Aerial photos from November 2017, Northern California",
        "crs": "EPSG:26910"
      }
    }
