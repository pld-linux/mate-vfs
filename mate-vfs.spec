# NOTE: this package is deprecated, meant for MATE <= 1.4 compatibility only
#
# Conditional build:
%bcond_with	hal		# build with HAL support (HAL is deprecated)
#
Summary:	MATE - virtual file system
Summary(pl.UTF-8):	MATE - wirtualny system plików
Name:		mate-vfs
Version:	1.4.0
Release:	1
License:	LGPL v2+
Group:		Applications
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz
# Source0-md5:	1e9d9384b739741c979fd834170f9214
Patch0:		%{name}-no_mate_mime.patch
Patch1:		%{name}-fstab_edit_crash.patch
Patch3:		%{name}-headers-define.patch
Patch4:		%{name}-ac-libs.patch
Patch5:		%{name}-glib.patch
Patch6:		%{name}-am.patch
URL:		http://mate-desktop.org
BuildRequires:	acl-devel >= 2.2.34
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	attr-devel
BuildRequires:	avahi-glib-devel >= 0.6.17
BuildRequires:	bzip2-devel
%{?with_hal:BuildRequires:	dbus-devel >= 0.32}
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	docbook-dtd412-xml >= 1.0-10
BuildRequires:	fam-devel
BuildRequires:	flex
BuildRequires:	gettext-devel >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.10.0
BuildRequires:	gtk-doc >= 1.0
%{?with_hal:BuildRequires:	hal-devel >= 0.5.7}
BuildRequires:	heimdal-devel
BuildRequires:	intltool >= 0.36.2
BuildRequires:	libselinux-devel
BuildRequires:	libsmbclient-devel >= 3.0
BuildRequires:	libtool >= 2:1.5.14
BuildRequires:	libxml2-devel >= 1:2.6.0
BuildRequires:	mate-common
BuildRequires:	mate-conf-devel >= 1.1.0
BuildRequires:	openssl-devel >= 0.9.8b
BuildRequires:	perl-base >= 5.002
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires(post,preun):	mate-conf >= 1.1.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	mate-conf >= 1.1.0
Requires:	shared-mime-info >= 0.18
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	mateconf_schema_install() \
	umask 022; \
	MATECONF_CONFIG_SOURCE="xml:readwrite:/etc/mateconf/mateconf.xml.defaults" /usr/bin/mateconftool-2 --makefile-install-rule /etc/mateconf/schemas/%{?1}%{!?1:*.schemas} > /dev/null ; \
	%{nil}

%define mateconf_schema_uninstall() \
	if [ $1 = 0 -a -x /usr/bin/mateconftool-2 ]; then \
		umask 022; \
		MATECONF_CONFIG_SOURCE="xml:readwrite:/etc/mateconf/mateconf.xml.defaults" /usr/bin/mateconftool-2 --makefile-uninstall-rule /etc/mateconf/schemas/%{?1} > /dev/null \
	fi ; \
	%{nil}

%description
MATE Virtual File System.

%description -l pl.UTF-8
Wirtualny Systemu Plików MATE.

%package libs
Summary:	mate-vfs library
Summary(pl.UTF-8):	Biblioteka mate-vfs
Group:		Libraries
%{?with_hal:Requires:	hal-libs >= 0.5.7}
Requires:	avahi-glib >= 0.6.17
Requires:	dbus-glib >= 0.60
Requires:	glib2 >= 1:2.10.0
Requires:	mate-conf-libs >= 1.1.0
Requires:	openssl >= 0.9.8b

%description libs
This package contains mate-vfs libraries.

%description libs -l pl.UTF-8
Pakiet zawiera biblioteki mate-vfs.

%package devel
Summary:	mate-vfs - header files
Summary(pl.UTF-8):	mate-vfs - pliki nagłówkowe
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	avahi-glib-devel >= 0.6.17
Requires:	dbus-glib-devel >= 0.60
Requires:	glib2-devel >= 1:2.10.0
Requires:	libselinux-devel
Requires:	mate-conf-devel >= 1.1.0
Requires:	openssl-devel >= 0.9.8b

%description devel
This package contains header files for mate-vfs library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki nagłówkowe biblioteki mate-vfs.

%package apidocs
Summary:	mate-vfs API documentation
Summary(pl.UTF-8):	Dokumentacja API mate-vfs
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
mate-vfs API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API mate-vfs.

