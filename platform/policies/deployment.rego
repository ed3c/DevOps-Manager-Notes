package manager.admission

import rego.v1

default allow := false

violations contains "IMAGE_NOT_IMMUTABLE" if {
  not contains(input.image, "@sha256:")
}

violations contains "RUN_AS_NON_ROOT_REQUIRED" if {
  input.securityContext.runAsNonRoot != true
}

violations contains "PRIVILEGED_FORBIDDEN" if {
  input.securityContext.privileged == true
}

violations contains "CPU_REQUEST_REQUIRED" if {
  not input.resources.requests.cpu
}

violations contains "MEMORY_REQUEST_REQUIRED" if {
  not input.resources.requests.memory
}

violations contains "CPU_LIMIT_REQUIRED" if {
  not input.resources.limits.cpu
}

violations contains "MEMORY_LIMIT_REQUIRED" if {
  not input.resources.limits.memory
}

allow if count(violations) == 0
