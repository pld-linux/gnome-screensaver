Summary:	GNOME screensaver
Summary(pl.UTF-8):	Wygaszacz ekranu GNOME
Name:		gnome-screensaver
Version:	3.1.92
Release:	0.1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-screensaver/3.1/%{name}-%{version}.tar.xz
# Source0-md5:	e2515c98d955d82909cce7806ef5a0d8
Source1:	%{name}.pamd
URL:		http://live.gnome.org/GnomeScreensaver
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.70
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gnome-desktop-devel >= 2.91.5
BuildRequires:	gnome-menus-devel >= 2.26.0
BuildRequires:	gsettings-desktop-schemas >= 0.1.7
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libgnomekbd-devel >= 2.26.0
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXxf86misc-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
Obsoletes:	gnome-screensaver-xscreensaver
Obsoletes:	xscreensaver-gnome2
Requires:	gsettings-desktop-schemas >= 0.1.7
Suggests:	accountsservice
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A new screensaver solution for GNOME, with better HIG dialogs and a
much better integration into the desktop than the old xscreensaver.

%description -l pl.UTF-8
Nowe rozwiązanie wygaszcza ekranu dla GNOME, z bardziej zgodnymi z HIG
oknami dialogowymi i lepszą integracją z desktopem niż stary
xscreensaver.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-locking \
	--with-mit-ext \
	--with-xf86gamma-ext \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/gnome-screensaver

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/gnome-screensaver
%attr(755,root,root) %{_bindir}/gnome-screensaver
%attr(755,root,root) %{_bindir}/gnome-screensaver-command
%attr(755,root,root) %{_libdir}/gnome-screensaver-dialog
%{_sysconfdir}/xdg/autostart/gnome-screensaver.desktop
#%{_pkgconfigdir}/gnome-screensaver.pc
%{_mandir}/man1/gnome-screensaver.1*
%{_mandir}/man1/gnome-screensaver-command.1*
