Name:           oc-inject
Version:        0.0.1
Release:        1%{?dist}
Summary:        Copy an executable to an OpenShift container and run it

License:        ASL 2.0
URL:            https://github.com/serhei/oc-inject
Source0:        https://github.com/serhei/oc-inject/archive/v0.0.1.tar.gz

#BuildRequires:  
BuildArch:      noarch
Requires:       python3

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
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
cp -a oc-inject %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_pkgdocdir}
cp -a README.md %{buildroot}%{_pkgdocdir}

%files
%{_bindir}/oc-inject
%license LICENSE
%doc README.md



%changelog
* Mon Dec 17 2018 Serhei Makarov <me@serhei.io> - 0.0.1-1
- Initial release to test rpmbuild and COPR.
