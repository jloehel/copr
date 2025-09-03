Name:           yadm
Version:        3.5.0
Release:        0%{?dist}
Summary:        Yet Another Dotfiles Manager
License:        GPL-3.0-only
Group:          Development/Tools/Version Control
URL:            https://yadm.io
Source0:        %{name}-%{version}.tar.gz
Source99:       %{name}-rpmlintrc
Patch0:         %{name}-fix-makefile.patch
Patch1:         %{name}-fix-shebangs.patch
BuildRequires:  make
Requires:       bash
Requires:       git
BuildArch:      noarch

%description
yadm is a tool for managing a collection of files across multiple computers,
using a shared Git repository. In addition, yadm provides a feature to select
alternate versions of files based on the operation system or host name. Lastly,
yadm supplies the ability to manage a subset of secure files, which are
encrypted before they are included in the repository.

%package bash-completion
Summary:        Bash completions for %{name}
Requires:       bash-completion
%if 0%{?fedora} || 0%{?suse_version}
Supplements:    (%{name} and bash-completion)
%endif
BuildArch:      noarch

%description bash-completion
The official bash completion script for %{name}.

%package fish-completion
Summary:        Fish Completion for %{name}
%if 0%{?fedora} || 0%{?suse_version}
Supplements:    (%{name} and fish)
%endif
BuildArch:      noarch

%description fish-completion
The official fish completion script for %{name}.

%package zsh-completion
Summary:        ZSH Completion for %{name}
%if 0%{?fedora} || 0%{?suse_version}
Supplements:    (%{name} and zsh)
%endif
BuildArch:      noarch

%description zsh-completion
The official zsh completion script for %{name}.

%prep
%autosetup -p1

%build

%install
%make_install PREFIX=%{_prefix}

install -Dm0644 completion/fish/%{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish
install -Dm0644 completion/bash/%{name} %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -Dm0644 completion/zsh/_%{name} %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

%files
%{_bindir}/yadm
%{_mandir}/man1/%{name}.1%{?ext_man}
%doc CHANGES CONTRIBUTORS contrib/*
%license LICENSE

%files bash-completion
%{_datadir}/bash-completion

%files fish-completion
%{_datadir}/fish

%files zsh-completion
%{_datadir}/zsh/

%changelog
%autochangelog
