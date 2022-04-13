# Change Log
All notable changes to this project will be documented in this file.

## [Unreleased]
### Added

### Changed

### Fixed

### Removed

## [4.1.0] - 2022-04-13
Bugfix and improvements release with little (visibly) new things

### Added
- Integrate django-post-office
- Add sentry integration
- Create codeql-analysis.yml
- Add commonly requested static files
  
### Changed
- Bump django-ckeditor from 6.2.0 to 6.3.0 in /requirements
- Bump django from 4.0.3 to 4.0.4 in /requirements
- Bump django-ckeditor from 6.3.0 to 6.3.2 in /requirements
- Bump sentry-sdk from 1.5.8 to 1.5.9 in /requirements by

### Fixed
- Hotfix/562 fix admin ordering by task and workplace
- Make admin timezone aware for shift/-templates
- Fix #575, broken icon in schedule template admin
- Fixes #570: regions nav bar items not sorted well
- Fixes #547: jQuery selector expected
- Correct shift details user view
- Fix URL redirection from remote source
- Fix URL date parsing
- Shift notification messages from managers *only*

## [4.0.0] - 2022-04-03
Revival. Volunteer Planner is back.

### Added
- privacy policy acception during registration in #437
- czech translation #406
- priority attribute for task and workplace, can be used to control listing order #476
- black and flake8 #518 #519
- GitHub templates for issues and feature requests
- Allow login in with email address as username #522

### Changed
- lift Django version (+ libraries and frameworks) #488
- Python3 #487
- PostgreSQL is now default DBMS
- automatically assign permissions, when promoted as manager #425
- on landing page list only facilities with open shifts #454
- update translations
- reduce number of SQL queries for facility, shift date and news listing #513
- restrict username variations #520

### Fixed
- check task and workplace match facility when creating shifts #433
- better filter for organization and facility membership / manager permission
- remove user from shift on account deletion #516
- Sending e-mail on membership approval was broken #533
- Make membership unique per user and facility / organization #524

### Removed
- short description removed from organization and facility #442
- shiftmailer removed #452
- user e-mail address removed from user account admin (so managers see less data uncontrolled) #490
- user e-mail address removed from admin shift list #505
- google_tools app removed #510

## [3.1.1] - 2017-02-06
### Added
- added french translation
- added portuguese translation (not fully translated yet)
- added turkish translation (not fully translated yet)

### Changed
- updated all existing translations (massive improvements in translation)

### Fixed
- fix #398: deleting a non-past shift failed hard when trying to gather information about email about to be sent

## [3.1.0] - 2016-10-10
### Added
- [UI] Display a warning when joining overlapping shifts #395
- [UI] shift managers can see the e-mail address of approved and pending facility members to contact them
- enhancements to the excel document that is sent to shift managers
- Some javascript files from different CDN are now included in Volunteer Planner distribution.
- [development] .editorconfig (PEP8 style)
- [development] new docstrings to source code
- [development] support for Docker containers for the test/development environment
- [development] makefile for base and mysql installations
- [development] travis badge added for readme.md

### Changed
- [UI] better alignment of page
- [UI] Additional information - if shifts span over midnight there is need of additional information to differentiate between shifts that start today and shifts that started yesterday. In these cases the date is shown in the field where the time is shown.
- fixed issue 360: From field of emails is now DEFAULT_FROM_EMAIL and not anymore the fake from email of the shift manager.
- All used CSS and Javascript files are delivered by Volunteer Planner (instead of using some CDNs)
- text of HTTP 500 error was shortened.
- [development] CHANGELOG is now Markdown
- [development] Refactoring of the shiftmailer and Excelgenerator
- [development] Refactor: only one repository for static files (both repositories have been merged)
- [development] better README

### Fixed
- UI: corrected wrong email for onboarding
- fixed issue 373: Shifts in shift history/future shifts are now shown correctly
- [development] some PEP8 fixes of the source code
- [development] removed hardcoded email from the source code, use settings file instead
- [development] removed one hardcoded link on image
- [development] .travis.yml fixups

### Removed
- static repository in non-logged-in-area was removed
- [development] application api removed (not used and no plans for usage)
- [development] application registration_history removed (since 03.10.15 not in use and no function anymore)
- [development] application stats removed (since 01.10.15 not in use and no function anymore)

## [3.0.1] - 2016-01-09
### Added
- [UI] User can her history of work shifts
- [UI] User can see upcoming shifts (the shifts she signed up for)
- Delete user: User can delete her account - the data is anonymized
- Social Impact Lab was added as supporter

### Changed
- updated translations and wording
- [UI] Account creation: There is now an explicit message on account creation form explaining what happens here. (users often mistake the creation form for the login form)
- [UI] Account creation: The help texts have been improved
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
