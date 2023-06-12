# This package contains the NRPE library (https://github.com/NagiosEnterprises/nrpe)
NRPE := nrpe

NRPE_BUILD := $(BUILD_HELPER_DIR)/$(NRPE)-build
NRPE_INSTALL := $(BUILD_HELPER_DIR)/$(NRPE)-install

NRPE_BUILD_DIR := $(BAZEL_BIN)/$(NRPE)/$(NRPE)

$(NRPE_BUILD):
	# run the Bazel build process which does all the dependency stuff
	$(BAZEL_BUILD) @$(NRPE)//:$(NRPE)

$(NRPE_INSTALL): $(NRPE_BUILD)
	$(RSYNC) --chmod=u+w $(NRPE_BUILD_DIR)/ $(DESTDIR)$(OMD_ROOT)/
