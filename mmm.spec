#
# Conditional build:
%bcond_with	sdl1	# SDL 1.x client
%bcond_without	sdl2	# SDL 2.x client

Summary:	Memory Mapped Machine
Summary(pl.UTF-8):	Memory Mapped Machine - sprzęt odwzorowany w pamięci
Name:		mmm
Version:	0.1.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/hodefoting/mmm/releases
Source0:	https://github.com/hodefoting/mmm/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b2d38082c3293ef1a44391cff7e0a109
URL:		https://github.com/hodefoting/mmm/
%{?with_sdl1:BuildRequires:	SDL-devel >= 1.2.0}
%{?with_sdl2:BuildRequires:	SDL2-devel >= 2.0.4}
BuildRequires:	meson >= 0.50.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
%{?with_sdl1:Requires:	SDL >= 1.2.0}
%{?with_sdl2:Requires:	SDL2 >= 2.0.4}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mmm is a shared memory protocol for virtualising access to framebuffer
graphics, audio output and input event. The mmm project provides a C
library and a couple of sample hosts. Both clients and hosts can be
statically linked, thus permitting a small static binary to be used
with hosts for multiple different environments. Once the ABI is
frozen; mmm clients could be a convenient way to distribute
stand-alone GUI applications.

%description -l pl.UTF-8
mmm to protokół pamięci współdzielonej mający na celu wirtualizację
dostępu do grafiki bufora ramki, wejścia dźwięku i zdarzeń
wejściowych. Projekt mmm udostępnia bibliotekę C oraz kilka
przykładowych hostów. Zarówno klienci, jak i hosty mogą być statycznie
konsolidowane, co pozwala na użycie małej statycznej binarki z hostami
dla wielu różnych środowisk. Po ustabilizowaniu ABI klienci mmm mogą
być wygodnym sposobem dystrybuowania małych, samodzielnych aplikacji
z graficznym interfejsem.

%package libs
Summary:	Shared mmm library
Summary(pl.UTF-8):	Biblioteka współdzielona mmm
Group:		Libraries

%description libs
Shared mmm library.

%description libs -l pl.UTF-8
Biblioteka współdzielona mmm.

%package devel
Summary:	Header files for mmm library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki mmm
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for mmm library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki mmm.

%package static
Summary:	Static mmm library
Summary(pl.UTF-8):	Statyczna biblioteka mmm
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static mmm library.

%description static -l pl.UTF-8
Statyczna biblioteka mmm.

%prep
%setup -q

%build
%meson \
	%{!?with_sdl1:-Dsdl1=disabled} \
	%{!?with_sdl2:-Dsdl2=disabled}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mmm
%attr(755,root,root) %{_bindir}/mmm.kobo
%attr(755,root,root) %{_bindir}/mmm.linux
%if %{with sdl1}
%attr(755,root,root) %{_bindir}/mmm.sdl
%endif
%if %{with sdl2}
%attr(755,root,root) %{_bindir}/mmm.sdl2
%endif

%files libs
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_libdir}/libmmm.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/mmm-0.1
%{_pkgconfigdir}/mmm.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmmm.a
