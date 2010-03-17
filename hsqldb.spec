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

%define _localstatedir %{_var}

%define gcj_support 0

%define section                devel

%define cvs_version        1_8_0_10

Name:           hsqldb
Version:        1.8.0.10
Release:        %mkrel 0.0.4
Epoch:          1
Summary:        Hsqldb Database Engine
License:        BSD
Url:            http://hsqldb.sourceforge.net/
Source0:        http://downloads.sourceforge.net/hsqldb/hsqldb_%{cvs_version}.zip
Source1:        %{name}-1.8.0-standard.cfg
Source2:        %{name}-1.8.0-standard-server.properties
Source3:        %{name}-1.8.0-standard-webserver.properties
Source4:        %{name}-1.8.0-standard-sqltool.rc
Patch0:         %{name}-1.8.0-scripts.patch
Patch1:         %{name}-tmp.patch
Patch2:         %{name}-1.8.0-initscript-restart.patch
Requires:       servletapi5
Requires(pre):  rpm-helper
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(postun): rpm-helper
Requires(post): servletapi5
Requires(post):	jpackage-utils
Requires(pre):  shadow-utils
BuildRequires:  ant
BuildRequires:  junit
%if %mdkversion >= 200810
BuildRequires:  java-rpmbuild >= 0:1.5
%else
BuildRequires:  java-devel-gcj
%endif
BuildRequires:  servletapi5
Group:          Development/Java
%if ! %{gcj_support}
Buildarch:      noarch
%endif
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%endif

%description
This package contains the hsqldb java classes. The server is contained
in the package %{name}-server.

%package manual
Summary:        Manual for %{name}
Group:          Development/Java

%description manual
Documentation for %{name}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%package demo
Summary:        Demo for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%package server
Summary:	Hsqldb database server
Group:		System/Servers
Conflicts:	hsqldb < 1:1.8.0.9-0.0.11
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description server
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

This package contains the server.

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
%{_bindir}/find . -type f -name '*.css' -o -name '*.html' -o -name '*.txt' | \
  %{_bindir}/xargs -t %{__perl} -pi -e 's/\r$//g'

%patch0
%patch1 -p1

cat > README.%{version}-%{release}.upgrade.urpmi <<EOF
The server has been removed from the hsqldb package and moved to a
separate package named %{name}-server as it is not needed by most users.
Install it if you wish to use the Hsqldb server.
EOF

%build
export CLASSPATH=$(build-classpath \
jsse/jsse \
jsse/jnet \
jsse/jcert \
jdbc-stdext \
servletapi5 \
junit)
pushd build
%ant jar javadoc
popd

%install
%{__rm} -rf %{buildroot}

# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} ${jar/-%{version}/}; done)
# bin
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -m 755 bin/runUtil.sh $RPM_BUILD_ROOT%{_bindir}/%{name}RunUtil
# sysv init
install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 bin/%{name} $RPM_BUILD_ROOT%{_initrddir}/%{name}
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
install -m 644 lib/functions         $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/lib
# data
install -d -m 755 $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/data
# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/demo
install -m 755 demo/*.sh         $RPM_BUILD_ROOT%{_datadir}/%{name}/demo
install -m 644 demo/*.html         $RPM_BUILD_ROOT%{_datadir}/%{name}/demo
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -r doc/src/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -rf doc/src
# manual
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -r doc/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp index.html $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
# Add the "hsqldb" user and group
# we need a shell to be able to use su - later

# (Anssi 01/2008) Previously _pre_groupadd was used here together with
# _pre_useradd, causing an error situation where group is created, but
# the user is not:
#    useradd: group hsqldb exists - if you want to add this user to that group, use -g.
# Therefore we remove the hsqldb group if it exists without the corresponding
# user.
getent group %{name} >/dev/null && ! getent passwd %{name} >/dev/null && groupdel %{name}  >/dev/null
getent passwd %{name} >/dev/null && chsh -s /bin/sh %{name} >/dev/null
%_pre_useradd %{name} %{_localstatedir}/lib/%{name} /bin/sh

%post server
%{__rm} -f %{_localstatedir}/lib/%{name}/lib/hsqldb.jar
%{__rm} -f %{_localstatedir}/lib/%{name}/lib/servlet.jar
(cd %{_localstatedir}/lib/%{name}/lib
    %{__ln_s} %{_javadir}/hsqldb.jar hsqldb.jar
    %{__ln_s} %{_javadir}/servletapi5.jar servlet.jar
)
%_post_service %{name}

%post
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun server
%_postun_userdel %{name}

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif

%preun server
if [ "$1" = "0" ]; then
    %{__rm} -f %{_localstatedir}/lib/%{name}/lib/hsqldb.jar
    %{__rm} -f %{_localstatedir}/lib/%{name}/lib/servlet.jar
%if 0
    %{_sbindir}/userdel %{name} >> /dev/null 2>&1 || :
    %{_sbindir}/groupdel %{name} >> /dev/null 2>&1 || :
%endif
fi
%_preun_service %{name}

%files
%defattr(0644,root,root,0755)
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/hsqldb_lic.txt
%doc README*.urpmi
%{_javadir}/*
%{gcj_files}

%files server
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_initrddir}/%{name}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/%{name}
%attr(0755,hsqldb,hsqldb) %{_localstatedir}/lib/%{name}/data
%{_localstatedir}/lib/%{name}/lib
%attr(0644,root,root) %{_localstatedir}/lib/%{name}/server.properties
%attr(0644,root,root) %{_localstatedir}/lib/%{name}/webserver.properties
%attr(0600,hsqldb,hsqldb) %{_localstatedir}/lib/%{name}/sqltool.rc
%dir %{_localstatedir}/lib/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%files demo
%defattr(-,root,root,0755)
%{_datadir}/%{name}
