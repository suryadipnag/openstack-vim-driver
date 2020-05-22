# Deployment Locations

A deployment location must be provided to an infrastructure request to indicate the Openstack environment to be used. The deployment location will be managed by the Stratoss&trade; Lifecycle Manager and Brent but must have particular properties to be successfully used by this driver.

# Properties

The following properties are supported by the driver:

| Name            | Default | Required                           | Detail                                                                                                                     |
| --------------- | ------- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| os_api_url      | -       | Y                                  | Defines the address of the Openstack environment. This address will be used for all API requests, including authentication |
| os_auth_enabled | True    | N                                  | Informs the driver that the Openstack environment requires authentication with keystone                                    |
| os_auth_api     | -       | Y - when `os_auth_enabled` is True | Defines the authentication API endpoint used to make authentication requests by this driver                                |
| os_cacert | - | N | The contents of the CA certificate to use when connecting with Openstack |
| os_cert | - | N | The contents of the client certificate bundle file to use when connecting with Openstack |
| os_keys | - | N | The contents of the client key file to use connecting with Openstack |

This driver currently supports password authentication only. The following properties may be set on a deployment location to configure the user for all requests:

| Name                        | Type    | Detail                          |
| --------------------------- | ------- | ------------------------------- |
| os_auth_domain_id           | String  | ID for domain scoping           |
| os_auth_domain_name         | String  | Name for domain scoping         |
| os_auth_project_id          | String  | ID for project scoping          |
| os_auth_project_name        | String  | Name for project scoping        |
| os_auth_project_domain_id   | String  | Domain ID for named project     |
| os_auth_project_domain_name | String  | Domain name for named project   |
| os_auth_trust_id            | String  | ID for trust scoping            |
| os_auth_user_id             | String  | ID of user for authentication   |
| os_auth_username            | String  | Name of user for authentication |
| os_auth_user_domain_id      | String  | Domain ID for named user        |
| os_auth_user_domain_name    | String  | Domain name for named user      |
| os_auth_password            | String  | Password for user               |
| os_auth_unscoped            | Boolean | Use unscoped tokens             |

You will not need to provide values for all of the above properties, it depends on the type of scoping you require. You must use one of the following combinations:

- domain_id
- domain_name
- project_id
- project_name + project_domain_id
- project_name + project_domain_name
- trust_id
- unscoped

In addition, you must set the user and password with one of the following combinations:

- user_id + user_domain_id + password
- user_id + user_domain_name + password
- username + password

The following example shows a full set of valid properties for an Openstack deployment location:

JSON:
```json
{
  "os_auth_project_name": "my-project",
  "os_auth_project_domain_name": "default",
  "os_auth_password": "secret",
  "os_auth_username": "jack",
  "os_auth_user_domain_name": "default",
  "os_auth_api": "v3",
  "os_api_url": "http://10.10.8.8:5000"
}
```

YAML:
```yaml
os_auth_project_name: my-project
os_auth_project_domain_name: default
os_auth_password: secret
os_auth_username: jack
os_auth_user_domain_name: default
os_auth_api: v3 #on some systems this may need to be identity/v3
os_api_url: http://10.10.8.8:5000
```

Full example of deployment location properties:

