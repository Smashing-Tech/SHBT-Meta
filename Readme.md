# Smash Hit Blender Tools Development Scripts

These are some utilities that make developing smash hit blender tools easier. They are part of a lot of the release workflow.

## Files

### `sign_update.py`

This will create a signature file for an SHBT update, given the path to the zip and the private key.

If you don't have a key pair, run:

```sh
python ./sign_update.py new-keys
```

to generate a new keypair. The public will go in the current dir and the private will go in the directory one level up in addition to having a random number appended to its name.

Then when you want to sign an update, run:

```sh
python ./sign_update.py /path/to/file/to/sign.zip /path/to/private.key
```

and the `.zip.sig` file will be generated!

## Todo

* Add `zip_release.py` for zipping a release
* Add `generate_release.py` for zipping and signing a release in one command
