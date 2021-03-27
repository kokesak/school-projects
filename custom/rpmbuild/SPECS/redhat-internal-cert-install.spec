Name:           redhat-internal-cert-install
Version:        0.1
Release:        9%{?dist}
Summary:        Red Hat, Inc. Internal Certification install
License:        Public Domain

Source0:        newca.crt
Source1:        2015-RH-IT-Root-CA.pem
Source2:        oracle_ebs.crt
Source3:        deployment.config
Source4:        deployment.properties
Source5:        Eng-CA.crt
Source6:        pki-ca-chain.crt

BuildArch:      noarch

Requires:       ca-certificates
Requires:       coreutils
Requires:       openldap

%description
This package installs the internal Red Hat CA Certificate.
This allows a trusted connection to internal Red Hat Services.

%install
mkdir -p %{buildroot}/%{_sysconfdir}/pki/ca-trust/source/anchors/
mkdir -p %{buildroot}/%{_sysconfdir}/pki/tls/certs/
mkdir -p %{buildroot}/%{_sysconfdir}/openldap/cacerts/
mkdir -p %{buildroot}/%{_sysconfdir}/.java/deployment/

install -m 644 %{SOURCE0} %{buildroot}/%{_sysconfdir}/pki/ca-trust/source/anchors/
install -m 640 %{SOURCE0} %{buildroot}/%{_sysconfdir}/pki/tls/certs/
install -m 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/pki/ca-trust/source/anchors/
install -m 640 %{SOURCE1} %{buildroot}/%{_sysconfdir}/pki/tls/certs/
install -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/pki/ca-trust/source/anchors/
install -m 640 %{SOURCE2} %{buildroot}/%{_sysconfdir}/pki/tls/certs/
install -m 644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/pki/ca-trust/source/anchors/
install -m 640 %{SOURCE5} %{buildroot}/%{_sysconfdir}/pki/tls/certs/
install -m 644 %{SOURCE6} %{buildroot}/%{_sysconfdir}/pki/ca-trust/source/anchors/
install -m 640 %{SOURCE6} %{buildroot}/%{_sysconfdir}/pki/tls/certs/

install -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/.java/deployment/
install -m 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/.java/deployment/

%post
if [ ! -h /etc/openldap/cacerts/7e757f6a.0 ]; then 
    ln -s /etc/pki/tls/certs/2015-RH-IT-Root-CA.pem /etc/openldap/cacerts/7e757f6a.0
fi

if [ ! -h /etc/openldap/cacerts/a275a5bb.0 ]; then 
    ln -s /etc/pki/tls/certs/newca.crt /etc/openldap/cacerts/a275a5bb.0
fi

sed -i '/## CSB addition start/,/## CSB addition end/d' /etc/openldap/ldap.conf
sed -i -e :a -e '/^\n*$/{$d;N;};/\n$/ba' /etc/openldap/ldap.conf

# add needed entries to /etc/openldap/ldap.conf
cat << EOF >> /etc/openldap/ldap.conf

## CSB addition start
# added by Oliver Haessler, requested by "Brian J. Atkisson" <batkisso@redhat.com>
# 2016-10-27
URI ldaps://ldap.corp.redhat.com/ ldaps://corp.ldap.prod.int.phx2.redhat.com
BASE dc=redhat,dc=com
SASL_MECH GSSAPI
TLS_REQCERT demand
## CSB addition end
EOF

update-ca-trust

%postun
if [ $1 == 0 ]; then
    if [ -f /etc/openldap/cacerts/7e757f6a.0 ]; then
        rm -f /etc/openldap/cacerts/7e757f6a.0
    fi
    if [ -f /etc/openldap/cacerts/a275a5bb.0 ]; then
        rm -f /etc/openldap/cacerts/a275a5bb.0
    fi

    sed -i '/## CSB addition start/,/## CSB addition end/d' /etc/openldap/ldap.conf
    sed -i -e :a -e '/^\n*$/{$d;N;};/\n$/ba' /etc/openldap/ldap.conf

    update-ca-trust
fi

%files
%dir %{_sysconfdir}/openldap/cacerts/
%{_sysconfdir}/pki/ca-trust/source/anchors/newca.crt
%{_sysconfdir}/pki/ca-trust/source/anchors/2015-RH-IT-Root-CA.pem
%{_sysconfdir}/pki/ca-trust/source/anchors/oracle_ebs.crt
%{_sysconfdir}/pki/ca-trust/source/anchors/Eng-CA.crt
%{_sysconfdir}/pki/ca-trust/source/anchors/pki-ca-chain.crt
%{_sysconfdir}/pki/tls/certs/newca.crt
%{_sysconfdir}/pki/tls/certs/2015-RH-IT-Root-CA.pem
%{_sysconfdir}/pki/tls/certs/oracle_ebs.crt
%{_sysconfdir}/pki/tls/certs/Eng-CA.crt
%{_sysconfdir}/pki/tls/certs/pki-ca-chain.crt
%{_sysconfdir}/.java/deployment/
%{_sysconfdir}/.java/deployment/deployment.properties

%changelog
* Mon Apr 09 2018 Oliver Haessler <oliver@redhat.com> - 0.1-9
- added new Requires to fullfill dependencies

* Tue Dec 12 2017 Oliver Haessler <oliver@redhat.com> - 0.1-8
- added Engineering certificates (INC0637780)

* Thu Oct 27 2016 Oliver Haessler <oliver@redhat.com> - 0.1-7
- change for new ldap infrastructure

* Tue Jun 07 2016 Oliver Haessler <oliver@redhat.com> - 0.1-6
- fixed setting in deployment.properties

* Mon Sep 14 2015 Oliver Haessler <oliver@redhat.com> - 0.1-5
- added Oracle EBS cert
- added IcedTea settings to prevent Pop Ups during start of Oracle Applications

* Fri Jul 24 2015 Oliver Haessler <oliver@redhat.com> - 0.1-4
- corrected creation of empty directory
- corrected postun section

* Fri Jul 24 2015 Oliver Haessler <oliver@redhat.com> - 0.1-3
- included needed changes to ldap.conf and added the cacerts
requested by "Brian J. Atkisson" <batkisso@redhat.com>

* Fri Jul 10 2015 Oliver Haessler <oliver@redhat.com> - 0.1-2
- added the new Red Hat root certificate

* Tue Jun 24 2014 Oliver Haessler <oliver@redhat.com> - 0.1-1
- initial build
