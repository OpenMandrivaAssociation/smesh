%bcond_with test

%define major 3
%define libname %mklibname smesh %{major}
%define develname %mklibname smesh -d

Name:           smesh
Version:        6.7.6
Release:        2
Summary:        OpenCascade based MESH framework
Group:          Graphics/3D

# This library is LGPLv2 with exceptions but links against the non-free library OCE.
License:        LGPLv2
URL:            https://github.com/tpaviot/smesh
Source0:        https://github.com/tpaviot/smesh/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  boost-devel
BuildRequires:  gcc-gfortran
BuildRequires:  f2c
BuildRequires:  dos2unix
BuildRequires:  opencascade-devel
BuildRequires:  graphviz
# New BRs
BuildRequires:  pkgconfig(tbb)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  freeimage-devel

# Dependencies for optional NETGENPlugin library.
#BuildRequires:  netgen-mesher-devel
#BuildRequires:  netgen-mesher-devel-private

%description
A complete OpenCascade based MESH framework.

%package -n %{libname}
Summary:        OpenCascade based MESH framework

%description -n %{libname}
A complete OpenCascade based MESH framework.

%package -n %{develname}
Summary:        Development files for %{name}
Requires:       %{libname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{develname}
Development files and headers for %{name}.

%package	doc
Summary:	Docs for %{name}

%description	doc
Docs for %{name}

%prep
%setup -q
%autopatch -p1

%{_bindir}/dos2unix -k LICENCE.lgpl.txt

%build
export CC=gcc
export CXX=g++
LDFLAGS='-Wl,--as-needed'; export LDFLAGS
%cmake \
       -DOCE_DIR=%{_datadir}/cmake/Modules \
       -DMONOLITHIC_BUILD=OFF \
       -DSMESH_TESTING=ON

%make_build

# Build documentation
%make_build doc

# Remove install script since we don't need it.
%__rm -f doc/html/installdox

%install
%make_install -C build

%if %{with test}
%check
make test -C build
%endif

%files -n %{libname}
%license LICENCE.lgpl.txt
%{_libdir}/*.so.%{major}{,.*}

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so

%files doc
%doc %{_docdir}/smesh/
