# Change Log

## [1.0.0](https://github.com/accanto-systems/openstack-vim-driver/tree/1.0.0) (2020-02-20)
[Full Changelog](https://github.com/accanto-systems/openstack-vim-driver/compare/0.7.1...1.0.0)

**Implemented enhancements:**

- Allow key properties to be used as inputs to Heat templates [\#39](https://github.com/accanto-systems/openstack-vim-driver/issues/39)

**Documentation:**
- Deployment Location properties format [\#35](https://github.com/accanto-systems/openstack-vim-driver/issues/35)
- Ensure documentation correct for 1.0.0 [\#38](https://github.com/accanto-systems/openstack-vim-driver/issues/38)

**Depdendencies:**
- Upgraded to Ignition version 1.0.0

## [0.7.1](https://github.com/accanto-systems/openstack-vim-driver/tree/0.7.1) (2020-02-17)
[Full Changelog](https://github.com/accanto-systems/openstack-vim-driver/compare/0.7.0...0.7.1)

**Fixed bugs:**

- Delete Infrastructure on a Stack that does not exists fails with internal server error [\#36](https://github.com/accanto-systems/openstack-vim-driver/issues/36)

## [0.7.0](https://github.com/accanto-systems/openstack-vim-driver/tree/0.7.0) (2020-01-30)
[Full Changelog](https://github.com/accanto-systems/openstack-vim-driver/compare/0.6.0...0.7.0)

**Implemented enhancements:**

- Add liveness and readiness probe to helm chart [\#33](https://github.com/accanto-systems/openstack-vim-driver/issues/33)
- Add SSL support [\#31](https://github.com/accanto-systems/openstack-vim-driver/issues/31)
- Autoscaling on CPU usage [\#29](https://github.com/accanto-systems/openstack-vim-driver/issues/29)

**Dependencies:**

- Upgraded to Ignition 0.8.0

## [0.6.0](https://github.com/accanto-systems/openstack-vim-driver/tree/0.6.0) (2020-01-13)
[Full Changelog](https://github.com/accanto-systems/openstack-vim-driver/compare/0.5.0...0.6.0)

**Implemented enhancements:**

- Update InfrastructureDriver to accept and make use of systemProperties [\#27](https://github.com/accanto-systems/openstack-vim-driver/issues/27)

**Maintenaince Tasks:**

- As part of [\#27](https://github.com/accanto-systems/openstack-vim-driver/issues/27), the Ignition version used by this driver has been updated to v0.7.0

## [0.5.0](https://github.com/accanto-systems/openstack-vim-driver/tree/0.5.0) (2019-12-13)
[Full Changelog](https://github.com/accanto-systems/openstack-vim-driver/compare/0.4.2...0.5.0)

**Maintenaince Tasks:**

- Upgrade ignition framework version to 0.6.2 [\#25](https://github.com/accanto-systems/openstack-vim-driver/issues/25)

## [0.4.2](https://github.com/accanto-systems/openstack-vim-driver/tree/0.4.2) (2019-12-09)
[Full Changelog](https://github.com/accanto-systems/openstack-vim-driver/compare/0.4.1...0.4.2)

**Fixed bugs:**

- Assume stack_id of "0" is the same as no stack_id

## [0.4.1](https://github.com/accanto-systems/openstack-vim-driver/tree/0.4.1) (2019-12-05)
[Full Changelog](https://github.com/accanto-systems/openstack-vim-driver/compare/0.4.0...0.4.1)

**Fixed bugs:**

- Check if stack_id is not None [\#24](https://github.com/accanto-systems/openstack-vim-driver/issues/24)

## [0.4.0](https://github.com/accanto-systems/openstack-vim-driver/tree/0.4.0) (2019-12-05)
[Full Changelog](https://github.com/accanto-systems/openstack-vim-driver/compare/0.3.0...0.4.0)

**Fixed bugs:**

- OSError('libc not found') when running with Guincorn [\#21](https://github.com/accanto-systems/openstack-vim-driver/issues/21)

**Implemented enhancements:**

- Recognise existing stacks on request [\#23](https://github.com/accanto-systems/openstack-vim-driver/issues/23)

**Maintenaince Tasks:**

- Tighten restrictions on dependency versions [\#18](https://github.com/accanto-systems/openstack-vim-driver/issues/18)
- Support building Docker image with development version of Ignition [\#19](https://github.com/accanto-systems/openstack-vim-driver/issues/19)

**Documentation:**

- Improve documentation layout and include descriptions of property handling [\#15](https://github.com/accanto-systems/openstack-vim-driver/issues/15)

## [0.3.0](https://github.com/accanto-systems/openstack-vim-driver/tree/0.3.0) (2019-10-09)
[Full Changelog](https://github.com/accanto-systems/openstack-vim-driver/compare/0.2.0...0.3.0)

**Dependencies:**

- Upgraded to Ignition 0.4.0

**Fixed bugs:**

- Configure helm chart to explicitly run the container as "old" user [\#9](https://github.com/accanto-systems/openstack-vim-driver/issues/9)

**Implemented enhancements:**

- Add affinity and toleration rules to helm chart [\#13](https://github.com/accanto-systems/openstack-vim-driver/issues/13)
- Configure K8s Label to enable Filebeat logging [\#11](https://github.com/accanto-systems/openstack-vim-driver/issues/11)
- Support Heat templates [\#7](https://github.com/accanto-systems/openstack-vim-driver/issues/7)
- Include resource requests and limits configuration in Helm chart [\#5](https://github.com/accanto-systems/openstack-vim-driver/issues/5)

## [0.2.0](https://github.com/accanto-systems/openstack-vim-driver/tree/0.2.0) (2019-09-18)
[Full Changelog](https://github.com/accanto-systems/openstack-vim-driver/compare/0.1.0...0.2.0)

**Fixed bugs:**

- Query infrastructure task does not return 4xx status code when not found [\#1](https://github.com/accanto-systems/openstack-vim-driver/issues/1)

**Closed issues:**

- Upgrade Ignition framework version to 0.2.0 [\#3](https://github.com/accanto-systems/openstack-vim-driver/issues/3)

**Merged pull requests:**

- Resolves \#3 by upgrading the Ignition version to 0.2.0 [\#4](https://github.com/accanto-systems/openstack-vim-driver/pull/4) ([dvaccarosenna](https://github.com/dvaccarosenna))
- issue1 - get infrastructure API to return a 400 when the stack cannot… [\#2](https://github.com/accanto-systems/openstack-vim-driver/pull/2) ([dvaccarosenna](https://github.com/dvaccarosenna))

## [0.1.0](https://github.com/accanto-systems/openstack-vim-driver/tree/0.1.0) (2019-09-02)


\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*