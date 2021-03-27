Name:           salina
Version:	0.1        
Release:        1%{?dist}
Summary:        Prints actual time

License:        GPLv3+
URL:            https://example.com/%{name}
Source0:        https://gitlab.cee.redhat.com/mlitwora/project_zero/-/archive/master/project_zero-master.tar.gz

BuildRequires:  bash
Requires:       bash
BuildArch:	noarch

%description
When called without arguments prints actual time. When used --version, display build date and hostname


%prep
%setup -q
%autosetup
find 
pwd

%build
find
pwd
sh ./build_me


%install
rm -rf $RPM_BUILD_ROOT
export DESTDIR=%{buildroot}
export PREFIX=/usr/ 

# druha moznost je dat PREFIX=neco sh ./instal_me
sh ./install_me


%files
/usr/bin/%{name}



%changelog
* Tue Jul 16 2019 Martin Litwora <mlitwora@redhat.com>
- Fisrt salina package 