JSON (note the certificate and key values shown here are single line strings (with newline separators `\n`) but may appear as multiple lines in your current browser):
```json
{
  "os_auth_project_name": "my-project",
  "os_auth_project_domain_name": "default",
  "os_auth_password": "secret",
  "os_auth_username": "jack",
  "os_auth_user_domain_name": "default",
  "os_auth_api": "v3",
  "os_api_url": "http://10.10.8.8:5000",
  "os_cacert": "-----BEGIN CERTIFICATE-----\nMIIC+zCCAeOgAwIBAgIUMN6V0m2QaJlp1mQ6qI5vH8NGHr4wDQYJKoZIhvcNAQEL\nBQAwDTELMAkGA1UEAwwCVUkwHhcNMjAwNDE2MTIzMDA0WhcNMzAwNDE0MTIzMDA0\nWjANMQswCQYDVQQDDAJVSTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB\nALuopzezuMRck3vw05RSJCEtbxnQJoWR8/ipOBp8jg2um2G8K2S92hZF4KSw29Cz\nX4f7CM0/Cg4ys6iElS3wIxvBDBx++Wa1peiWgr1yo88IVCunLL3ZtYooTYkKocqK\nU4BmmfJHKGgumq6I8JBoLHWItfFfaXthXcUu/P/U5VzcFrfkwRVgx2OYTUSiD/66\nMWKn4fHtW++9BHJSK8W0Cfc/zILOQr7uzsdwafyZaj/wN2sajXWb+LeuEE3oM2c+\n8zkRSLcV3dpWa36JvdyahwSgzwFd4f7MJsEAuhBcIonaWC7Gw5W/gH+ceT7dc/KT\niVNPXdI/k0/MJJZoRXDGzlMCAwEAAaNTMFEwHQYDVR0OBBYEFOB0ny+QIau5HzIy\nhCtHWMo8venpMB8GA1UdIwQYMBaAFOB0ny+QIau5HzIyhCtHWMo8venpMA8GA1Ud\nEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAKFugRFzxptoZcG58gLC5WCq\ntnurFblxJP8T9DtP5zvIPR7Gc933lBfOHP+8F+WKTp11Xi9ndnIYEoXzII+UBXTz\nocDCul2aAsubz7kS/yXzMY1F+7q36y4eeM+CDnawhhOc85Xg0tbvzNMlCyJX0TJk\nMImt7TfvebCx48mVkuV65BXEuGUD3bVmBEeakGIJSOIwuGwnFnhe+gh/LNq8BsxW\n+UNp5gs0oiS7o7H+QuArQRajdK2ANKMyCrGmE8lBexOyPqD/YBE1W68HdmYJKG9S\njV+RlU5SkGhUe439pgFHRmOw4f4CaeikC6OhO55ro0IJR6SUomcnG+GAZ/Hdj8g=\n-----END CERTIFICATE-----\n",
  "os_cert": "-----BEGIN CERTIFICATE-----\nAAAA+zCCAeOgAwIBAgIUMN6V0m2QaJlp1mQ6qI5vH8NGHr4wDQYJKoZIhvcNAQEL\nBQAwDTELMAkGA1UEAwwCVUkwHhcNMjAwNDE2MTIzMDA0WhcNMzAwNDE0MTIzMDA0\nWjANMQswCQYDVQQDDAJVSTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB\nALuopzezuMRck3vw05RSJCEtbxnQJoWR8/ipOBp8jg2um2G8K2S92hZF4KSw29Cz\nX4f7CM0/Cg4ys6iElS3wIxvBDBx++Wa1peiWgr1yo88IVCunLL3ZtYooTYkKocqK\nU4BmmfJHKGgumq6I8JBoLHWItfFfaXthXcUu/P/U5VzcFrfkwRVgx2OYTUSiD/66\nMWKn4fHtW++9BHJSK8W0Cfc/zILOQr7uzsdwafyZaj/wN2sajXWb+LeuEE3oM2c+\n8zkRSLcV3dpWa36JvdyahwSgzwFd4f7MJsEAuhBcIonaWC7Gw5W/gH+ceT7dc/KT\niVNPXdI/k0/MJJZoRXDGzlMCAwEAAaNTMFEwHQYDVR0OBBYEFOB0ny+QIau5HzIy\nhCtHWMo8venpMB8GA1UdIwQYMBaAFOB0ny+QIau5HzIyhCtHWMo8venpMA8GA1Ud\nEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAKFugRFzxptoZcG58gLC5WCq\ntnurFblxJP8T9DtP5zvIPR7Gc933lBfOHP+8F+WKTp11Xi9ndnIYEoXzII+UBXTz\nocDCul2aAsubz7kS/yXzMY1F+7q36y4eeM+CDnawhhOc85Xg0tbvzNMlCyJX0TJk\nMImt7TfvebCx48mVkuV65BXEuGUD3bVmBEeakGIJSOIwuGwnFnhe+gh/LNq8BsxW\n+UNp5gs0oiS7o7H+QuArQRajdK2ANKMyCrGmE8lBexOyPqD/YBE1W68HdmYJKG9S\njV+RlU5SkGhUe439pgFHRmOw4f4CaeikC6OhO55ro0IJR6SUomcnG+GAZ/Hdj8g=\n-----END CERTIFICATE-----\n",
  "os_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7qKc3s7jEXJN7\n8NOUUiQhLW8Z0CaFkfP4qTgafI4NrpthvCtkvdoWReCksNvQs1+H+wjNPwoOMrOo\nhJUt8CMbwQwcfvlmtaXoloK9cqPPCFQrpyy92bWKKE2JCqHKilOAZpnyRyhoLpqu\niPCQaCx1iLXxX2l7YV3FLvz/1OVc3Ba35MEVYMdjmE1Eog/+ujFip+Hx7VvvvQRy\nUivFtAn3P8yCzkK+7s7HcGn8mWo/8DdrGo11m/i3rhBN6DNnPvM5EUi3Fd3aVmt+\nib3cmocEoM8BXeH+zCbBALoQXCKJ2lguxsOVv4B/nHk+3XPyk4lTT13SP5NPzCSW\naEVwxs5TAgMBAAECggEBAJKbMAhUYAUITjCF9MXrZk6FMEb6Vx4C6JdbnHkU1eXa\ng4nXeA88QyUjcl03zoM9n2ScukOe/DwbYEBHVESPVt5X8x5QFIgpYXRUIc/fwBn+\nZ8Oy10F61FkbI3fs1nlll9a4UYz2CptZzX6NfWNT/2fTZlEsOTwq1Rc3nnA/4vCn\nqaU/Iwe/F+pjwl2rgPcDRPrbNHkrF1iJIyii3O+6Ke7j9tvwjcxdMgKYGfk7f3J6\naTA2SSPFZyr2SCQm3hREDtSdlNaZ3TvVq9kbT4htjn08ky0vWkRqGxfQg05E0/wQ\n4SVX3CZE+B1jOdBG3IFoqSrVh/AAcNFStGE2Dz+bwAECgYEA7F9YYjY5OBkyvnPM\nMiTbkKWtF8ABKHd+Kk+FMGDa6nsVRB4G1eXYpb0chBsb9DsHh1ijlIOBrz6SndnH\nVZ1pvt5LHcgtUaLphpFJl08krr7OLVQpfwT+Q85MMVey76SlBnrxeXuKfWH+Jw1t\nMIzSfi7kHxCTxD36d615u7JGuTcCgYEAyz3IzyhDj7kjagI0wODjcqrmEruvUYgV\nRgwM9ELQCOE3dstNS+dFh0gJg9/IYKtW8w8bfFXetlnrgvYiIpzctYLfPY1lFqsC\nxpzlEUD+sLLjMIH98wl2XnVd/5uAEUp2xelO4cquddLr9w48Mwk/jPb8RXLow8fh\npZw9VfSvccUCgYEAqLfJw5iGsSczVEQdfbFXU+EeMzSm3vakBJlsLUMFH5epb0yr\nfmQohuz8fMNI6cR0tEQtxuUzXR4h0zBOmyrX/xh2r5Rh3MKXQ6lSyQEB4wVo72wC\njprGzylis1mw7GMuM/jvgdIP4T1gBwoLZTsvSEg6Jn5TqyC+NkyJ9tLirnMCgYA8\n23tNzJiuaJmaHJ7/QlfY9iN+aITOvRjhqKoYWglBH28kOywiFlZTc9aljlTJ3YRj\ns5pfWLcfkz1aMal3A9Fy6IVAQR6L8xkZr9FHoVaiQm6VD9ei9qpjDnHfIAjxJIL8\nMChWpAIpdccCa1jLT3GgHDTd9tKMDUYb+PTE0EfYoQKBgG990/rnjsLam/TzkvAU\nJqzvIO/13bR63laC9CNhdu0L2khgQ2hHgB5ksZ7NucstehSrTLD0sus9ocZLMvCT\nOq18rA4QA34ur3YgFJC8Bl63+yfYnE4z2WP250Q0z0sWNw3i2PkTh5/gozkv1Xld\nIvrRjS2RTSoHYw5Ug0WfHR9A\n-----END PRIVATE KEY-----\n"
}
```

