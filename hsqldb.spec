# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global cvs_version 1_8_1_3

Name:       hsqldb
Version:    1.8.1.3
Release:    6
Epoch:	    1
Summary:    HyperSQL Database Engine
License:    BSD
URL:        http://hsqldb.sourceforge.net/
Source0:    http://downloads.sourceforge.net/hsqldb/%{name}_%{cvs_version}.zip
Source1:    %{name}-1.8.0-standard.cfg
Source2:    %{name}-1.8.0-standard-server.properties
Source3:    %{name}-1.8.0-standard-webserver.properties
Source4:    %{name}-1.8.0-standard-sqltool.rc
Source5:    http://mirrors.ibiblio.org/pub/mirrors/maven2/%{name}/%{name}/1.8.0.10/%{name}-1.8.0.10.pom
Patch0:     %{name}-1.8.0-scripts.patch
Patch1:     hsqldb-tmp.patch
Patch2:     %{name}-1.8.0-specify-su-shell.patch
Requires:   servlet25
Requires(post):   coreutils
Requires(preun):  coreutils
Requires(preun): initscripts
Requires(pre):  shadow-utils
Requires(post): jpackage-utils
Requires(postun): jpackage-utils
BuildRequires:  ant
BuildRequires:  junit
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  servlet25
Group:      Databases
BuildArch:  noarch

%description
HSQLdb is a relational database engine written in JavaTM , with a JDBC
driver, supporting a subset of ANSI-92 SQL. It offers a small (about
100k), fast database engine which offers both in memory and disk based
tables. Embedded and server modes are available. Additionally, it
includes tools such as a minimal web server, in-memory query and
management tools (can be run as applets or servlets, too) and a number
of demonstration examples.
Downloaded code should be regarded as being of production quality. The
product is currently being used as a database and persistence engine in
many Open Source Software projects and even in commercial projects and
products! In it's current version it is extremely stable and reliable.
It is best known for its small size, ability to execute completely in
memory and its speed. Yet it is a completely functional relational
database management system that is completely free under the Modified
BSD License. Yes, that's right, completely free of cost or restrictions!

%package manual
Summary:    Manual for %{name}
Group:      Development/Java

%description manual
Documentation for %{name}.

%package javadoc
Summary:    Javadoc for %{name}
Group:      Development/Java
Requires:   jpackage-utils

%description javadoc
Javadoc for %{name}.

%package demo
Summary:    Demo for %{name}
Group:      Development/Java
Requires:   %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -T -c -n %{name}
(cd ..
unzip -q %{SOURCE0} 
)
# set right permissions
find . -name "*.sh" -exec chmod 755 \{\} \;
# remove all _notes directories
for dir in `find . -name _notes`; do rm -rf $dir; done
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;
find . -name "*.war" -exec rm -f {} \;
# correct silly permissions
chmod -R go=u-w *

%patch0
%patch1 -p1
%patch2

cp %{SOURCE5} ./pom.xml

%build
export CLASSPATH=$(build-classpath \
servlet \
junit)
pushd build
ant jar javadoc
popd

