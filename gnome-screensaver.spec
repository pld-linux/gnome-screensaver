Summary:	GNOME screensaver
Summary(pl.UTF-8):	Wygaszacz ekranu GNOME
Name:		gnome-screensaver
Version:	2.24.1
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-screensaver/2.24/%{name}-%{version}.tar.bz2
# Source0-md5:	f0b9cc3108bb9105141a8c22b56bf615
Source1:	%{name}.pamd
Source2:	http://ep09.pld-linux.org/~havner/%{name}-xscreensaver.tar.gz
# Source2-md5:	58ad753724418430fa93f02558056eab
Patch0:		%{name}-cosmos_theme_dir.patch
BuildRequires:	GConf2-devel >= 2.24.0
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.18.0
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gnome-desktop-devel >= 2.24.0
BuildRequires:	gnome-menus-devel >= 2.24.0
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libglade2-devel >= 1:2.6.2
BuildRequires:	libgnomekbd-devel >= 2.24.0
BuildRequires:	libnotify-devel
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-lib-libXmu-devel
Requires(post,preun):	GConf2
Requires:	xdg-menus
Obsoletes:	xscreensaver-gnome2
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A new screensaver solution for GNOME, with better HIG dialogs and a
much better integration into the desktop than the old xscreensaver.

%description -l pl.UTF-8
Nowe rozwiązanie wygaszcza ekranu dla GNOME, z bardziej zgodnymi z HIG
dialogami i lepszą integracją z desktopem niż stary xscreensaver.

%package xscreensaver
Summary:	Support for xscreensaver
Summary(pl.UTF-8):	Wsparcie dla xscreensavera
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	xscreensaver-savers

%description xscreensaver
Support for xscreensaver.

%description xscreensaver -l pl.UTF-8
Wsparcie dla xscreensavera.

%prep
%setup -q -a2
%patch0 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-pam \
	--enable-locking \
	--with-dpms-ext \
	--with-mit-ext \
	--with-shadow \
	--with-xf86gamma-ext \
	--with-xf86vmode-ext \
	--with-xidle-ext \
	--with-xinerama-ext \
	--with-xscreensaverdir=%{_datadir}/xscreensaver \
	--with-xscreensaverhackdir=%{_libdir}/xscreensaver \
	--with-gdm-config=%{_datadir}/gdm/defaults.conf
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/gnome-screensaver

_DIR=$(pwd)
cd %{name}-xscreensaver
# this one is provided by gnome-screensaver
rm -f popsquares.desktop
install * $RPM_BUILD_ROOT%{_desktopdir}/screensavers
echo '%defattr(644,root,root,755)' > $_DIR/xscreensaver.files
for I in *; do
	echo "%{_desktopdir}/screensavers/$I" >> $_DIR/xscreensaver.files
done
cd $_DIR

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install gnome-screensaver.schemas

%preun
%gconf_schema_uninstall gnome-screensaver.schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/gnome-screensaver
%attr(755,root,root) %{_bindir}/gnome-screensaver
%attr(755,root,root) %{_bindir}/gnome-screensaver-command
%attr(755,root,root) %{_bindir}/gnome-screensaver-preferences
%dir %{_libdir}/gnome-screensaver
%attr(755,root,root) %{_libdir}/gnome-screensaver/floaters
%attr(755,root,root) %{_libdir}/gnome-screensaver/popsquares
%attr(755,root,root) %{_libdir}/gnome-screensaver/slideshow
%attr(755,root,root) %{_libdir}/gnome-screensaver-dialog
%attr(755,root,root) %{_libdir}/gnome-screensaver-gl-helper
%{_datadir}/%{name}
%{_datadir}/desktop-directories/gnome-screensaver.directory
%dir %{_desktopdir}/screensavers
%{_desktopdir}/screensavers/cosmos-slideshow.desktop
%{_desktopdir}/screensavers/footlogo-floaters.desktop
%{_desktopdir}/screensavers/personal-slideshow.desktop
%{_desktopdir}/screensavers/popsquares.desktop
%{_desktopdir}/gnome-screensaver-preferences.desktop
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/gnome-screensaver.schemas
%{_sysconfdir}/xdg/menus/gnome-screensavers.menu
%{_pkgconfigdir}/gnome-screensaver.pc
%{_mandir}/man1/gnome-screensaver.1*
%{_mandir}/man1/gnome-screensaver-command.1*
%{_mandir}/man1/gnome-screensaver-preferences.1*

%files xscreensaver -f xscreensaver.files
%defattr(644,root,root,755)
