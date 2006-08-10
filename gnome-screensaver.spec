Summary:	GNOME screensaver
Summary(pl):	Wygaszacz ekranu GNOME
Name:		gnome-screensaver
Version:	2.15.6
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-screensaver/2.15/%{name}-%{version}.tar.bz2
# Source0-md5:	fad605326dc2e922264bdea96bfa981f
Source1:	%{name}.pamd
Source2:	http://ep09.pld-linux.org/~havner/%{name}-xscreensaver.tar.gz
# Source2-md5:	58ad753724418430fa93f02558056eab
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-cosmos_theme_dir.patch
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.71
BuildRequires:	gnome-common >= 2.12.0
BuildRequires:	gnome-menus-devel >= 2.15.91
BuildRequires:	gnome-vfs2-devel >= 2.15.91
BuildRequires:	gtk+2-devel >= 2:2.10.1
BuildRequires:	intltool >= 0.35
BuildRequires:	libexif-devel >= 1:0.6.13
BuildRequires:	libglade2 >= 1:2.6.0
BuildRequires:	libgnomeui-devel >= 2.15.91
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	xmlto
Requires(post,preun):   GConf2 >= 2.14.0
Requires:	libgnomeui >= 2.15.91
Requires:	xdg-menus
Obsoletes:	xscreensaver-gnome2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A new screensaver solution for GNOME, with better HIG dialogs and a
much better integration into the desktop than the old xscreensaver.

%description -l pl
Nowe rozwi±zanie wygaszcza ekranu dla GNOME, z bardziej zgodnymi z HIG
dialogami i lepsz± integracj± z desktopem ni¿ stary xscreensaver.

%package xscreensaver
Summary:        Support for xscreensaver
Summary(pl):    Wsparcie dla xscreensaver
Group:          X11/Applications
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       xscreensaver-savers

%description xscreensaver
Support for xscreensaver.

%description xscreensaver -l pl
Wsparcie dla xscreensaver.

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
	--with-xscreensaverdir=%{_sysconfdir}/X11/xscreensaver \
	--with-xscreensaverhackdir=%{_libdir}/xscreensaver \
	--with-gdm-config=%{_sysconfdir}/gdm/gdm.conf
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
install * $RPM_BUILD_ROOT%{_datadir}/%{name}/themes
echo '%defattr(644,root,root,755)' > $_DIR/xscreensaver.files
for I in *; do
        echo "%{_datadir}/%{name}/themes/$I" >> $_DIR/xscreensaver.files
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
%{_desktopdir}/screensavers/*.desktop
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/gnome-screensaver.schemas
%{_sysconfdir}/xdg/menus/*
