Summary:	A simple painting program
Summary(pl.UTF-8):	Prosty program graficzny
Name:		mtpaint
Version:	3.40
Release:	4
License:	GPL v3+
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/mtpaint/%{name}-%{version}.tar.bz2
# Source0-md5:	957c8035dd62c6bfdb594cd0a4467d22
Source1:	%{name}.desktop
URL:		http://mtpaint.sourceforge.net/
BuildRequires:	gettext-devel
BuildRequires:	giflib-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.2.27
BuildRequires:	libtiff-devel
BuildRequires:	openjpeg-devel
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	which
BuildRequires:	zlib-devel
Requires:	desktop-file-utils
Requires:	shared-mime-info
Suggests:	gifsicle
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A simple GTK+ paint program.

%description -l pl.UTF-8
Prosty program graficzny oparty na bibliotece GTK+.

%prep
%setup -q

%build
./configure gtk2 thread GIF man pod intl jpeg jp2 tiff \
	--mandir=%{_mandir}/man1 \
	--prefix=%{_prefix}
cat >> _conf.txt <<'EOF'
LDFLAG += %{rpmldflags}
CFLAG  += %{rpmcflags}
CC = %{__cc} -Wall -Wno-pointer-sign
EOF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

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
%update_desktop_database_postun
if [ $1 = 0 ]; then
        umask 022
        update-mime-database %{_datadir}/mime
fi


%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/*/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
