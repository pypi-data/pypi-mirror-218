# Bandersnatch Updated Plugin

A [bandersnatch](https://pypi.org/project/bandersnatch/) plugin to filter out
old packages.

This plugin works by checking if the `upload_time` field in a package's release
file is older than a given number of days, and filtering it out if it is.

## Configuration

To use, install this package and add the following to your `bandersnatch.conf`:

```cfg
[plugins]
enabled =
    ...
    updated

[updated]
maximum_days_old = 1095
```

Change `maximum_days_old` to your desired age.
