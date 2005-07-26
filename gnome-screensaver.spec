Summary:	GNOME screensaver
Summary(pl):	Wygaszacz ekranu GNOME
Name:		gnome-screensaver
Version:	0.0.8
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-screensaver/0.0/%{name}-%{version}.tar.gz
# Source0-md5:	7f5b63f61aa7019dfd411054cf53916a
Source1:	%{name}.pamd
Patch0:		%{name}-desktop.patch
BuildRequires:	GConf2-devel >= 2.6.1
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.30
BuildRequires:	gnome-vfs2-devel >= 2.6.0
BuildRequires:	gtk+2-devel >= 2:2.6.0
BuildRequires:	intltool >= 0.29
BuildRequires:	libglade2 >= 2.5.0
BuildRequires:	libgnomeui-devel >= 2.6.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.6.0
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
Requires(post,preun):   GConf2
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
	--with-proc-interrupts \
	--with-randr-ext \
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
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/gnome-screensaver
%{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*
%{_datadir}/%{name}
%{_desktopdir}/*.desktop