YAML:
```yaml
os_auth_project_name: my-project
os_auth_project_domain_name: default
os_auth_password: secret
os_auth_username: jack
os_auth_user_domain_name: default
os_auth_api: v3 #on some systems this may need to be identity/v3
os_api_url: http://10.10.8.8:5000
os_cacert: |
  -----BEGIN CERTIFICATE-----
  MIIC+zCCAeOgAwIBAgIUMN6V0m2QaJlp1mQ6qI5vH8NGHr4wDQYJKoZIhvcNAQEL
  BQAwDTELMAkGA1UEAwwCVUkwHhcNMjAwNDE2MTIzMDA0WhcNMzAwNDE0MTIzMDA0
  WjANMQswCQYDVQQDDAJVSTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB
  ALuopzezuMRck3vw05RSJCEtbxnQJoWR8/ipOBp8jg2um2G8K2S92hZF4KSw29Cz
  X4f7CM0/Cg4ys6iElS3wIxvBDBx++Wa1peiWgr1yo88IVCunLL3ZtYooTYkKocqK
  U4BmmfJHKGgumq6I8JBoLHWItfFfaXthXcUu/P/U5VzcFrfkwRVgx2OYTUSiD/66
  MWKn4fHtW++9BHJSK8W0Cfc/zILOQr7uzsdwafyZaj/wN2sajXWb+LeuEE3oM2c+
  8zkRSLcV3dpWa36JvdyahwSgzwFd4f7MJsEAuhBcIonaWC7Gw5W/gH+ceT7dc/KT
  iVNPXdI/k0/MJJZoRXDGzlMCAwEAAaNTMFEwHQYDVR0OBBYEFOB0ny+QIau5HzIy
  hCtHWMo8venpMB8GA1UdIwQYMBaAFOB0ny+QIau5HzIyhCtHWMo8venpMA8GA1Ud
  EwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAKFugRFzxptoZcG58gLC5WCq
  tnurFblxJP8T9DtP5zvIPR7Gc933lBfOHP+8F+WKTp11Xi9ndnIYEoXzII+UBXTz
  ocDCul2aAsubz7kS/yXzMY1F+7q36y4eeM+CDnawhhOc85Xg0tbvzNMlCyJX0TJk
  MImt7TfvebCx48mVkuV65BXEuGUD3bVmBEeakGIJSOIwuGwnFnhe+gh/LNq8BsxW
  +UNp5gs0oiS7o7H+QuArQRajdK2ANKMyCrGmE8lBexOyPqD/YBE1W68HdmYJKG9S
  jV+RlU5SkGhUe439pgFHRmOw4f4CaeikC6OhO55ro0IJR6SUomcnG+GAZ/Hdj8g=
  -----END CERTIFICATE-----
os_cert: |
  -----BEGIN CERTIFICATE-----
  AAAA+zCCAeOgAwIBAgIUMN6V0m2QaJlp1mQ6qI5vH8NGHr4wDQYJKoZIhvcNAQEL
  BQAwDTELMAkGA1UEAwwCVUkwHhcNMjAwNDE2MTIzMDA0WhcNMzAwNDE0MTIzMDA0
  WjANMQswCQYDVQQDDAJVSTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB
  ALuopzezuMRck3vw05RSJCEtbxnQJoWR8/ipOBp8jg2um2G8K2S92hZF4KSw29Cz
  X4f7CM0/Cg4ys6iElS3wIxvBDBx++Wa1peiWgr1yo88IVCunLL3ZtYooTYkKocqK
  U4BmmfJHKGgumq6I8JBoLHWItfFfaXthXcUu/P/U5VzcFrfkwRVgx2OYTUSiD/66
  MWKn4fHtW++9BHJSK8W0Cfc/zILOQr7uzsdwafyZaj/wN2sajXWb+LeuEE3oM2c+
  8zkRSLcV3dpWa36JvdyahwSgzwFd4f7MJsEAuhBcIonaWC7Gw5W/gH+ceT7dc/KT
  iVNPXdI/k0/MJJZoRXDGzlMCAwEAAaNTMFEwHQYDVR0OBBYEFOB0ny+QIau5HzIy
  hCtHWMo8venpMB8GA1UdIwQYMBaAFOB0ny+QIau5HzIyhCtHWMo8venpMA8GA1Ud
  EwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAKFugRFzxptoZcG58gLC5WCq
  tnurFblxJP8T9DtP5zvIPR7Gc933lBfOHP+8F+WKTp11Xi9ndnIYEoXzII+UBXTz
  ocDCul2aAsubz7kS/yXzMY1F+7q36y4eeM+CDnawhhOc85Xg0tbvzNMlCyJX0TJk
  MImt7TfvebCx48mVkuV65BXEuGUD3bVmBEeakGIJSOIwuGwnFnhe+gh/LNq8BsxW
  +UNp5gs0oiS7o7H+QuArQRajdK2ANKMyCrGmE8lBexOyPqD/YBE1W68HdmYJKG9S
  jV+RlU5SkGhUe439pgFHRmOw4f4CaeikC6OhO55ro0IJR6SUomcnG+GAZ/Hdj8g=
  -----END CERTIFICATE-----
os_key: |
  -----BEGIN PRIVATE KEY-----
  MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7qKc3s7jEXJN7
  8NOUUiQhLW8Z0CaFkfP4qTgafI4NrpthvCtkvdoWReCksNvQs1+H+wjNPwoOMrOo
  hJUt8CMbwQwcfvlmtaXoloK9cqPPCFQrpyy92bWKKE2JCqHKilOAZpnyRyhoLpqu
  iPCQaCx1iLXxX2l7YV3FLvz/1OVc3Ba35MEVYMdjmE1Eog/+ujFip+Hx7VvvvQRy
  UivFtAn3P8yCzkK+7s7HcGn8mWo/8DdrGo11m/i3rhBN6DNnPvM5EUi3Fd3aVmt+
  ib3cmocEoM8BXeH+zCbBALoQXCKJ2lguxsOVv4B/nHk+3XPyk4lTT13SP5NPzCSW
  aEVwxs5TAgMBAAECggEBAJKbMAhUYAUITjCF9MXrZk6FMEb6Vx4C6JdbnHkU1eXa
  g4nXeA88QyUjcl03zoM9n2ScukOe/DwbYEBHVESPVt5X8x5QFIgpYXRUIc/fwBn+
  Z8Oy10F61FkbI3fs1nlll9a4UYz2CptZzX6NfWNT/2fTZlEsOTwq1Rc3nnA/4vCn
  qaU/Iwe/F+pjwl2rgPcDRPrbNHkrF1iJIyii3O+6Ke7j9tvwjcxdMgKYGfk7f3J6
  aTA2SSPFZyr2SCQm3hREDtSdlNaZ3TvVq9kbT4htjn08ky0vWkRqGxfQg05E0/wQ
  4SVX3CZE+B1jOdBG3IFoqSrVh/AAcNFStGE2Dz+bwAECgYEA7F9YYjY5OBkyvnPM
  MiTbkKWtF8ABKHd+Kk+FMGDa6nsVRB4G1eXYpb0chBsb9DsHh1ijlIOBrz6SndnH
  VZ1pvt5LHcgtUaLphpFJl08krr7OLVQpfwT+Q85MMVey76SlBnrxeXuKfWH+Jw1t
  MIzSfi7kHxCTxD36d615u7JGuTcCgYEAyz3IzyhDj7kjagI0wODjcqrmEruvUYgV
  RgwM9ELQCOE3dstNS+dFh0gJg9/IYKtW8w8bfFXetlnrgvYiIpzctYLfPY1lFqsC
  xpzlEUD+sLLjMIH98wl2XnVd/5uAEUp2xelO4cquddLr9w48Mwk/jPb8RXLow8fh
  pZw9VfSvccUCgYEAqLfJw5iGsSczVEQdfbFXU+EeMzSm3vakBJlsLUMFH5epb0yr
  fmQohuz8fMNI6cR0tEQtxuUzXR4h0zBOmyrX/xh2r5Rh3MKXQ6lSyQEB4wVo72wC
  jprGzylis1mw7GMuM/jvgdIP4T1gBwoLZTsvSEg6Jn5TqyC+NkyJ9tLirnMCgYA8
  23tNzJiuaJmaHJ7/QlfY9iN+aITOvRjhqKoYWglBH28kOywiFlZTc9aljlTJ3YRj
  s5pfWLcfkz1aMal3A9Fy6IVAQR6L8xkZr9FHoVaiQm6VD9ei9qpjDnHfIAjxJIL8
  MChWpAIpdccCa1jLT3GgHDTd9tKMDUYb+PTE0EfYoQKBgG990/rnjsLam/TzkvAU
  JqzvIO/13bR63laC9CNhdu0L2khgQ2hHgB5ksZ7NucstehSrTLD0sus9ocZLMvCT
  Oq18rA4QA34ur3YgFJC8Bl63+yfYnE4z2WP250Q0z0sWNw3i2PkTh5/gozkv1Xld
  IvrRjS2RTSoHYw5Ug0WfHR9A
  -----END PRIVATE KEY-----
```