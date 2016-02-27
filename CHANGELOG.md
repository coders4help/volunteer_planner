# Change Log
All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- new docstrings to source code

### Changed
- CHANGELOG is now Markdown

### Fixed
- some PEP8 fixes of the source code

### Removed


## [3.0.1] - 2016-01-09
### Added
- UI: User can her history of work shifts
- UI: User can see upcoming shifts (the shifts she signed up for)
- Delete user: User can delete her account - the data is anonymized
- Social Impact Lab was added as supporter

### Changed
- updated translations and wording
- UI/Account creation: There is now an explicit message on account creation form explaining what happens here. (users often mistake the creation form for the login form)
- UI/Account creation: The help texts have been improved
- Maps: Google Maps links have been removed, Openstreetmap links have been added
- several static information webpages (e.g FAQ) have been migrated from static html sites to django-flatpages
- Do not throw away user entered data during registration (It is fairly frustrating for new users to have te re-enter e-mail
addresses and passwords etc.)

### Fixed
- default PostgreSQL settings have been fixed
- several PEP8 fixes of the source code (whitespaces, empty lines, lowercase variables)
- fix of registration form
- small fix of README.md
- ordering of facilities at landing page fixed
- add psycopg2 to requirements.txt

### Removed
- Google maps (see Changed)
- several static webpages (see Changed)

## [3.0.0] - 2015-11-08
### Added / Changed / Fixed / Removed
- see git log

## [2.2.0] - 2015-10-22
### Added / Changed / Fixed / Removed
- see git log

## [2.1.0] - 2015-10-09
### Added / Changed / Fixed / Removed
- see git log

## [2.0.0] - 2015-10-04
### Added / Changed / Fixed / Removed
- see git log

## [1.4.0] - 2015-09-16
### Added / Changed / Fixed / Removed
- Bug fix: creating new volunteer resulted in too long action and HTTP 502 error
- Some UI cleanup (navigation bar and admin area).
- Localization
- Data model clean up
- Facebook integration (preview image) improved
- fix email privacy in email notification
- fix UI problems

## [1.3.0] - 2015-09-14
### Added / Changed / Fixed / Removed
- Add pretty admin theme
- Prevent volunteers from subscribing to shifts if their time is conflicting with already
  subscribed-to shifts.
- Add py.test, factory-boy and basic factories.
- Add Travis CI integration for pull requests.
- Add django-extensions for dev, for ./manage.py shell_plus and graphing models.
- Simplify views, remove statistics app, move registration app.
- Subscribe button is hidden when already subscribed to shift.
- Add a basic i18n workflow and mark some strings.
- Email notifications for deleted shifts.

## [1.2.0] - 2015-09-13
### Added / Changed / Fixed / Removed
- see git log

## [1.1.0] - 2015-09-12
### Added / Changed / Fixed / Removed
- see git log

## [1.0.0] - 2015-09-08
### Added / Changed / Fixed / Removed
- see git log