Summary:	Memory Mapped Machine
Summary(pl.UTF-8):	Memory Mapped Machine - sprzęt odwzorowany w pamięci
Name:		mmm
Version:	0
%define	gitref	58892979d9725a0eda0e3aea373cdefd0b01f6a1
%define	snap	20191113
Release:	0.%{snap}.1
License:	MIT
Group:		Libraries
Source0:	https://github.com/hodefoting/mmm/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	dc6459747c3be126c02e48a0b1f62884
Patch0:		%{name}-missing.patch
URL:		https://github.com/hodefoting/mmm/
BuildRequires:	SDL-devel >= 1.2
BuildRequires:	meson >= 0.50.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
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
%setup -q -n %{name}-%{gitref}
%patch0 -p1

%build
%meson build

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mmm.kobo
%attr(755,root,root) %{_bindir}/mmm.linux
%attr(755,root,root) %{_bindir}/mmm.sdl

%files libs
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_libdir}/libmmm.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/mmm-0.0
%{_pkgconfigdir}/mmm.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmmm.a
