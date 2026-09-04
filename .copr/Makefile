# COPR executes: make -f .copr/Makefile srpm outdir="$(outdir)" spec="$(spec)"

srpm:
	# 1. Install required build dependencies
	dnf install -y cargo rust rpm-build rpmdevtools git tar rpmautospec

	# 2. Download upstream release tarball (Source0)
	spectool -g -C . $(spec)

	# 3. Create offline vendor archive for Cargo (Source1)
	rm -rf source vendor
	git clone https://github.com/OSInside/flake-pilot source
	cd source && cargo vendor ../vendor
	tar -czf flake-pilot-vendor.tar.gz vendor
	rm -rf source vendor

	# 4. Expand %autochangelog directly using the spec path (spec_file: $(spec), target_dir: $(spec))
	rpmautospec process-distgit $(spec) $(spec)

	# 5. Build SRPM directly to COPR's outdir
	rpmbuild -bs \
		--define "_sourcedir ." \
		--define "_srcrpmdir $(outdir)" \
		$(spec)
