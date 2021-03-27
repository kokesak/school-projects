# This will not necessarily match the RPM Version if the real version number is
# not representable in RPM. For example, a release candidate might be 0.15.0rc1
# but that is not usable for the RPM Version because it sorts higher than
# 0.15.0, so the RPM will have Version 0.15.0 and Release 0.rc1 in that case.
%global upstream_name beaker

Name:           %{upstream_name}
Version:        26.3
Release:        1%{?dist}
Summary:        Full-stack software and hardware integration testing system
Group:          Applications/Internet
License:        GPLv2+ and BSD
URL:            https://beaker-project.org/

Source0:        https://beaker-project.org/releases/%{upstream_name}-%{version}.tar.xz
# Explicitly remove building server from the Makefiles
Patch1:         0001_dont_build_server.diff

BuildArch:      noarch
BuildRequires:  python2-setuptools
BuildRequires:  python2-nose
BuildRequires:  python2-unittest2
BuildRequires:  python2-mock
BuildRequires:  python2-devel
BuildRequires:  python2-docutils
BuildRequires:  python2-sphinx
BuildRequires:  python2-sphinxcontrib-httpdomain

%package common
Summary:        Common components for Beaker packages
Group:          Applications/Internet
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} < 0.17.0-1

%package client
Summary:        Command-line client for interacting with Beaker
Group:          Applications/Internet
Requires:       %{name}-common = %{version}-%{release}
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  python2-krbv
BuildRequires:  python2-lxml
BuildRequires:  python2-libxslt
BuildRequires:  python2-prettytable
Requires:       python2-setuptools
Requires:       python2-krbv
Requires:       python2-lxml
Requires:       python2-requests
Requires:       python2-libxslt
Requires:       python2-libxml2
Requires:       python2-prettytable
Requires:       python2-jinja2
# beaker-wizard was moved from rhts-devel to here in 4.52
Conflicts:      rhts-devel < 4.52

%description
Beaker is a full stack software and hardware integration testing system, with
the ability to manage a globally distributed network of test labs.

%description common
Python modules which are used by other Beaker packages.

%description client
The bkr client is a command-line tool for interacting with Beaker servers. You
can use it to submit Beaker jobs, fetch results, and perform many other tasks.

%prep
%setup -q -n %{upstream_name}-%{version}
%patch1 -p1
# The server relies on a great many packages which are intended to be bundled
# source, and its documentation greatly inflates the number of BR packages
# required. Until those are packaged separately, building those subpackages is
# unnnecessary
rm -r Server documentation/server-api IntegrationTests LabController

%build
make

%install
DESTDIR=%{buildroot} make install

rm -rf %{buildroot}%{_datadir}/beaker-integration-tests/
rm -rf %{buildroot}%{python2_sitelib}/bkr/inttest
rm -rf %{buildroot}%{python2_sitelib}/beaker_integration_tests*
# These are for lab-controller stuff, which depends on server
rm -rf %{buildroot}%{_mandir}/man8/

%check
make check

%files common
%doc README.md
%license COPYING
%dir %{python2_sitelib}/bkr/
%{python2_sitelib}/bkr/__init__.py*
%{python2_sitelib}/bkr/timeout_xmlrpclib.py*
%{python2_sitelib}/bkr/common/
%{python2_sitelib}/bkr/log.py*
%{python2_sitelib}/%{name}_common-%{version}-py2.7.egg-info/

%files client
%dir %{_sysconfdir}/%{name}
%doc Client/client.conf.example
%{python2_sitelib}/bkr/client/
%{python2_sitelib}/%{name}_client-%{version}-py2.7-nspkg.pth
%{python2_sitelib}/%{name}_client-%{version}-py2.7.egg-info/
%{_bindir}/%{name}-wizard
%{_bindir}/bkr
%{_mandir}/man1/beaker-wizard.1.gz
%{_mandir}/man1/bkr.1.gz
%{_mandir}/man1/bkr-*.1.gz
%{_datadir}/bash-completion

%changelog
* Thu Jan 24 2019 Greg Hellings <greg.hellings@gmail.com> - 26.3-1
- New upstream 26.3

* Fri Nov 02 2018 Greg Hellings <greg.hellings@gmail.com> - 26.0-1
- New upstream 26.0

* Wed Sep 05 2018 Greg Hellings <greg.hellings@gmail.com> - 25.6-1
- New upstream 25.6

* Fri Aug 03 2018 Greg Hellings <greg.hellings@gmail.com> - 25.5-2
- Remove lab-controller, which depends on server
- Remove integration tests, which are designed for server use
- Shuffle BR/Requires to bring into line with upstream

* Wed Jul 25 2018 Greg Hellings <greg.hellings@gmail.com> - 25.5-1
- Upstream version 25.5
- Fixes BZ1607380
- Added deps for gevent and werkzeug
- Added labcontroller subpackage

* Fri Jul 13 2018 Dan Callaghan <dcallagh@redhat.com> - 25.4-3
- Explicitly invoke python2 instead of python:
  https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 25 2018 Greg Hellings <greg.hellings@gmail.com> - 25.4-1
- Upstream version 25.4
- Fixes BZ 1579575

* Mon May 14 2018 Greg Hellings <greg.hellings@gmail.com> - 25.2-1
- Upstream version 25.2
- Fixes BZ1566043

* Tue Mar 13 2018 Greg Hellings <greg.hellings@gmail.com> - 25.0-1
- Upstream version 25.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 24.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 16 2017 Greg Hellings <greg.hellings@gmail.com> - 24.5-1
- Upstream release 24.5

* Tue Oct 03 2017 Greg Hellings <greg.hellings@gmail.com> - 24.4-1
- Upstream release 24.4

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 24.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 30 2017 Greg Hellings <greg.hellings@gmail.com> - 24.3-1
- Upstream release 24.3

* Thu Apr 06 2017 Greg Hellings <greg.hellings@gmail.com> - 24.2-1
- Upstream release 24.2

* Mon Mar 06 2017 Greg Hellings <greg.hellings@gmail.com> - 24.1-2
- Fixed broken dependency

* Mon Mar 06 2017 Greg Hellings <greg.hellings@gmail.com> - 24.1-1
- New upstream release 24.1
- Imported to official builds

* Wed Mar 01 2017 Greg Hellings <greg.hellings@gmail.com> - 24.0-2
- Renamed child packages per review

* Thu Feb 23 2017 Greg Hellings <greg.hellings@gmail.com> - 24.0-1
- Upgraded to upstream 24.0

* Wed Dec 21 2016 Greg Hellings <greg.hellings@gmail.com> - 23.3-1
- Initial build
