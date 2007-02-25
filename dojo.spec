Summary:	dojo - the JavaScript Toolkit
Name:		dojo
Version:	0.4.1
Release:	0.1
License:	AFL 2.1 or BSD
Group:		Applications/WWW
Source0:	http://download.dojotoolkit.org/release-0.4.1/%{name}-%{version}-core.tar.gz
# Source0-md5:	90ff4443c6fca40663ee44edd3761373
URL:		http://www.dojotoolkit.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Dojo is a portable JavaScript toolkit for web application developers
and JavaScript professionals. Dojo solves real-world problems by
providing powerful abstractions and solid, tested implementations.

%prep
%setup -q -n %{name}-%{version}-core

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -a dojo.js $RPM_BUILD_ROOT%{_appdir}

install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README LICENSE
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%{_appdir}
