Summary:	MATE window manager
Name:		mate-window-manager
Version:	1.6.2
Release:	5
License:	GPL v2+
Group:		X11/Window Managers
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	8f6ef12e31d74840aa3db7275149907d
Source1:	http://art.gnome.org/download/themes/metacity/1148/MCity-Simplebox.tar.gz
# Source1-md5:	033c5509bb4c573001fb7fef490f8bff
Patch0:		%{name}-freddix.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	startup-notification-devel
Requires(post,postun):	glib-gio-gsettings
Requires:	%{name}-libs = %{version}-%{release}
Provides:	window-manager
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE window manager.

%package libs
Summary:	MATE window manager - marco library
Group:		X11/Libraries

%description libs
This package contains marco library.

%package devel
Summary:	MATE - header files
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains header files for marco library.

%package themes
Summary:	Basic MATE window manager themes
Group:		Themes/GTK+
Requires:	%{name} = %{version}-%{release}

%description themes
Basic MATE window manager themes.

%prep
%setup -q -a1
%patch0 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	MATEDIALOG=%{_bindir}/matedialog	\
	--disable-schemas-install		\
	--disable-scrollkeeper			\
	--disable-silent-rules			\
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/xml/marco

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install doc/marco-theme.dtd $RPM_BUILD_ROOT%{_datadir}/xml/marco

cp -ar Simplebox $RPM_BUILD_ROOT%{_datadir}/themes

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/*.convert
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw,ha,ig,la}

%find_lang marco --with-mate

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache

%postun
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f marco.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README rationales.txt doc/theme-format.txt
%attr(755,root,root) %{_bindir}/marco
%attr(755,root,root) %{_bindir}/marco-message
%attr(755,root,root) %{_bindir}/marco-theme-viewer
%attr(755,root,root) %{_bindir}/marco-window-demo
%{_datadir}/glib-2.0/schemas/org.mate.marco.gschema.xml
%{_datadir}/mate-control-center/keybindings/*.xml
%{_datadir}/mate-window-manager
%{_datadir}/mate/wm-properties/marco-wm.desktop
%{_datadir}/themes/Simplebox
%{_datadir}/xml/marco
%{_desktopdir}/marco.desktop
%{_mandir}/man1/marco*.1*

%files themes
%defattr(644,root,root,755)
%{_datadir}/themes/ClearlooksRe
%{_datadir}/themes/Dopple
%{_datadir}/themes/Dopple-Left
%{_datadir}/themes/DustBlue
%{_datadir}/themes/Spidey
%{_datadir}/themes/Spidey-Left
%{_datadir}/themes/Splint
%{_datadir}/themes/Splint-Left
%{_datadir}/themes/WinMe
%{_datadir}/themes/eOS

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libmarco-private.so.?
%attr(755,root,root) %{_libdir}/libmarco-private.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog HACKING doc/dialogs.txt
%attr(755,root,root) %{_libdir}/libmarco-private.so
%{_includedir}/marco-1
%{_pkgconfigdir}/libmarco-private.pc

