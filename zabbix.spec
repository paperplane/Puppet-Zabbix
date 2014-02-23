%define _topdir         /root/zabbix

Summary:		Zabbix - The Ultimate Open Source Monitoring Solution
Name:			zabbix
Version:		2.2.0
Release:		2
License:		GPL v2+
Group:			Networking/Admin
Source0:		%{name}-%{version}.tar.gz
URL:			http://zabbix.sourceforge.net/
BuildRequires:  	mysql-devel
BuildRequires:		net-snmp-devel
BuildRequires:		openssl-devel
BuildRequires:		gcc
BuildRequires:		curl-devel
BuildRequires:		libcurl-devel
BuildRequires:		libxml2-devel
BuildRequires:		libssh2-devel
BuildRequires:		OpenIPMI-devel
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):		/usr/sbin/groupadd
Requires(pre):		/usr/sbin/useradd
Provides:		group(zabbix)
Provides:		user(zabbix)
BuildRoot: 		%{_topdir}/%{name}-%{version}-root

%define         _prefixdir      /usr/local/%{name}
%define         _bindir		/usr/local/%{name}/bin
%define         _sbindir        /usr/local/%{name}/sbin
%define		_sysconfdir	/usr/local/%{name}/etc
%define		_appdir		/usr/local/%{name}/share
%define		_mandir		/usr/local/%{name}/share/man
%define		_libdir		/usr/local/%{name}/lib
%define		_webrootdir	/usr/local/nginx/html

%description
Zabbix is the ultimate enterprise-level software designed for 
monitoring availability and performance of IT infrastructure 
components. Zabbix is open source and comes at no cost.

%package agent
Summary:	Standalone agent for zabbix
Group:		Networking/Admin
Requires:	%{name} = %{version}
Requires:	openssl-devel
%description agent
This package provides the zabbix agent

%package frontend-php
Summary:	PHP frontend for zabbix
Group:		Networking/Admin
Requires:	php
Requires:	php-devel
Requires:	php-fpm
Requires:	php-common
Requires:	php-mbstring
Requires:	php-pdo
Requires:	php-pear
Requires:	php-bcmath
Requires:	php-mysql
Requires:	php-gd
Requires:	php-xml
%description frontend-php
This package provides web based (PHP) frontend for zabbix.

%package get
Summary:	Program retrieving data from the zabbix agentd daemon
Group:		Networking/Admin
%description get
This package provides a program retrieving data from zabbix agentd daemon.

%package sender
Summary:	Zabbix sender
Group:		Networking/Admin
%description sender
This package provides the zabbix sender.

%package server
Summary:	Zabbix server
Group:		Networking/Admin
Requires:	%{name} = %{version}
%description server
This package provides the zabbix server.  

%package proxy
Summary:	Program used as a proxy between zabbix servers and agents
Group:		Networking/Admin
Requires:       %{name} = %{version}
%description proxy
This package provides a program that acts as a proxy between zabbix servers 
and agents, to assist in passing through firewalls and NAT

%prep
%setup -q

%build
%configure \
	--with-openipmi \
        --with-libcurl \
        --with-libxml2 \
	--with-mysql \
	--with-libcurl \
	--enable-server \
	--enable-proxy \
	--enable-agent \
	--with-net-snmp \
 	--with-ssh2 \
	--prefix=%{_prefixdir} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --mandir=%{_mandir} \
        --libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir} \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},%{_webrootdir}}
mkdir -p $RPM_BUILD_ROOT/var/log/zabbix

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install conf/zabbix_{agent,server,proxy,agentd}.conf $RPM_BUILD_ROOT%{_sysconfdir}
install -d conf/zabbix_agentd $RPM_BUILD_ROOT%{_sysconfdir}
cp -r frontends/php/* $RPM_BUILD_ROOT%{_webrootdir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
user_check="`grep zabbix /etc/passwd | wc -l`"
group_check="`grep zabbix /etc/group | wc -l`"

if [[ $user_check -eq 0 ]]; 
then
	groupadd zabbix
fi

if [[ $group_check -eq 0 ]]; 
then
	useradd -d %{_appdir} -g zabbix -c "Zabbix User" -s /bin/false zabbix
fi

%post

%postun
userdel --force zabbix 2> /dev/null; true

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README ChangeLog
%attr(750,zabbix,zabbix) %dir %{_sysconfdir}
%attr(750,zabbix,zabbix) %dir %{_appdir}
%attr(750,zabbix,zabbix) %dir %{_libdir}

%files agent
%defattr(644,root,root,755)
%attr(750,zabbix,zabbix) %dir /var/log/zabbix
%attr(640,zabbix,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agentd.conf 
%attr(640,zabbix,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agent.conf 
%attr(755,root,root) %{_sbindir}/zabbix_agentd 
%attr(755,root,root) %{_sbindir}/zabbix_agent
%{_mandir}/man8/zabbix_agentd.8*

%files frontend-php
%defattr(644,root,root,755)
%attr(775,apache,apache) %{_webrootdir}

%files get
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zabbix_get
%{_mandir}/man1/zabbix_get.1*

%files sender
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zabbix_sender
%{_mandir}/man1/zabbix_sender.1*

%files server
%defattr(644,root,root,755)
%attr(750,zabbix,zabbix) %dir /var/log/zabbix
%attr(644,root,root) %doc upgrades
%attr(640,zabbix,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_server.conf
%attr(755,root,root) %{_sbindir}/zabbix_server
%{_mandir}/man8/zabbix_server.8*

%files proxy
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/zabbix_proxy
%attr(640,zabbix,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_proxy.conf
%{_mandir}/man8/zabbix_proxy.8*

%changelog
