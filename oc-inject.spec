Name:           oc-inject
Version:        0.7.9
Release:        3%{?dist}
Summary:        Copy an executable to an OpenShift container and run it

License:        ASL 2.0
URL:            https://github.com/serhei/oc-inject
Source0:        https://github.com/serhei/oc-inject/releases/download/v0.7.9/oc-inject-0.7.9.tar.gz

#BuildRequires:  pandoc
BuildArch:      noarch
Requires:       python3
%if 0%{?fedora}
Recommends:     origin-clients
#Recommends:      kubernetes-client
Suggests:       java
%endif

%description
Copy an executable to an OpenShift container and run the executable.

oc-inject is a prototype tool for last-resort troubleshooting of a
running container, when a required debugging tool is not present in
the container image.

%global debug_package %{nil}
%prep
%autosetup


%build


%install
mkdir -p %{buildroot}%{_bindir}
cp -a oc-inject %{buildroot}%{_bindir}
chmod 0755 %{buildroot}%{_bindir}/oc-inject
mkdir -p %{buildroot}%{_mandir}/man1
cp -a oc-inject.1 %{buildroot}%{_mandir}/man1/oc-inject.1
sed -i "s/VERSION/%{version}/g" %{buildroot}%{_mandir}/man1/oc-inject.1
chmod 0644 %{buildroot}%{_mandir}/man1/oc-inject.1
mkdir -p %{buildroot}%{_pkgdocdir}
cp -a README.md %{buildroot}%{_pkgdocdir}

%files
%{_bindir}/oc-inject
%{_mandir}/man1/oc-inject.1.*

%license LICENSE
%doc README.md

%changelog
* Thu Jan 21 2021 Serhei Makarov <me@serhei.io> - 0.7.9-3
- Add dependency on origin-clients (oc).
- Note soft dependency on Java runtime environment.

* Wed Jan 20 2021 Serhei Makarov <me@serhei.io> - 0.7.9-2
- Fix Source0 URL.

* Fri Jan 15 2021 Serhei Makarov <me@serhei.io> - 0.7.9-1
- Draft version for Fedora package review.
- Added man page, updated install procedure.

* Mon Feb 10 2020 Serhei Makarov <me@serhei.io> - 0.0.3-1
- Updated version with rudimentary support for JDK tools.

* Wed Dec 11 2019 Serhei Makarov <me@serhei.io> - 0.0.2-1
- Updated version for Red Hat Developer Blog demos.

* Mon Dec 17 2018 Serhei Makarov <me@serhei.io> - 0.0.1-1
- Initial release to test rpmbuild and COPR.
