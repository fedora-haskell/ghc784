%define pkg_name @PACKAGE@
%define ghc_version @GHC_VERSION@

%define pkg_libdir %{_libdir}/ghc-%{ghc_version}/%{pkg_name}-%{version}
%define pkg_docdir %{_docdir}/ghc/libraries/%{pkg_name}

%define build_prof 1
%define build_doc 1

# ghc does not emit debug information
%define debug_package %{nil}

Name:		ghc-%{pkg_name}
Version:	@VERSION@
Release:	1%{?dist}
Summary:	Haskell %{pkg_name} library *FIXME*

Group:		Development/Libraries
License:	BSD
URL:		http://hackage.haskell.org/cgi-bin/hackage-scripts/package/%{pkg_name}
Source0:	http://hackage.haskell.org/packages/archive/%{pkg_name}/%{version}/%{pkg_name}-%{version}.tar.gz
Provides:	%{name}-devel = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# ghc has only been bootstrapped on the following archs:
ExclusiveArch:	i386 x86_64 ppc
BuildRequires:	ghc = %{ghc_version}
%if %{build_prof}
BuildRequires:	ghc-prof = %{ghc_version}
%endif
Requires:	ghc = %{ghc_version}
Requires(post):	ghc = %{ghc_version}
Requires(preun): ghc = %{ghc_version}
Requires(postun): ghc = %{ghc_version}

%description
Haskell %{pkg_name} library for ghc-%{ghc_version}. *FIXME*


%if %{build_prof}
%package prof
Summary: Profiling libraries for %{name}
Group: Development/Libraries
Requires: ghc-prof = %{ghc_version}

%description prof
This package contains profiling libraries for ghc %{ghc_version}.
%endif


%prep
%setup -q -n %{pkg_name}-%{version}


%build
%cabal_configure --ghc \
%if %{build_prof}
  -p
%else
%{nil}
%endif
%cabal_build
%if %{build_doc}
%cabal_haddock
%endif
%ghc_gen_scripts


%install
rm -rf $RPM_BUILD_ROOT
%cabal_install
%ghc_install_scripts
%ghc_gen_filelists %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post 
%ghc_postinst_script
%if %{build_doc}
%ghc_reindex_haddock
%endif


%preun 
%ghc_preun_script


%postun
if [ "$1" -eq 0 ] ; then
%if %{build_doc}
  %ghc_reindex_haddock
%endif
fi


%files -f %{name}.files
%defattr(-,root,root,-)
%doc LICENSE
%if %{build_doc}
%{pkg_docdir}
%endif


%if %{build_prof}
%files prof -f %{name}-prof.files
%defattr(-,root,root,-)
%doc LICENSE
%endif


%changelog
* @DATE@ @PACKAGER@ <@EMAIL@> - @VERSION@-1
- initial packaging for Fedora