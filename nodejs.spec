%define   _base node
%define   _dist_ver %(sh /usr/lib/rpm/redhat/dist.sh)
%define   _name_prefix cmgd_

# the latest version of this spec file will always live in git at:
# <https://github.com/jantman/nodejs-rpm-centos5/>

Name:          %{_name_prefix}%{_base}js
Version:       0.10.9
Release:       2%{?dist}
Summary:       Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model. This is a very unofficial package.
Group:         Development/Libraries
License:       MIT License
URL:           http://nodejs.org
Source0:       %{url}/dist/v%{version}/%{_base}-v%{version}.tar.gz
# the following is just a warning about lack of -devel, headers, node-gyp
Source1:       README.nodejs
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-tmp
Prefix:        /usr
Obsoletes:     npm
Provides:      npm
BuildRequires: redhat-rpm-config
BuildRequires: tar
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: libstdc++-devel
BuildRequires: zlib-devel
%if "%{_dist_ver}" == ".el5"
# require EPEL
BuildRequires: python26
%endif
Patch0: node-js.centos5.configure.patch

%description
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

This package is NOT build to Fedora/EPEL specifications - it deviates from them in many ways. Installing this
package is very different from what you'd get when installing nodejs from EPEL or Fedora repos. It just uses
the nodejs makefile to build a binary tarball and then packages the contents of that.
Please see <https://github.com/jantman/nodejs-rpm-centos5> for more information.

%package binary
Summary: Node.js build binary tarballs
Group:         Development/Libraries
License:       MIT License
URL:           http://nodejs.org

%description binary
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

This package is NOT build to Fedora/EPEL specifications - it deviates from them in many ways. Installing this
package is very different from what you'd get when installing nodejs from EPEL or Fedora repos. It just uses
the nodejs makefile to build a binary tarball and then packages the contents of that.
Please see <https://github.com/jantman/nodejs-rpm-centos5> for more information.

%package npm
Summary: Node.js package manager
Group:         Development/Libraries
License:       MIT License
URL:           http://nodejs.org

%description npm
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

This package is NOT build to Fedora/EPEL specifications - it deviates from them in many ways. Installing this
package is very different from what you'd get when installing nodejs from EPEL or Fedora repos. It just uses
the nodejs makefile to build a binary tarball and then packages the contents of that.
Please see <https://github.com/jantman/nodejs-rpm-centos5> for more information.

%package devel
Summary:       Node.js developlment libraries placeholder
Group:         Development/Libraries
License:       MIT License
URL:           http://nodejs.org

%description devel
This is just a placeholder that puts a warning readme in /usr/share/node and /usr/include/node

Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

This package is NOT build to Fedora/EPEL specifications - it deviates from them in many ways. Installing this
package is very different from what you'd get when installing nodejs from EPEL or Fedora repos. It just uses
the nodejs makefile to build a binary tarball and then packages the contents of that.
Please see <https://github.com/jantman/nodejs-rpm-centos5> for more information.

%prep
rm -rf %{buildroot}
%setup -q -n %{_base}-v%{version}
%if "%{_dist_ver}" == ".el5"
%patch0 -p1
%endif

%build
%if "%{_dist_ver}" == ".el5"
export PYTHON=python26
%endif
%define _node_arch %{nil}
%ifarch x86_64
  %define _node_arch x64
%endif
%ifarch i386 i686
  %define _node_arch x86
%endif
if [ -z %{_node_arch} ];then
  echo "bad arch"
  exit 1
fi

./configure \
    --shared-openssl \
    --shared-openssl-includes=%{_includedir} \
    --shared-zlib \
    --shared-zlib-includes=%{_includedir}
make binary %{?_smp_mflags}
cd $RPM_SOURCE_DIR
mv $RPM_BUILD_DIR/%{_base}-v%{version}/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz .
rm  -rf %{_base}-v%{version}
tar zxvf %{_base}-v%{version}-linux-%{_node_arch}.tar.gz