%prep
%setup -q -n mate-vfs-%{version}
%patch0 -p1
%patch1 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	MATECONFTOOL=/usr/bin/mateconftool-2 \
	%{!?with_hal:--disable-hal} \
	--disable-howl \
	--disable-schemas-install \
	--disable-static \
	--enable-gtk-doc \
	--enable-ipv6 \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la \
	$RPM_BUILD_ROOT%{_libdir}/mate-vfs-2.0/modules/*.la

%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{sr@ije,sr@ijekavian}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%mateconf_schema_install desktop_default_applications.schemas
%mateconf_schema_install desktop_mate_url_handlers.schemas
%mateconf_schema_install system_dns_sd.schemas
%mateconf_schema_install system_http_proxy.schemas
%mateconf_schema_install system_smb.schemas

%preun
%mateconf_schema_uninstall desktop_default_applications.schemas
%mateconf_schema_uninstall desktop_mate_url_handlers.schemas
%mateconf_schema_uninstall system_dns_sd.schemas
%mateconf_schema_uninstall system_http_proxy.schemas
%mateconf_schema_uninstall system_smb.schemas

%post	libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%dir %{_sysconfdir}/mate-vfs-2.0
%dir %{_sysconfdir}/mate-vfs-2.0/modules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mate-vfs-2.0/modules/default-modules.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mate-vfs-2.0/modules/smb-module.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mate-vfs-2.0/modules/ssl-modules.conf
%{_sysconfdir}/mateconf/schemas/desktop_default_applications.schemas
%{_sysconfdir}/mateconf/schemas/desktop_mate_url_handlers.schemas
%{_sysconfdir}/mateconf/schemas/system_dns_sd.schemas
%{_sysconfdir}/mateconf/schemas/system_http_proxy.schemas
%{_sysconfdir}/mateconf/schemas/system_smb.schemas
%attr(755,root,root) %{_bindir}/matevfs-cat
%attr(755,root,root) %{_bindir}/matevfs-copy
%attr(755,root,root) %{_bindir}/matevfs-df
%attr(755,root,root) %{_bindir}/matevfs-info
%attr(755,root,root) %{_bindir}/matevfs-ls
%attr(755,root,root) %{_bindir}/matevfs-mkdir
%attr(755,root,root) %{_bindir}/matevfs-monitor
%attr(755,root,root) %{_bindir}/matevfs-mv
%attr(755,root,root) %{_bindir}/matevfs-rm
%attr(755,root,root) %{_libexecdir}/mate-vfs-daemon
%dir %{_libdir}/mate-vfs-2.0/modules
%attr(755,root,root) %{_libdir}/mate-vfs-2.0/modules/libbzip2.so
%attr(755,root,root) %{_libdir}/mate-vfs-2.0/modules/libcomputer.so
%attr(755,root,root) %{_libdir}/mate-vfs-2.0/modules/libdns-sd.so
%attr(755,root,root) %{_libdir}/mate-vfs-2.0/modules/libfile.so
%attr(755,root,root) %{_libdir}/mate-vfs-2.0/modules/libftp.so
%attr(755,root,root) %{_libdir}/mate-vfs-2.0/modules/libgzip.so
%attr(755,root,root) %{_libdir}/mate-vfs-2.0/modules/libhttp.so
%attr(755,root,root) %{_libdir}/mate-vfs-2.0/modules/libnetwork.so
%attr(755,root,root) %{_libdir}/mate-vfs-2.0/modules/libnntp.so
%attr(755,root,root) %{_libdir}/mate-vfs-2.0/modules/libsftp.so
%attr(755,root,root) %{_libdir}/mate-vfs-2.0/modules/libsmb.so
%attr(755,root,root) %{_libdir}/mate-vfs-2.0/modules/libtar.so
%attr(755,root,root) %{_libdir}/mate-vfs-2.0/modules/libvfs-test.so
%{_datadir}/dbus-1/services/mate-vfs-daemon.service

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmatevfs-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmatevfs-2.so.0
%dir %{_libdir}/mate-vfs-2.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmatevfs-2.so
%{_includedir}/mate-vfs-2.0
%{_includedir}/mate-vfs-module-2.0
%{_libdir}/mate-vfs-2.0/include
%{_pkgconfigdir}/mate-vfs-2.0.pc
%{_pkgconfigdir}/mate-vfs-module-2.0.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mate-vfs-2.0
