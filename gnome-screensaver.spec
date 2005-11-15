Summary:	GNOME screensaver
Summary(pl):	Wygaszacz ekranu GNOME
Name:		gnome-screensaver
Version:	0.0.19
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-screensaver/0.0/%{name}-%{version}.tar.bz2
# Source0-md5:	3dd904bdd99cef5d73aec5d9a3cc88cd
Source1:	%{name}.pamd
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-cosmos_theme_dir.patch
BuildRequires:	GConf2-devel >= 2.12.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.36
BuildRequires:	gnome-common >= 2.12.0
BuildRequires:	gnome-menus-devel >= 2.12.0
BuildRequires:	gnome-vfs2-devel >= 2.12.0
BuildRequires:	gtk+2-devel >= 2:2.8.3
BuildRequires:	intltool >= 0.34.1
BuildRequires:	libglade2 >= 1:2.5.1
BuildRequires:	libgnomeui-devel >= 2.12.0
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
Requires(post,preun):   GConf2
Requires:	xdg-menus
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A new screensaver solution for GNOME, with better HIG dialogs and a
much better integration into the desktop than the old xscreensaver.

%description -l pl
Nowe rozwi±zanie wygaszcza ekranu dla GNOME, z bardziej zgodnymi z HIG
dialogami i lepsz± integracj± z desktopem ni¿ stary xscreensaver.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
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
	--with-gdm-config=%{_sysconfdir}/X11/gdm/gdm.conf
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/gnome-screensaver

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

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
%attr(755,root,root) %{_libdir}/gnome-screensaver-dialog
%attr(755,root,root) %{_libdir}/gnome-screensaver
%{_datadir}/%{name}
%{_datadir}/desktop-directories/*
%{_desktopdir}/*.desktop
%{_sysconfdir}/gconf/schemas/gnome-screensaver.schemas
%{_sysconfdir}/xdg/menus/*
