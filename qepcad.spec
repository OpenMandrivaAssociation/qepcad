%define name		qepcad
%define qepcaddir	%{_datadir}/%{name}

Name:		%{name}
Group:		Sciences/Mathematics
License:	BSD
Summary:	Quantifier Elimination by Partial Cylindrical Algebraic Decomposition
Version:	B1.50
Release:	%mkrel 2
Source0:	http://www.usna.edu/Users/cs/qepcad/INSTALL/qepcad-B.1.53.tar.gz
Source1:	http://www.usna.edu/Users/cs/qepcad/INSTALL/saclib2.2.1.tar.gz
URL:		https://www.usna.edu/Users/cs/qepcad/B/QEPCAD.html
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  GL-devel
BuildRequires:  mesaglu-devel
BuildRequires:  mesaglut-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	tcsh
BuildRequires:	singular

# FIXME no prebuild Makefile/etc files for x86_64
ExcludeArch:	x86_64

%description
QEPCAD is an implementation of quantifier elimination by partial cylindrical
algebraic decomposition due orginally to Hoon Hong, and subsequently added
on to by many others. It is an interactive command-line program written in C,
and based on the SACLIB library of computer algebra functions. Presented here
is QEPCAD B version 1, the "B" designating a substantial departure from the
original QEPCAD and distinguishing it from any development of the original
that may proceed in a different direction

%prep
%setup -q -n %{name} -c -a 1


%build
export CC=gcc
export saclib=`pwd`/saclib2.2.1
pushd $saclib/bin
    ./sconf
    ./mkproto
    ./mkmake
    ./mklib all
popd

export qe=`pwd`/qesource
pushd $qe
    perl -pi -e 's|#(SINGULAR)|$1|;' default.qepcadrc
    gmake
    for dir in extensions cad2d plot2d; do
	pushd $dir
	    make
	popd
    done
popd

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{qepcaddir}/bin
pushd qesource/source
    chmod a+r %{name}.help
    cp -f %{name} %{buildroot}%{qepcaddir}/bin
    cp -f %{name}.help  %{buildroot}%{qepcaddir}/bin
    cp -f ../plot2d/ADJ2D_plot  %{buildroot}%{qepcaddir}/bin
    chmod a+r ../default.qepcadrc
    cp -f ../default.qepcadrc %{buildroot}%{qepcaddir}
popd

cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh

[ -z $qe ] && export qe=%{qepcaddir}
%{qepcaddir}/bin/%{name} $*
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%dir %{qepcaddir}
%{qepcaddir}/*
