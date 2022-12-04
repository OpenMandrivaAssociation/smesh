%define major 		8.3
%define libname		%mklibname smesh %{major}
%define develname	%mklibname smesh -d

%bcond_with test

Summary:        OpenCascade based MESH framework
Name:           smesh
Version:        9.8.0.2
Release:        1
Group:          Graphics/3D

# This library is LGPLv2 with exceptions but links against the non-free library OCE.
License:        LGPLv2
URL:            https://github.com/trelau/SMESH
# Upstream uses git submodules
# pip intall "patch==1.*"
# git clone --recurse-submodules https://github.com/trelau/SMESH.git
# cd SMESH
# git archive --prefix smesh-<VERSION>/ -o smesh-<VERSION>.tar v<VERSION TAG>
# python prepare.py
# gtar --transform='s,^src,smesh-<VERSION>/src,' -rf smesh-<VERSION>.tar src/*
# gzip smesh-<VERSION>.tar
Source0:        https://github.com/trelau/SMESH/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:		smesh-cmake.patch
# (fedora)
Patch10:	smesh-std_swap.patch
Patch11:	netgen_sizet.patch
BuildRequires:	cmake
BuildRequires:	ninja
#BuildRequires:  catch-devel
BuildRequires:	doxygen
BuildRequires:	boost-devel
BuildRequires:	freeimage-devel
BuildRequires:	graphviz
BuildRequires:	opencascade-devel
BuildRequires:	cmake(verdict)
BuildRequires:	pkgconfig(tbb)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	vtk-devel
# Dependencies for optional NETGENPlugin library.
#BuildRequires:	netgen-mesher-devel
#BuildRequires:	netgen-mesher-devel-private

%description
A complete OpenCascade based MESH framework.

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:        OpenCascade based MESH framework

%description -n %{libname}
A complete OpenCascade based MESH framework.

%files -n %{libname}
%license LICENSE.txt
%doc README.md
%{_libdir}/*.so

#---------------------------------------------------------------------------

%package -n %{develname}
Summary:        Development files for %{name}
Requires:       %{libname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{develname}
Development files and headers for %{name}.

%files -n %{develname}
%{_includedir}/*
#{_libdir}/*.so
%{_libdir}/cmake/*.cmake

#---------------------------------------------------------------------------
#
#package	doc
#Summary:	Docs for %{name}
#
#description	doc
#Docs for %{name}
#
#files doc
#doc %{_docdir}/smesh/
#
#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}

%build
# FIXME as of 9.7.0.1, clang 13.0.0, fails to build with clang
export CC=gcc
export CXX=g++
LDFLAGS='-Wl,--as-needed'; export LDFLAGS
%cmake \
	-DSMESH_TESTING=%{?with_test:ON}%{!?with_test:OFF} \
	-DENABLE_NETGEN:BOOL=ON \
	-DNEW_NETGEN_INTERFACE:BOOL=ON \
	-DENABLE_MED:BOOL=OFF \
	-DBUILD_TESTS:BOOL=TRUE \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

%check
%if %{with test}
make test -C build
%endif

