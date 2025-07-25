Summary:	GNOME screensaver
Summary(pl.UTF-8):	Wygaszacz ekranu GNOME
Name:		gnome-screensaver
Version:	3.6.1
Release:	13
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-screensaver/3.6/%{name}-%{version}.tar.xz
# Source0-md5:	881cc58daa7cd8602737912ae5715cc8
Source1:	%{name}.pamd
Patch0:		am.patch
Patch1:		%{name}-systemd.patch
Patch2:		gnome-desktop335.patch
URL:		https://wiki.gnome.org/Attic/GnomeScreensaver
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.10
BuildRequires:	dbus-glib-devel >= 0.70
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gnome-desktop-devel >= 3.1.91
BuildRequires:	gsettings-desktop-schemas >= 0.1.7
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libgnomekbd-devel >= 2.26.0
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	systemd-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xz
Requires:	gsettings-desktop-schemas >= 0.1.7
Suggests:	accountsservice
Obsoletes:	f-spot-screensaver < 0.9
Obsoletes:	gnome-screensaver-xscreensaver < 3
Obsoletes:	xscreensaver-gnome2 < 1:5.06
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
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

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
	--with-systemd \
	--with-console-kit \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/gnome-screensaver

# directory for external provides (eg. f-spot)
install -d $RPM_BUILD_ROOT%{_libdir}/gnome-screensaver

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/gnome-screensaver
%attr(755,root,root) %{_bindir}/gnome-screensaver
%attr(755,root,root) %{_bindir}/gnome-screensaver-command
%attr(755,root,root) %{_libexecdir}/gnome-screensaver-dialog
%dir %{_libdir}/gnome-screensaver
%{_sysconfdir}/xdg/autostart/gnome-screensaver.desktop
%{_mandir}/man1/gnome-screensaver.1*
%{_mandir}/man1/gnome-screensaver-command.1*
