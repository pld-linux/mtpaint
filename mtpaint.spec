Summary:	A simple painting program
Summary(pl.UTF-8):	Prosty program graficzny
Name:		mtpaint
Version:	3.50
Release:	1
License:	GPL v3+
Group:		X11/Applications/Graphics
Source0:	https://downloads.sourceforge.net/mtpaint/%{name}-%{version}.tar.bz2
# Source0-md5:	bd50c57259e22a96989b9c923743d1d0
Source1:	%{name}.desktop
Patch0:		%{name}-gcc.patch
Patch1:		%{name}-flags.patch
URL:		https://mtpaint.sourceforge.net/
BuildRequires:	gettext-tools
BuildRequires:	giflib-devel
BuildRequires:	gtk+3-devel >= 3.0
BuildRequires:	lcms2-devel >= 2
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.2.27
BuildRequires:	libtiff-devel
BuildRequires:	libwebp-devel
BuildRequires:	openjpeg2-devel >= 2
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
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
%patch -P0 -p1
%patch -P1 -p1

%build
CC="%{__cc}" \
./configure debug gtk3 thread GIF man pod intl jpeg jp2v2 lcms2 tiff \
	--mandir=%{_mandir} \
	--prefix=%{_prefix}

cat >> _conf.txt <<'EOF'
LDFLAG += %{rpmldflags}
CFLAG  += %{rpmcflags}
EOF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -p src/icons1/icon.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.xpm

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_mime_database

%postun
%update_desktop_database_postun
%update_mime_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/mtpaint
%{_mandir}/man1/mtpaint.1*
%{_desktopdir}/mtpaint.desktop
%{_pixmapsdir}/mtpaint.png
%{_pixmapsdir}/mtpaint.xpm
