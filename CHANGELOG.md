# CHANGELOG


## v0.6.10 (2025-04-27)

### Bug Fixes

- Fix all the broken changes from the last pr
  ([#36](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/36),
  [`fa5d1fa`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/fa5d1fa1a949fc63b05b2fade35dd78756d6f928))

### Description

This PR improve documentation, Adds `unittest`, that, don't use mock data, to ensure it works. Make
  the code work again.

Fixes #35

- Fix documentation ([#38](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/38),
  [`9d34eb7`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/9d34eb71de0f02c2448b7fecff7631d45e771b8a))

### Description

Remove `UV` from documentation deployment.

Fixes #37

### Refactoring

- Re-arrange the project to make improvements
  ([#34](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/34),
  [`087ecff`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/087ecff5d2b07e840b9cb113878208846f188400))

### Description

This PR adds a few things:

- [x] Documentation page - [x] Pre-commit CI - [ ] Pytest CI - [x] Integration test CI

Fixes #29

This is a breaking changes.


## v0.6.9 (2025-03-28)

### Bug Fixes

- File generation for mqpy command
  ([`e2e395a`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/e2e395a4349dcab87858f3dd804f8e2562721e2d))

- File generation for mqpy command
  ([`e106a62`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/e106a62b67362d106f12bdaf42836e4aea9b099a))

- File generation for mqpy command
  ([`e6b6a21`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/e6b6a219c7a92b77e76415353fcec0a7cbe6c14a))

### Build System

- **deps**: Bump actions/checkout from 2 to 4
  ([#9](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/9),
  [`83e4fa6`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/83e4fa648cba3edd65d67730e7028b8f9cd7b535))

Bumps [actions/checkout](https://github.com/actions/checkout) from 2 to 4. - [Release
  notes](https://github.com/actions/checkout/releases) -
  [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/actions/checkout/compare/v2...v4)

--- updated-dependencies: - dependency-name: actions/checkout dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump actions/setup-python from 2 to 5
  ([#8](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/8),
  [`e386757`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/e386757679984be8170e4ba1cd95cc63abc029af))

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 2 to 5. - [Release
  notes](https://github.com/actions/setup-python/releases) -
  [Commits](https://github.com/actions/setup-python/compare/v2...v5)

--- updated-dependencies: - dependency-name: actions/setup-python dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump metatrader5 from 5.0.45 to 5.0.4682
  ([#10](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/10),
  [`d011a4a`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/d011a4a78db7d1a2231ec2cc37771c9f60ca51f6))

Bumps [metatrader5](https://www.metatrader5.com) from 5.0.45 to 5.0.4682.

--- updated-dependencies: - dependency-name: metatrader5 dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump metatrader5 in the python-requirements group
  ([#14](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/14),
  [`672ace8`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/672ace84a9cb7a038596b0b5036cddafe67cde15))

Bumps the python-requirements group with 1 update: [metatrader5](https://www.metatrader5.com).

Updates `metatrader5` from 5.0.45 to 5.0.4682

--- updated-dependencies: - dependency-name: metatrader5 dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-requirements ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump metatrader5 in the python-requirements group
  ([#15](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/15),
  [`5fe3dc1`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/5fe3dc1256cd10cb2d2d19b6533c740dae043dde))

Bumps the python-requirements group with 1 update: [metatrader5](https://www.metatrader5.com).

Updates `metatrader5` from 5.0.4682 to 5.0.4687

--- updated-dependencies: - dependency-name: metatrader5 dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-requirements ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump metatrader5 in the python-requirements group
  ([#16](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/16),
  [`4da9c50`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/4da9c50593bd22fea886a8e4e44caad0e82e4873))

Bumps the python-requirements group with 1 update: [metatrader5](https://www.metatrader5.com).

Updates `metatrader5` from 5.0.4682 to 5.0.4687

--- updated-dependencies: - dependency-name: metatrader5 dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-requirements ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump metatrader5 in the python-requirements group
  ([#17](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/17),
  [`3ac0f09`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/3ac0f091b0c55be25004500c4e07c40d2859ebb2))

Bumps the python-requirements group with 1 update: [metatrader5](https://www.metatrader5.com).

Updates `metatrader5` from 5.0.4687 to 5.0.4732

--- updated-dependencies: - dependency-name: metatrader5 dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-requirements ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump metatrader5 in the python-requirements group
  ([#18](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/18),
  [`73c668e`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/73c668eaf35b5c39a242893c9c47a39a210c2a58))

Bumps the python-requirements group with 1 update: [metatrader5](https://www.metatrader5.com).

Updates `metatrader5` from 5.0.4687 to 5.0.4732

--- updated-dependencies: - dependency-name: metatrader5 dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-requirements ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump metatrader5 in the python-requirements group
  ([#19](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/19),
  [`f0b2918`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/f0b29187a6dcd181e4c517c207e7506d7a2c7260))

Bumps the python-requirements group with 1 update: [metatrader5](https://www.metatrader5.com).

Updates `metatrader5` from 5.0.4732 to 5.0.4738

--- updated-dependencies: - dependency-name: metatrader5 dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-requirements ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump metatrader5 in the python-requirements group
  ([#20](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/20),
  [`381a459`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/381a4593d3c499376d3376501cd3a224174ffe2c))

Bumps the python-requirements group with 1 update: [metatrader5](https://www.metatrader5.com).

Updates `metatrader5` from 5.0.4732 to 5.0.4738

--- updated-dependencies: - dependency-name: metatrader5 dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-requirements ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump metatrader5 in the python-requirements group
  ([#23](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/23),
  [`7bcc150`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/7bcc150754ce3cf63fd5f55a98df0664b8548416))

Bumps the python-requirements group with 1 update: [metatrader5](https://www.metatrader5.com).

Updates `metatrader5` from 5.0.4738 to 5.0.4803

--- updated-dependencies: - dependency-name: metatrader5 dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-requirements ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump metatrader5 in the python-requirements group
  ([#24](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/24),
  [`a06a0b8`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/a06a0b8d76de3f2d9057e6c0d3edce717807416d))

Bumps the python-requirements group with 1 update: [metatrader5](https://www.metatrader5.com).

Updates `metatrader5` from 5.0.4738 to 5.0.4803

--- updated-dependencies: - dependency-name: metatrader5 dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-requirements ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump metatrader5 in the python-requirements group
  ([#25](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/25),
  [`a4ebcd8`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/a4ebcd88f161269a316ecaf326444ee9a169b9b9))

Bumps the python-requirements group with 1 update: [metatrader5](https://www.metatrader5.com).

Updates `metatrader5` from 5.0.4803 to 5.0.4874

--- updated-dependencies: - dependency-name: metatrader5 dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-requirements ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump setuptools from 69.0.2 to 75.6.0
  ([#12](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/12),
  [`07c6c63`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/07c6c6311b35b41bf3d4869222bd3e8112d2fa81))

Bumps [setuptools](https://github.com/pypa/setuptools) from 69.0.2 to 75.6.0. - [Release
  notes](https://github.com/pypa/setuptools/releases) -
  [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst) -
  [Commits](https://github.com/pypa/setuptools/compare/v69.0.2...v75.6.0)

--- updated-dependencies: - dependency-name: setuptools dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump setuptools in the python-requirements group
  ([#21](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/21),
  [`12b55ee`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/12b55ee69f0c49bc00e972c4faf81611d19b94a2))

Bumps the python-requirements group with 1 update: [setuptools](https://github.com/pypa/setuptools).

Updates `setuptools` from 75.6.0 to 75.7.0 - [Release
  notes](https://github.com/pypa/setuptools/releases) -
  [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst) -
  [Commits](https://github.com/pypa/setuptools/compare/v75.6.0...v75.7.0)

--- updated-dependencies: - dependency-name: setuptools dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-requirements ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump setuptools in the python-requirements group
  ([#22](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/22),
  [`655da8f`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/655da8f12473292c265b68cf9b53c050f68dd938))

Bumps the python-requirements group with 1 update: [setuptools](https://github.com/pypa/setuptools).

Updates `setuptools` from 75.7.0 to 75.8.0 - [Release
  notes](https://github.com/pypa/setuptools/releases) -
  [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst) -
  [Commits](https://github.com/pypa/setuptools/compare/v75.7.0...v75.8.0)

--- updated-dependencies: - dependency-name: setuptools dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-requirements ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump the python-requirements group with 2 updates
  ([#28](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/28),
  [`63de899`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/63de899ac9e8b103cecb34c10169aedbd5a8738b))

Bumps the python-requirements group with 2 updates: [metatrader5](https://www.metatrader5.com) and
  [setuptools](https://github.com/pypa/setuptools).

Updates `metatrader5` from 5.0.4803 to 5.0.4874

Updates `setuptools` from 75.8.0 to 78.1.0 - [Release
  notes](https://github.com/pypa/setuptools/releases) -
  [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst) -
  [Commits](https://github.com/pypa/setuptools/compare/v75.8.0...v78.1.0)

--- updated-dependencies: - dependency-name: metatrader5 dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-requirements

- dependency-name: setuptools dependency-type: direct:production

update-type: version-update:semver-major

dependency-group: python-requirements ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump black from 23.11.0 to 24.8.0
  ([#13](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/13),
  [`0c2de63`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/0c2de6351c92eb5ce282d2731eb6467d003ff2ac))

Bumps [black](https://github.com/psf/black) from 23.11.0 to 24.8.0. - [Release
  notes](https://github.com/psf/black/releases) -
  [Changelog](https://github.com/psf/black/blob/main/CHANGES.md) -
  [Commits](https://github.com/psf/black/compare/23.11.0...24.8.0)

--- updated-dependencies: - dependency-name: black dependency-type: direct:development

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump isort from 5.12.0 to 5.13.2
  ([#11](https://github.com/Joaopeuko/Mql5-Python-Integration/pull/11),
  [`085b198`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/085b198b8d4ffbfb482992b280f69c7917dca6d2))

Bumps [isort](https://github.com/pycqa/isort) from 5.12.0 to 5.13.2. - [Release
  notes](https://github.com/pycqa/isort/releases) -
  [Changelog](https://github.com/PyCQA/isort/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/pycqa/isort/compare/5.12.0...5.13.2)

--- updated-dependencies: - dependency-name: isort dependency-type: direct:development

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Documentation

- Add github template
  ([`db14270`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/db1427033b8ab7f397a1a5fb1f39584a66b9922a))

- Improve README information
  ([`b1f70dd`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/b1f70ddc408a29236df661009c8c55db2d236c02))

- Improve README information
  ([`e0fd27d`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/e0fd27db11bbb07800fa29e2e149ca61607cbe1b))

### Features

- Add command for autogenerating boilerplate code
  ([`1e0033e`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/1e0033e9cb32684e1188973c7be983f6ed88d579))

### Refactoring

- Rearrange file structure for better organization
  ([`a6c79a7`](https://github.com/Joaopeuko/Mql5-Python-Integration/commit/a6c79a7c13255ef0c8d4ec4ed0846cc43b5258eb))
