Summary:	GNOME screensaver
Summary(pl.UTF-8):	Wygaszacz ekranu GNOME
Name:		gnome-screensaver
Version:	2.20.0
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-screensaver/2.20/%{name}-%{version}.tar.bz2
# Source0-md5:	d166a3ebf69289331b2ebcf5c0187fd9
Source1:	%{name}.pamd
Source2:	http://ep09.pld-linux.org/~havner/%{name}-xscreensaver.tar.gz
# Source2-md5:	58ad753724418430fa93f02558056eab
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-cosmos_theme_dir.patch
BuildRequires:	GConf2-devel >= 2.18.0.1
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.73
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gnome-menus-devel >= 2.20.0
BuildRequires:	gnome-vfs2-devel >= 2.20.0
BuildRequires:	gtk+2-devel >= 2:2.12.0
BuildRequires:	intltool >= 0.35.5
BuildRequires:	libexif-devel >= 1:0.6.13
BuildRequires:	libglade2 >= 1:2.6.0
BuildRequires:	libgnomekbd-devel >= 2.18.0
BuildRequires:	libgnomeui-devel >= 2.18.1
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libXmu-devel
Requires(post,preun):	GConf2
Requires:	libgnomeui >= 2.18.1
Requires:	xdg-menus
Obsoletes:	xscreensaver-gnome2
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
%patch1 -p1

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
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/gnome-screensaver
%attr(755,root,root) %{_libdir}/gnome-screensaver-dialog
%attr(755,root,root) %{_libdir}/gnome-screensaver-gl-helper
%{_datadir}/%{name}
%{_datadir}/desktop-directories/*
%dir %{_desktopdir}/screensavers
%{_desktopdir}/screensavers/cosmos-slideshow.desktop
%{_desktopdir}/screensavers/footlogo-floaters.desktop
%{_desktopdir}/screensavers/personal-slideshow.desktop
%{_desktopdir}/screensavers/popsquares.desktop
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/gnome-screensaver.schemas
%{_sysconfdir}/xdg/menus/*
%{_pkgconfigdir}/*.pc

%files xscreensaver -f xscreensaver.files
%defattr(644,root,root,755)
