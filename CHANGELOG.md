## [0.11.0] - 2025-06-17
### Added
- Force SSL for the aiohttp client to ensure secure connections to the Talkback API.

### Fixed
- Fixed an issue where searching for `title:*` would no longer return a wildcard search result. This was due to a change in the Talkback API.
  - Implemented a new search that doesn't use a query variable to return all results where required

### Changed
- GraphQL queries are now stored in files and loaded at runtime, instead of being hardcoded in the codebase. This allows for easier updates and modifications to the queries without changing the code.

## [0.10.0] - 2025-02-22
### Changed
- Changed authentication to email and password for generating token (Thanks Elttam for the API changes)
- Additional information is now collected from the API, without having to scrape the resource webpage. (Thanks Elttam for more API changes!)

### Fixed
- Vendor subscriptions weren't being imported. This has now been fixed.

## [0.9.1] - 2025-02-07
- Add licence information and other metadata

## [0.9.0] - 2025-02-07
- Beta release 0.9.0
