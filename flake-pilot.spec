Name:           flake-pilot
Version:        0.1.0
Release:        1%{?dist}
Summary:        Launcher for execution of applications inside containers and VMs

License:        MIT
URL:            https://github.com/OSInside/flake-pilot
Source0:        %{url}/archive/refs/heads/main.tar.gz#/flake-pilot-main.tar.gz
Source1:        flake-pilot-vendor.tar.gz

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo-rpm-macros >= 25
BuildRequires:  gcc

Recommends:     podman
Suggests:       firecracker

%description
Flake Pilot provides an application launcher and registration utility for
applications executed inside isolated runtime environments such as OCI
containers or Firecracker MicroVMs.

%prep
%autosetup -n flake-pilot-main -a1
%cargo_prep -v vendor

%build
%cargo_build
%cargo_vendor_manifest

%install
%cargo_install

%check
%cargo_test

%files
%license LICENSE cargo-vendor.txt
%doc README.md
%{_bindir}/flake-ctl
%{_bindir}/podman-pilot
%{_bindir}/firecracker-pilot