%install
# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
# bin
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -m 755 bin/runUtil.sh $RPM_BUILD_ROOT%{_bindir}/%{name}RunUtil
# sysv init
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -m 755 bin/%{name} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}
# config
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
# serverconfig
install -d -m 755 $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/server.properties
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/webserver.properties
install -m 600 %{SOURCE4} $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/sqltool.rc
# lib
install -d -m 755 $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/lib
install -m 644 lib/functions $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/lib
# data
install -d -m 755 $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/data
# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/demo
install -m 755 demo/*.sh $RPM_BUILD_ROOT%{_datadir}/%{name}/demo
install -m 644 demo/*.html $RPM_BUILD_ROOT%{_datadir}/%{name}/demo
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -r doc/src/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf doc/src
# manual
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -r doc/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp index.html $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# Maven metadata
install -pD -T -m 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}

pushd $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/lib
    ln -s $(build-classpath hsqldb) hsqldb.jar
    ln -s $(build-classpath servlet) servlet.jar
popd

%preun
if [ $1 = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%pre
# Add the "hsqldb" user and group
# we need a shell to be able to use su - later
%{_sbindir}/groupadd -g 96 -f -r %{name} 2> /dev/null || :
%{_sbindir}/useradd -u 96 -g %{name} -s /sbin/nologin \
    -d %{_localstatedir}/lib/%{name} -r %{name} 2> /dev/null || :

%post
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add %{name}

%update_maven_depmap

%postun
%update_maven_depmap

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files
%defattr(-,root,root,-)
%doc doc/hsqldb_lic.txt
%{_javadir}/*
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0700,hsqldb,hsqldb) %{_localstatedir}/lib/%{name}/data
%{_localstatedir}/lib/%{name}/lib
%{_localstatedir}/lib/%{name}/server.properties
%{_localstatedir}/lib/%{name}/webserver.properties
%attr(0600,hsqldb,hsqldb) %{_localstatedir}/lib/%{name}/sqltool.rc
%dir %{_localstatedir}/lib/%{name}
%{_mavendepmapfragdir}/*
%{_mavenpomdir}/*

%files manual
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}
%doc doc/hsqldb_lic.txt

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}
%doc doc/hsqldb_lic.txt

%files demo
%defattr(-,root,root,-)
%{_datadir}/%{name}



%changelog
* Sun Nov 27 2011 Guilherme Moro <guilherme@mandriva.com> 1:1.8.1.3-5
+ Revision: 733975
- rebuild
- imported package hsqldb

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.8.0.10-0.0.5mdv2011.0
+ Revision: 605880
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.8.0.10-0.0.4mdv2010.1
+ Revision: 522848
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1:1.8.0.10-0.0.3mdv2010.0
+ Revision: 425153
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 1:1.8.0.10-0.0.2mdv2009.1
+ Revision: 351237
- rebuild

* Wed Jun 18 2008 Alexander Kurtakov <akurtakov@mandriva.org> 1:1.8.0.10-0.0.1mdv2009.0
+ Revision: 223788
- new version 1.8.0.10, use java-rpmbuild, disable gcj_compile

* Fri Feb 15 2008 Anssi Hannula <anssi@mandriva.org> 1:1.8.0.9-0.0.11mdv2008.1
+ Revision: 169057
- split server to hsqldb-server subpackage, as OOo needs the classes only

* Mon Jan 14 2008 David Walluck <walluck@mandriva.org> 1:1.8.0.9-0.0.10mdv2008.1
+ Revision: 151139
- do not call build-classpath in %%post
- comment out unused %%preun code

  + Marcelo Ricardo Leitner <mrl@mandriva.com>
    - Protect java-rpmbuild buildrequires to mdkversion >= 200810, so we can easily
      backport this package to 2008.0.

* Fri Jan 04 2008 David Walluck <walluck@mandriva.org> 1:1.8.0.9-0.0.9mdv2008.1
+ Revision: 145272
- silence commands in %%post

* Fri Jan 04 2008 David Walluck <walluck@mandriva.org> 1:1.8.0.9-0.0.8mdv2008.1
+ Revision: 144825
- rebuild

* Thu Jan 03 2008 David Walluck <walluck@mandriva.org> 1:1.8.0.9-0.0.7mdv2008.1
+ Revision: 143483
- bump release
- fix patch name in spec
- hsqldb user needs a shell or the service can't start
- patch initscript so that restart works even when no server is currently running

* Thu Jan 03 2008 Anssi Hannula <anssi@mandriva.org> 1:1.8.0.9-0.0.6mdv2008.1
+ Revision: 142848
- remove macros from comments causing %%pre errors (Oden)

* Thu Jan 03 2008 David Walluck <walluck@mandriva.org> 1:1.8.0.9-0.0.5mdv2008.1
+ Revision: 141139
- spec cleanup

  + Anssi Hannula <anssi@mandriva.org>
    - fix hsqldb user creation

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Dec 31 2007 David Walluck <walluck@mandriva.org> 1:1.8.0.9-0.0.4mdv2008.1
+ Revision: 139941
- fix JAVA_HOME, JAVACMD, and jar locations hsqldb-1.8.0-standard.cfg
- build with GCJ (1.5.0) for now due to JDBC API changes in 1.7.0

  + Anssi Hannula <anssi@mandriva.org>
    - post requires jpackage-utils for build-classpath
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 09 2007 David Walluck <walluck@mandriva.org> 1:1.8.0.9-0.0.1mdv2008.1
+ Revision: 116615
- 1.8.0.9

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 1:1.8.0.8-1.0.2mdv2008.0
+ Revision: 87386
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Mon Sep 03 2007 David Walluck <walluck@mandriva.org> 1:1.8.0.8-1.0.1mdv2008.0
+ Revision: 78860
- 1.8.0.8

* Tue Apr 17 2007 David Walluck <walluck@mandriva.org> 1:1.8.0.7-2.1mdv2008.0
+ Revision: 14164
- Import hsqldb



* Thu Feb 02 2007 David Walluck <walluck@mandriva.org> 1:1.8.0.7-2.1mdv2007.1
- release

* Mon Jan 22 2007 Deepak Bhole <dbhole@redhat.com> 1:1.8.0.7-2jpp
- Update copyright date

* Thu Jan 11 2007 Deepak Bhole <dbhole@redhat.com> 1.8.0.7-1jpp
- Updgrade to 1.8.0.7

* Wed Nov 29 2006 Deepak Bhole <dbhole@redhat.com> 1.8.0.4-4jpp
- Added missing entries to the files section
- From fnasser@redhat.com:
  - Add post requires for servletapi5 to ensure installation order
- From sgrubb@redhat.com:
  - Apply patch correcting tmp file usage

* Mon Aug 21 2006 Deepak Bhole <dbhole@redhat.com> 1:1.8.0.4-3jpp
- Add missing postun section.

* Fri Aug 04 2006 Deepak Bhole <dbhole@redhat.com> 1:1.8.0.4-2jpp
- Add missing requirements.
- Merge with fc spec.
  - From gbenson@redhat.com:
    - Change /etc/init.d to /etc/rc.d/init.d.
    - Create hsqldb user and group with low IDs (RH bz #165670).
    - Do not remove hsqldb user and group on uninstall.
    - Build with servletapi5.
  - From ashah@redhat.com:
    - Change hsqldb user shell to /sbin/nologin.
  - From notting@redhat.com
    - use an assigned user/group id

* Fri Apr 28 2006 Fernando Nasser <fnasser@redhat.com> 1:1.8.0.4-1jpp
- First JPP 1.7 build
- Upgrade to 1.8.0.4

* Tue Jul 26 2005 Fernando Nasser <fnasser@redhat.com> 0:1.80.1-1jpp
- Upgrade to 1.8.0.1

* Mon Mar 07 2005 Fernando Nasser <fnasser@redhat.com> 0:1.73.3-1jpp
- Upgrade to 1.7.3.3

* Wed Mar 02 2005 Fernando Nasser <fnasser@redhat.com> 0:1.73.0-1jpp
- Upgrade to 1.7.3.0

* Wed Aug 25 2004 Ralph Apel <r.apel at r-apel.de> 0:1.72.3-2jpp
- Build with ant-1.6.2

* Mon Aug 16 2004 Ralph Apel <r.apel at r-apel.de> 0:1.72.3-1jpp
- 1.7.2.3 stable

* Fri Jun 04 2004 Ralph Apel <r.apel at r-apel.de> 0:1.72-0.rc6b.1jpp
- 1.7.2 preview

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 0:1.71-1jpp
- 1.71
- update for JPackage 1.5

* Mon Mar 18 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.61-6jpp 
- generic servlet support

* Mon Jan 21 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.61-5jpp 
- versioned dir for javadoc
- no dependencies for javadoc package
- stricter dependencies for demo package
- section macro
- adaptation to new servlet3 package

* Mon Dec 17 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.61-4jpp
- javadoc in javadoc package
- doc reorganisation
- removed Requires: ant
- patches regenerated and bzipped

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.61-3jpp
- removed packager tag
- new jpp extension

* Fri Nov 09 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.61-2jpp
- added BuildRequires:        servletapi3 ant
- added Requires:        servletapi3 ant

* Fri Nov 09 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.61-1jpp
- complete spec restyle
- splitted & improved linuxization patch

* Fri Nov 09 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.60-1jpp
- 1.60 first "official release" of Hsqldb

* Fri Nov 09 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.43-2jpp
- fixed version

* Fri Nov 09 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.43-1jpp
- first release
- linuxization patch (doc + script)
