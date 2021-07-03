# Changelog

## nbfc-linux-0.1.2 (2012-07-03)
- Added more debug information on service startup
- Maked `EmbeddedControllerType` configurable
- Dropped the usage of `lm_sensors.c` in favour of `fs_sensors.c` because of build problems on some platforms
- Moved `tools/argany` to a separate project: [argparse-tool](https://github.com/braph/argparse-tool)

## nbfc-linux-0.1.1 (2012-05-02)
- Fixed type `--config-fie` to `--config-file`
- Using default temperature thresholds if those in config are empty or not present.  [Issue #2](https://github.com/braph/nbfc-linux/issues/2#issue-897727519)

## nbfc-linux-0.1.0 (2021-05-19)
- Added CHANGELOG.md
- Added --version flags to all programs
- Added pre-commit hook
