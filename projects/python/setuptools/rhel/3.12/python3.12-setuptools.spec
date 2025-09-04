%global python3_pkgversion 3.12
%global srcname setuptools
# Virtual provides for the packages bundled by setuptools.
# Bundled packages are defined in multiple files. Generate the list with:
# pip freeze --path setuptools/_vendor > vendored.txt
# %%{_rpmconfigdir}/pythonbundles.py --namespace 'python%%{python3_pkgversion}dist' vendored.txt
%global bundled %{expand:
Provides: bundled(python%{python3_pkgversion}dist(autocommand)) = 2.2.2
Provides: bundled(python%{python3_pkgversion}dist(backports-tarfile)) = 1.2
Provides: bundled(python%{python3_pkgversion}dist(importlib-metadata)) = 8
Provides: bundled(python%{python3_pkgversion}dist(inflect)) = 7.3.1
Provides: bundled(python%{python3_pkgversion}dist(jaraco-collections)) = 5.1
Provides: bundled(python%{python3_pkgversion}dist(jaraco-context)) = 5.3
Provides: bundled(python%{python3_pkgversion}dist(jaraco-functools)) = 4.0.1
Provides: bundled(python%{python3_pkgversion}dist(jaraco-text)) = 3.12.1
Provides: bundled(python%{python3_pkgversion}dist(more-itertools)) = 10.3
Provides: bundled(python%{python3_pkgversion}dist(packaging)) = 24.2
Provides: bundled(python%{python3_pkgversion}dist(platformdirs)) = 4.2.2
Provides: bundled(python%{python3_pkgversion}dist(tomli)) = 2.0.1
Provides: bundled(python%{python3_pkgversion}dist(typeguard)) = 4.3
Provides: bundled(python%{python3_pkgversion}dist(typing-extensions)) = 4.12.2
Provides: bundled(python%{python3_pkgversion}dist(wheel)) = 0.45.1
Provides: bundled(python%{python3_pkgversion}dist(zipp)) = 3.19.2
}

Name:           python%{python3_pkgversion}-%{srcname}
Version:        80.9.0
Release:        0%{?dist}
Summary:        Easily build and distribute Python packages
License:        MIT AND Apache-2.0 AND (BSD-2-Clause OR Apache-2.0) AND Python-2.0.1 AND LGPL-3.0-only
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %{pypi_source %{srcname} %{version}}
BuildArch:      noarch
BuildRequires:  python3-rpm-generators >= 12-8
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-%{srcname}
%{bundled}

%description
Setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.

# For users who might see ModuleNotFoundError: No module named 'pkg_resoureces'
# NB: Those are two different provides: one contains underscore, the other hyphen
%py_provides    python%{python3_pkgversion}-pkg_resources
%py_provides    python%{python3_pkgversion}-pkg-resources

%package -n     %{python_wheel_pkg_prefix}-%{srcname}-wheel
Summary:        The setuptools wheel
%{bundled}

%description -n %{python_wheel_pkg_prefix}-%{srcname}-wheel
A Python wheel of setuptools to use with venv.

%prep
%autosetup -p1 -n %{srcname}-%{version}
# Strip shbang
find setuptools pkg_resources -name \*.py | xargs sed -i -e '1 {/^#!\//d}'
# Remove bundled exes
rm -f setuptools/*.exe
# Don't ship these
rm -r docs/conf.py

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l setuptools pkg_resources _distutils_hack
sed -Ei '/\/tests\b/d' %{pyproject_files}

# https://github.com/pypa/setuptools/issues/2709
find %{buildroot}%{python3_sitelib} -name tests -print0 | xargs -0 rm -r

# Install the wheel for the python-setuptools-wheel package
# and inject SBOM into it (if the macro is available)
mkdir -p %{buildroot}%{python_wheel_dir}
install -p %{_pyproject_wheeldir}/%{srcname}-%{version}-py3-none-any.whl -t %{buildroot}%{python_wheel_dir}
%{?python_wheel_inject_sbom:%python_wheel_inject_sbom %{buildroot}%{python_wheel_dir}/%{srcname}-%{version}-py3-none-any.whl}

%files -n python%{python3_pkgversion}-%{srcname} -f %{pyproject_files}
%doc docs/* NEWS.rst README.rst
%{python3_sitelib}/distutils-precedence.pth

%files -n %{python_wheel_pkg_prefix}-%{srcname}-wheel
%license LICENSE
# we own the dir for simplicity
%dir %{python_wheel_dir}/
%{python_wheel_dir}/%{srcname}-%{version}-py3-none-any.whl

%changelog
* Thu Sep 04 2025 Jürgen Löhel <packaging@loehel.de>
- Initial commit: 80.9.0

