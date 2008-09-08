#TODO
# - pld init script
# - apply patch to kernel
# - BR, R
#
Summary:	-
Summary(pl.UTF-8):	-
Name:		ttyrpld
Version:	2.52
Release:	0.1
License:	- (enter GPL/GPL v2/GPL v3/LGPL/BSD/BSD-like/other license name here)
Group:		Applications
Source0:	http://dl.sourceforge.net/ttyrpld/%{name}-%{version}.tar.bz2
# Source0-md5:	322674047f27652702ba35a196ca3c74
URL:		-
BuildRequires:	autoconf
BuildRequires:	libHX-devel >= 1.25
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ttyrpld is a multi-os kernel-level tty logger (key- and screenlogger
for ttys) with (a)synchronous replay supprt. It supports most tty
types, including vc, bsd and unix98-style ptys (xterm/ssh), serial,
isdn, etc. Being implemented within the kernel makes it unavoidable
for the default user. It runs with no overhead if the logging daemon
is not active.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d  $RPM_BUILD_ROOT/etc/rc.d/init.d
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_sysconfdir}/init.d/rpld $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpld.conf
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
