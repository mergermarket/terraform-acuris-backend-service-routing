variable "env" {
  type = string
}

variable "component_name" {
  type    = string
  default = ""
}

variable "override_dns_name" {
  type    = string
  default = ""
}

variable "dns_domain" {
  type    = string
  default = ""
}

variable "aws_account_alias" {
  type = string
}

variable "backend_dns" {
  type = string
}

variable "simple_dns_name" {
  type    = bool
  default = false
}
