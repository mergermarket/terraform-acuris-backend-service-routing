output "target_group_arn" {
  value       = "${aws_alb_target_group.target_group.arn}"
  description = "The ARN of the target group"
}

output "dns_name" {
  value       = "${local.target_host_name}"
  description = "The DNS name for the service."
}
