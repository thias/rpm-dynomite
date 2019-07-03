Summary: Thin, distributed dynamo layer for Redis and Memcached
Name: dynomite
Version: 0.6.14
Release: 0%{?dist}
License: ASL 2.0
URL: https://github.com/Netflix/dynomite/
Source0: https://github.com/Netflix/dynomite/archive/v%{version}.tar.gz
Source1: dynomite.service
Source2: dynomite.logrotate
#Requires: 
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: git-core
BuildRequires: openssl-devel
%{?systemd_requires}

%description
Dynomite, inspired by Dynamo whitepaper, is a thin, distributed dynamo layer
for different storage engines and protocols. Currently these include Redis and
Memcached. Dynomite supports multi-datacenter replication and is designed for
high availability.

The ultimate goal with Dynomite is to be able to implement high availability
and cross-datacenter replication on storage engines that do not inherently
provide that functionality. The implementation is efficient, not complex (few
moving parts), and highly performant.


%prep
%setup -q


%build
autoreconf -fvi
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/dynomite.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}/etc/logrotate.d/dynomite
install -D -p -m 0640 conf/dynomite.yml %{buildroot}/etc/dynomite.yml
mkdir -p %{buildroot}/var/log/dynomite


%clean
rm -rf %{buildroot}


%pre
getent group dynomite >/dev/null || groupadd -r dynomite
getent passwd dynomite >/dev/null || \
  useradd -r -d / -g dynomite \
  -s /sbin/nologin -c "Dynomite" dynomite

%post
%systemd_post dynomite.service

%preun
%systemd_preun dynomite.service

%postun
%systemd_postun dynomite.service


%files
%license LICENSE
%doc CONTRIBUTING.md NOTICE README.md conf/ notes/ scripts/
%attr(0640, root, dynomite) %config(noreplace) /etc/dynomite.yml
%config(noreplace) /etc/logrotate.d/dynomite
%{_unitdir}/dynomite.service
%{_bindir}/dynomite-hash-tool
%{_sbindir}/dynomite
%{_sbindir}/dynomite-test
%{_mandir}/man8/dynomite.8*
%attr(0770, root, dynomite) %dir /var/log/dynomite


%changelog
* Thu Jun 27 2019 Matthias Saou <matthias@saou.eu> 0.6.14-0
- Initial RPM release.

