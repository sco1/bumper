# Changelog
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (`<major>`.`<minor>`.`<patch>`)

## [v2.0.1]
### Changed
* #9 Change expected CalVer format to `<YYYY>.<MM>.<MICRO>`
* #10 Feedback is now provided on the command line if a bump target file receives no changes
* Feedback is now provided on the command line for each file that receives a bump

## [v2.0.0]
### Changed
* #7 `versioning_type` is now a required configuration key for the `[tool.bumper]` table

### Added
* #7 Add support for CalVer, specified as `<YYYY>.<0M>.<MICRO>`

## [v1.0.0]
Initial release
