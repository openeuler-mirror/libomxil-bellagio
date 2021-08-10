Name:           libomxil-bellagio
Version:        0.9.3
Release:        22
Summary:        OpenMAX Integration Layer
License:        LGPLv2+
URL:            http://omxil.sourceforge.net
Source0:        http://downloads.sourceforge.net/omxil/%{name}-%{version}.tar.gz
Patch0001:      libomxil-bellagio-0.9.3-fix_Werror.patch
Patch0002:      libomxil-bellagio-0.9.3-unused.patch
Patch0003:      libomxil-bellagio-0.9.3-nodoc.patch
Patch0004:      bellagio-0.9.3-dynamicloader-linking.patch
Patch0005:      bellagio-0.9.3-parallel-build.patch
Patch0006:      bellagio-0.9.3-segfault-on-removeFromWaitResource.patch
Patch0007:      omxil_version.patch
Patch0008:      libomxil-bellagio-0.9.3-memcpy.patch
Patch0009:      libomxil-bellagio-0.9.3-valgrind_register.patch
Patch0010:      fix-stringop-overflow.patch
Patch0011:      fix-multi-define.patch
BuildRequires:  doxygen libtool gcc-c++

%description
OpenMAX Integration Layer (IL) is a standard API to access Multimedia Components
on mobile platforms. By means of the OpenMAX IL API, multimedia frameworks can
access hardware accelerators on platforms that provide it.

%package        devel
Summary:        Development files for libomxil-bellagio
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains libraries and header files for developing applications using libomxil-bellagio.

%package        test
Summary:        Test cases for libomxil-bellagio
Requires:       %{name} = %{version}-%{release}

%description    test
The libomxil-bellagio-test package contains binaries for testing libomxil-bellagio.

%package        help
Summary:        man info for libomxil-bellagio

%description    help
The libomxil-bellagio-help package contains man information for libomxil-bellagio.

%prep
%autosetup -p1
autoreconf -vif


%build
%configure --disable-static

sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build || %make_build

ln -sf src bellagio
make check LDFLAGS="-L$PWD/src/.libs"  CFLAGS="$RPM_OPT_FLAGS -I$PWD/include -I$PWD"


%install
%make_install
%delete_la

install -d $RPM_BUILD_ROOT%{_bindir}
install -pm 0755 test/components/audio_effects/.libs/{omxaudiomixertest,omxvolcontroltest} $RPM_BUILD_ROOT%{_bindir}
install -pm 0755 test/components/resource_manager/.libs/{omxprioritytest,omxrmtest} $RPM_BUILD_ROOT%{_bindir}

%post 
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%exclude %{_docdir}/%{name}/README
%exclude %{_docdir}/%{name}/TODO
%exclude %{_libdir}/pkgconfig
%exclude %{_libdir}/libomxil-bellagio.so
%exclude %{_libdir}/pkgconfig/libomxil-bellagio.pc
%exclude %{_bindir}/omxregister-bellagio
%doc AUTHORS ChangeLog COPYING
%{_bindir}/omxregister-bellagio
%{_libdir}/*


%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libomxil-bellagio.pc

%files test
%{_bindir}/*

%files help
%{_mandir}/man1/omxregister-bellagio.1.*
%doc NEWS README TODO


%changelog
* Sat Jul 31 2021 luweitao <luweitao2@huawei.com> - 0.9.3-22
- fix failure by upgrade to GCC-10

* Tue Dec 31 2019 zoushuangshuang <zoushuangshuang@huawei.com> - 0.9.3-21
- Package init
