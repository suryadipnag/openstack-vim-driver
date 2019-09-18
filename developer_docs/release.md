# Release

The following steps detail how the Openstack VIM driver release is produced. This may only be performed by a user with admin rights to this Github, Docker and Pypi repository.

## 1. Setting the Version

1.1. Start by setting the version of the release and ignition-framework version (if update needed) in `osvimdriver/pkg_info.json`:

```
{
  "version": "<release version number>",
  "ignition-version": "==0.1.0"
}
```

1.2. Ensure the `docker.version` in `helm/os-vim-driver/values.yaml` includes the correct version number.

1.3. Ensure the `version` and `appVersion` in `helm/os-vim-driver/Chart.yaml` includes the correct version number

1.4 Push all version number changes to Github

1.5 Tag the commit with the new version in Git

## 2. Build Python Wheel

Build the python wheel by navigating to the root directory of this project and executing:

```
python3 setup.py bdist_wheel
```

The whl file is created in `dist/`

## 3. Package the docs

Create a TAR of the docs directory:

```
tar -cvzf os-vim-driver-<release version number>-docs.tgz docs/ --transform s/docs/os-vim-driver-<release version number>-docs/
```

## 4. Build Docker Image

4.1. Move the whl now in `dist` to the `docker/whl` directory (ensure no additional whls are in the docker directory)

```
cp dist/os_vim_driver-<release version number>-py3-none-any.whl docker/whls/
```

4.2. Navigate to the `docker` directory

```
cd docker
```

4.3. Build the docker image (**tag with release version number and accanto repository**)

```
docker build -t accanto/os-vim-driver:<release version number> .
```

## 5. Build Helm Chart

Package the helm chart (**don't forget to ensure the Chart.yaml and values.yaml have correct version numbers**)

```
helm package helm/os-vim-driver
```

## 6. Create release on Github

6.1 Navigate to Releases on the Github repository for this project and create a new release.

6.2 Ensure the version tag and title correspond with the version number set in the pkg_info file earlier.

6.3 Attach the docs archive to the release

6.4 Attach the helm chart archive to the release

6.5 Push the docker image to Dockerhub with:

```
docker push accanto/os-vim-driver:<release version number>
```

## 7. Generate Release Notes

Release notes are produced by updating the CHANGELOG.md, then copying the section for this version to the description field in the created Github release.

The CHANGELOG is updated using [github-changelog-generator](https://github.com/github-changelog-generator/github-changelog-generator#why-should-i-care)

7.1 Update CHANGELOG.md

```
github_changelog_generator accanto-systems/ignition
```

7.2 Commit the updated CHANGELOG.md

7.3 Copy the section for the newly released version from CHANGELOG.md into the description of the release created on Github

## 8. Set next development version

Usually the next dev version should be an minor increment of the previous, with `dev0` added. For example, after releasing 0.1.0 it would be `0.2.0.dev0`.

8.1 Set the version of the next development version in `osvimdriver/pkg_info.json`:

```
{
  "version": "<next development version number>",
  "ignition-version": "<next ignition version number if different>"
}
```

8.2. Update the `docker.version` in `helm/os-vim-driver/values.yaml` to the next development version number.

8.3. Update the `version` and `appVersion` in `helm/os-vim-driver/Chart.yaml` to the next development version number.

8.4 Push version number changes to Github