%install
rm -rf $RPM_BUILD_ROOT
mkdir  -p $RPM_BUILD_ROOT/%{_prefix}
cp -Rp $RPM_SOURCE_DIR/%{_base}-v%{version}-linux-%{_node_arch}/* $RPM_BUILD_ROOT/usr/
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/share/doc/%{_base}-v%{version}/
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/share/%{_base}/
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/include/%{_base}/

for file in ChangeLog LICENSE README.md ; do
    mv $RPM_BUILD_ROOT/usr/$file $RPM_BUILD_ROOT/%{_prefix}/share/doc/%{_base}-v%{version}/
done
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/share/%{_base}js
mv $RPM_SOURCE_DIR/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz $RPM_BUILD_ROOT/%{_prefix}/share/%{_base}js/

%{__install} -m0644 %{SOURCE1} ${RPM_BUILD_ROOT}/%{_prefix}/share/%{_base}/README.nodejs
%{__install} -m0644 %{SOURCE1} ${RPM_BUILD_ROOT}/%{_prefix}/include/%{_base}/README.nodejs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_prefix}/share/doc/%{_base}-v%{version}
%{_prefix}/lib/dtrace/node.d
%defattr(755,root,root)
%{_bindir}/node

%doc
/%{_prefix}/share/man/man1/node.1.gz

%files binary
%defattr(-,root,root,-)
%{_prefix}/share/%{_base}js/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz

%files npm
%defattr(-,root,root,-)
%{_prefix}/lib/node_modules/npm
%{_bindir}/npm

%files devel
%defattr(-,root,root,-)
%{_prefix}/share/%{_base}/README.nodejs
%{_prefix}/include/%{_base}/README.nodejs


%changelog
* Thu Jun  6 2013 Jason Antman <jason@jasonantman.com> 0.10.9-2
- Forked from Kazuhisa's git repo at https://github.com/kazuhisya/nodejs-rpm
- Added warnings that this isn't EPEL/Fedora compatible in summary and description
- Added a name prefix to the package name (_name_prefix) to make the above clear
- Updated prep from rm -rf $RPM_SOURCE_DIR/%{_base}-v%{version} to rm -rf %{buildroot}
- Split npm into a subpackage
- Added a devel subpackage with just README.nodejs warning about missing devel
- Changed /usr/ to /%{_prefix}/ in spec
* Sat Jun  1 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.9
* Sun May 26 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.8
* Tue May 21 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.7
* Thu May 16 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.6
* Fri May  1 2013 Andrew Grimberg <agrimberg@linuxfoundation.org>
- Updated to node.js version 0.10.5
* Fri Apr 19 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.4
* Fri Apr  5 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.3
* Tue Apr  2 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.2
* Wed Mar 27 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.1
* Wed Mar 27 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.0
* Thu Mar 14 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.22
* Thu Feb 28 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.21
* Fri Feb 22 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.20 by @laapsaap
- Fixed #14
* Tue Feb 12 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.19
- Make formatting more consistent by @adambrod
- Cleanup of the %files section, removes warning by @steevel
* Sun Jan 20 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.18
* Sun Jan 13 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.17
* Sun Dec 30 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Added patch for CentOS and some BuildRequires by @smellman
* Mon Dec 17 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.16
* Sun Dec  2 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.15
- Fix build failure on i386 arch by @symm
* Sun Oct 28 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.14 by @Pitel
* Thu Oct 18 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Fixed issues #9, Unneeded dependency on git
* Wed Oct 17 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Fixed missing spaces for Fedora 18 (syntax error)
- Added BuildRequires: tar
* Mon Oct 15 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.12 by @brandonramirez
* Sat Sep 29 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.11
- Making Source0 "spectool friendly" by @elus
* Wed Sep 12 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.9
- Added build dependency by @knalli
- Fixed missing spaces (syntax error) by @knalli
* Thu Aug 23 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.8
* Sun Aug 19 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.7
- Added Architecture check
- Build came to pass in "make binary" a single
* Sat Aug 11 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.6
- Added as a package to build a binary tarball
- Various minor fixes and improvements
* Sun Aug  5 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.5
* Sat Jul 28 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.4
* Sat Jul 28 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Fixed issues #4, workaround for Avoid having to
  remove the rpm in the installation section
* Fri Jul 20 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.3
* Fri Jul  6 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.1
* Tue Jun 26 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.0
* Sun Jun 10 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.19
* Fri May 18 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.18
* Mon May  7 2012 Pete Fritchman <petef@databits.net>
- Updated to node.js version 0.6.17
* Sat Apr 14 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.15
* Sat Mar 31 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.14
* Tue Mar 20 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.13
* Sat Mar  3 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.12
* Sun Feb  5 2012 Pete Fritchman <petef@databits.net>
- Updated to node.js version 0.6.10
* Sat Jan  7 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.7
* Fri Dec 16 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.6
* Sun Dec  4 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.5
* Tue Nov 29 2011 Pete Fritchman <petef@databits.net>
- Updated to node.js version 0.6.3
* Tue Oct 11 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.9
* Sun Oct  2 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.8
* Sat Sep 18 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.7
* Sat Sep 10 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.6
* Mon Aug 29 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.5
* Fri Aug 12 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.4
* Wed Aug  3 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.3
* Tue Jul 19 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Initial version
