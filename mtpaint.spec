#
Summary:	A simple painting program
Summary(pl):	Prosty program graficzny
Name:		mtpaint
Version:	2.30
Release:	1
License:	GPL v2
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# Source0-md5:	8582e791cf781d2f6ba85460823da247
Source1:	%{name}.desktop
URL:		http://mtpaint.sourceforge.net/
BuildRequires:	gettext-devel
BuildRequires:	giflib-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	perl-tools-pod
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
Requires:	desktop-file-utils
Requires:	shared-mime-info
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A simple GTK paint program.

%description -l pl
Prosty program graficzny oparty na bibliotece GTK.


%prep
%setup -q


%build
%configure man pod intl
echo 'LDFLAG += %{rpmldflags}' >> _conf.txt
echo 'CFLAG  += %{rpmcflags}'  >> _conf.txt
%{__make}


%install
rm -rf $RPM_BUILD_ROOT

%{__sed} -i "s,=\"/usr,=\"$RPM_BUILD_ROOT/usr," _conf.txt
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install src/icons1/icon.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.xpm

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
umask 022
update-mime-database %{_datadir}/mime ||:


%postun
%update-desktop-database-postun
if [ $1 = 0 ]; then
        umask 022
        update-mime-database %{_datadir}/mime
fi


%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/*
%{_desktopdir}/*
%{_pixmapsdir}/*
